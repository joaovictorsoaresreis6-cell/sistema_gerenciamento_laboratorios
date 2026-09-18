from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import SessionLocal
from backend.models import Usuario, Laboratorio, Reserva, Aula, Manutencao
from backend.schemas import ReservaCreate


router = APIRouter(
    prefix="/reservas",
    tags=["Reservas"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", status_code=201)
def realizar_reserva(
    dados: ReservaCreate,
    db: Session = Depends(get_db)
):
    # Verifica se o usuário existe
    usuario = (
        db.query(Usuario)
        .filter(Usuario.idUsuario == dados.idUsuario)
        .first()
    )

    if not usuario:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado."
        )

    # Verifica se o laboratório existe
    laboratorio = (
        db.query(Laboratorio)
        .filter(Laboratorio.idLaboratorio == dados.idLaboratorio)
        .first()
    )

    if not laboratorio:
        raise HTTPException(
            status_code=404,
            detail="Laboratório não encontrado."
        )

    # Verifica se o laboratório está ativo
    if laboratorio.status != "Ativo":
        raise HTTPException(
            status_code=409,
            detail="O laboratório não está disponível para reservas."
        )

    # Verifica se o horário é válido
    if dados.horaFim <= dados.horaInicio:
        raise HTTPException(
            status_code=400,
            detail="O horário final deve ser posterior ao horário inicial."
        )

    # Verifica conflito com outra reserva
    conflito_reserva = (
        db.query(Reserva)
        .filter(
            Reserva.idLaboratorio == dados.idLaboratorio,
            Reserva.data == dados.data,
            Reserva.status == "Ativa",
            Reserva.horaInicio < dados.horaFim,
            Reserva.horaFim > dados.horaInicio
        )
        .first()
    )

    if conflito_reserva:
        raise HTTPException(
            status_code=409,
            detail="Já existe uma reserva para esse laboratório nesse horário."
        )

    # Verifica conflito com aula
    conflito_aula = (
        db.query(Aula)
        .filter(
            Aula.idLaboratorio == dados.idLaboratorio,
            Aula.data == dados.data,
            Aula.horaInicio < dados.horaFim,
            Aula.horaFim > dados.horaInicio
        )
        .first()
    )

    if conflito_aula:
        raise HTTPException(
            status_code=409,
            detail="Existe uma aula agendada para esse laboratório nesse horário."
        )

    # Verifica conflito com manutenção
    conflito_manutencao = (
        db.query(Manutencao)
        .filter(
            Manutencao.idLaboratorio == dados.idLaboratorio,
            Manutencao.status == "Ativa",
            Manutencao.dataInicio <= dados.data,
            Manutencao.dataFim >= dados.data
        )
        .first()
    )

    if conflito_manutencao:
        raise HTTPException(
            status_code=409,
            detail="O laboratório está em manutenção nessa data."
        )

    # Cria a reserva
    nova_reserva = Reserva(
        data=dados.data,
        horaInicio=dados.horaInicio,
        horaFim=dados.horaFim,
        status="Ativa",
        idUsuario=dados.idUsuario,
        idLaboratorio=dados.idLaboratorio
    )

    db.add(nova_reserva)
    db.commit()
    db.refresh(nova_reserva)

    return nova_reserva
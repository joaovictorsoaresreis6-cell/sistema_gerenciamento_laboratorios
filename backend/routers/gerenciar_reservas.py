from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import SessionLocal
from backend.models import Reserva, Laboratorio, Aula, Manutencao
from backend.schemas import ReservaUpdate


router = APIRouter(
    prefix="/gerenciar-reservas",
    tags=["Gerenciar Reservas"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def listar_reservas(db: Session = Depends(get_db)):
    return db.query(Reserva).all()


@router.get("/{id_reserva}")
def consultar_reserva(
    id_reserva: int,
    db: Session = Depends(get_db)
):
    reserva = (
        db.query(Reserva)
        .filter(Reserva.idReserva == id_reserva)
        .first()
    )

    if not reserva:
        raise HTTPException(
            status_code=404,
            detail="Reserva não encontrada."
        )

    return reserva


@router.put("/{id_reserva}")
def alterar_reserva(
    id_reserva: int,
    dados: ReservaUpdate,
    db: Session = Depends(get_db)
):
    reserva = (
        db.query(Reserva)
        .filter(Reserva.idReserva == id_reserva)
        .first()
    )

    if not reserva:
        raise HTTPException(
            status_code=404,
            detail="Reserva não encontrada."
        )

    if dados.horaFim <= dados.horaInicio:
        raise HTTPException(
            status_code=400,
            detail="O horário final deve ser posterior ao horário inicial."
        )

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

    if laboratorio.status != "Ativo":
        raise HTTPException(
            status_code=409,
            detail="O laboratório não está disponível para reservas."
        )

    conflito_reserva = (
        db.query(Reserva)
        .filter(
            Reserva.idReserva != id_reserva,
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
            detail="Já existe outra reserva para esse laboratório nesse horário."
        )

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

    reserva.data = dados.data
    reserva.horaInicio = dados.horaInicio
    reserva.horaFim = dados.horaFim
    reserva.idLaboratorio = dados.idLaboratorio

    db.commit()
    db.refresh(reserva)

    return reserva


@router.delete("/{id_reserva}")
def cancelar_reserva(
    id_reserva: int,
    db: Session = Depends(get_db)
):
    reserva = (
        db.query(Reserva)
        .filter(Reserva.idReserva == id_reserva)
        .first()
    )

    if not reserva:
        raise HTTPException(
            status_code=404,
            detail="Reserva não encontrada."
        )

    if reserva.status == "Cancelada":
        raise HTTPException(
            status_code=409,
            detail="A reserva já está cancelada."
        )

    reserva.status = "Cancelada"

    db.commit()
    db.refresh(reserva)

    return {
        "mensagem": "Reserva cancelada com sucesso.",
        "idReserva": reserva.idReserva,
        "status": reserva.status
    }
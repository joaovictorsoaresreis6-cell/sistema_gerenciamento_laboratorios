from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database import SessionLocal
from backend.models import Laboratorio, Reserva, Aula, Manutencao
from backend.schemas import DisponibilidadeRequest


router = APIRouter(
    prefix="/disponibilidade",
    tags=["Disponibilidade"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def consultar_disponibilidade(
    dados: DisponibilidadeRequest,
    db: Session = Depends(get_db)
):
    laboratorios = (
        db.query(Laboratorio)
        .filter(Laboratorio.status == "Ativo")
        .all()
    )

    disponiveis = []

    for laboratorio in laboratorios:

        conflito_reserva = (
            db.query(Reserva)
            .filter(
                Reserva.idLaboratorio == laboratorio.idLaboratorio,
                Reserva.data == dados.data,
                Reserva.status == "Ativa",
                Reserva.horaInicio < dados.horaFim,
                Reserva.horaFim > dados.horaInicio
            )
            .first()
        )

        conflito_aula = (
            db.query(Aula)
            .filter(
                Aula.idLaboratorio == laboratorio.idLaboratorio,
                Aula.data == dados.data,
                Aula.horaInicio < dados.horaFim,
                Aula.horaFim > dados.horaInicio
            )
            .first()
        )

        conflito_manutencao = (
            db.query(Manutencao)
            .filter(
                Manutencao.idLaboratorio == laboratorio.idLaboratorio,
                Manutencao.status == "Ativa",
                Manutencao.dataInicio <= dados.data,
                Manutencao.dataFim >= dados.data
            )
            .first()
        )

        if not conflito_reserva and not conflito_aula and not conflito_manutencao:
            disponiveis.append(laboratorio)

    return {
        "data": dados.data,
        "horaInicio": dados.horaInicio,
        "horaFim": dados.horaFim,
        "laboratoriosDisponiveis": [
            {
                "idLaboratorio": laboratorio.idLaboratorio,
                "nome": laboratorio.nome,
                "localizacao": laboratorio.localizacao,
                "capacidade": laboratorio.capacidade,
                "status": laboratorio.status
            }
            for laboratorio in disponiveis
        ]
    }
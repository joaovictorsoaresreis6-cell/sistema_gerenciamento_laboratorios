
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import SessionLocal
from backend.models import Manutencao, Laboratorio
from backend.schemas import (
    ManutencaoCreate,
    ManutencaoUpdate,
    ManutencaoResponse
)

router = APIRouter(
    prefix="/manutencoes",
    tags=["Manutenções"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@router.post("/", response_model=ManutencaoResponse, status_code=201)
def cadastrar_manutencao(
    dados: ManutencaoCreate,
    db: Session = Depends(get_db)
):
    # Verifica se o laboratório existe
    laboratorio = (
        db.query(Laboratorio)
        .filter(
            Laboratorio.idLaboratorio == dados.idLaboratorio
        )
        .first()
    )

    if not laboratorio:
        raise HTTPException(
            status_code=404,
            detail="Laboratório não encontrado."
        )

    # Verifica se as datas são válidas
    if dados.dataFim < dados.dataInicio:
        raise HTTPException(
            status_code=400,
            detail="A data final deve ser igual ou posterior à inicial."
        )

    # Cria a manutenção
    nova_manutencao = Manutencao(
        dataInicio=dados.dataInicio,
        dataFim=dados.dataFim,
        motivo=dados.motivo,
        status="Ativa",
        idLaboratorio=dados.idLaboratorio
    )

    db.add(nova_manutencao)
    db.commit()
    db.refresh(nova_manutencao)

    return nova_manutencao


@router.get("/", response_model=list[ManutencaoResponse])
def listar_manutencoes(
    db: Session = Depends(get_db)
):
    manutencoes = (
        db.query(Manutencao)
        .order_by(Manutencao.dataInicio.desc())
        .all()
    )

    return manutencoes


@router.patch("/{id_manutencao}", response_model=ManutencaoResponse)
def encerrar_manutencao(
    id_manutencao: int,
    dados: ManutencaoUpdate,
    db: Session = Depends(get_db)
):
    manutencao = (
        db.query(Manutencao)
        .filter(Manutencao.idManutencao == id_manutencao)
        .first()
    )

    if not manutencao:
        raise HTTPException(
            status_code=404,
            detail="Manutenção não encontrada."
        )

    if manutencao.status != "Ativa":
        raise HTTPException(
            status_code=409,
            detail="Esta manutenção já foi encerrada."
        )

    manutencao.status = dados.status

    db.commit()
    db.refresh(manutencao)

    return manutencao

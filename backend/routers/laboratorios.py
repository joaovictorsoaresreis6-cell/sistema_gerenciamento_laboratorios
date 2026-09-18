from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import SessionLocal
from backend.models import Laboratorio, Reserva, Aula, Manutencao
from backend.schemas import LaboratorioCreate, LaboratorioResponse


router = APIRouter(
    prefix="/laboratorios",
    tags=["Laboratórios"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =========================
# CONSULTAR LABORATÓRIOS
# =========================

@router.get("/", response_model=list[LaboratorioResponse])
def listar_laboratorios(db: Session = Depends(get_db)):
    return db.query(Laboratorio).all()


# =========================
# CADASTRAR LABORATÓRIO
# =========================

@router.post("/", response_model=LaboratorioResponse, status_code=201)
def cadastrar_laboratorio(
    laboratorio: LaboratorioCreate,
    db: Session = Depends(get_db)
):
    laboratorio_existente = (
        db.query(Laboratorio)
        .filter(Laboratorio.nome == laboratorio.nome)
        .first()
    )

    if laboratorio_existente:
        raise HTTPException(
            status_code=409,
            detail="Já existe um laboratório com esse nome."
        )

    novo_laboratorio = Laboratorio(
        nome=laboratorio.nome,
        localizacao=laboratorio.localizacao,
        capacidade=laboratorio.capacidade,
        status=laboratorio.status
    )

    db.add(novo_laboratorio)
    db.commit()
    db.refresh(novo_laboratorio)

    return novo_laboratorio


# =========================
# ALTERAR LABORATÓRIO
# =========================

@router.put("/{id_laboratorio}", response_model=LaboratorioResponse)
def alterar_laboratorio(
    id_laboratorio: int,
    laboratorio: LaboratorioCreate,
    db: Session = Depends(get_db)
):
    laboratorio_existente = (
        db.query(Laboratorio)
        .filter(Laboratorio.idLaboratorio == id_laboratorio)
        .first()
    )

    if not laboratorio_existente:
        raise HTTPException(
            status_code=404,
            detail="Laboratório não encontrado."
        )

    outro_laboratorio = (
        db.query(Laboratorio)
        .filter(
            Laboratorio.nome == laboratorio.nome,
            Laboratorio.idLaboratorio != id_laboratorio
        )
        .first()
    )

    if outro_laboratorio:
        raise HTTPException(
            status_code=409,
            detail="Já existe outro laboratório com esse nome."
        )

    laboratorio_existente.nome = laboratorio.nome
    laboratorio_existente.localizacao = laboratorio.localizacao
    laboratorio_existente.capacidade = laboratorio.capacidade
    laboratorio_existente.status = laboratorio.status

    db.commit()
    db.refresh(laboratorio_existente)

    return laboratorio_existente


# =========================
# REMOVER LABORATÓRIO
# =========================

@router.delete("/{id_laboratorio}")
def remover_laboratorio(
    id_laboratorio: int,
    db: Session = Depends(get_db)
):
    laboratorio = (
        db.query(Laboratorio)
        .filter(Laboratorio.idLaboratorio == id_laboratorio)
        .first()
    )

    if not laboratorio:
        raise HTTPException(
            status_code=404,
            detail="Laboratório não encontrado."
        )

    possui_reservas = (
        db.query(Reserva)
        .filter(Reserva.idLaboratorio == id_laboratorio)
        .first()
    )

    possui_aulas = (
        db.query(Aula)
        .filter(Aula.idLaboratorio == id_laboratorio)
        .first()
    )

    possui_manutencoes = (
        db.query(Manutencao)
        .filter(Manutencao.idLaboratorio == id_laboratorio)
        .first()
    )

    if possui_reservas or possui_aulas or possui_manutencoes:
        raise HTTPException(
            status_code=409,
            detail=(
                "Não é possível remover o laboratório porque "
                "existem reservas, aulas ou períodos de manutenção "
                "vinculados a ele."
            )
        )

    db.delete(laboratorio)
    db.commit()

    return {
        "mensagem": "Laboratório removido com sucesso."
    }
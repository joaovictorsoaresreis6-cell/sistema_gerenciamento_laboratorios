from datetime import date, time, datetime

from pydantic import BaseModel, ConfigDict, Field


# =========================
# LABORATÓRIO
# =========================

class LaboratorioBase(BaseModel):
    nome: str = Field(min_length=1, max_length=100)
    localizacao: str = Field(min_length=1, max_length=150)
    capacidade: int = Field(gt=0)
    status: str = Field(default="Ativo", max_length=30)


class LaboratorioCreate(LaboratorioBase):
    pass


class LaboratorioResponse(LaboratorioBase):
    idLaboratorio: int

    model_config = ConfigDict(from_attributes=True)


# =========================
# RESERVA
# =========================

class ReservaCreate(BaseModel):
    data: date
    horaInicio: time
    horaFim: time
    idUsuario: int
    idLaboratorio: int


class ReservaUpdate(BaseModel):
    data: date
    horaInicio: time
    horaFim: time
    idLaboratorio: int


class ReservaResponse(BaseModel):
    idReserva: int
    data: date
    horaInicio: time
    horaFim: time
    status: str
    idUsuario: int
    idLaboratorio: int

    model_config = ConfigDict(from_attributes=True)


# =========================
# DISPONIBILIDADE
# =========================

class DisponibilidadeRequest(BaseModel):
    data: date
    horaInicio: time
    horaFim: time


# =========================
# NOTIFICAÇÃO
# =========================

class NotificacaoResponse(BaseModel):
    idNotificacao: int
    mensagem: str
    dataHora: datetime
    tipo: str
    idReserva: int
    idUsuario: int

    model_config = ConfigDict(from_attributes=True)
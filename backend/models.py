from sqlalchemy import Column, Integer, String, Date, Time, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from backend.database import Base


class Usuario(Base):
    __tablename__ = "usuario"

    idUsuario = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(150), nullable=False, unique=True)
    tipo = Column(String(50), nullable=False)
    senha = Column(String(255), nullable=False)

    reservas = relationship("Reserva", back_populates="usuario")
    notificacoes = relationship("Notificacao", back_populates="usuario")


class Laboratorio(Base):
    __tablename__ = "laboratorio"

    idLaboratorio = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False, unique=True)
    localizacao = Column(String(150), nullable=False)
    capacidade = Column(Integer, nullable=False)
    status = Column(String(30), nullable=False, default="Ativo")

    computadores = relationship("Computador", back_populates="laboratorio")
    aulas = relationship("Aula", back_populates="laboratorio")
    reservas = relationship("Reserva", back_populates="laboratorio")
    manutencoes = relationship("Manutencao", back_populates="laboratorio")


class Computador(Base):
    __tablename__ = "computador"

    idComputador = Column(Integer, primary_key=True, index=True)
    patrimonio = Column(String(50), nullable=False, unique=True)
    especificacao = Column(String(255))
    status = Column(String(30), nullable=False, default="Disponível")

    idLaboratorio = Column(
        Integer,
        ForeignKey("laboratorio.idLaboratorio"),
        nullable=False
    )

    laboratorio = relationship("Laboratorio", back_populates="computadores")


class Professor(Base):
    __tablename__ = "professor"

    idProfessor = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(150), nullable=False, unique=True)
    matricula = Column(String(50), nullable=False, unique=True)

    aulas = relationship("Aula", back_populates="professor")


class Aula(Base):
    __tablename__ = "aula"

    idAula = Column(Integer, primary_key=True, index=True)
    disciplina = Column(String(100), nullable=False)
    data = Column(Date, nullable=False)
    horaInicio = Column(Time, nullable=False)
    horaFim = Column(Time, nullable=False)

    idProfessor = Column(
        Integer,
        ForeignKey("professor.idProfessor"),
        nullable=False
    )

    idLaboratorio = Column(
        Integer,
        ForeignKey("laboratorio.idLaboratorio"),
        nullable=False
    )

    professor = relationship("Professor", back_populates="aulas")
    laboratorio = relationship("Laboratorio", back_populates="aulas")


class Manutencao(Base):
    __tablename__ = "manutencao"

    idManutencao = Column(Integer, primary_key=True, index=True)
    dataInicio = Column(Date, nullable=False)
    dataFim = Column(Date, nullable=False)
    motivo = Column(String(255), nullable=False)
    status = Column(String(30), nullable=False, default="Ativa")

    idLaboratorio = Column(
        Integer,
        ForeignKey("laboratorio.idLaboratorio"),
        nullable=False
    )

    laboratorio = relationship("Laboratorio", back_populates="manutencoes")


class Reserva(Base):
    __tablename__ = "reserva"

    idReserva = Column(Integer, primary_key=True, index=True)
    data = Column(Date, nullable=False)
    horaInicio = Column(Time, nullable=False)
    horaFim = Column(Time, nullable=False)
    status = Column(String(30), nullable=False, default="Ativa")

    idUsuario = Column(
        Integer,
        ForeignKey("usuario.idUsuario"),
        nullable=False
    )

    idLaboratorio = Column(
        Integer,
        ForeignKey("laboratorio.idLaboratorio"),
        nullable=False
    )

    usuario = relationship("Usuario", back_populates="reservas")
    laboratorio = relationship("Laboratorio", back_populates="reservas")
    notificacoes = relationship("Notificacao", back_populates="reserva")


class Notificacao(Base):
    __tablename__ = "notificacao"

    idNotificacao = Column(Integer, primary_key=True, index=True)
    mensagem = Column(String(255), nullable=False)
    dataHora = Column(DateTime, nullable=False)
    tipo = Column(String(50), nullable=False)

    idReserva = Column(
        Integer,
        ForeignKey("reserva.idReserva"),
        nullable=False
    )

    idUsuario = Column(
        Integer,
        ForeignKey("usuario.idUsuario"),
        nullable=False
    )

    reserva = relationship("Reserva", back_populates="notificacoes")
    usuario = relationship("Usuario", back_populates="notificacoes")
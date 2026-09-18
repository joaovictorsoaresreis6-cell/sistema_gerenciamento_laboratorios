from fastapi import FastAPI

from backend.database import Base, engine
from backend import models
from backend.routers.laboratorios import router as laboratorios_router
from backend.routers.disponibilidade import router as disponibilidade_router
from backend.routers.reservas import router as reservas_router
from backend.routers.gerenciar_reservas import router as gerenciar_reservas_router

Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Sistema de Gerenciamento de Laboratórios",
    description="API para gerenciamento de laboratórios, disponibilidade e reservas.",
    version="1.0.0"
)


for rota in laboratorios_router.routes:
    app.router.routes.append(rota)

for rota in disponibilidade_router.routes:
    app.router.routes.append(rota)

for rota in reservas_router.routes:
    app.router.routes.append(rota)

for rota in gerenciar_reservas_router.routes:
    app.router.routes.append(rota)

@app.get("/")
def inicio():
    return {
        "mensagem": "Sistema de Gerenciamento de Laboratórios funcionando!"
    }
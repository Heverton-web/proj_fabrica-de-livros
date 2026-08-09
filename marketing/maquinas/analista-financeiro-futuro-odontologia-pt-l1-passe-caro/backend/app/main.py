from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import leads, emails, funil, webhooks
from app.database.connection import init_db
from app.database.migrations import run_migrations

app = FastAPI(
    title="Máquina de Vendas API",
    description="Backend para gestão de leads, funil de vendas e automação de emails",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():
    init_db()
    run_migrations()


app.include_router(leads.router, prefix="/api/leads", tags=["Leads"])
app.include_router(emails.router, prefix="/api/emails", tags=["Emails"])
app.include_router(funil.router, prefix="/api/funil", tags=["Funil"])
app.include_router(webhooks.router, prefix="/api/webhooks", tags=["Webhooks"])


@app.get("/health")
def health():
    return {"status": "ok"}

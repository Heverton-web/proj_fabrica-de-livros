from fastapi import APIRouter, HTTPException

from app.models.campanha import Campanha
from app.services.email_service import EmailService

router = APIRouter()
service = EmailService()


@router.get("/campanhas")
def listar_campanhas(status: str = None):
    return {"campanhas": [c.to_dict() for c in service.listar_campanhas(status=status)]}


@router.post("/campanhas", status_code=201)
def criar_campanha(data: dict):
    camp = Campanha(
        nome=data.get("nome", ""),
        descricao=data.get("descricao", ""),
        tipo=data.get("tipo", "email"),
        template_assunto=data.get("template_assunto", ""),
        template_corpo=data.get("template_corpo", ""),
        segmento_tags=data.get("segmento_tags", ""),
    )
    camp = service.criar_campanha(camp)
    return camp.to_dict()


@router.post("/campanhas/{campanha_id}/enviar")
def enviar_campanha(campanha_id: int):
    resultado = service.enviar_campanha(campanha_id)
    return resultado


@router.get("/enviados")
def listar_emails_enviados(lead_id: int = None, campanha_id: int = None):
    return {"emails": service.listar_enviados(lead_id=lead_id, campanha_id=campanha_id)}

from fastapi import APIRouter, HTTPException, Query
from typing import Optional

from app.models.lead import Lead
from app.services.lead_service import LeadService
from app.services.scoring_service import calcular_score

router = APIRouter()
service = LeadService()


@router.get("/")
def listar_leads(
    etapa: Optional[str] = None,
    fonte: Optional[str] = None,
    score_min: Optional[int] = Query(None, ge=0, le=100),
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
):
    leads = service.listar(etapa=etapa, fonte=fonte, score_min=score_min, limit=limit, offset=offset)
    return {"leads": [l.to_dict() for l in leads], "total": service.contar(etapa=etapa, fonte=fonte, score_min=score_min)}


@router.get("/{lead_id}")
def obter_lead(lead_id: int):
    lead = service.obter(lead_id)
    if not lead:
        raise HTTPException(404, "Lead não encontrado")
    return lead.to_dict()


@router.post("/", status_code=201)
def criar_lead(data: dict):
    lead = Lead(
        nome=data.get("nome", ""),
        email=data.get("email", ""),
        telefone=data.get("telefone", ""),
        empresa=data.get("empresa", ""),
        cargo=data.get("cargo", ""),
        fonte=data.get("fonte", ""),
        etapa_funil=data.get("etapa_funil", "novo"),
        tags=data.get("tags", ""),
        notas=data.get("notas", ""),
    )
    lead.score = calcular_score(lead)
    lead = service.criar(lead)
    return lead.to_dict()


@router.put("/{lead_id}")
def atualizar_lead(lead_id: int, data: dict):
    lead = service.obter(lead_id)
    if not lead:
        raise HTTPException(404, "Lead não encontrado")
    for campo in ("nome", "email", "telefone", "empresa", "cargo", "fonte", "etapa_funil", "tags", "notas"):
        if campo in data:
            setattr(lead, campo, data[campo])
    lead.score = calcular_score(lead)
    service.atualizar(lead)
    return lead.to_dict()


@router.delete("/{lead_id}", status_code=204)
def deletar_lead(lead_id: int):
    if not service.obter(lead_id):
        raise HTTPException(404, "Lead não encontrado")
    service.deletar(lead_id)


@router.post("/{lead_id}/mover")
def mover_etapa(lead_id: int, data: dict):
    nova_etapa = data.get("etapa")
    if not nova_etapa:
        raise HTTPException(400, "Campo 'etapa' obrigatório")
    lead = service.obter(lead_id)
    if not lead:
        raise HTTPException(404, "Lead não encontrado")
    lead.etapa_funil = nova_etapa
    service.atualizar(lead)
    return lead.to_dict()

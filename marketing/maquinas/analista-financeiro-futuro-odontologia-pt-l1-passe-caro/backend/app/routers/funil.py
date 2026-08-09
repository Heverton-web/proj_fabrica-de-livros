from fastapi import APIRouter

from app.services.lead_service import LeadService
from app.services.metricas_service import MetricasService

router = APIRouter()
lead_service = LeadService()
metricas_service = MetricasService()


@router.get("/pipeline")
def get_pipeline():
    etapas = ["novo", "qualificado", "proposta", "negociacao", "ganho", "perdido"]
    pipeline = {}
    for etapa in etapas:
        leads = lead_service.listar(etapa=etapa, limit=1000)
        pipeline[etapa] = {
            "count": len(leads),
            "leads": [l.to_dict() for l in leads],
        }
    return pipeline


@router.get("/conversao")
def taxas_conversao():
    return metricas_service.taxas_conversao()


@router.get("/dashboard")
def dashboard():
    return metricas_service.dashboard_geral()

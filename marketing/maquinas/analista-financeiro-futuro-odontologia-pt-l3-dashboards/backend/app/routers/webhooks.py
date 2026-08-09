import hashlib
import hmac
import json

from fastapi import APIRouter, Request, HTTPException

from app.config import settings
from app.services.lead_service import LeadService
from app.services.auto_correct import AutoCorrect

router = APIRouter()
lead_service = LeadService()
auto_correct = AutoCorrect()


def _verificar_assinatura(payload: bytes, signature: str) -> bool:
    esperado = hmac.new(
        settings.WEBHOOK_SECRET.encode(), payload, hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(esperado, signature)


@router.post("/lead")
async def receber_lead(request: Request):
    body = await request.body()
    signature = request.headers.get("X-Webhook-Signature", "")
    if not _verificar_assinatura(body, signature):
        raise HTTPException(401, "Assinatura inválida")

    data = json.loads(body)
    data_corrigido = auto_correct.corrigir_lead(data)
    lead = lead_service.criar_de_dict(data_corrigido)
    return {"status": "recebido", "lead_id": lead.id}


@router.post("/evento")
async def receber_evento(request: Request):
    body = await request.body()
    data = json.loads(body)
    tipo = data.get("tipo", "")
    lead_id = data.get("lead_id")

    if not lead_id:
        raise HTTPException(400, "lead_id obrigatório")

    lead = lead_service.obter(lead_id)
    if not lead:
        raise HTTPException(404, "Lead não encontrado")

    from app.services.scoring_service import registrar_interacao_e_recalcular
    registrar_interacao_e_recalcular(lead_id, tipo, data.get("descricao", ""))

    return {"status": "ok"}

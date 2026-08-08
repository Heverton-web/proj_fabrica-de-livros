from dataclasses import dataclass
from typing import Optional


@dataclass
class Campanha:
    id: Optional[int] = None
    nome: str = ""
    descricao: str = ""
    tipo: str = "email"  # email, sms, whatsapp
    status: str = "rascunho"  # rascunho, ativa, pausada, finalizada
    template_assunto: str = ""
    template_corpo: str = ""
    segmento_tags: str = ""  # CSV de tags para filtrar leads
    agendada_para: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    @classmethod
    def from_row(cls, row: dict) -> "Campanha":
        return cls(**{k: row[k] for k in row.keys() if k in cls.__dataclass_fields__})

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "nome": self.nome,
            "descricao": self.descricao,
            "tipo": self.tipo,
            "status": self.status,
            "template_assunto": self.template_assunto,
            "template_corpo": self.template_corpo,
            "segmento_tags": self.segmento_tags,
            "agendada_para": self.agendada_para,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

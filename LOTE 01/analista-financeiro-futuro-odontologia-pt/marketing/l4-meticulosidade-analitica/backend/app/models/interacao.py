from dataclasses import dataclass
from typing import Optional


@dataclass
class Interacao:
    id: Optional[int] = None
    lead_id: int = 0
    tipo: str = ""  # email_enviado, email_aberto, email_clicado, visita_site, formulario, ligacao, reuniao
    descricao: str = ""
    metadata: str = ""  # JSON
    created_at: Optional[str] = None

    @classmethod
    def from_row(cls, row: dict) -> "Interacao":
        return cls(**{k: row[k] for k in row.keys() if k in cls.__dataclass_fields__})

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "lead_id": self.lead_id,
            "tipo": self.tipo,
            "descricao": self.descricao,
            "metadata": self.metadata,
            "created_at": self.created_at,
        }

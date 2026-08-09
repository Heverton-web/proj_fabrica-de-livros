from dataclasses import dataclass
from typing import Optional


@dataclass
class Venda:
    id: Optional[int] = None
    lead_id: int = 0
    valor: float = 0.0
    moeda: str = "BRL"
    status: str = "proposta"  # proposta, aceita, recusada, cancelada
    produto: str = ""
    notas: str = ""
    closed_at: Optional[str] = None
    created_at: Optional[str] = None

    @classmethod
    def from_row(cls, row: dict) -> "Venda":
        return cls(**{k: row[k] for k in row.keys() if k in cls.__dataclass_fields__})

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "lead_id": self.lead_id,
            "valor": self.valor,
            "moeda": self.moeda,
            "status": self.status,
            "produto": self.produto,
            "notas": self.notas,
            "closed_at": self.closed_at,
            "created_at": self.created_at,
        }

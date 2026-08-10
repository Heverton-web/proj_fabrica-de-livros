from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Lead:
    id: Optional[int] = None
    nome: str = ""
    email: str = ""
    telefone: str = ""
    empresa: str = ""
    cargo: str = ""
    fonte: str = ""  # organico, paid, referral, evento
    etapa_funil: str = "novo"  # novo, qualificado, proposta, negociacao, ganho, perdido
    score: int = 0
    tags: str = ""  # CSV
    notas: str = ""
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    @classmethod
    def from_row(cls, row: dict) -> "Lead":
        return cls(**{k: row[k] for k in row.keys() if k in cls.__dataclass_fields__})

    def to_dict(self) -> dict:
        d = {
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "telefone": self.telefone,
            "empresa": self.empresa,
            "cargo": self.cargo,
            "fonte": self.fonte,
            "etapa_funil": self.etapa_funil,
            "score": self.score,
            "tags": self.tags,
            "notas": self.notas,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
        return d

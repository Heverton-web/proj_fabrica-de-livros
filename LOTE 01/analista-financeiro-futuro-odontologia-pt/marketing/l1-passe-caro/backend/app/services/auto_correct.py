import re


class AutoCorrect:
    """Corrige e normaliza dados de leads antes de persistir."""

    def corrigir_lead(self, data: dict) -> dict:
        data = dict(data)  # cópia
        data["nome"] = self._normalizar_nome(data.get("nome", ""))
        data["email"] = self._normalizar_email(data.get("email", ""))
        data["telefone"] = self._normalizar_telefone(data.get("telefone", ""))
        data["empresa"] = data.get("empresa", "").strip()
        data["cargo"] = data.get("cargo", "").strip()
        data["fonte"] = self._normalizar_fonte(data.get("fonte", ""))
        data["tags"] = self._normalizar_tags(data.get("tags", ""))
        return data

    def _normalizar_nome(self, nome: str) -> str:
        nome = nome.strip().title()
        nome = re.sub(r"\s+", " ", nome)
        return nome

    def _normalizar_email(self, email: str) -> str:
        email = email.strip().lower()
        email = re.sub(r"\s+", "", email)
        return email

    def _normalizar_telefone(self, tel: str) -> str:
        digits = re.sub(r"\D", "", tel)
        if len(digits) == 11:
            return f"({digits[:2]}) {digits[2:7]}-{digits[7:]}"
        if len(digits) == 10:
            return f"({digits[:2]}) {digits[2:6]}-{digits[6:]}"
        return tel.strip()

    def _normalizar_fonte(self, fonte: str) -> str:
        fonte = fonte.strip().lower()
        validas = {"organico", "paid", "referral", "evento", "webhook", "manual", "indicacao"}
        if fonte in validas:
            return fonte
        return "outro"

    def _normalizar_tags(self, tags: str) -> str:
        if not tags:
            return ""
        partes = [t.strip().lower() for t in re.split(r"[,;]", tags) if t.strip()]
        return ",".join(sorted(set(partes)))

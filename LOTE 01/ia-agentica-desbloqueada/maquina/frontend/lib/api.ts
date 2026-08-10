const API_BASE = process.env.NEXT_PUBLIC_BASE_URL || "";

export interface Lead {
  id: number;
  nome: string | null;
  email: string;
  slug: string;
  origem: string;
  status: string;
  createdAt: string;
}

export interface Venda {
  id: number;
  email: string;
  valor: number;
  slug: string;
  status: string;
  createdAt: string;
}

export async function captureLead(data: { nome?: string; email: string }) {
  const res = await fetch(`${API_BASE}/api/lead`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });

  if (!res.ok) {
    const body = await res.json();
    throw new Error(body.error || "Erro ao capturar lead");
  }

  return res.json();
}

export async function healthCheck() {
  const res = await fetch(`${API_BASE}/api/health`);
  return res.json();
}

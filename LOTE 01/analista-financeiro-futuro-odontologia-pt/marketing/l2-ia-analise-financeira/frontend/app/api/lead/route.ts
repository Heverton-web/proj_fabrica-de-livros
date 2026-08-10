import { NextRequest, NextResponse } from "next/server";
import { z } from "zod";

const leadSchema = z.object({
  nome: z.string().min(2).optional(),
  email: z.string().email("E-mail inválido"),
});

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const parsed = leadSchema.safeParse(body);

    if (!parsed.success) {
      return NextResponse.json(
        { error: parsed.error.issues[0].message },
        { status: 400 }
      );
    }

    const { nome, email } = parsed.data;

    // TODO: Salvar no banco de dados
    // await db.leads.create({ data: { nome, email, slug: "analista-financeiro-futuro-odontologia-pt-l2-ia-analise-financeira" } });

    // TODO: Enviar e-mail de boas-vindas via Resend
    // await resend.emails.send({ ... });

    // Log para debug
    console.log("[Lead Capturado]", { nome, email, slug: "analista-financeiro-futuro-odontologia-pt-l2-ia-analise-financeira", timestamp: new Date().toISOString() });

    return NextResponse.json({ success: true, message: "Lead capturado com sucesso" });
  } catch {
    return NextResponse.json(
      { error: "Erro interno do servidor" },
      { status: 500 }
    );
  }
}

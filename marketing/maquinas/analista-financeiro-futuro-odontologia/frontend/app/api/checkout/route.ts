import { NextRequest, NextResponse } from "next/server";
import { z } from "zod";

const checkoutSchema = z.object({
  nome: z.string().min(2, "Informe seu nome completo"),
  email: z.string().email("E-mail inválido"),
  produto: z.string().optional().default("dentista-gestor-livro"),
});

const BACKEND_URL =
  process.env.BACKEND_URL || process.env.NEXT_PUBLIC_BACKEND_URL || "http://127.0.0.1:8000";

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const parsed = checkoutSchema.safeParse(body);

    if (!parsed.success) {
      return NextResponse.json(
        { error: parsed.error.issues[0].message },
        { status: 400 }
      );
    }

    const { nome, email, produto } = parsed.data;

    // Registra o lead no backend da máquina (funil)
    let leadBackend = false;
    try {
      const resp = await fetch(`${BACKEND_URL}/api/leads/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          nome,
          email,
          origem: "checkout",
          produto,
        }),
      });
      leadBackend = resp.ok;
    } catch {
      leadBackend = false;
    }

    // TODO: integrar gateway de pagamento real (Hotmart, Kiwify, Mercado Pago...).
    // A máquina devolve o link do webhook como pagamento simulado para o checkout local.
    const paymentLink = `${BACKEND_URL}/api/webhooks/lead`;

    console.log("[Checkout Solicitado]", {
      nome,
      email,
      produto,
      leadBackend,
      timestamp: new Date().toISOString(),
    });

    return NextResponse.json({
      success: true,
      message: "Pedido registrado. Siga para o pagamento.",
      redirect_url: "/obrigado",
      payment_link: paymentLink,
      produto,
      valor: 97,
    });
  } catch (err) {
    console.error("[Checkout Erro]", err);
    // Form urlencoded (HTML puro) não passa por request.json() —
    // o checkout page envia JSON via fetch; exigir esse content-type.
    const isJsonParse = err instanceof SyntaxError;
    return NextResponse.json(
      {
        error: isJsonParse
          ? "Payload inválido. Envie JSON com nome e email (Content-Type: application/json)."
          : "Erro interno do servidor",
      },
      { status: isJsonParse ? 400 : 500 }
    );
  }
}

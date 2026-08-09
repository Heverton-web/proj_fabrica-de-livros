import { NextRequest, NextResponse } from "next/server";

export async function POST(request: NextRequest) {
  try {
    const body = await request.text();
    const signature = request.headers.get("stripe-signature");

    // TODO: Verificar assinatura do Stripe
    // const event = stripe.webhooks.constructEvent(body, signature!, process.env.STRIPE_WEBHOOK_SECRET!);

    // TODO: Processar evento
    // switch (event.type) {
    //   case "checkout.session.completed":
    //     const session = event.data.object;
    //     await db.vendas.create({ data: { email: session.customer_email, slug: "livros/harness-engineering" } });
    //     await resend.emails.send({ to: session.customer_email, subject: "Compra confirmada!" });
    //     break;
    // }

    console.log("[Webhook] Payload recebido:", { signature, bodyLength: body.length });

    return NextResponse.json({ received: true });
  } catch {
    return NextResponse.json(
      { error: "Erro ao processar webhook" },
      { status: 400 }
    );
  }
}

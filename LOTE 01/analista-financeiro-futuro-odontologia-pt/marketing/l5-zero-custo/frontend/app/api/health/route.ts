import { NextResponse } from "next/server";

export async function GET() {
  return NextResponse.json({
    status: "healthy",
    slug: "analista-financeiro-futuro-odontologia-pt-l5-zero-custo",
    timestamp: new Date().toISOString(),
    uptime: process.uptime(),
  });
}

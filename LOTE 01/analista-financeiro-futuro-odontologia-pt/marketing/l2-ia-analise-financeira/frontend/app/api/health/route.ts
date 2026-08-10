import { NextResponse } from "next/server";

export async function GET() {
  return NextResponse.json({
    status: "healthy",
    slug: "analista-financeiro-futuro-odontologia-pt-l2-ia-analise-financeira",
    timestamp: new Date().toISOString(),
    uptime: process.uptime(),
  });
}

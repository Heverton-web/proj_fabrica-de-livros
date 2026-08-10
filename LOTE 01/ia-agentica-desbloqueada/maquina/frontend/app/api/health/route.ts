import { NextResponse } from "next/server";

export async function GET() {
  return NextResponse.json({
    status: "healthy",
    slug: "livros/ia-agentica-desbloqueada",
    timestamp: new Date().toISOString(),
    uptime: process.uptime(),
  });
}

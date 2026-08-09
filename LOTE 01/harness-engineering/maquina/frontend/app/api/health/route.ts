import { NextResponse } from "next/server";

export async function GET() {
  return NextResponse.json({
    status: "healthy",
    slug: "livros/harness-engineering",
    timestamp: new Date().toISOString(),
    uptime: process.uptime(),
  });
}

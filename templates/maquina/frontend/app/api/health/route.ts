import { NextResponse } from "next/server";

export async function GET() {
  return NextResponse.json({
    status: "healthy",
    slug: "{{SLUG}}",
    timestamp: new Date().toISOString(),
    uptime: process.uptime(),
  });
}

import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Harness Engineering",
  description: "Harness Engineering: do modelo ao sistema autônomo confiável — testes, guardrails, loops e observabilidade para agentes de IA em produção.",
  openGraph: {
    title: "Harness Engineering",
    description: "Método completo para dominar Harness Engineering",
    type: "website",
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="pt-BR">
      <body className="font-sans antialiased bg-white text-gray-900">
        {children}
      </body>
    </html>
  );
}

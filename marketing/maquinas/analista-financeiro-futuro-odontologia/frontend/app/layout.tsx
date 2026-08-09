import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "O Dentista Gestor — Finanças de Clínica com IA",
  description:
    "Guia para dentistas donos de clínica: fluxo de caixa, ticket médio, custo por sessão e KPIs de gestão montados com IA gratuita.",
  openGraph: {
    title: "O Dentista Gestor — Finanças de Clínica com IA",
    description:
      "Sua clínica sabe quanto ganha por cadeira? Fluxo de caixa, KPIs e IA gratuita para a gestão financeira odontológica.",
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

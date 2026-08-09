import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Analista Financeiro Futuro Odontologia Pt L5 Zero Custo",
  description: "Aprenda a dominar Analista Financeiro Futuro Odontologia Pt L5 Zero Custo com o método comprovado que já ajudou centenas de pessoas.",
  openGraph: {
    title: "Analista Financeiro Futuro Odontologia Pt L5 Zero Custo",
    description: "Método completo para dominar Analista Financeiro Futuro Odontologia Pt L5 Zero Custo",
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

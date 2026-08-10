import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Livros/Ia Agentica Desbloqueada",
  description: "Aprenda a dominar Livros/Ia Agentica Desbloqueada com o método comprovado que já ajudou centenas de pessoas.",
  openGraph: {
    title: "Livros/Ia Agentica Desbloqueada",
    description: "Método completo para dominar Livros/Ia Agentica Desbloqueada",
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

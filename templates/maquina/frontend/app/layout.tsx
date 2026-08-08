import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "{{TITULO}}",
  description: "Aprenda a dominar {{TITULO}} com o método comprovado que já ajudou centenas de pessoas.",
  openGraph: {
    title: "{{TITULO}}",
    description: "Método completo para dominar {{TITULO}}",
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

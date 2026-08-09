"use client";

import { useState } from "react";

export default function CheckoutPage() {
  const [status, setStatus] = useState<"idle" | "loading" | "success" | "error">("idle");
  const [errorMsg, setErrorMsg] = useState("");

  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setStatus("loading");
    setErrorMsg("");

    const form = e.currentTarget;
    const data = Object.fromEntries(new FormData(form));

    try {
      const res = await fetch("/api/checkout", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });

      if (!res.ok) {
        const body = await res.json();
        throw new Error(body.error || "Erro ao processar pedido");
      }

      setStatus("success");
      form.reset();
      window.location.href = "/obrigado";
    } catch (err) {
      setStatus("error");
      setErrorMsg(err instanceof Error ? err.message : "Erro ao processar pedido");
    }
  }

  return (
    <main className="min-h-screen bg-gray-50 flex items-center justify-center px-4 py-16">
      <div className="max-w-md w-full">
        <div className="card text-center">
          <div className="text-5xl mb-4">🔒</div>
          <h1 className="text-2xl font-extrabold text-gray-900 mb-2">
            Finalizar Compra
          </h1>
          <p className="text-gray-600 mb-6">
            Você está adquirindo <strong>{{TITULO}}</strong>
          </p>

          <div className="bg-gray-50 rounded-xl p-6 mb-6">
            <p className="text-sm text-gray-500 mb-1">Valor total</p>
            <p className="text-4xl font-extrabold text-primary-600">
              {{PRECO}}
            </p>
            <p className="text-sm text-gray-500 mt-1">Pagamento único</p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4 text-left">
            <div>
              <label htmlFor="nome" className="block text-sm font-medium text-gray-700 mb-1">
                Nome completo
              </label>
              <input
                id="nome"
                name="nome"
                type="text"
                required
                minLength={2}
                placeholder="Seu nome"
                className="w-full rounded-lg border border-gray-300 px-4 py-3 focus:outline-none focus:ring-2 focus:ring-primary-500"
              />
            </div>
            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
                E-mail
              </label>
              <input
                id="email"
                name="email"
                type="email"
                required
                placeholder="Seu melhor e-mail"
                className="w-full rounded-lg border border-gray-300 px-4 py-3 focus:outline-none focus:ring-2 focus:ring-primary-500"
              />
            </div>

            {status === "error" && (
              <p className="text-sm text-red-600">{errorMsg}</p>
            )}

            <button
              type="submit"
              disabled={status === "loading"}
              className="btn-primary w-full text-xl py-5 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {status === "loading" ? "PROCESSANDO..." : `PAGAR {{PRECO}} →`}
            </button>
          </form>

          {status === "success" && (
            <p className="text-sm text-green-600 mt-4">
              Pedido registrado! Redirecionando...
            </p>
          )}

          <div className="flex items-center justify-center gap-4 mt-6 text-xs text-gray-400">
            <span>🔒 SSL Seguro</span>
            <span>•</span>
            <span>PIX · Cartão · Boleto</span>
          </div>
        </div>
      </div>
    </main>
  );
}

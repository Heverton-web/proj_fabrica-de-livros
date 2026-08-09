"use client";

import { useState } from "react";

interface LeadFormProps {
  variant?: "light" | "dark";
  showName?: boolean;
}

export default function LeadForm({ variant = "light", showName = false }: LeadFormProps) {
  const [status, setStatus] = useState<"idle" | "loading" | "success" | "error">("idle");
  const [errorMsg, setErrorMsg] = useState("");

  const isDark = variant === "dark";

  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setStatus("loading");
    setErrorMsg("");

    const form = e.currentTarget;
    const data = Object.fromEntries(new FormData(form));

    try {
      const res = await fetch("/api/lead", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });

      if (!res.ok) {
        const body = await res.json();
        throw new Error(body.error || "Erro ao enviar");
      }

      setStatus("success");
      form.reset();
      window.location.href = "/obrigado";
    } catch (err) {
      setStatus("error");
      setErrorMsg(err instanceof Error ? err.message : "Erro inesperado");
    }
  }

  if (status === "success") {
    return (
      <div className="text-center py-8">
        <div className="text-5xl mb-4">✅</div>
        <p className={isDark ? "text-white text-lg font-bold" : "text-gray-900 text-lg font-bold"}>
          Recebido! Verifique seu e-mail.
        </p>
      </div>
    );
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {showName && (
        <input
          type="text"
          name="nome"
          placeholder="Seu nome"
          required
          className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-primary-500 text-gray-900"
        />
      )}
      <input
        type="email"
        name="email"
        placeholder="Seu melhor e-mail"
        required
        className={`w-full px-4 py-3 rounded-lg border focus:outline-none focus:ring-2 focus:ring-primary-500 text-gray-900 ${
          isDark ? "border-gray-600 bg-gray-800 text-white placeholder-gray-400" : "border-gray-300"
        }`}
      />
      <button
        type="submit"
        disabled={status === "loading"}
        className={`w-full py-3 rounded-lg font-bold text-lg transition-all ${
          isDark
            ? "bg-accent-500 text-gray-900 hover:bg-accent-600"
            : "bg-primary-600 text-white hover:bg-primary-700"
        } disabled:opacity-50 disabled:cursor-not-allowed`}
      >
        {status === "loading" ? "Enviando..." : "QUERO RECEBER GRÁTIS →"}
      </button>

      {status === "error" && (
        <p className="text-red-500 text-sm text-center">{errorMsg}</p>
      )}

      <p className={`text-xs text-center ${isDark ? "text-gray-500" : "text-gray-400"}`}>
        Prometemos: sem spam. Cancele quando quiser.
      </p>
    </form>
  );
}

export default function PricingCard() {
  return (
    <div className="bg-white rounded-3xl shadow-2xl p-8 md:p-10 text-gray-900 relative overflow-hidden">
      {/* Badge */}
      <div className="absolute top-0 right-0 bg-accent-500 text-gray-900 text-xs font-bold px-4 py-1 rounded-bl-xl">
        MAIS POPULAR
      </div>

      <h3 className="text-2xl font-extrabold mb-2">Acesso Completo</h3>
      <p className="text-gray-500 mb-6">
        Tudo que você precisa para dominar Analista Financeiro Futuro Odontologia Pt L2 Ia Analise Financeira
      </p>

      <div className="mb-6">
        <span className="text-sm text-gray-400 line-through mr-2">R$ 705</span>
        <span className="text-5xl font-extrabold text-primary-600">
          R$ 97
        </span>
        <span className="text-gray-500 ml-1">/pagamento único</span>
      </div>

      <ul className="space-y-3 text-left mb-8">
        {[
          "Método completo passo a passo",
          "Planilha de acompanhamento",
          "Videoaulas bônus",
          "Comunidade exclusiva",
          "Templates prontos para usar",
          "Acesso imediato e vitalício",
          "Garantia incondicional de 7 dias",
        ].map((item) => (
          <li key={item} className="flex items-start gap-2">
            <span className="text-green-500 mt-0.5">✓</span>
            <span className="text-gray-700">{item}</span>
          </li>
        ))}
      </ul>

      <a
        href="/checkout"
        className="btn-primary w-full text-xl py-5 rounded-xl"
      >
        GARANTIR MINHA VAGA →
      </a>

      <div className="flex items-center justify-center gap-3 mt-4 text-xs text-gray-400">
        <span>🔒 Pagamento seguro</span>
        <span>•</span>
        <span>PIX · Cartão · Boleto</span>
      </div>
    </div>
  );
}

export default function Guarantee() {
  return (
    <section className="py-16 md:py-24 bg-amber-50">
      <div className="max-w-3xl mx-auto px-4 text-center">
        <div className="text-7xl mb-6">🛡️</div>
        <h2 className="section-heading text-gray-900 mb-4">
          Garantia Incondicional de 7 Dias
        </h2>
        <p className="text-lg md:text-xl text-gray-600 max-w-2xl mx-auto mb-6">
          Experimente o método por 7 dias completos. Se por qualquer motivo
          você não ficar satisfeito, devolvemos <strong>100% do seu dinheiro</strong> —
          sem perguntas, sem burocracia.
        </p>
        <div className="flex flex-col sm:flex-row items-center justify-center gap-6 mt-8">
          <div className="flex items-center gap-3">
            <span className="text-3xl">💰</span>
            <div className="text-left">
              <p className="font-bold text-gray-900">Reembolso total</p>
              <p className="text-sm text-gray-500">Sem perguntas</p>
            </div>
          </div>
          <div className="flex items-center gap-3">
            <span className="text-3xl">⏱️</span>
            <div className="text-left">
              <p className="font-bold text-gray-900">7 dias</p>
              <p className="text-sm text-gray-500">Tempo para testar</p>
            </div>
          </div>
          <div className="flex items-center gap-3">
            <span className="text-3xl">🔒</span>
            <div className="text-left">
              <p className="font-bold text-gray-900">Zero risco</p>
              <p className="text-sm text-gray-500">O risco é todo nosso</p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

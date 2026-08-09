export default function CheckoutPage() {
  return (
    <main className="min-h-screen bg-gray-50 flex items-center justify-center px-4 py-16">
      <div className="max-w-md w-full">
        <div className="card text-center">
          <div className="text-5xl mb-4">🔒</div>
          <h1 className="text-2xl font-extrabold text-gray-900 mb-2">
            Finalizar Compra
          </h1>
          <p className="text-gray-600 mb-6">
            Você está adquirindo <strong>Analista Financeiro Futuro Odontologia Pt L2 Ia Analise Financeira</strong>
          </p>

          <div className="bg-gray-50 rounded-xl p-6 mb-6">
            <p className="text-sm text-gray-500 mb-1">Valor total</p>
            <p className="text-4xl font-extrabold text-primary-600">
              R$ 97
            </p>
            <p className="text-sm text-gray-500 mt-1">Pagamento único</p>
          </div>

          <div className="space-y-3 text-left text-sm text-gray-600 mb-8">
            <div className="flex items-center gap-2">
              <span className="text-green-500">✓</span> Acesso imediato
            </div>
            <div className="flex items-center gap-2">
              <span className="text-green-500">✓</span> Garantia de 7 dias
            </div>
            <div className="flex items-center gap-2">
              <span className="text-green-500">✓</span> Pagamento 100% seguro
            </div>
          </div>

          <form action="/api/checkout" method="POST">
            <button type="submit" className="btn-primary w-full text-xl py-5">
              PAGAR R$ 97 →
            </button>
          </form>

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

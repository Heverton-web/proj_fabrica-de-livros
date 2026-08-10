export default function AdminEmailsPage() {
  const sequences = [
    {
      id: 1,
      nome: "Boas-vindas (Lead Magnet)",
      emails: 3,
      enviados: 128,
      abertos: "62%",
      cliques: "18%",
      status: "Ativa",
    },
    {
      id: 2,
      nome: "Nutração Pré-venda",
      emails: 5,
      enviados: 85,
      abertos: "48%",
      cliques: "12%",
      status: "Ativa",
    },
    {
      id: 3,
      nome: "Carrinho abandonado",
      emails: 2,
      enviados: 34,
      abertos: "55%",
      cliques: "22%",
      status: "Ativa",
    },
    {
      id: 4,
      nome: "Pós-compra + Upsell",
      emails: 3,
      enviados: 21,
      abertos: "71%",
      cliques: "28%",
      status: "Ativa",
    },
  ];

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Sequências de E-mail</h1>
        <button className="px-4 py-2 bg-primary-600 text-white rounded-lg text-sm font-medium hover:bg-primary-700">
          + Nova Sequência
        </button>
      </div>

      <div className="grid gap-4">
        {sequences.map((seq) => (
          <div key={seq.id} className="card flex items-center justify-between">
            <div>
              <h3 className="font-bold text-gray-900">{seq.nome}</h3>
              <p className="text-sm text-gray-500 mt-1">
                {seq.emails} e-mails · {seq.enviados} enviados
              </p>
            </div>
            <div className="flex items-center gap-6 text-sm">
              <div className="text-center">
                <p className="text-gray-500">Abertura</p>
                <p className="font-bold text-gray-900">{seq.abertos}</p>
              </div>
              <div className="text-center">
                <p className="text-gray-500">Cliques</p>
                <p className="font-bold text-gray-900">{seq.cliques}</p>
              </div>
              <span className="px-3 py-1 bg-green-100 text-green-700 rounded-full text-xs font-semibold">
                {seq.status}
              </span>
              <button className="text-primary-600 hover:text-primary-700 font-medium text-sm">
                Editar →
              </button>
            </div>
          </div>
        ))}
      </div>

      {/* Stats resumo */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mt-8">
        <div className="card text-center">
          <p className="text-sm text-gray-500">Total Enviados</p>
          <p className="text-3xl font-extrabold text-gray-900 mt-1">268</p>
        </div>
        <div className="card text-center">
          <p className="text-sm text-gray-500">Taxa Abertura Média</p>
          <p className="text-3xl font-extrabold text-gray-900 mt-1">57%</p>
        </div>
        <div className="card text-center">
          <p className="text-sm text-gray-500">Taxa Clique Média</p>
          <p className="text-3xl font-extrabold text-gray-900 mt-1">19%</p>
        </div>
      </div>
    </div>
  );
}

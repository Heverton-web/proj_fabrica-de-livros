export default function AdminLeadsPage() {
  const leads = [
    { id: 1, nome: "Maria Silva", email: "maria@email.com", data: "08/01/2026", origem: "Captura", status: "Novo" },
    { id: 2, nome: "João Santos", email: "joao@email.com", data: "08/01/2026", origem: "Página de Vendas", status: "Convertido" },
    { id: 3, nome: "Ana Costa", email: "ana@email.com", data: "07/01/2026", origem: "Captura", status: "Novo" },
    { id: 4, nome: "Pedro Lima", email: "pedro@email.com", data: "07/01/2026", origem: "Orgânico", status: "E-mail enviado" },
    { id: 5, nome: "Carla Souza", email: "carla@email.com", data: "06/01/2026", origem: "Captura", status: "Convertido" },
  ];

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Leads</h1>
        <div className="flex gap-2">
          <input
            type="text"
            placeholder="Buscar lead..."
            className="px-4 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary-500"
          />
          <button className="px-4 py-2 bg-primary-600 text-white rounded-lg text-sm font-medium hover:bg-primary-700">
            Exportar CSV
          </button>
        </div>
      </div>

      <div className="card overflow-hidden p-0">
        <table className="w-full text-sm">
          <thead className="bg-gray-50">
            <tr>
              <th className="text-left py-3 px-4 font-semibold text-gray-600">Nome</th>
              <th className="text-left py-3 px-4 font-semibold text-gray-600">E-mail</th>
              <th className="text-left py-3 px-4 font-semibold text-gray-600">Data</th>
              <th className="text-left py-3 px-4 font-semibold text-gray-600">Origem</th>
              <th className="text-left py-3 px-4 font-semibold text-gray-600">Status</th>
            </tr>
          </thead>
          <tbody>
            {leads.map((lead) => (
              <tr key={lead.id} className="border-b border-gray-100 hover:bg-gray-50">
                <td className="py-3 px-4 font-medium">{lead.nome}</td>
                <td className="py-3 px-4 text-gray-600">{lead.email}</td>
                <td className="py-3 px-4 text-gray-500">{lead.data}</td>
                <td className="py-3 px-4 text-gray-500">{lead.origem}</td>
                <td className="py-3 px-4">
                  <span
                    className={`inline-block px-2 py-0.5 rounded-full text-xs font-semibold ${
                      lead.status === "Convertido"
                        ? "bg-green-100 text-green-700"
                        : lead.status === "E-mail enviado"
                        ? "bg-yellow-100 text-yellow-700"
                        : "bg-blue-100 text-blue-700"
                    }`}
                  >
                    {lead.status}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="flex items-center justify-between mt-4 text-sm text-gray-500">
        <span>Mostrando 5 de 42 leads</span>
        <div className="flex gap-1">
          <button className="px-3 py-1 rounded border border-gray-300 hover:bg-gray-100">← Anterior</button>
          <button className="px-3 py-1 rounded bg-primary-600 text-white">1</button>
          <button className="px-3 py-1 rounded border border-gray-300 hover:bg-gray-100">2</button>
          <button className="px-3 py-1 rounded border border-gray-300 hover:bg-gray-100">3</button>
          <button className="px-3 py-1 rounded border border-gray-300 hover:bg-gray-100">Próxima →</button>
        </div>
      </div>
    </div>
  );
}

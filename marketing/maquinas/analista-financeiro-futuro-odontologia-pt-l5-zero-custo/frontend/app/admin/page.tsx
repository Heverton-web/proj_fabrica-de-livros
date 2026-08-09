export default function AdminDashboard() {
  const stats = [
    { label: "Leads Hoje", value: "12", change: "+3", color: "text-green-600" },
    { label: "Vendas Hoje", value: "3", change: "+1", color: "text-green-600" },
    { label: "Receita Hoje", value: "R$ 267", change: "+R$ 89", color: "text-green-600" },
    { label: "Taxa Conversão", value: "25%", change: "+5%", color: "text-green-600" },
  ];

  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-900 mb-6">Dashboard</h1>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        {stats.map((stat) => (
          <div key={stat.label} className="card">
            <p className="text-sm text-gray-500 mb-1">{stat.label}</p>
            <p className="text-3xl font-extrabold text-gray-900">{stat.value}</p>
            <p className={`text-sm mt-1 ${stat.color}`}>{stat.change} vs ontem</p>
          </div>
        ))}
      </div>

      {/* Recent Leads */}
      <div className="card">
        <h2 className="text-lg font-bold text-gray-900 mb-4">Leads Recentes</h2>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-gray-100">
                <th className="text-left py-3 px-2 font-semibold text-gray-600">Nome</th>
                <th className="text-left py-3 px-2 font-semibold text-gray-600">E-mail</th>
                <th className="text-left py-3 px-2 font-semibold text-gray-600">Data</th>
                <th className="text-left py-3 px-2 font-semibold text-gray-600">Status</th>
              </tr>
            </thead>
            <tbody>
              {[
                { nome: "Maria Silva", email: "maria@email.com", data: "08/01/2026", status: "Novo" },
                { nome: "João Santos", email: "joao@email.com", data: "08/01/2026", status: "Convertido" },
                { nome: "Ana Costa", email: "ana@email.com", data: "07/01/2026", status: "Novo" },
              ].map((lead) => (
                <tr key={lead.email} className="border-b border-gray-50 hover:bg-gray-50">
                  <td className="py-3 px-2 font-medium">{lead.nome}</td>
                  <td className="py-3 px-2 text-gray-600">{lead.email}</td>
                  <td className="py-3 px-2 text-gray-500">{lead.data}</td>
                  <td className="py-3 px-2">
                    <span
                      className={`inline-block px-2 py-0.5 rounded-full text-xs font-semibold ${
                        lead.status === "Convertido"
                          ? "bg-green-100 text-green-700"
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
      </div>
    </div>
  );
}

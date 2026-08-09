import MetricsChart from "@/components/MetricsChart";

export default function AdminMetricasPage() {
  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-900 mb-6">Métricas</h1>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        <div className="card">
          <p className="text-sm text-gray-500">Receita Total (30d)</p>
          <p className="text-3xl font-extrabold text-gray-900 mt-1">R$ 4.327</p>
          <p className="text-sm text-green-600 mt-1">+22% vs mês anterior</p>
        </div>
        <div className="card">
          <p className="text-sm text-gray-500">Total de Vendas (30d)</p>
          <p className="text-3xl font-extrabold text-gray-900 mt-1">48</p>
          <p className="text-sm text-green-600 mt-1">+15% vs mês anterior</p>
        </div>
        <div className="card">
          <p className="text-sm text-gray-500">Leads Capturados (30d)</p>
          <p className="text-3xl font-extrabold text-gray-900 mt-1">213</p>
          <p className="text-sm text-green-600 mt-1">+31% vs mês anterior</p>
        </div>
        <div className="card">
          <p className="text-sm text-gray-500">Ticket Médio</p>
          <p className="text-3xl font-extrabold text-gray-900 mt-1">R$ 90,15</p>
          <p className="text-sm text-gray-500 mt-1">Estável</p>
        </div>
      </div>

      {/* Charts */}
      <div className="grid lg:grid-cols-2 gap-6 mb-8">
        <div className="card">
          <h2 className="text-lg font-bold text-gray-900 mb-4">Receita (últimos 30 dias)</h2>
          <MetricsChart
            type="area"
            data={[
              { dia: "01/01", valor: 89 },
              { dia: "05/01", valor: 178 },
              { dia: "10/01", valor: 267 },
              { dia: "15/01", valor: 356 },
              { dia: "20/01", valor: 178 },
              { dia: "25/01", valor: 445 },
              { dia: "30/01", valor: 534 },
            ]}
            dataKey="valor"
            xAxisKey="dia"
            color="#2563eb"
          />
        </div>
        <div className="card">
          <h2 className="text-lg font-bold text-gray-900 mb-4">Leads por Origem</h2>
          <MetricsChart
            type="bar"
            data={[
              { origem: "Captura", total: 98 },
              { origem: "Orgânico", total: 54 },
              { origem: "Anúncios", total: 38 },
              { origem: "Indicação", total: 23 },
            ]}
            dataKey="total"
            xAxisKey="origem"
            color="#f59e0b"
          />
        </div>
      </div>

      {/* Funil */}
      <div className="card">
        <h2 className="text-lg font-bold text-gray-900 mb-6">Funil de Conversão (30d)</h2>
        <div className="space-y-4">
          {[
            { etapa: "Visitantes", valor: "2.847", pct: "100%", width: "100%" },
            { etapa: "Leads Capturados", valor: "213", pct: "7,5%", width: "75%" },
            { etapa: "Cliques no Checkout", valor: "89", pct: "3,1%", width: "31%" },
            { etapa: "Vendas", valor: "48", pct: "1,7%", width: "17%" },
          ].map((item) => (
            <div key={item.etapa}>
              <div className="flex justify-between text-sm mb-1">
                <span className="font-medium text-gray-700">{item.etapa}</span>
                <span className="text-gray-500">
                  {item.valor} ({item.pct})
                </span>
              </div>
              <div className="w-full bg-gray-100 rounded-full h-3">
                <div
                  className="bg-primary-500 h-3 rounded-full transition-all"
                  style={{ width: item.width }}
                />
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

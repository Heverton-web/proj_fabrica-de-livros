export default function ValueStack() {
  const items = [
    {
      icon: "📘",
      titulo: "Módulo Completo Passo a Passo",
      desc: "O método principal com todas as etapas detalhadas para você executar sem dúvida.",
      valor: "R$ 297",
    },
    {
      icon: "📋",
      titulo: "Planilha de Acompanhamento",
      desc: "Acompanhe seu progresso dia a dia com nossa planilha exclusiva.",
      valor: "R$ 47",
    },
    {
      icon: "🎥",
      titulo: "Bônus: Videoaulas Extras",
      desc: "Conteúdo complementar em vídeo para aprofundar os pontos-chave.",
      valor: "R$ 197",
    },
    {
      icon: "👥",
      titulo: "Bônus: Comunidade Exclusiva",
      desc: "Acesso ao grupo privado para networking e suporte com outros alunos.",
      valor: "R$ 97",
    },
    {
      icon: "🎫",
      titulo: "Bônus: Templates Prontos",
      desc: "Modelos testados e aprovados para você aplicar imediatamente.",
      valor: "R$ 67",
    },
  ];

  const total = items.reduce((acc, item) => {
    const num = parseInt(item.valor.replace(/\D/g, ""));
    return acc + num;
  }, 0);

  return (
    <section className="py-16 md:py-24 bg-gray-50">
      <div className="max-w-3xl mx-auto px-4 text-center">
        <span className="inline-block px-4 py-1 bg-amber-100 text-amber-700 rounded-full text-sm font-semibold mb-4">
          TUDO QUE VOCÊ VAI RECEBER
        </span>
        <h2 className="section-heading text-gray-900 mb-4">
          Veja o Valor Completo do Pacote
        </h2>
        <p className="text-gray-600 text-lg mb-10">
          Cada item foi desenhado para acelerar seus resultados
        </p>

        <div className="space-y-4 text-left">
          {items.map((item) => (
            <div
              key={item.titulo}
              className="card flex items-center gap-4"
            >
              <span className="text-3xl flex-shrink-0">{item.icon}</span>
              <div className="flex-1 min-w-0">
                <h3 className="font-bold text-gray-900">{item.titulo}</h3>
                <p className="text-sm text-gray-600">{item.desc}</p>
              </div>
              <span className="text-sm font-semibold text-gray-400 line-through flex-shrink-0">
                {item.valor}
              </span>
            </div>
          ))}
        </div>

        {/* Total */}
        <div className="mt-8 pt-6 border-t-2 border-dashed border-gray-300">
          <div className="flex items-center justify-center gap-4">
            <span className="text-lg text-gray-500">
              Valor total:{" "}
              <span className="line-through">R$ {total}</span>
            </span>
            <span className="text-2xl font-extrabold text-primary-600">
              por apenas {{PRECO}}
            </span>
          </div>
          <p className="text-sm text-gray-500 mt-2">
            Economia de R$ {total - parseInt({{PRECO}}.replace(/\D/g, ""))} — oferta por tempo limitado
          </p>
        </div>
      </div>
    </section>
  );
}

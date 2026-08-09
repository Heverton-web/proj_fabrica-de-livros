export default function Hero() {
  return (
    <section className="relative overflow-hidden bg-gradient-to-br from-primary-600 via-primary-700 to-primary-900 text-white">
      <div className="absolute inset-0 opacity-10 bg-[url('data:image/svg+xml;charset=utf-8,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20viewBox%3D%220%200%2080%2080%22%3E%3Cpath%20fill%3D%22%23fff%22%20d%3D%22M0%200h80v80H0z%22%2F%3E%3Cpath%20fill%3D%22%23ccc%22%20d%3D%22M0%2040h80v1H0z%22%2F%3E%3Cpath%20fill%3D%22%23ccc%22%20d%3D%22M40%200v80h1V0z%22%2F%3E%3C%2Fsvg%3E')]" />

      <div className="relative max-w-5xl mx-auto px-4 py-20 md:py-32 text-center">
        <span className="inline-block px-4 py-1 bg-white/10 backdrop-blur-sm rounded-full text-sm font-medium mb-6 border border-white/20">
          ⚙️ Engenharia de agentes de IA confiáveis
        </span>

        <h1 className="text-4xl md:text-5xl lg:text-6xl font-extrabold leading-tight mb-6 tracking-tight">
          Seu agente de IA erra em silêncio.<br />
          <span className="text-accent-500">O harness resolve.</span>
        </h1>

        <p className="text-lg md:text-xl text-primary-100 max-w-2xl mx-auto mb-10">
          O modelo não basta: é a engenharia ao redor — testes determinísticos,
          guardrails, loops de execução e observabilidade — que separa um
          experimento de um sistema em produção. Aprenda o caminho completo.
        </p>

        <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-8">
          <a href="#comprar" className="btn-accent text-xl px-10 py-5 rounded-full">
            QUERO O LIVRO COMPLETO →
          </a>
          <a
            href="#depoimentos"
            className="text-primary-200 hover:text-white underline underline-offset-4 transition-colors"
          >
            Ver o que dizem engenheiros
          </a>
        </div>

        <div className="flex flex-wrap justify-center gap-6 text-sm text-primary-200">
          <span>✅ 8 capítulos + playbook</span>
          <span>✅ Exemplos com código executável</span>
          <span>✅ Garantia de 7 dias</span>
        </div>
      </div>
    </section>
  );
}

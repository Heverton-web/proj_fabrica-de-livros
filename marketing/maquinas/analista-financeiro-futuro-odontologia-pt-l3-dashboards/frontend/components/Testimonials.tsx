export default function Testimonials() {
  const testimonials = [
    {
      nome: "Maria Fernanda",
      foto: "MF",
      cargo: "Empreendedora Digital",
      texto: "Em 30 dias aplicando o método, faturei R$ 4.500 a mais no meu negócio. Nunca imaginei que seria tão simples quando se tem o caminho certo.",
      estrelas: 5,
    },
    {
      nome: "Ricardo Santos",
      foto: "RS",
      cargo: "Analista de Marketing",
      texto: "Eu tinha assistido dezenas de cursos antes, mas nenhum me deu um passo a passo tão claro. As planilhas e templates são ouro puro.",
      estrelas: 5,
    },
    {
      nome: "Camila Oliveira",
      foto: "CO",
      cargo: "Freelancer",
      texto: "O suporte na comunidade fez toda a diferença. Quando tive dúvida, recebi resposta em minutos. Vale cada centavo do investimento.",
      estrelas: 5,
    },
    {
      nome: "Lucas Mendes",
      foto: "LM",
      cargo: "Estudante de TI",
      texto: "Comecei do zero absoluto. Em 2 meses já estava tendo meus primeiros resultados reais. Recomendo para qualquer pessoa que queira sair do lugar.",
      estrelas: 5,
    },
    {
      nome: "Ana Beatriz",
      foto: "AB",
      cargo: "Coach de Carreira",
      texto: "Aplicar o método me deu confiança para cobrar mais pelo meu trabalho. Meu faturamento triplicou em 90 dias.",
      estrelas: 5,
    },
    {
      nome: "Fernando Costa",
      foto: "FC",
      cargo: "Pequeno Empresário",
      texto: "Já investi mais de R$ 3.000 em cursos que não funcionaram. Este foi o único que me trouxe resultado real e mensurável.",
      estrelas: 5,
    },
  ];

  return (
    <section className="py-16 md:py-24" id="depoimentos">
      <div className="max-w-5xl mx-auto px-4 text-center">
        <span className="inline-block px-4 py-1 bg-green-100 text-green-700 rounded-full text-sm font-semibold mb-4">
          DEPOIMENTOS REAIS
        </span>
        <h2 className="section-heading text-gray-900 mb-4">
          O que nossos alunos dizem
        </h2>
        <p className="text-gray-600 text-lg mb-10">
          Resultados reais de pessoas reais que aplicaram o método
        </p>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6 text-left">
          {testimonials.map((t) => (
            <div key={t.nome} className="card">
              <div className="flex items-center gap-3 mb-4">
                <div className="w-12 h-12 rounded-full bg-primary-100 text-primary-700 flex items-center justify-center font-bold text-lg">
                  {t.foto}
                </div>
                <div>
                  <p className="font-bold text-gray-900">{t.nome}</p>
                  <p className="text-sm text-gray-500">{t.cargo}</p>
                </div>
              </div>
              <div className="text-amber-400 mb-3">
                {"★".repeat(t.estrelas)}
              </div>
              <p className="text-gray-600 text-sm leading-relaxed">
                &ldquo;{t.texto}&rdquo;
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

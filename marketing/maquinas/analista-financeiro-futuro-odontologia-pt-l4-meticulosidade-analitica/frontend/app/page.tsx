import Hero from "@/components/Hero";
import ValueStack from "@/components/ValueStack";
import Testimonials from "@/components/Testimonials";
import PricingCard from "@/components/PricingCard";
import Guarantee from "@/components/Guarantee";
import LeadForm from "@/components/LeadForm";

export default function SalesPage() {
  return (
    <main>
      {/* HERO */}
      <Hero />

      {/* DOR */}
      <section className="py-16 md:py-24 bg-gray-50">
        <div className="max-w-4xl mx-auto px-4 text-center">
          <h2 className="section-heading text-gray-900 mb-6">
            Você está cansado de...
          </h2>
          <div className="grid md:grid-cols-3 gap-6 mt-10">
            {[
              {
                icon: "😤",
                title: "Não ver resultados",
                desc: "Mesmo se esforçando, os resultados não aparecem. Sente que está perdendo tempo.",
              },
              {
                icon: "🤯",
                title: "Informação demais",
                desc: "YouTube, cursos, livros... Tanta informação que você não sabe por onde começar.",
              },
              {
                icon: "😰",
                title: "Medo de investir",
                desc: "Já gastou dinheiro com cursos que não funcionaram e tem medo de errar de novo.",
              },
            ].map((item) => (
              <div key={item.title} className="card text-center">
                <div className="text-5xl mb-4">{item.icon}</div>
                <h3 className="text-xl font-bold mb-2">{item.title}</h3>
                <p className="text-gray-600">{item.desc}</p>
              </div>
            ))}
          </div>
          <p className="text-xl md:text-2xl text-gray-700 mt-12 max-w-2xl mx-auto">
            Se você se identifica com pelo menos <strong>uma dessas situações</strong>,
            saiba que <strong>não é culpa sua</strong>. O problema está no método, não em você.
          </p>
        </div>
      </section>

      {/* SOLUÇÃO */}
      <section className="py-16 md:py-24">
        <div className="max-w-4xl mx-auto px-4 text-center">
          <span className="inline-block px-4 py-1 bg-primary-100 text-primary-700 rounded-full text-sm font-semibold mb-4">
            A SOLUÇÃO
          </span>
          <h2 className="section-heading text-gray-900 mb-6">
            Apresentamos: Analista Financeiro Futuro Odontologia Pt L4 Meticulosidade Analitica
          </h2>
          <p className="text-lg md:text-xl text-gray-600 max-w-3xl mx-auto mb-10">
            O método completo e testado que elimina a adivinhação e te guia
            passo a passo do zero até os resultados reais. Sem enrolação,
            sem teoria inútil — apenas o que funciona.
          </p>
          <div className="grid md:grid-cols-2 gap-8 text-left mt-12">
            {[
              {
                num: "01",
                title: "Método Passo a Passo",
                desc: "Instruções claras e objetivas para você executar sem dúvida alguma.",
              },
              {
                num: "02",
                title: "Resultados Comprovados",
                desc: "Centenas de alunos já aplicaram este método e obtiveram resultados reais.",
              },
              {
                num: "03",
                title: "Suporte Especializado",
                desc: "Tire suas dúvidas diretamente com quem já trilhou esse caminho.",
              },
              {
                num: "04",
                title: "Acesso Imediato",
                desc: "Comece agora mesmo. Todo o conteúdo disponível assim que você adquirir.",
              },
            ].map((item) => (
              <div key={item.num} className="flex gap-4">
                <div className="flex-shrink-0 w-12 h-12 bg-primary-600 text-white rounded-lg flex items-center justify-center font-bold text-lg">
                  {item.num}
                </div>
                <div>
                  <h3 className="text-lg font-bold mb-1">{item.title}</h3>
                  <p className="text-gray-600">{item.desc}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* VALUE STACK */}
      <ValueStack />

      {/* DEPOIMENTOS */}
      <Testimonials />

      {/* PRICING */}
      <section className="py-16 md:py-24 bg-primary-900" id="comprar">
        <div className="max-w-lg mx-auto px-4 text-center">
          <h2 className="section-heading text-white mb-4">
            Invista no seu futuro
          </h2>
          <p className="text-primary-200 text-lg mb-10">
            Escolha o plano ideal para você começar agora
          </p>
          <PricingCard />
        </div>
      </section>

      {/* GARANTIA */}
      <Guarantee />

      {/* CTA FINAL */}
      <section className="py-16 md:py-24 bg-gradient-to-br from-primary-600 to-primary-800">
        <div className="max-w-3xl mx-auto px-4 text-center">
          <h2 className="section-heading text-white mb-6">
            Chega de adiar. Comece agora.
          </h2>
          <p className="text-primary-100 text-lg md:text-xl mb-8 max-w-2xl mx-auto">
            Cada dia que passa sem agir é um dia a mais de estagnação.
            Você merece os resultados que tanto deseja — e este é o caminho.
          </p>
          <a
            href="#comprar"
            className="btn-accent text-xl px-12 py-5 rounded-full"
          >
            QUERO COMEÇAR AGORA →
          </a>
          <p className="text-primary-200 mt-4 text-sm">
            Pagamento seguro · Acesso imediato · Garantia de 7 dias
          </p>
        </div>
      </section>

      {/* CAPTURA DE LEAD (rodapé) */}
      <section className="py-16 bg-gray-900">
        <div className="max-w-xl mx-auto px-4">
          <h3 className="text-2xl font-bold text-white text-center mb-2">
            Ainda não tem certeza?
          </h3>
          <p className="text-gray-400 text-center mb-8">
            Receba um capítulo gratuito no seu e-mail e tire suas dúvidas.
          </p>
          <LeadForm variant="dark" />
        </div>
      </section>

      {/* FOOTER */}
      <footer className="py-8 bg-gray-950 text-gray-500 text-center text-sm">
        <p>© {new Date().getFullYear()} Analista Financeiro Futuro Odontologia Pt L4 Meticulosidade Analitica. Todos os direitos reservados.</p>
        <p className="mt-2">
          <a href="/captura" className="underline hover:text-gray-300">Política de Privacidade</a>
          {" · "}
          <a href="/captura" className="underline hover:text-gray-300">Termos de Uso</a>
        </p>
      </footer>
    </main>
  );
}

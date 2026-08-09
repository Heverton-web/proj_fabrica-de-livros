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
                icon: "😰",
                title: "Não saber o lucro real",
                desc: "Agenda cheia, muito trabalho, e no fim do mês a contadora diz que a clínica deu prejuízo. Você não sabe explicar por quê.",
              },
              {
                icon: "💸",
                title: "Misturar as contas",
                desc: "O dinheiro da clínica e o da família no mesmo cartão. Pró-labore? Nunca definiu — e o caixa vive no susto.",
              },
              {
                icon: "🦷",
                title: "Precificar no chute",
                desc: "Preço baseado no concorrente, desconto para não perder paciente e parcela longa demais. A margem some e você nem vê.",
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
            saiba que <strong>não é falta de esforço</strong>. A faculdade de Odontologia
            não ensina gestão — e o problema está no método, não em você.
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
            Apresentamos: O Dentista Gestor
          </h2>
          <p className="text-lg md:text-xl text-gray-600 max-w-3xl mx-auto mb-10">
            Um sistema completo de gestão financeira para a sua clínica, construído
            com <strong>IA gratuita</strong> — do fluxo de caixa diário ao painel de
            comando semanal. Em 4 capítulos práticos, você sai do caos do fim de
            expediente para decidir com números na mão.
          </p>
          <div className="grid md:grid-cols-2 gap-8 text-left mt-12">
            {[
              {
                num: "01",
                title: "Fluxo de caixa e DRE na prática",
                desc: "Monte o prontuário financeiro da clínica com planilha e um chat de IA gratuito — sem instalar nada.",
              },
              {
                num: "02",
                title: "Ticket médio e custo por sessão",
                desc: "Descubra quanto cada atendimento vale e quanto custa abrir a cadeira — a régua da precificação.",
              },
              {
                num: "03",
                title: "KPIs e dashboards gratuitos",
                desc: "Looker Studio e Power BI: semáforos, alertas e a reunião semanal de 5 minutos com o painel.",
              },
              {
                num: "04",
                title: "IA segura e conforme",
                desc: "Anonimização de dados de pacientes (LGPD), modelos locais e as regras do setor (CNES, CFO, Simples).",
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
            Assuma o comando da sua clínica
          </h2>
          <p className="text-primary-200 text-lg mb-10">
            Um livro, um painel e o seu fim de expediente transformado
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
            Chega de fechar o mês no escuro. Comece hoje.
          </h2>
          <p className="text-primary-100 text-lg md:text-xl mb-8 max-w-2xl mx-auto">
            A clínica que quebra não é a que tem poucos pacientes — é a que nunca
            olha os próprios números. Com IA gratuita e o método deste livro,
            você decide com dado, não com susto.
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
            Receba o Checklist de Saúde Financeira da Clínica no seu e-mail e
            descubra a cor do seu caixa.
          </p>
          <LeadForm variant="dark" />
        </div>
      </section>

      {/* FOOTER */}
      <footer className="py-8 bg-gray-950 text-gray-500 text-center text-sm">
        <p>© {new Date().getFullYear()} O Dentista Gestor. Todos os direitos reservados.</p>
        <p className="mt-2">
          <a href="/captura" className="underline hover:text-gray-300">Política de Privacidade</a>
          {" · "}
          <a href="/captura" className="underline hover:text-gray-300">Termos de Uso</a>
        </p>
      </footer>
    </main>
  );
}

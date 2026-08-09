import LeadForm from "@/components/LeadForm";

export default function CapturaPage() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-gray-900 to-primary-900 flex items-center justify-center px-4 py-16">
      <div className="max-w-lg w-full">
        <div className="text-center mb-8">
          <span className="inline-block px-4 py-1 bg-primary-500/20 text-primary-300 rounded-full text-sm font-semibold mb-4">
            CAPÍTULO GRATUITO
          </span>
          <h1 className="text-3xl md:text-4xl font-extrabold text-white mb-4">
            Baixe o 1º Capítulo de Analista Financeiro Futuro Odontologia Pt L4 Meticulosidade Analitica
          </h1>
          <p className="text-gray-300 text-lg">
            Descubra o método que já transformou a vida de centenas de pessoas.
            Preencha o formulário e receba gratuitamente.
          </p>
        </div>

        <div className="card">
          <LeadForm variant="light" showName />
        </div>

        <p className="text-gray-500 text-center text-xs mt-6">
          Prometemos: sem spam. Você pode cancelar a qualquer momento.
        </p>
      </div>
    </main>
  );
}

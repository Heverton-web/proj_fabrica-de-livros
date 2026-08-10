import Link from "next/link";

export default function ObrigadoPage() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-green-50 to-white flex items-center justify-center px-4">
      <div className="max-w-lg w-full text-center">
        <div className="text-7xl mb-6">🎉</div>
        <h1 className="text-3xl md:text-4xl font-extrabold text-gray-900 mb-4">
          Obrigado por se inscrever!
        </h1>
        <p className="text-lg text-gray-600 mb-8">
          Verifique seu e-mail — enviamos o capítulo gratuito para você.
          Se não encontrar na caixa de entrada, confira o spam.
        </p>
        <div className="space-y-4">
          <Link href="/" className="btn-primary w-full">
            Voltar para a página inicial
          </Link>
          <p className="text-sm text-gray-500">
            Enquanto isso, que tal dar uma olhada no que preparamos para você?
          </p>
        </div>
      </div>
    </main>
  );
}

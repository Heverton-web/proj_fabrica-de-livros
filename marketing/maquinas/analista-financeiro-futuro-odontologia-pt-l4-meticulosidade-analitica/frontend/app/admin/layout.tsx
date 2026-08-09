import Link from "next/link";

const navItems = [
  { href: "/admin", label: "Dashboard", icon: "📊" },
  { href: "/admin/leads", label: "Leads", icon: "👥" },
  { href: "/admin/emails", label: "E-mails", icon: "📧" },
  { href: "/admin/metricas", label: "Métricas", icon: "📈" },
];

export default function AdminLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="min-h-screen bg-gray-100">
      {/* Topbar */}
      <header className="bg-white border-b border-gray-200 px-6 py-3 flex items-center justify-between">
        <Link href="/admin" className="text-lg font-bold text-gray-900">
          ⚙️ Admin — Analista Financeiro Futuro Odontologia Pt L4 Meticulosidade Analitica
        </Link>
        <nav className="flex gap-1">
          {navItems.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className="px-4 py-2 rounded-lg text-sm font-medium text-gray-600 hover:bg-gray-100 hover:text-gray-900 transition-colors"
            >
              <span className="mr-1">{item.icon}</span>
              {item.label}
            </Link>
          ))}
        </nav>
        <Link href="/" className="text-sm text-gray-500 hover:text-gray-700">
          Ver site →
        </Link>
      </header>

      {/* Content */}
      <main className="p-6 max-w-7xl mx-auto">{children}</main>
    </div>
  );
}

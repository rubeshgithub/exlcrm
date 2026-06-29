# frontend/src/components/layout/Sidebar.tsx
"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const navigation = [
  { name: "Dashboard", href: "/dashboard", icon: "📊" },
  { name: "Contacts", href: "/contacts", icon: "👥" },
  { name: "Cases", href: "/cases", icon: "📁" },
  { name: "Encounters", href: "/encounters", icon: "🏥" },
  { name: "Appointments", href: "/appointments", icon: "📅" },
  { name: "Communications", href: "/communications", icon: "💬" },
  { name: "Documents", href: "/documents", icon: "📄" },
  { name: "Forms", href: "/forms", icon: "📋" },
  { name: "Workflows", href: "/workflows", icon: "⚡" },
  { name: "Billing", href: "/billing", icon: "💰" },
  { name: "Reports", href: "/reports", icon: "📈" },
  { name: "Settings", href: "/settings", icon: "⚙️" },
];

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="w-64 bg-white border-r border-gray-200 flex flex-col h-screen sticky top-0">
      {/* Logo */}
      <div className="p-4 border-b border-gray-200">
        <Link href="/dashboard" className="flex items-center gap-2">
          <span className="text-2xl font-bold text-brand-600">EXL-CRM</span>
        </Link>
      </div>

      {/* Navigation */}
      <nav className="flex-1 overflow-y-auto p-3">
        <ul className="space-y-1">
          {navigation.map((item) => {
            const isActive = pathname === item.href || pathname.startsWith(item.href + "/");
            return (
              <li key={item.name}>
                <Link
                  href={item.href}
                  className={`flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium transition ${
                    isActive
                      ? "bg-brand-50 text-brand-700"
                      : "text-gray-700 hover:bg-gray-100"
                  }`}
                >
                  <span className="text-base">{item.icon}</span>
                  {item.name}
                </Link>
              </li>
            );
          })}
        </ul>
      </nav>

      {/* Footer */}
      <div className="p-4 border-t border-gray-200">
        <p className="text-xs text-gray-500">© 2026 EXL-CRM</p>
      </div>
    </aside>
  );
}

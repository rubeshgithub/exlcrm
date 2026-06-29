# frontend/src/app/(dashboard)/dashboard/page.tsx
"use client";

import { useEffect, useState } from "react";

interface DashboardStats {
  totalContacts: number;
  activeCases: number;
  upcomingAppointments: number;
  pendingDocuments: number;
}

export default function DashboardPage() {
  const [stats, setStats] = useState<DashboardStats>({
    totalContacts: 0,
    activeCases: 0,
    upcomingAppointments: 0,
    pendingDocuments: 0,
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // TODO: Fetch stats from API
    // const { data } = await api.get("/api/v1/dashboard/stats");
    setLoading(false);
  }, []);

  return (
    <div>
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-gray-500">Welcome back to EXL-CRM</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        <StatCard
          title="Total Contacts"
          value={stats.totalContacts}
          icon="👥"
          color="bg-blue-500"
        />
        <StatCard
          title="Active Cases"
          value={stats.activeCases}
          icon="📁"
          color="bg-green-500"
        />
        <StatCard
          title="Appointments"
          value={stats.upcomingAppointments}
          icon="📅"
          color="bg-purple-500"
        />
        <StatCard
          title="Pending Docs"
          value={stats.pendingDocuments}
          icon="📄"
          color="bg-orange-500"
        />
      </div>

      {/* Quick Actions */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-xl border border-gray-200 p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h2>
          <div className="grid grid-cols-2 gap-3">
            <QuickActionButton icon="➕" label="New Contact" href="/contacts?action=new" />
            <QuickActionButton icon="📁" label="New Case" href="/cases?action=new" />
            <QuickActionButton icon="📅" label="New Appointment" href="/appointments?action=new" />
            <QuickActionButton icon="✉️" label="Send Email" href="/communications?action=email" />
          </div>
        </div>

        <div className="bg-white rounded-xl border border-gray-200 p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Recent Activity</h2>
          <div className="text-gray-500 text-sm text-center py-8">
            No recent activity. Start by adding contacts!
          </div>
        </div>
      </div>
    </div>
  );
}

function StatCard({ title, value, icon, color }: { title: string; value: number; icon: string; color: string }) {
  return (
    <div className="bg-white rounded-xl border border-gray-200 p-5">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm text-gray-500">{title}</p>
          <p className="text-2xl font-bold text-gray-900 mt-1">{value}</p>
        </div>
        <div className={`w-12 h-12 ${color} rounded-lg flex items-center justify-center text-xl`}>
          {icon}
        </div>
      </div>
    </div>
  );
}

function QuickActionButton({ icon, label, href }: { icon: string; label: string; href: string }) {
  return (
    <a
      href={href}
      className="flex items-center gap-3 p-3 bg-gray-50 hover:bg-brand-50 border border-gray-200 hover:border-brand-200 rounded-lg transition"
    >
      <span className="text-lg">{icon}</span>
      <span className="text-sm font-medium text-gray-700">{label}</span>
    </a>
  );
}

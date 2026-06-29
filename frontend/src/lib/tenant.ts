# frontend/src/lib/tenant.ts
/**
 * Tenant context and helpers
 */

export interface Tenant {
  id: string;
  name: string;
  industry: "immigration" | "healthcare";
  subdomain: string;
  plan: "starter" | "professional" | "enterprise";
  is_active: boolean;
  brand_name?: string;
  brand_logo_url?: string;
  brand_primary_color?: string;
  settings: Record<string, any>;
}

export function getIndustryLabel(industry: string): string {
  return industry === "immigration" ? "Immigration & Recruitment" : "Healthcare";
}

export function getIndustryIcon(industry: string): string {
  return industry === "immigration" ? "✈️" : "🏥";
}

export function getPlanLabel(plan: string): string {
  const labels: Record<string, string> = {
    starter: "Starter",
    professional: "Professional",
    enterprise: "Enterprise",
  };
  return labels[plan] || plan;
}

export function getPlanColor(plan: string): string {
  const colors: Record<string, string> = {
    starter: "bg-gray-100 text-gray-800",
    professional: "bg-blue-100 text-blue-800",
    enterprise: "bg-purple-100 text-purple-800",
  };
  return colors[plan] || "bg-gray-100 text-gray-800";
}

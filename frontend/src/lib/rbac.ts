# frontend/src/lib/rbac.ts
/**
 * Role-Based Access Control helpers for frontend
 */

export type UserRole = "super_admin" | "tenant_admin" | "supervisor" | "user";

export const ROLE_LEVELS: Record<UserRole, number> = {
  super_admin: 100,
  tenant_admin: 80,
  supervisor: 60,
  user: 40,
};

export const PERMISSIONS: Record<string, { minRole: UserRole; description: string }> = {
  "users:create": { minRole: "tenant_admin", description: "Invite new users" },
  "users:read": { minRole: "supervisor", description: "View user list" },
  "users:update": { minRole: "tenant_admin", description: "Edit user details" },
  "users:delete": { minRole: "tenant_admin", description: "Deactivate users" },
  "roles:manage": { minRole: "tenant_admin", description: "Manage roles & permissions" },
  "contacts:create": { minRole: "user", description: "Create contacts" },
  "contacts:read": { minRole: "user", description: "View contacts" },
  "contacts:update": { minRole: "user", description: "Edit contacts" },
  "contacts:delete": { minRole: "supervisor", description: "Delete contacts" },
  "cases:create": { minRole: "user", description: "Create cases" },
  "cases:read": { minRole: "user", description: "View cases" },
  "cases:update": { minRole: "user", description: "Edit cases" },
  "cases:delete": { minRole: "supervisor", description: "Delete cases" },
  "encounters:create": { minRole: "user", description: "Create encounters" },
  "encounters:read": { minRole: "user", description: "View encounters" },
  "encounters:update": { minRole: "user", description: "Edit encounters" },
  "encounters:delete": { minRole: "supervisor", description: "Delete encounters" },
  "communications:send": { minRole: "user", description: "Send emails/SMS" },
  "communications:read": { minRole: "user", description: "View communications" },
  "documents:create": { minRole: "user", description: "Upload documents" },
  "documents:read": { minRole: "user", description: "View documents" },
  "documents:delete": { minRole: "supervisor", description: "Delete documents" },
  "forms:manage": { minRole: "supervisor", description: "Manage form templates" },
  "forms:submit": { minRole: "user", description: "Submit forms" },
  "workflows:manage": { minRole: "supervisor", description: "Manage workflows" },
  "billing:access": { minRole: "tenant_admin", description: "Access billing" },
  "reports:export": { minRole: "supervisor", description: "Export reports" },
  "settings:manage": { minRole: "tenant_admin", description: "Manage settings" },
  "audit:read": { minRole: "tenant_admin", description: "View audit logs" },
};

export function hasPermission(role: UserRole | undefined, permission: string): boolean {
  if (!role) return false;
  const perm = PERMISSIONS[permission];
  if (!perm) return false;
  const userLevel = ROLE_LEVELS[role] || 0;
  const requiredLevel = ROLE_LEVELS[perm.minRole] || 0;
  return userLevel >= requiredLevel;
}

export function canAccess(role: UserRole | undefined, minRole: UserRole): boolean {
  if (!role) return false;
  return (ROLE_LEVELS[role] || 0) >= ROLE_LEVELS[minRole];
}

# frontend/src/lib/auth.ts
/**
 * NextAuth configuration for EXL-CRM
 */

import NextAuth from "next-auth";
import Credentials from "next-auth/providers/credentials";
import { authApi } from "./api";

export const { handlers, signIn, signOut, auth } = NextAuth({
  providers: [
    Credentials({
      name: "EXL-CRM",
      credentials: {
        email: { label: "Email", type: "email" },
        password: { label: "Password", type: "password" },
      },
      async authorize(credentials) {
        try {
          const { data } = await authApi.login(
            credentials.email as string,
            credentials.password as string
          );

          if (data.access_token) {
            // Store tokens
            if (typeof window !== "undefined") {
              localStorage.setItem("access_token", data.access_token);
              localStorage.setItem("refresh_token", data.refresh_token);
            }

            // Get user info
            const { data: userData } = await authApi.me();

            return {
              id: userData.user_id,
              email: userData.email,
              name: userData.email,
              role: userData.role,
              tenantId: userData.tenant_id,
            };
          }
          return null;
        } catch {
          return null;
        }
      },
    }),
  ],
  callbacks: {
    async jwt({ token, user }) {
      if (user) {
        token.role = (user as any).role;
        token.tenantId = (user as any).tenantId;
      }
      return token;
    },
    async session({ session, token }) {
      (session.user as any).role = token.role;
      (session.user as any).tenantId = token.tenantId;
      return session;
    },
  },
  pages: {
    signIn: "/login",
  },
  session: {
    strategy: "jwt",
    maxAge: 24 * 60 * 60, // 24 hours
  },
});

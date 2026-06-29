# frontend/src/lib/api.ts
/**
 * API client - Axios instance with interceptors
 * Handles JWT token management and error handling
 */

import axios, { AxiosInstance, InternalAxiosRequestConfig, AxiosError } from "axios";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

// Create axios instance
export const api: AxiosInstance = axios.create({
  baseURL: API_URL,
  timeout: 30000,
  headers: {
    "Content-Type": "application/json",
  },
});

// Request interceptor - add JWT token
api.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const token = typeof window !== "undefined" ? localStorage.getItem("access_token") : null;
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor - handle 401 and token refresh
api.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const originalRequest = error.config as InternalAxiosRequestConfig & { _retry?: boolean };

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = typeof window !== "undefined" ? localStorage.getItem("refresh_token") : null;
        if (!refreshToken) {
          // No refresh token, redirect to login
          if (typeof window !== "undefined") {
            window.location.href = "/login";
          }
          return Promise.reject(error);
        }

        const { data } = await axios.post(`${API_URL}/api/v1/auth/refresh`, {
          refresh_token: refreshToken,
        });

        if (typeof window !== "undefined") {
          localStorage.setItem("access_token", data.access_token);
          localStorage.setItem("refresh_token", data.refresh_token);
        }

        if (originalRequest.headers) {
          originalRequest.headers.Authorization = `Bearer ${data.access_token}`;
        }
        return api(originalRequest);
      } catch {
        // Refresh failed, redirect to login
        if (typeof window !== "undefined") {
          localStorage.removeItem("access_token");
          localStorage.removeItem("refresh_token");
          window.location.href = "/login";
        }
        return Promise.reject(error);
      }
    }

    return Promise.reject(error);
  }
);

// === API Helper Functions ===

export const authApi = {
  login: (email: string, password: string) =>
    api.post("/api/v1/auth/login", { email, password }),
  register: (data: { email: string; password: string; first_name: string; last_name: string }) =>
    api.post("/api/v1/auth/register", data),
  refresh: (refreshToken: string) =>
    api.post("/api/v1/auth/refresh", { refresh_token: refreshToken }),
  me: () => api.get("/api/v1/auth/me"),
  logout: () => api.post("/api/v1/auth/logout"),
};

export const contactsApi = {
  list: (params?: Record<string, any>) => api.get("/api/v1/contacts/", { params }),
  get: (id: string) => api.get(`/api/v1/contacts/${id}`),
  create: (data: any) => api.post("/api/v1/contacts/", data),
  update: (id: string, data: any) => api.put(`/api/v1/contacts/${id}`, data),
  delete: (id: string, hard?: boolean) => api.delete(`/api/v1/contacts/${id}`, { params: { hard } }),
  search: (q: string) => api.get("/api/v1/contacts/search/", { params: { q } }),
  timeline: (id: string) => api.get(`/api/v1/contacts/${id}/timeline`),
};

export const communicationsApi = {
  sendEmail: (data: any) => api.post("/api/v1/communications/email", data),
  sendSms: (data: any) => api.post("/api/v1/communications/sms", data),
  logCall: (data: any) => api.post("/api/v1/communications/call-log", data),
  logNote: (data: any) => api.post("/api/v1/communications/note", data),
  history: (contactId: string, params?: Record<string, any>) =>
    api.get(`/api/v1/communications/history/${contactId}`, { params }),
};

export const documentsApi = {
  upload: (formData: FormData) =>
    api.post("/api/v1/documents/upload", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    }),
  downloadUrl: (id: string) => api.get(`/api/v1/documents/${id}/download`),
  delete: (id: string) => api.delete(`/api/v1/documents/${id}`),
  sendForSignature: (id: string, signers: any[]) =>
    api.post(`/api/v1/documents/${id}/send-for-signature`, signers),
};

export const tenantsApi = {
  create: (data: any) => api.post("/api/v1/tenants/", data),
  get: (id: string) => api.get(`/api/v1/tenants/${id}`),
  update: (id: string, data: any) => api.put(`/api/v1/tenants/${id}`, data),
  list: () => api.get("/api/v1/tenants/"),
};

export const usersApi = {
  list: (params?: Record<string, any>) => api.get("/api/v1/users/", { params }),
  get: (id: string) => api.get(`/api/v1/users/${id}`),
  create: (data: any) => api.post("/api/v1/users/", data),
  update: (id: string, data: any) => api.put(`/api/v1/users/${id}`, data),
  delete: (id: string) => api.delete(`/api/v1/users/${id}`),
  permissions: () => api.get("/api/v1/users/me/permissions"),
};

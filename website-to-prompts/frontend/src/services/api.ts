import axios from "axios";

const API_BASE = import.meta.env.VITE_BACKEND_URL || "http://localhost:8000";

const api = axios.create({
  baseURL: API_BASE,
});

// Attach Supabase JWT to every request
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("sb_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export interface PromptStep {
  step: number;
  title: string;
  prompt: string;
}

export interface Blueprint {
  id: string;
  url: string;
  techStack: string;
  frontendPrompts: PromptStep[];
  backendPrompts: PromptStep[];
  createdAt: string;
}

export async function generateBlueprint(url: string): Promise<Blueprint> {
  const { data } = await api.post("/blueprint/generate", { url });
  return data;
}

export async function getBlueprints(): Promise<Blueprint[]> {
  const { data } = await api.get("/blueprint/list");
  return data;
}

export async function getBlueprint(id: string): Promise<Blueprint> {
  const { data } = await api.get(`/blueprint/${id}`);
  return data;
}

export default api;
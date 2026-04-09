import { create } from "zustand";
import { persist } from "zustand/middleware";

export interface UserProfile {
  id: number;
  username: string;
  email: string;
  age?: number;
  weight?: number;
  height?: number;
  sex?: string;
  goal?: string;
  activity_level?: string;
  target_kcal?: number;
  target_protein?: number;
  target_fat?: number;
  target_carbs?: number;
}

interface AuthState {
  token: string | null;
  user: UserProfile | null;
  setAuth: (token: string, user: UserProfile) => void;
  setUser: (user: UserProfile) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      token: null,
      user: null,
      setAuth: (token, user) => set({ token, user }),
      setUser: (user) => set({ user }),
      logout: () => set({ token: null, user: null }),
    }),
    { name: "auth" }
  )
);

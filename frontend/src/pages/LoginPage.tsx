import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import client from "../api/client";
import { useAuthStore } from "../store/authStore";

const schema = z.object({
  username: z.string().min(1),
  password: z.string().min(1),
});
type F = z.infer<typeof schema>;

export default function LoginPage() {
  const { register, handleSubmit, formState: { errors } } = useForm<F>({ resolver: zodResolver(schema) });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const setAuth = useAuthStore((s) => s.setAuth);

  const onSubmit = async (data: F) => {
    setLoading(true);
    setError("");
    try {
      const form = new URLSearchParams();
      form.append("username", data.username);
      form.append("password", data.password);
      const res = await client.post("/auth/login", form, {
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
      });
      setAuth(res.data.access_token, res.data.user);
      navigate("/menu");
    } catch (e: any) {
      setError(e.response?.data?.detail || "Помилка входу");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="bg-white rounded-2xl shadow-lg p-8 w-full max-w-sm">
        <h1 className="text-2xl font-bold text-primary mb-1">SuperSportyk</h1>
        <p className="text-gray-500 mb-6 text-sm">Вхід до акаунту</p>
        {error && <div className="bg-red-50 text-red-600 rounded-lg p-3 mb-4 text-sm">{error}</div>}
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-1">Ім'я користувача</label>
            <input {...register("username")} className="input w-full" />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Пароль</label>
            <input {...register("password")} type="password" className="input w-full" />
          </div>
          <button type="submit" disabled={loading} className="btn-primary w-full">
            {loading ? "Вхід..." : "Увійти"}
          </button>
        </form>
        <p className="mt-4 text-sm text-center text-gray-500">
          Немає акаунту?{" "}
          <Link to="/register" className="text-primary font-medium hover:underline">
            Зареєструватись
          </Link>
        </p>
      </div>
    </div>
  );
}

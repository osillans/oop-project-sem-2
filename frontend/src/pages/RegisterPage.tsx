import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import client from "../api/client";
import { useAuthStore } from "../store/authStore";

const schema = z.object({
  username: z.string().min(2, "Мінімум 2 символи"),
  email: z.string().email("Невірний email"),
  password: z.string().min(6, "Мінімум 6 символів"),
  age: z.coerce.number().min(10).max(120).optional().or(z.literal("")),
  weight: z.coerce.number().min(20).max(300).optional().or(z.literal("")),
  height: z.coerce.number().min(100).max(250).optional().or(z.literal("")),
  sex: z.enum(["male", "female", ""]).optional(),
  goal: z.enum(["lose", "gain", "maintain"]).default("maintain"),
  activity_level: z.enum(["sedentary","light","moderate","active","very_active"]).default("moderate"),
});
type F = z.infer<typeof schema>;

export default function RegisterPage() {
  const { register, handleSubmit, formState: { errors } } = useForm<F>({
    resolver: zodResolver(schema),
    defaultValues: { goal: "maintain", activity_level: "moderate" },
  });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const setAuth = useAuthStore((s) => s.setAuth);

  const onSubmit = async (data: F) => {
    setLoading(true);
    setError("");
    try {
      const payload = { ...data, age: data.age || null, weight: data.weight || null, height: data.height || null, sex: data.sex || null };
      const res = await client.post("/auth/register", payload);
      setAuth(res.data.access_token, res.data.user);
      navigate("/profile");
    } catch (e: any) {
      setError(e.response?.data?.detail || "Помилка реєстрації");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-8">
      <div className="bg-white rounded-2xl shadow-lg p-8 w-full max-w-md">
        <h1 className="text-2xl font-bold text-primary mb-1">SuperSportyk</h1>
        <p className="text-gray-500 mb-6 text-sm">Реєстрація нового акаунту</p>
        {error && <div className="bg-red-50 text-red-600 rounded-lg p-3 mb-4 text-sm">{error}</div>}
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-sm font-medium mb-1">Ім'я користувача</label>
              <input {...register("username")} className="input w-full" />
              {errors.username && <p className="err">{errors.username.message}</p>}
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Email</label>
              <input {...register("email")} type="email" className="input w-full" />
              {errors.email && <p className="err">{errors.email.message}</p>}
            </div>
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Пароль</label>
            <input {...register("password")} type="password" className="input w-full" />
            {errors.password && <p className="err">{errors.password.message}</p>}
          </div>
          <p className="text-xs text-gray-400">Необов'язкові дані для розрахунку КБЖВ:</p>
          <div className="grid grid-cols-3 gap-3">
            <div>
              <label className="block text-sm font-medium mb-1">Вік</label>
              <input {...register("age")} type="number" className="input w-full" />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Вага (кг)</label>
              <input {...register("weight")} type="number" step="0.1" className="input w-full" />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Зріст (см)</label>
              <input {...register("height")} type="number" className="input w-full" />
            </div>
          </div>
          <div className="grid grid-cols-3 gap-3">
            <div>
              <label className="block text-sm font-medium mb-1">Стать</label>
              <select {...register("sex")} className="input w-full">
                <option value="">—</option>
                <option value="male">Чол</option>
                <option value="female">Жін</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Ціль</label>
              <select {...register("goal")} className="input w-full">
                <option value="maintain">Підтримка</option>
                <option value="lose">Схуднення</option>
                <option value="gain">Набір</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Активність</label>
              <select {...register("activity_level")} className="input w-full">
                <option value="sedentary">Сидяча</option>
                <option value="light">Легка</option>
                <option value="moderate">Помірна</option>
                <option value="active">Активна</option>
                <option value="very_active">Висока</option>
              </select>
            </div>
          </div>
          <button type="submit" disabled={loading} className="btn-primary w-full">
            {loading ? "Реєстрація..." : "Зареєструватись"}
          </button>
        </form>
        <p className="mt-4 text-sm text-center text-gray-500">
          Вже є акаунт?{" "}
          <Link to="/login" className="text-primary font-medium hover:underline">Увійти</Link>
        </p>
      </div>
    </div>
  );
}

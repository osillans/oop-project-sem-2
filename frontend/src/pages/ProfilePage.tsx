import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { useState } from "react";
import client from "../api/client";
import { useAuthStore } from "../store/authStore";
import NutritionBar from "../components/NutritionBar";

const schema = z.object({
  age: z.coerce.number().min(10).max(120),
  weight: z.coerce.number().min(20).max(300),
  height: z.coerce.number().min(100).max(250),
  sex: z.enum(["male", "female"]),
  goal: z.enum(["lose", "gain", "maintain"]),
  activity_level: z.enum(["sedentary","light","moderate","active","very_active"]),
});
type F = z.infer<typeof schema>;

const GOAL_LABELS = { lose: "Схуднення", gain: "Набір маси", maintain: "Підтримка ваги" };
const ACTIVITY_LABELS = {
  sedentary: "Сидячий спосіб життя",
  light: "Легка активність",
  moderate: "Помірна активність",
  active: "Активний",
  very_active: "Дуже активний",
};

export default function ProfilePage() {
  const { user, setUser } = useAuthStore();
  const [success, setSuccess] = useState(false);
  const [loading, setLoading] = useState(false);

  const { register, handleSubmit, formState: { errors } } = useForm<F>({
    resolver: zodResolver(schema),
    defaultValues: {
      age: user?.age ?? undefined,
      weight: user?.weight ?? undefined,
      height: user?.height ?? undefined,
      sex: (user?.sex as "male" | "female") ?? "male",
      goal: (user?.goal as "lose"|"gain"|"maintain") ?? "maintain",
      activity_level: (user?.activity_level as F["activity_level"]) ?? "moderate",
    },
  });

  const onSubmit = async (data: F) => {
    setLoading(true);
    setSuccess(false);
    try {
      const res = await client.put("/users/me", data);
      setUser(res.data);
      setSuccess(true);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto py-8 px-4">
      <h1 className="text-2xl font-bold mb-6">Мій профіль</h1>

      {user?.target_kcal && (
        <div className="bg-white rounded-xl shadow-sm border p-5 mb-6">
          <h2 className="font-semibold text-gray-700 mb-4">Цільові показники КБЖВ</h2>
          <NutritionBar label="Калорії" value={user.target_kcal} max={user.target_kcal} color="#f97316" unit="ккал" />
          <NutritionBar label="Білки" value={user.target_protein!} max={user.target_protein!} color="#3b82f6" />
          <NutritionBar label="Жири" value={user.target_fat!} max={user.target_fat!} color="#f59e0b" />
          <NutritionBar label="Вуглеводи" value={user.target_carbs!} max={user.target_carbs!} color="#16a34a" />
          <div className="grid grid-cols-4 gap-2 mt-3 text-center">
            {[
              { label: "Ккал", value: user.target_kcal, color: "text-orange-500" },
              { label: "Білки", value: user.target_protein, color: "text-blue-500" },
              { label: "Жири", value: user.target_fat, color: "text-yellow-500" },
              { label: "Вуглеводи", value: user.target_carbs, color: "text-green-600" },
            ].map(({ label, value, color }) => (
              <div key={label} className="bg-gray-50 rounded-lg p-2">
                <div className={`text-lg font-bold ${color}`}>{value?.toFixed(0)}</div>
                <div className="text-xs text-gray-500">{label}</div>
              </div>
            ))}
          </div>
        </div>
      )}

      <div className="bg-white rounded-xl shadow-sm border p-5">
        <h2 className="font-semibold text-gray-700 mb-4">Параметри</h2>
        {success && <div className="bg-green-50 text-green-700 rounded-lg p-3 mb-4 text-sm">Збережено та перераховано КБЖВ</div>}
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          <div className="grid grid-cols-3 gap-3">
            {[
              { key: "age" as const, label: "Вік", unit: "років" },
              { key: "weight" as const, label: "Вага", unit: "кг" },
              { key: "height" as const, label: "Зріст", unit: "см" },
            ].map(({ key, label, unit }) => (
              <div key={key}>
                <label className="block text-sm font-medium mb-1">{label}</label>
                <div className="relative">
                  <input {...register(key)} type="number" step="0.1" className="input w-full pr-10" />
                  <span className="absolute right-2 top-2 text-gray-400 text-xs">{unit}</span>
                </div>
                {errors[key] && <p className="err">{errors[key]?.message}</p>}
              </div>
            ))}
          </div>
          <div className="grid grid-cols-3 gap-3">
            <div>
              <label className="block text-sm font-medium mb-1">Стать</label>
              <select {...register("sex")} className="input w-full">
                <option value="male">Чоловіча</option>
                <option value="female">Жіноча</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Ціль</label>
              <select {...register("goal")} className="input w-full">
                {Object.entries(GOAL_LABELS).map(([k, v]) => <option key={k} value={k}>{v}</option>)}
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Активність</label>
              <select {...register("activity_level")} className="input w-full">
                {Object.entries(ACTIVITY_LABELS).map(([k, v]) => <option key={k} value={k}>{v}</option>)}
              </select>
            </div>
          </div>
          <button type="submit" disabled={loading} className="btn-primary w-full">
            {loading ? "Збереження..." : "Зберегти та перерахувати КБЖВ"}
          </button>
        </form>
      </div>
    </div>
  );
}

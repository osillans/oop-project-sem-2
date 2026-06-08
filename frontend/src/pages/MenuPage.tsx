import { useState } from "react";
import client from "../api/client";
import { useAuthStore } from "../store/authStore";
import { useProductsStore } from "../store/productsStore";
import MenuCard from "../components/MenuCard";
import NutritionBar from "../components/NutritionBar";
import { useNavigate } from "react-router-dom";

interface MenuItem {
  id: number;
  product_id: number;
  product_name: string;
  meal_number: number;
  weight_g: number;
  kcal: number;
  protein: number;
  fat: number;
  carbs: number;
}

interface Menu {
  id: number;
  meals_count: number;
  total_kcal: number;
  total_protein: number;
  total_fat: number;
  total_carbs: number;
  items: MenuItem[];
}

export default function MenuPage() {
  const { user } = useAuthStore();
  const { selectedIds } = useProductsStore();
  const [mealsCount, setMealsCount] = useState(3);
  const [strategy, setStrategy] = useState("proportional");
  const [menu, setMenu] = useState<Menu | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const generate = async () => {
    setLoading(true);
    setError("");
    try {
      const body: any = { meals_count: mealsCount, strategy };
      if (selectedIds.length > 0) body.product_ids = selectedIds;
      const res = await client.post("/menu/generate", body);
      setMenu(res.data);
    } catch (e: any) {
      setError(e.response?.data?.detail || "Помилка генерації");
    } finally {
      setLoading(false);
    }
  };

  const groupedItems = menu
    ? Array.from({ length: menu.meals_count }, (_, i) =>
        menu.items.filter((item) => item.meal_number === i + 1)
      )
    : [];

  return (
    <div className="max-w-4xl mx-auto py-8 px-4">
      <h1 className="text-2xl font-bold mb-6">Генератор меню</h1>

      {!user?.target_kcal && (
        <div className="bg-yellow-50 border border-yellow-200 rounded-xl p-4 mb-6 text-sm text-yellow-800">
          Спочатку заповніть{" "}
          <button onClick={() => navigate("/profile")} className="underline font-medium">
            профіль
          </button>{" "}
          для розрахунку норми КБЖВ.
        </div>
      )}

      {selectedIds.length > 0 ? (
        <div className="bg-green-50 border border-green-200 rounded-xl p-3 mb-4 text-sm text-green-800 flex items-center justify-between">
          <span>Вибрано продуктів для генерації: <strong>{selectedIds.length}</strong></span>
          <button onClick={() => navigate("/products")} className="underline text-xs">
            змінити вибір
          </button>
        </div>
      ) : (
        <div className="bg-blue-50 border border-blue-200 rounded-xl p-3 mb-4 text-sm text-blue-800">
          Продукти не вибрано — буде використано всі доступні.{" "}
          <button onClick={() => navigate("/products")} className="underline font-medium">
            Вибрати продукти →
          </button>
        </div>
      )}

      <div className="bg-white rounded-xl shadow-sm border p-5 mb-6">
        <div className="flex flex-wrap gap-4 items-end">
          <div>
            <label className="block text-sm font-medium mb-1">Кількість прийомів їжі</label>
            <div className="flex gap-2">
              {[3, 4, 5].map((n) => (
                <button
                  key={n}
                  onClick={() => setMealsCount(n)}
                  className={`w-10 h-10 rounded-lg font-medium border transition ${
                    mealsCount === n
                      ? "bg-primary text-white border-primary"
                      : "border-gray-200 hover:border-primary"
                  }`}
                >
                  {n}
                </button>
              ))}
            </div>
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Стратегія розподілу</label>
            <select
              value={strategy}
              onChange={(e) => setStrategy(e.target.value)}
              className="input"
            >
              <option value="proportional">Пропорційна</option>
              <option value="uniform">Рівномірна</option>
            </select>
          </div>
          <button
            onClick={generate}
            disabled={loading || !user?.target_kcal}
            className="btn-primary h-10 px-6"
          >
            {loading ? "Розраховую..." : "Згенерувати меню"}
          </button>
        </div>
        {error && <p className="text-red-500 text-sm mt-3">{error}</p>}
      </div>

      {menu && (
        <>
          <div className="bg-white rounded-xl shadow-sm border p-5 mb-6">
            <h2 className="font-semibold text-gray-700 mb-4">Підсумок дня</h2>
            <NutritionBar label="Калорії" value={menu.total_kcal} max={user?.target_kcal ?? menu.total_kcal} color="#f97316" unit="ккал" />
            <NutritionBar label="Білки" value={menu.total_protein} max={user?.target_protein ?? menu.total_protein} color="#3b82f6" />
            <NutritionBar label="Жири" value={menu.total_fat} max={user?.target_fat ?? menu.total_fat} color="#f59e0b" />
            <NutritionBar label="Вуглеводи" value={menu.total_carbs} max={user?.target_carbs ?? menu.total_carbs} color="#16a34a" />
            <div className="mt-3 flex justify-end">
              <button
                onClick={() => navigate(`/analytics?menu_id=${menu.id}`)}
                className="text-primary text-sm underline"
              >
                Переглянути аналітику →
              </button>
            </div>
          </div>

          <div className="space-y-4">
            {groupedItems.map((items, idx) => (
              items.length > 0 && (
                <MenuCard key={idx} mealNumber={idx + 1} items={items} />
              )
            ))}
          </div>
        </>
      )}
    </div>
  );
}

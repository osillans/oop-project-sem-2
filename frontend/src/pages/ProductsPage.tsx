import { useEffect, useState } from "react";
import client from "../api/client";
import ProductForm from "../components/ProductForm";
import { useProductsStore } from "../store/productsStore";

interface Product {
  id: number;
  name: string;
  kcal_per_100g: number;
  protein: number;
  fat: number;
  carbs: number;
}

export default function ProductsPage() {
  const [products, setProducts] = useState<Product[]>([]);
  const [search, setSearch] = useState("");
  const [modal, setModal] = useState<{ mode: "add" | "edit"; product?: Product } | null>(null);
  const [loading, setLoading] = useState(false);
  const [seeding, setSeeding] = useState(false);
  const { selectedIds, toggle, selectAll, clearAll } = useProductsStore();

  const load = async (q = "") => {
    const res = await client.get(`/products?search=${q}`);
    setProducts(res.data);
  };

  useEffect(() => { load(); }, []);

  const handleSeed = async () => {
    setSeeding(true);
    try {
      const res = await client.post("/products/seed");
      await load(search);
      alert(`Додано ${res.data.added} базових продуктів`);
    } finally {
      setSeeding(false);
    }
  };

  const handleDelete = async (id: number) => {
    if (!confirm("Видалити продукт?")) return;
    await client.delete(`/products/${id}`);
    load(search);
  };

  const handleSubmit = async (data: Omit<Product, "id">) => {
    setLoading(true);
    try {
      if (modal?.mode === "edit" && modal.product) {
        await client.put(`/products/${modal.product.id}`, data);
      } else {
        await client.post("/products", data);
      }
      setModal(null);
      load(search);
    } finally {
      setLoading(false);
    }
  };

  const allVisible = products.map((p) => p.id);
  const allChecked = allVisible.length > 0 && allVisible.every((id) => selectedIds.includes(id));

  return (
    <div className="max-w-4xl mx-auto py-8 px-4">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold">База продуктів</h1>
          {selectedIds.length > 0 && (
            <p className="text-sm text-primary mt-0.5">
              Вибрано для меню: <span className="font-semibold">{selectedIds.length}</span> продуктів
              <button onClick={clearAll} className="ml-2 text-gray-400 hover:text-red-500 text-xs underline">
                скинути
              </button>
            </p>
          )}
        </div>
        <div className="flex gap-2">
          <button onClick={handleSeed} disabled={seeding} className="btn-secondary">
            {seeding ? "Завантаження..." : "Базові продукти"}
          </button>
          <button onClick={() => setModal({ mode: "add" })} className="btn-primary">
            + Додати продукт
          </button>
        </div>
      </div>

      <input
        type="text"
        placeholder="Пошук продукту..."
        value={search}
        onChange={(e) => { setSearch(e.target.value); load(e.target.value); }}
        className="input w-full mb-4"
      />

      {modal && (
        <div className="fixed inset-0 bg-black/40 flex items-center justify-center z-50">
          <div className="bg-white rounded-2xl shadow-xl p-6 w-full max-w-md">
            <h2 className="text-lg font-semibold mb-4">
              {modal.mode === "add" ? "Новий продукт" : "Редагувати продукт"}
            </h2>
            <ProductForm
              initial={modal.product}
              onSubmit={handleSubmit as any}
              onCancel={() => setModal(null)}
              loading={loading}
            />
          </div>
        </div>
      )}

      {products.length === 0 ? (
        <div className="text-center text-gray-400 py-16">
          <p className="text-4xl mb-2">🥦</p>
          <p>Продуктів ще немає. Додайте перший!</p>
        </div>
      ) : (
        <div className="bg-white rounded-xl shadow-sm border overflow-hidden">
          <table className="w-full text-sm">
            <thead className="bg-gray-50 border-b">
              <tr>
                <th className="p-3 w-10">
                  <input
                    type="checkbox"
                    checked={allChecked}
                    onChange={() => allChecked ? clearAll() : selectAll(allVisible)}
                    className="w-4 h-4 accent-green-600 cursor-pointer"
                    title="Вибрати всі"
                  />
                </th>
                <th className="text-left p-3 font-medium text-gray-600">Продукт</th>
                <th className="text-right p-3 font-medium text-gray-600">Ккал</th>
                <th className="text-right p-3 font-medium text-gray-600 text-blue-600">Б</th>
                <th className="text-right p-3 font-medium text-gray-600 text-orange-500">Ж</th>
                <th className="text-right p-3 font-medium text-gray-600 text-green-600">В</th>
                <th className="p-3"></th>
              </tr>
            </thead>
            <tbody>
              {products.map((p) => {
                const checked = selectedIds.includes(p.id);
                return (
                  <tr
                    key={p.id}
                    onClick={() => toggle(p.id)}
                    className={`border-b last:border-0 cursor-pointer transition ${
                      checked ? "bg-green-50 hover:bg-green-100" : "hover:bg-gray-50"
                    }`}
                  >
                    <td className="p-3 text-center" onClick={(e) => e.stopPropagation()}>
                      <input
                        type="checkbox"
                        checked={checked}
                        onChange={() => toggle(p.id)}
                        className="w-4 h-4 accent-green-600 cursor-pointer"
                      />
                    </td>
                    <td className="p-3 font-medium">{p.name}</td>
                    <td className="p-3 text-right">{p.kcal_per_100g}</td>
                    <td className="p-3 text-right text-blue-600">{p.protein}</td>
                    <td className="p-3 text-right text-orange-500">{p.fat}</td>
                    <td className="p-3 text-right text-green-600">{p.carbs}</td>
                    <td className="p-3 text-right" onClick={(e) => e.stopPropagation()}>
                      <button
                        onClick={() => setModal({ mode: "edit", product: p })}
                        className="text-gray-500 hover:text-primary mr-2 text-xs border rounded px-2 py-0.5"
                      >
                        Ред.
                      </button>
                      <button
                        onClick={() => handleDelete(p.id)}
                        className="text-red-400 hover:text-red-600 text-xs border border-red-200 rounded px-2 py-0.5"
                      >
                        Вид.
                      </button>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
          <p className="text-xs text-gray-400 p-3">* Показники на 100г продукту. Натисни рядок щоб вибрати продукт для генерації меню.</p>
        </div>
      )}
    </div>
  );
}

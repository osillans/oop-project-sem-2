import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import client from "../api/client";
import { useAuthStore } from "../store/authStore";
import MacroChart from "../components/MacroChart";
import {
    BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Cell
} from "recharts";

interface Summary {
    menu_id: number;
    target: { kcal: number; protein: number; fat: number; carbs: number };
    actual: { kcal: number; protein: number; fat: number; carbs: number };
    percent: { kcal: number; protein: number; fat: number; carbs: number };
}

export default function AnalyticsPage() {
    const [params] = useSearchParams();
    const { user } = useAuthStore();
    const [summary, setSummary] = useState<Summary | null>(null);
    const [menuId, setMenuId] = useState(params.get("menu_id") || "");
    const [error, setError] = useState("");

    const load = async (id: string) => {
        if (!id) return;
        setError("");
        try {
            const res = await client.get(`/analytics/summary?menu_id=${id}`);
            setSummary(res.data);
        } catch (e: any) {
            setError(e.response?.data?.detail || "Меню не знайдено");
            setSummary(null);
        }
    };

    useEffect(() => { if (menuId) load(menuId); }, []);

    const barData = summary
        ? [
            { name: "Ккал", ціль: summary.target.kcal, факт: summary.actual.kcal },
            { name: "Білки (г)", ціль: summary.target.protein, факт: summary.actual.protein },
            { name: "Жири (г)", ціль: summary.target.fat, факт: summary.actual.fat },
            { name: "Вуглеводи (г)", ціль: summary.target.carbs, факт: summary.actual.carbs },
        ]
        : [];

    const pctColor = (pct: number) =>
        pct >= 90 && pct <= 110 ? "#16a34a" : pct >= 75 ? "#f59e0b" : "#ef4444";

    return (
        <div className="max-w-4xl mx-auto py-8 px-4">
            <h1 className="text-2xl font-bold mb-6">Аналітика меню</h1>

            <div className="bg-white rounded-xl shadow-sm border p-5 mb-6">
                <div className="flex gap-3 items-end">
                    <div className="flex-1">
                        <label className="block text-sm font-medium mb-1">ID меню</label>
                        <input
                            type="number"
                            value={menuId}
                            onChange={(e) => setMenuId(e.target.value)}
                            className="input w-full"
                            placeholder="Введіть ID меню"
                        />
                    </div>
                    <button onClick={() => load(menuId)} className="btn-primary h-10 px-5">
                        Аналізувати
                    </button>
                </div>
                {error && <p className="text-red-500 text-sm mt-2">{error}</p>}
            </div>

            {summary && (
                <>
                    <div className="grid grid-cols-4 gap-3 mb-6">
                        {[
                            { label: "Калорії", pct: summary.percent.kcal, actual: summary.actual.kcal, target: summary.target.kcal, unit: "ккал" },
                            { label: "Білки", pct: summary.percent.protein, actual: summary.actual.protein, target: summary.target.protein, unit: "г" },
                            { label: "Жири", pct: summary.percent.fat, actual: summary.actual.fat, target: summary.target.fat, unit: "г" },
                            { label: "Вуглеводи", pct: summary.percent.carbs, actual: summary.actual.carbs, target: summary.target.carbs, unit: "г" },
                        ].map(({ label, pct, actual, target, unit }) => (
                            <div key={label} className="bg-white rounded-xl border shadow-sm p-4 text-center">
                                <div className="text-2xl font-bold" style={{ color: pctColor(pct) }}>
                                    {pct}%
                                </div>
                                <div className="text-sm font-medium text-gray-700 mt-1">{label}</div>
                                <div className="text-xs text-gray-400 mt-1">
                                    {actual.toFixed(0)} / {target.toFixed(0)} {unit}
                                </div>
                            </div>
                        ))}
                    </div>

                    <div className="grid grid-cols-2 gap-6">
                        <div className="bg-white rounded-xl shadow-sm border p-5">
                            <h2 className="font-semibold text-gray-700 mb-4">Ціль vs Факт</h2>
                            <ResponsiveContainer width="100%" height={260}>
                                <BarChart data={barData} margin={{ top: 5, right: 10, left: -10, bottom: 5 }}>
                                    <CartesianGrid strokeDasharray="3 3" />
                                    <XAxis dataKey="name" tick={{ fontSize: 11 }} />
                                    <YAxis tick={{ fontSize: 11 }} />
                                    <Tooltip />
                                    <Legend />
                                    <Bar dataKey="ціль" fill="#d1d5db" />
                                    <Bar dataKey="факт" fill="#16a34a" />
                                </BarChart>
                            </ResponsiveContainer>
                        </div>

                        <div className="bg-white rounded-xl shadow-sm border p-5">
                            <h2 className="font-semibold text-gray-700 mb-4">Розподіл макросів (факт)</h2>
                            <MacroChart
                                protein={summary.actual.protein}
                                fat={summary.actual.fat}
                                carbs={summary.actual.carbs}
                            />
                        </div>
                    </div>
                </>
            )}
        </div>
    );
}

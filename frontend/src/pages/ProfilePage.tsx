import { useAuthStore } from "../store/authStore";
import NutritionBar from "../components/NutritionBar";

export default function ProfilePage() {
    const { user } = useAuthStore();

    return (
        <div className="max-w-2xl mx-auto py-8 px-4">
            <h1 className="text-2xl font-bold mb-6">Мій профіль</h1>
            <div className="bg-white rounded-xl shadow-sm border p-5 mb-6">
                <h2 className="font-semibold text-gray-700 mb-3">Дані акаунту</h2>
                <div className="grid grid-cols-2 gap-3 text-sm">
                    <div><span className="text-gray-400">Імʼя:</span> <span className="font-medium">{user?.username}</span></div>
                    <div><span className="text-gray-400">Email:</span> <span className="font-medium">{user?.email}</span></div>
                    <div><span className="text-gray-400">Вік:</span> <span className="font-medium">{user?.age ?? "—"}</span></div>
                    <div><span className="text-gray-400">Вага:</span> <span className="font-medium">{user?.weight ? `${user.weight} кг` : "—"}</span></div>
                    <div><span className="text-gray-400">Зріст:</span> <span className="font-medium">{user?.height ? `${user.height} см` : "—"}</span></div>
                    <div><span className="text-gray-400">Стать:</span> <span className="font-medium">{user?.sex === "male" ? "Чоловіча" : user?.sex === "female" ? "Жіноча" : "—"}</span></div>
                    <div><span className="text-gray-400">Ціль:</span> <span className="font-medium">{user?.goal === "lose" ? "Схуднення" : user?.goal === "gain" ? "Набір маси" : "Підтримка"}</span></div>
                    <div><span className="text-gray-400">Активність:</span> <span className="font-medium">{user?.activity_level ?? "—"}</span></div>
                </div>
            </div>

            {user?.target_kcal && (
                <div className="bg-white rounded-xl shadow-sm border p-5">
                    <h2 className="font-semibold text-gray-700 mb-4">Добова норма КБЖВ</h2>
                    <NutritionBar label="Калорії" value={user.target_kcal} max={user.target_kcal} color="#f97316" unit="ккал" />
                    <NutritionBar label="Білки" value={user.target_protein!} max={user.target_protein!} color="#3b82f6" />
                    <NutritionBar label="Жири" value={user.target_fat!} max={user.target_fat!} color="#f59e0b" />
                    <NutritionBar label="Вуглеводи" value={user.target_carbs!} max={user.target_carbs!} color="#16a34a" />
                    <div className="grid grid-cols-4 gap-2 mt-4 text-center">
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
        </div>
    );
}
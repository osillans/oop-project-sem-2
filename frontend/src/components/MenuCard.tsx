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

interface Props {
  mealNumber: number;
  items: MenuItem[];
}

const MEAL_NAMES: Record<number, string> = {
  1: "Сніданок",
  2: "Другий сніданок",
  3: "Обід",
  4: "Полудень",
  5: "Вечеря",
};

export default function MenuCard({ mealNumber, items }: Props) {
  const totals = items.reduce(
    (acc, i) => ({
      kcal: acc.kcal + i.kcal,
      protein: acc.protein + i.protein,
      fat: acc.fat + i.fat,
      carbs: acc.carbs + i.carbs,
    }),
    { kcal: 0, protein: 0, fat: 0, carbs: 0 }
  );

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-4">
      <h3 className="font-semibold text-primary text-lg mb-3">
        {MEAL_NAMES[mealNumber] ?? `Прийом ${mealNumber}`}
      </h3>
      <table className="w-full text-sm">
        <thead>
          <tr className="text-gray-400 border-b">
            <th className="text-left pb-1">Продукт</th>
            <th className="text-right pb-1">Вага</th>
            <th className="text-right pb-1">Ккал</th>
            <th className="text-right pb-1">Б</th>
            <th className="text-right pb-1">Ж</th>
            <th className="text-right pb-1">В</th>
          </tr>
        </thead>
        <tbody>
          {items.map((item) => (
            <tr key={item.id} className="border-b last:border-0">
              <td className="py-1 font-medium">{item.product_name}</td>
              <td className="text-right text-gray-500">{item.weight_g} г</td>
              <td className="text-right">{item.kcal}</td>
              <td className="text-right text-blue-600">{item.protein}</td>
              <td className="text-right text-orange-500">{item.fat}</td>
              <td className="text-right text-green-600">{item.carbs}</td>
            </tr>
          ))}
        </tbody>
        <tfoot>
          <tr className="font-semibold text-gray-700 border-t">
            <td className="pt-2">Разом</td>
            <td></td>
            <td className="text-right pt-2">{totals.kcal.toFixed(0)}</td>
            <td className="text-right pt-2 text-blue-600">{totals.protein.toFixed(1)}</td>
            <td className="text-right pt-2 text-orange-500">{totals.fat.toFixed(1)}</td>
            <td className="text-right pt-2 text-green-600">{totals.carbs.toFixed(1)}</td>
          </tr>
        </tfoot>
      </table>
    </div>
  );
}

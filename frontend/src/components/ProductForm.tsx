import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";

const schema = z.object({
  name: z.string().min(1, "Назва обов'язкова"),
  kcal_per_100g: z.coerce.number().positive("Має бути > 0"),
  protein: z.coerce.number().min(0),
  fat: z.coerce.number().min(0),
  carbs: z.coerce.number().min(0),
});

type FormData = z.infer<typeof schema>;

interface Props {
  initial?: Partial<FormData>;
  onSubmit: (data: FormData) => Promise<void>;
  onCancel: () => void;
  loading?: boolean;
}

export default function ProductForm({ initial, onSubmit, onCancel, loading }: Props) {
  const { register, handleSubmit, formState: { errors } } = useForm<FormData>({
    resolver: zodResolver(schema),
    defaultValues: initial,
  });

  const fields: { key: keyof FormData; label: string; unit: string }[] = [
    { key: "kcal_per_100g", label: "Ккал / 100г", unit: "ккал" },
    { key: "protein", label: "Білки / 100г", unit: "г" },
    { key: "fat", label: "Жири / 100г", unit: "г" },
    { key: "carbs", label: "Вуглеводи / 100г", unit: "г" },
  ];

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-3">
      <div>
        <label className="block text-sm font-medium mb-1">Назва продукту</label>
        <input {...register("name")} className="input w-full" placeholder="напр. Куряче філе" />
        {errors.name && <p className="text-red-500 text-xs mt-1">{errors.name.message}</p>}
      </div>
      <div className="grid grid-cols-2 gap-3">
        {fields.map(({ key, label, unit }) => (
          <div key={key}>
            <label className="block text-sm font-medium mb-1">{label}</label>
            <div className="relative">
              <input {...register(key)} type="number" step="0.1" className="input w-full pr-8" />
              <span className="absolute right-2 top-2 text-gray-400 text-xs">{unit}</span>
            </div>
            {errors[key] && <p className="text-red-500 text-xs mt-1">{errors[key]?.message}</p>}
          </div>
        ))}
      </div>
      <div className="flex gap-2 pt-2">
        <button type="submit" disabled={loading} className="btn-primary flex-1">
          {loading ? "Збереження..." : "Зберегти"}
        </button>
        <button type="button" onClick={onCancel} className="btn-secondary flex-1">
          Скасувати
        </button>
      </div>
    </form>
  );
}

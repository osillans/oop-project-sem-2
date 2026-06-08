interface Props {
    label: string;
    value: number;
    max: number;
    color: string;
    unit?: string;
}

export default function NutritionBar({ label, value, max, color, unit = "г" }: Props) {
    const pct = max > 0 ? Math.min((value / max) * 100, 100) : 0;
    return (
        <div className="mb-2">
            <div className="flex justify-between text-sm mb-1">
                <span className="font-medium text-gray-700">{label}</span>
                <span className="text-gray-500">{value.toFixed(0)} / {max.toFixed(0)} {unit}</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-3">
                <div className="h-3 rounded-full transition-all" style={{ width: `${pct}%`, backgroundColor: color }} />
            </div>
        </div>
    );
}

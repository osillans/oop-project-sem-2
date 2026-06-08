import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer } from "recharts";

interface Props {
    protein: number;
    fat: number;
    carbs: number;
}

const COLORS = ["#3b82f6", "#f97316", "#16a34a"];

export default function MacroChart({ protein, fat, carbs }: Props) {
    const data = [
        { name: "Білки", value: Math.round(protein * 4) },
        { name: "Жири", value: Math.round(fat * 9) },
        { name: "Вуглеводи", value: Math.round(carbs * 4) },
    ];

    return (
        <ResponsiveContainer width="100%" height={240}>
            <PieChart>
                <Pie
                    data={data}
                    cx="50%"
                    cy="50%"
                    innerRadius={60}
                    outerRadius={90}
                    paddingAngle={3}
                    dataKey="value"
                    label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                    labelLine={false}
                >
                    {data.map((_, i) => (
                        <Cell key={i} fill={COLORS[i % COLORS.length]} />
                    ))}
                </Pie>
                <Tooltip formatter={(v: number) => `${v} ккал`} />
            </PieChart>
        </ResponsiveContainer>
    );
}
import numpy as np
from scipy.optimize import minimize
from typing import List, Dict
import random


# ── Паттерн Strategy: стратегії розподілу калорій між прийомами їжі ──────────
# UniformStrategy — рівні частки для кожного прийому
# ProportionalStrategy — реалістичний розподіл (сніданок/обід/вечеря/перекуси)

class UniformStrategy:
    def get_meal_ratios(self, meals_count: int) -> List[float]:
        return [1.0 / meals_count] * meals_count


class ProportionalStrategy:
    PATTERNS = {
        3: [0.30, 0.40, 0.30],
        4: [0.25, 0.35, 0.25, 0.15],
        5: [0.25, 0.35, 0.20, 0.10, 0.10],
    }

    def get_meal_ratios(self, meals_count: int) -> List[float]:
        return self.PATTERNS.get(meals_count, [1.0 / meals_count] * meals_count)


def get_strategy(name: str):
    return UniformStrategy() if name == "uniform" else ProportionalStrategy()


# ── Максимально допустима вага порції залежно від калорійності продукту ───────
# Низькокалорійні (овочі) — до 300г, середні — до 500г, жирні (горіхи) — до 100г

def get_max_weight(p: Dict) -> int:
    k = p["kcal_per_100g"]
    if k < 50:  return 300
    if k < 150: return 500
    if k > 500: return 100
    return 400


# ── Словник ключових слів для визначення харчової групи продукту ──────────────
# Використовується для підбору продуктів, сумісних за типом прийому їжі

FOOD_GROUP_KEYWORDS: Dict[str, List[str]] = {
    "grain":          ["гречк", "рис", "вівсян", "пластівц", "макарон", "хліб", "кукурудз", "перловк", "батат", "картопл"],
    "protein_meat":   ["курич", "яловичин", "свинин", "індичк", "тунець", "лосось", "скумбр"],
    "protein_dairy":  ["сир", "йогурт", "молоко", "кефір", "сметан"],
    "protein_egg":    ["яєчн", "яйц"],
    "vegetable":      ["броколі", "морква", "огірок", "томат", "капуст", "цибул", "шпинат", "перець", "кабачок", "картопл"],
    "fruit":          ["яблук", "банан", "апельсин", "полуниц", "чорниц", "груш"],
    "fat_nut":        ["мигдал", "горіх", "арахіс", "арахісов"],
    "fat_oil":        ["олія"],
    "fat_avocado":    ["авокадо"],
    "legume":         ["сочевиц", "нут", "квасол"],
}

# ── Тип прийому їжі за порядковим номером ────────────────────────────────────
MEAL_TYPE_BY_IDX = {
    0: "breakfast",
    1: "lunch",
    2: "dinner",
    3: "snack",
    4: "snack",
}

# ── Допустимі харчові групи для кожного типу прийому їжі ─────────────────────
# Визначає "що логічно їсти" на сніданок, обід, вечерю та перекус
MEAL_COMPOSITION: Dict[str, List[str]] = {
    "breakfast": ["grain", "protein_dairy", "protein_egg", "fruit", "fat_nut"],
    "lunch":     ["protein_meat", "grain", "vegetable", "legume", "fat_avocado"],
    "dinner":    ["protein_meat", "vegetable", "legume", "protein_dairy", "fat_avocado"],
    "snack":     ["fruit", "protein_dairy", "fat_nut", "grain"],
}

# ── Несумісні пари харчових груп в одному прийомі ────────────────────────────
# Наприклад, оливкова олія не поєднується з фруктами чи молочними
INCOMPATIBLE_PAIRS = [
    ("fat_oil", "fruit"),
    ("fat_oil", "protein_dairy"),
    ("fat_oil", "fat_nut"),
    ("grain",   "fruit"),
]


def get_food_group(p: Dict) -> str:
    """Визначає харчову групу продукту за назвою, з резервним аналізом макросів."""
    name = p["name"].lower()
    for group, keywords in FOOD_GROUP_KEYWORDS.items():
        if any(kw in name for kw in keywords):
            return group
    k = p["kcal_per_100g"]
    if k == 0: return "other"
    if p["protein"] * 4 / k >= 0.35: return "protein_meat"
    if p["fat"]     * 9 / k >= 0.50: return "fat_nut"
    if p["carbs"]   * 4 / k >= 0.50: return "grain"
    if k < 50: return "vegetable"
    return "other"


def dominant_macro(p: Dict) -> str:
    """Повертає домінуючий макронутрієнт продукту за часткою від загальної калорійності."""
    k = p["kcal_per_100g"]
    if k == 0: return "other"
    if p["protein"] * 4 / k >= 0.35: return "protein"
    if p["fat"]     * 9 / k >= 0.50: return "fat"
    if p["carbs"]   * 4 / k >= 0.50: return "carbs"
    if k < 50: return "veggie"
    return "other"


def are_compatible(groups_in_meal: List[str], new_group: str) -> bool:
    """Перевіряє, чи можна додати продукт певної групи до вже зібраного прийому їжі."""
    for existing in groups_in_meal:
        if (existing, new_group) in INCOMPATIBLE_PAIRS:
            return False
        if (new_group, existing) in INCOMPATIBLE_PAIRS:
            return False
    return True


def select_meal_products(
    products: List[Dict],
    meal_idx: int,
    meals_count: int,
    used_ids: set,
    rng: random.Random,
    min_products: int = 3,
    max_products: int = 6,
) -> List[Dict]:
    """
    Вибирає 3-6 продуктів для одного прийому їжі за логікою:
    1. Фільтрує продукти за допустимими групами для даного типу прийому
    2. Перевіряє сумісність кожного нового продукту з уже вибраними
    3. Якщо не вистачає — доповнює сумісними продуктами з решти
    4. Крайній випадок — будь-які ще не використані продукти
    """
    meal_key = MEAL_TYPE_BY_IDX.get(meal_idx, "dinner" if meal_idx % 2 == 0 else "snack")
    allowed_groups = MEAL_COMPOSITION[meal_key]

    candidates = [p for p in products if get_food_group(p) in allowed_groups and p["id"] not in used_ids]
    rng.shuffle(candidates)

    selected = []
    selected_groups = []

    for p in candidates:
        if len(selected) >= max_products:
            break
        g = get_food_group(p)
        if are_compatible(selected_groups, g):
            selected.append(p)
            selected_groups.append(g)

    if len(selected) < min_products:
        rest = [p for p in products if p["id"] not in {s["id"] for s in selected} and p["id"] not in used_ids]
        rng.shuffle(rest)
        for p in rest:
            if len(selected) >= max_products:
                break
            g = get_food_group(p)
            if are_compatible(selected_groups, g):
                selected.append(p)
                selected_groups.append(g)

    if len(selected) < min_products:
        rest = [p for p in products if p["id"] not in {s["id"] for s in selected}]
        rng.shuffle(rest)
        selected.extend(rest[:min_products - len(selected)])

    return selected


def optimize_single_meal(
    products: List[Dict],
    target_kcal: float,
    target_protein: float,
    target_fat: float,
    target_carbs: float,
) -> List[Dict]:
    """
    Оптимізує вагу кожного продукту в межах одного прийому їжі.

    Алгоритм:
    1. Початкові ваги розраховуються рівномірно відносно цільового калоражу
    2. Функція MSE мінімізується методом L-BFGS-B (градієнтний спуск з обмеженнями):
       MSE = 2.0*(ΔКкал)² + 1.5*(ΔБілки)² + 2.5*(ΔЖири)² + 2.5*(ΔВуглеводи)²
       Жири та вуглеводи мають вищу вагу — вони частіше не добираються
    3. Обмеження (bounds): мінімум 0г, максимум залежить від калорійності продукту
    4. Продукти з вагою < 20г після оптимізації відкидаються
    """
    n = len(products)
    if n == 0:
        return []

    x0 = np.clip(
        np.array([(target_kcal / n) / max(p["kcal_per_100g"], 1) * 100 for p in products]),
        20, 200,
    )

    def objective(w):
        w = np.clip(w, 0, None)
        ak = sum(p["kcal_per_100g"] * w[i] / 100 for i, p in enumerate(products))
        ap = sum(p["protein"]        * w[i] / 100 for i, p in enumerate(products))
        af = sum(p["fat"]            * w[i] / 100 for i, p in enumerate(products))
        ac = sum(p["carbs"]          * w[i] / 100 for i, p in enumerate(products))
        return (
            2.0 * ((ak - target_kcal)    / (target_kcal    + 1)) ** 2 +
            1.5 * ((ap - target_protein) / (target_protein + 1)) ** 2 +
            2.5 * ((af - target_fat)     / (target_fat     + 1)) ** 2 +
            2.5 * ((ac - target_carbs)   / (target_carbs   + 1)) ** 2
        )

    bounds = [(0, get_max_weight(p)) for p in products]
    res = minimize(objective, x0, method="L-BFGS-B", bounds=bounds,
                   options={"maxiter": 3000, "ftol": 1e-15})
    weights = np.clip(res.x, 0, None)

    result = []
    for i, p in enumerate(products):
        w = round(float(weights[i]))
        if w >= 20:
            result.append({
                "product_id":   p["id"],
                "product_name": p["name"],
                "weight_g":     w,
                "kcal":    round(p["kcal_per_100g"] * w / 100, 1),
                "protein": round(p["protein"]        * w / 100, 1),
                "fat":     round(p["fat"]            * w / 100, 1),
                "carbs":   round(p["carbs"]          * w / 100, 1),
            })

    if not result:
        top = sorted(products, key=lambda p: p["kcal_per_100g"], reverse=True)[:3]
        w = max(50, min(round(target_kcal / max(len(top), 1) / max(top[0]["kcal_per_100g"], 1) * 100), 300))
        for p in top:
            result.append({
                "product_id": p["id"], "product_name": p["name"], "weight_g": w,
                "kcal":    round(p["kcal_per_100g"] * w / 100, 1),
                "protein": round(p["protein"]        * w / 100, 1),
                "fat":     round(p["fat"]            * w / 100, 1),
                "carbs":   round(p["carbs"]          * w / 100, 1),
            })

    return result


def fix_excess(result_items: List[Dict], target_protein: float, target_fat: float, target_carbs: float, target_kcal: float = 0) -> List[Dict]:
    """
    Коригує перевищення загального калоражу.
    Якщо сума ккал перевищує ціль більш ніж на 3% — пропорційно зменшує
    вагу та КБЖВ всіх позицій меню до цільового рівня.
    """
    if target_kcal > 0:
        total_kcal = sum(i["kcal"] for i in result_items)
        if total_kcal > target_kcal * 1.03:
            scale = target_kcal / total_kcal
            for item in result_items:
                item["weight_g"] = round(item["weight_g"] * scale)
                item["kcal"]     = round(item["kcal"]     * scale, 1)
                item["protein"]  = round(item["protein"]  * scale, 1)
                item["fat"]      = round(item["fat"]      * scale, 1)
                item["carbs"]    = round(item["carbs"]    * scale, 1)
    return [i for i in result_items if i["weight_g"] >= 20]


def fix_deficits(
    result_items: List[Dict],
    products: List[Dict],
    target_protein: float,
    target_fat: float,
    target_carbs: float,
) -> List[Dict]:
    """
    Усуває дефіцит макронутрієнтів після основної оптимізації.
    Якщо фактичне значення білків/жирів/вуглеводів < 88% від цілі:
    1. Знаходить продукт з найбільшою концентрацією дефіцитного макросу
    2. Розраховує необхідну вагу для покриття дефіциту
    3. Додає цей продукт у той прийом, де дефіцит найбільший
    """
    for macro, target in [("protein", target_protein), ("fat", target_fat), ("carbs", target_carbs)]:
        total = sum(i[macro] for i in result_items)
        if total >= target * 0.88:
            continue
        sources = sorted(
            [p for p in products if dominant_macro(p) == macro],
            key=lambda p: p[macro], reverse=True,
        )
        if not sources:
            continue
        best = sources[0]
        deficit_g = target - total
        extra_w = max(30, min(round(deficit_g / max(best[macro], 0.1) * 100), get_max_weight(best)))

        meals = sorted(set(i["meal_number"] for i in result_items))
        meal_totals = {m: sum(i[macro] for i in result_items if i["meal_number"] == m) for m in meals}
        target_meal = min(meal_totals, key=meal_totals.get)

        result_items.append({
            "product_id":   best["id"],
            "product_name": best["name"],
            "meal_number":  target_meal,
            "weight_g":     extra_w,
            "kcal":    round(best["kcal_per_100g"] * extra_w / 100, 1),
            "protein": round(best["protein"]        * extra_w / 100, 1),
            "fat":     round(best["fat"]            * extra_w / 100, 1),
            "carbs":   round(best["carbs"]          * extra_w / 100, 1),
        })

    return result_items


def optimize_menu(
    products: List[Dict],
    target_kcal: float,
    target_protein: float,
    target_fat: float,
    target_carbs: float,
    meals_count: int,
    strategy_name: str = "proportional",
) -> List[Dict]:
    """
    Головна функція генерації денного меню. Алгоритм:

    1. Вибір стратегії розподілу калорій (рівномірна / пропорційна)
    2. Для кожного прийому їжі:
       a. select_meal_products — підбір 3-6 сумісних продуктів за типом прийому
       b. optimize_single_meal — MSE-оптимізація ваг через L-BFGS-B
    3. fix_excess  — обрізання загального калоражу якщо > 103% цілі
    4. fix_deficits — добір продуктів якщо макрос < 88% цілі
    5. fix_excess  — повторна перевірка після добору
    """
    if not products:
        return []

    strategy    = get_strategy(strategy_name)
    meal_ratios = strategy.get_meal_ratios(meals_count)
    rng         = random.Random(42)
    used_ids: set = set()
    result_items: List[Dict] = []

    for meal_idx, ratio in enumerate(meal_ratios):
        slot = select_meal_products(products, meal_idx, meals_count, used_ids, rng)
        used_ids.update(p["id"] for p in slot)

        items = optimize_single_meal(
            slot,
            target_kcal    * ratio,
            target_protein * ratio,
            target_fat     * ratio,
            target_carbs   * ratio,
        )
        for item in items:
            item["meal_number"] = meal_idx + 1
        result_items.extend(items)

    result_items = fix_excess(result_items, target_protein, target_fat, target_carbs, target_kcal)
    result_items = fix_deficits(result_items, products, target_protein, target_fat, target_carbs)
    result_items = fix_excess(result_items, target_protein, target_fat, target_carbs, target_kcal)

    return result_items

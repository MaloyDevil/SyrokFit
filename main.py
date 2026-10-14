import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import json
import os
import flet as ft

APP_TITLE = "SyrokFit"
APP_SUBTITLE = "by Syrok • Smart Macro & Ration Tracker"

# База продуктов с привязкой к поштучному и порционному весу
DEFAULT_FOODS = [
    {"id": "f0", "name": "Сырок творожный (Syrok Special)", "cat": "Молочные", "emoji": "🍫", "kcal": 320, "p": 8.5, "f": 20.0, "c": 26.5, "unit_g": 45, "unit_name": "сырок"},
    {"id": "f1", "name": "Куриная грудка (филе)", "cat": "Мясо", "emoji": "🍗", "kcal": 113, "p": 23.6, "f": 1.9, "c": 0.4, "unit_g": 180, "unit_name": "филе"},
    {"id": "f2", "name": "Индейка (филе)", "cat": "Мясо", "emoji": "🦃", "kcal": 104, "p": 21.6, "f": 1.7, "c": 0.0, "unit_g": 180, "unit_name": "филе"},
    {"id": "f3", "name": "Говядина постная", "cat": "Мясо", "emoji": "🥩", "kcal": 158, "p": 22.2, "f": 7.1, "c": 0.0, "unit_g": 150, "unit_name": "стейк"},
    {"id": "f4", "name": "Лосось / Сёмга", "cat": "Рыба", "emoji": "🍣", "kcal": 208, "p": 20.0, "f": 13.0, "c": 0.0, "unit_g": 150, "unit_name": "стейк"},
    {"id": "f5", "name": "Тунец в собств. соку", "cat": "Рыба", "emoji": "🐟", "kcal": 96, "p": 21.0, "f": 1.2, "c": 0.0, "unit_g": 130, "unit_name": "банка"},
    {"id": "f6", "name": "Минтай / Треска", "cat": "Рыба", "emoji": "🐠", "kcal": 72, "p": 16.0, "f": 0.9, "c": 0.0, "unit_g": 160, "unit_name": "филе"},
    {"id": "f7", "name": "Яйцо куриное", "cat": "Молочные", "emoji": "🥚", "kcal": 157, "p": 12.7, "f": 11.5, "c": 0.7, "unit_g": 55, "unit_name": "шт."},
    {"id": "f8", "name": "Творог 5%", "cat": "Молочные", "emoji": "🥣", "kcal": 121, "p": 17.2, "f": 5.0, "c": 1.8, "unit_g": 180, "unit_name": "пачка"},
    {"id": "f9", "name": "Творог 0%", "cat": "Молочные", "emoji": "🍚", "kcal": 71, "p": 16.5, "f": 0.5, "c": 1.3, "unit_g": 180, "unit_name": "пачка"},
    {"id": "f10", "name": "Греческий йогурт 2%", "cat": "Молочные", "emoji": "🥛", "kcal": 66, "p": 8.0, "f": 2.0, "c": 4.2, "unit_g": 140, "unit_name": "баночка"},
    {"id": "f11", "name": "Сыр твёрдый 45%", "cat": "Молочные", "emoji": "🧀", "kcal": 334, "p": 24.0, "f": 26.0, "c": 0.0, "unit_g": 20, "unit_name": "ломтик"},
    {"id": "f12", "name": "Овсяные хлопья", "cat": "Крупы", "emoji": "🌾", "kcal": 342, "p": 12.3, "f": 6.1, "c": 59.5, "unit_g": 25, "unit_name": "ст. л."},
    {"id": "f13", "name": "Гречка отварная", "cat": "Крупы", "emoji": "🍲", "kcal": 110, "p": 4.2, "f": 1.1, "c": 21.3, "unit_g": 180, "unit_name": "порц."},
    {"id": "f14", "name": "Рис белый отварной", "cat": "Крупы", "emoji": "🍚", "kcal": 116, "p": 2.2, "f": 0.5, "c": 24.9, "unit_g": 180, "unit_name": "порц."},
    {"id": "f15", "name": "Макароны отварные", "cat": "Крупы", "emoji": "🍝", "kcal": 112, "p": 3.5, "f": 0.4, "c": 23.2, "unit_g": 200, "unit_name": "порц."},
    {"id": "f16", "name": "Картофель запечённый", "cat": "Крупы", "emoji": "🥔", "kcal": 93, "p": 2.5, "f": 0.1, "c": 21.0, "unit_g": 100, "unit_name": "шт."},
    {"id": "f17", "name": "Чечевица / Нут отварной", "cat": "Крупы", "emoji": "🫘", "kcal": 116, "p": 9.0, "f": 0.4, "c": 20.0, "unit_g": 180, "unit_name": "порц."},
    {"id": "f18", "name": "Хлеб цельнозерновой", "cat": "Крупы", "emoji": "🍞", "kcal": 247, "p": 10.0, "f": 3.4, "c": 43.0, "unit_g": 35, "unit_name": "кус."},
    {"id": "f19", "name": "Банан", "cat": "Овощи/Фрукты", "emoji": "🍌", "kcal": 89, "p": 1.1, "f": 0.3, "c": 22.8, "unit_g": 120, "unit_name": "шт."},
    {"id": "f20", "name": "Яблоко", "cat": "Овощи/Фрукты", "emoji": "🍎", "kcal": 52, "p": 0.3, "f": 0.2, "c": 13.8, "unit_g": 150, "unit_name": "шт."},
    {"id": "f21", "name": "Авокадо", "cat": "Овощи/Фрукты", "emoji": "🥑", "kcal": 160, "p": 2.0, "f": 14.7, "c": 1.8, "unit_g": 140, "unit_name": "шт."},
    {"id": "f22", "name": "Салат из свежих овощей", "cat": "Овощи/Фрукты", "emoji": "🥗", "kcal": 25, "p": 1.0, "f": 0.2, "c": 4.5, "unit_g": 150, "unit_name": "миска"},
    {"id": "f23", "name": "Брокколи на пару", "cat": "Овощи/Фрукты", "emoji": "🥦", "kcal": 34, "p": 2.8, "f": 0.4, "c": 6.6, "unit_g": 150, "unit_name": "порц."},
    {"id": "f24", "name": "Орехи (миндаль/грецкий)", "cat": "Жиры/Спорт", "emoji": "🥜", "kcal": 609, "p": 18.6, "f": 54.5, "c": 13.0, "unit_g": 25, "unit_name": "горсть"},
    {"id": "f25", "name": "Арахисовая паста", "cat": "Жиры/Спорт", "emoji": "🍯", "kcal": 588, "p": 25.0, "f": 50.0, "c": 20.0, "unit_g": 20, "unit_name": "ст. л."},
    {"id": "f26", "name": "Оливковое масло", "cat": "Жиры/Спорт", "emoji": "🫒", "kcal": 884, "p": 0.0, "f": 100.0, "c": 0.0, "unit_g": 10, "unit_name": "ст. л."},
    {"id": "f27", "name": "Сывороточный протеин", "cat": "Жиры/Спорт", "emoji": "🥤", "kcal": 390, "p": 78.0, "f": 5.5, "c": 6.5, "unit_g": 30, "unit_name": "скуп"},
]

# Готовые шаблоны рационов с привязкой к целям
RATION_TEMPLATES = [
    {
        "id": "t_syrok",
        "title": "🍫 Фирменный баланс от Syrok",
        "desc": "Сбалансированный рацион на каждый день с творожным сырком на перекус!",
        "goals": [-10, 0, 15],
        "items": {
            "breakfast": [("f12", 75), ("f7", 110), ("f19", 120)],
            "lunch": [("f1", 180), ("f13", 180), ("f22", 150)],
            "dinner": [("f2", 180), ("f14", 180), ("f26", 10)],
            "snack": [("f0", 45), ("f8", 180)],
        }
    },
    {
        "id": "t_cut",
        "title": "🔥 Сушка и рельеф (Высокобелковый)",
        "desc": "Максимум белка и клетчатки для сытости при дефиците калорий.",
        "goals": [-20, -10],
        "items": {
            "breakfast": [("f7", 110), ("f12", 50), ("f20", 150)],
            "lunch": [("f1", 180), ("f13", 150), ("f22", 150)],
            "dinner": [("f6", 200), ("f23", 180), ("f26", 10)],
            "snack": [("f9", 180), ("f10", 140), ("f24", 25)],
        }
    },
    {
        "id": "t_mass",
        "title": "💪 Спортивный массонабор",
        "desc": "Повышенная калорийность, сложные углеводы и протеин для роста мышц.",
        "goals": [15, 0],
        "items": {
            "breakfast": [("f12", 85), ("f7", 165), ("f19", 120), ("f25", 20)],
            "lunch": [("f3", 180), ("f15", 240), ("f22", 150), ("f26", 10)],
            "dinner": [("f1", 180), ("f14", 220), ("f11", 40)],
            "snack": [("f27", 30), ("f8", 180), ("f0", 45)],
        }
    },
    {
        "id": "t_student",
        "title": "🎓 Бюджетный и быстрый (Студенческий)",
        "desc": "Простые и доступные продукты: курица, гречка, яйца, макароны и творог.",
        "goals": [-20, -10, 0, 15],
        "items": {
            "breakfast": [("f12", 75), ("f7", 110), ("f19", 120)],
            "lunch": [("f1", 180), ("f15", 200), ("f22", 150)],
            "dinner": [("f1", 160), ("f13", 180), ("f18", 35)],
            "snack": [("f8", 180), ("f20", 150)],
        }
    },
    {
        "id": "t_med",
        "title": "🍣 Средиземноморский (С рыбой и авокадо)",
        "desc": "Богат Омега-3, полезными жирами, рыбой и свежими овощами.",
        "goals": [-10, 0],
        "items": {
            "breakfast": [("f18", 70), ("f21", 70), ("f7", 110)],
            "lunch": [("f4", 150), ("f14", 180), ("f22", 150)],
            "dinner": [("f5", 130), ("f16", 200), ("f23", 150), ("f26", 10)],
            "snack": [("f10", 140), ("f24", 25), ("f20", 150)],
        }
    },
    {
        "id": "t_veg",
        "title": "🌱 Вегетарианский (Без мяса и рыбы)",
        "desc": "Белок из яиц, творога, греческого йогурта, бобовых и орехов.",
        "goals": [-20, -10, 0, 15],
        "items": {
            "breakfast": [("f12", 75), ("f7", 110), ("f19", 120)],
            "lunch": [("f17", 240), ("f14", 180), ("f21", 70), ("f22", 150)],
            "dinner": [("f8", 180), ("f16", 200), ("f11", 40)],
            "snack": [("f10", 140), ("f25", 20), ("f20", 150)],
        }
    }
]

MEAL_TYPES = [
    ("breakfast", "🌅 Завтрак"),
    ("lunch", "☀️ Обед"),
    ("dinner", "🌙 Ужин"),
    ("snack", "🍏 Перекус"),
]

STORAGE_DIR = os.environ.get("FLET_APP_STORAGE_DATA", ".")
STATE_FILE = os.path.join(STORAGE_DIR, "syrokfit_data.json")


# Перевод граммов в понятные штуки, сырки, ложки и порции
def format_units(item_or_food, grams):
    unit_g = item_or_food.get("unit_g", 0)
    unit_name = item_or_food.get("unit_name", "")
    if not unit_g or not unit_name:
        for df in DEFAULT_FOODS:
            if df["id"] == item_or_food.get("id"):
                unit_g = df.get("unit_g", 0)
                unit_name = df.get("unit_name", "")
                break
    if not unit_g or not unit_name:
        return f"{grams} г"

    count = grams / float(unit_g)
    rounded = round(count * 2) / 2.0
    if rounded <= 0:
        rounded = 0.5
    cnt_str = str(int(rounded)) if rounded.is_integer() else str(rounded)
    return f"{grams} г (~{cnt_str} {unit_name})"


def load_state():
    default = {
        "gender": "male",
        "age": 18,
        "weight": 72,
        "height": 178,
        "activity": 1.55,
        "goal": 0,
        "macro_preset": "balanced",
        "water": 1000,
        "active_meal": "breakfast",
        "meals": {"breakfast": [], "lunch": [], "dinner": [], "snack": []},
        "custom_foods": []
    }
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                for k, v in default.items():
                    if k not in data:
                        data[k] = v
                return data
        except Exception:
            pass
    return default


# Надёжная кнопка для Flet 1.0+ (без конфликтов верстки)
def make_btn(text, on_click, bg="#10b981", fg="#0f172a", expand=False, pad=9, radius=10, size=12):
    return ft.Container(
        expand=expand,
        bgcolor=bg,
        border_radius=radius,
        padding=pad,
        content=ft.Row(
            [ft.Text(text, size=size, weight=ft.FontWeight.BOLD, color=fg)],
            alignment=ft.MainAxisAlignment.CENTER,
            tight=not expand,
        ),
        on_click=on_click,
    )


def main(page: ft.Page):
    page.title = f"{APP_TITLE} — Калькулятор КБЖУ"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#0f172a"
    page.padding = 0
    # На ПК задаёт удобный размер мобильного телефона, а на Android автоматически игнорируется
    page.window.width = 430
    page.window.height = 860

    state = load_state()

    def get_all_foods():
        return state.get("custom_foods", []) + DEFAULT_FOODS

    def save_state():
        try:
            os.makedirs(STORAGE_DIR, exist_ok=True)
            with open(STATE_FILE, "w", encoding="utf-8") as f:
                json.dump(state, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def calc_targets():
        w = float(state["weight"])
        h = float(state["height"])
        a = float(state["age"])
        act = float(state["activity"])
        goal = float(state["goal"])

        bmr = (10 * w + 6.25 * h - 5 * a + 5) if state["gender"] == "male" else (10 * w + 6.25 * h - 5 * a - 161)
        tdee = bmr * act
        kcal = round(tdee * (1 + goal / 100.0))

        ratios = {
            "balanced": (0.30, 0.30, 0.40),
            "high_protein": (0.35, 0.25, 0.40),
            "athletic": (0.25, 0.25, 0.50),
            "low_carb": (0.35, 0.45, 0.20),
        }.get(state.get("macro_preset", "balanced"), (0.30, 0.30, 0.40))

        bmi = round(w / ((h / 100.0) ** 2), 1)

        return {
            "bmr": round(bmr),
            "tdee": round(tdee),
            "kcal": kcal,
            "p": round((kcal * ratios[0]) / 4),
            "f": round((kcal * ratios[1]) / 9),
            "c": round((kcal * ratios[2]) / 4),
            "water": round(w * 33),
            "bmi": bmi
        }

    def calc_totals():
        kcal = p = f = c = 0.0
        for m_list in state["meals"].values():
            for item in m_list:
                mult = item["grams"] / 100.0
                kcal += item["kcal"] * mult
                p += item["p"] * mult
                f += item["f"] * mult
                c += item["c"] * mult
        return {"kcal": round(kcal), "p": round(p), "f": round(f), "c": round(c)}

    def apply_ration_template(template, scale_to_target=True):
        foods_map = {f["id"]: f for f in get_all_foods()}
        targets = calc_targets()

        base_kcal = 0.0
        for m_key, pairs in template["items"].items():
            for fid, grams in pairs:
                if fid in foods_map:
                    base_kcal += foods_map[fid]["kcal"] * (grams / 100.0)

        scale = (targets["kcal"] / base_kcal) if (scale_to_target and base_kcal > 0) else 1.0
        scale = max(0.5, min(2.5, scale))

        new_meals = {"breakfast": [], "lunch": [], "dinner": [], "snack": []}
        for m_key, pairs in template["items"].items():
            for fid, grams in pairs:
                if fid in foods_map:
                    fd = foods_map[fid]
                    raw_g = grams * scale
                    if fd.get("unit_name") in ("шт.", "ломтик", "кус.", "скуп", "сырок"):
                        ug = fd["unit_g"]
                        units_cnt = max(1, round(raw_g / ug))
                        scaled_grams = int(units_cnt * ug)
                    else:
                        scaled_grams = max(10, int(round(raw_g / 10.0) * 10))

                    new_meals[m_key].append({
                        "id": fd["id"],
                        "name": fd["name"],
                        "emoji": fd["emoji"],
                        "grams": scaled_grams,
                        "kcal": fd["kcal"],
                        "p": fd["p"],
                        "f": fd["f"],
                        "c": fd["c"],
                        "unit_g": fd.get("unit_g", 0),
                        "unit_name": fd.get("unit_name", "")
                    })

        state["meals"] = new_meals
        save_state()
        set_tab(0)

    # Верхняя фирменная шапка SyrokFit
    top_bar = ft.Container(
        bgcolor="#1e293b",
        padding=12,
        border_radius=16,
        content=ft.Row([
            ft.Container(
                bgcolor="#10b981",
                border_radius=12,
                padding=8,
                content=ft.Text("🍫", size=18)
            ),
            ft.Column([
                ft.Text(APP_TITLE, size=18, weight=ft.FontWeight.BOLD, color="white"),
                ft.Text(APP_SUBTITLE, size=11, color="#10b981"),
            ], spacing=1, expand=True),
        ], spacing=10)
    )

    main_scroll = ft.Column(spacing=12, scroll=ft.ScrollMode.AUTO, expand=True)

    # ================= ВКЛАДКА 1: ДНЕВНИК =================
    def build_diary_controls():
        targets = calc_targets()
        totals = calc_totals()
        pct_kcal = min(1.0, totals["kcal"] / max(1, targets["kcal"]))

        def change_water(delta):
            state["water"] = max(0, state["water"] + delta)
            save_state()
            render_current_tab()

        def clear_day(e):
            state["meals"] = {"breakfast": [], "lunch": [], "dinner": [], "snack": []}
            save_state()
            render_current_tab()

        def adjust_item_grams(meal_key, idx, delta):
            item = state["meals"][meal_key][idx]
            new_g = item["grams"] + delta
            if new_g <= 0:
                state["meals"][meal_key].pop(idx)
            else:
                item["grams"] = new_g
            save_state()
            render_current_tab()

        def remove_item(meal_key, idx):
            state["meals"][meal_key].pop(idx)
            save_state()
            render_current_tab()

        def jump_to_add_food(meal_key):
            state["active_meal"] = meal_key
            save_state()
            set_tab(2)

        diff = targets["kcal"] - totals["kcal"]
        status_label = f"Осталось: {diff} ккал" if diff >= 0 else f"Профицит: +{abs(diff)} ккал"
        status_color = "#10b981" if diff >= 0 else "#f43f5e"

        def macro_col(title, cur, target, text_col, bar_col):
            val = min(1.0, cur / max(1, target))
            return ft.Container(
                expand=True,
                bgcolor="#0f172a",
                border_radius=12,
                padding=10,
                content=ft.Column([
                    ft.Text(title, size=11, color=text_col, weight=ft.FontWeight.BOLD),
                    ft.Text(f"{cur} / {target} г", size=12, color="white", weight=ft.FontWeight.W_600),
                    ft.ProgressBar(value=val, color=bar_col, bgcolor="#334155", height=6),
                ], spacing=5)
            )

        summary_card = ft.Container(
            bgcolor="#1e293b",
            border_radius=18,
            padding=16,
            content=ft.Column([
                ft.Row([
                    ft.Column([
                        ft.Text("ДНЕВНОЙ БАЛАНС КАЛОРИЙ", size=10, color="#94a3b8", weight=ft.FontWeight.BOLD),
                        ft.Text(f"{totals['kcal']} / {targets['kcal']} ккал", size=22, weight=ft.FontWeight.BOLD, color="white"),
                        ft.Text(status_label, size=12, color=status_color, weight=ft.FontWeight.W_600),
                    ], expand=True, spacing=2),
                    ft.Container(
                        bgcolor="#0f172a",
                        border_radius=14,
                        padding=10,
                        content=ft.Column([
                            ft.Text(f"{int(pct_kcal * 100)}%", size=16, weight=ft.FontWeight.BOLD, color="#10b981"),
                            ft.Text("нормы", size=10, color="#94a3b8"),
                        ], spacing=1, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.ProgressBar(value=pct_kcal, color="#10b981", bgcolor="#0f172a", height=8),
                ft.Row([
                    macro_col("Белки", totals["p"], targets["p"], "#60a5fa", "#3b82f6"),
                    macro_col("Жиры", totals["f"], targets["f"], "#fbbf24", "#f59e0b"),
                    macro_col("Углеводы", totals["c"], targets["c"], "#34d399", "#10b981"),
                ], spacing=8)
            ], spacing=12)
        )

        water_pct = min(1.0, state["water"] / max(1, targets["water"]))
        water_card = ft.Container(
            bgcolor="#1e293b",
            border_radius=18,
            padding=14,
            content=ft.Column([
                ft.Row([
                    ft.Column([
                        ft.Text("💧 Водный баланс", size=12, color="#94a3b8"),
                        ft.Text(f"{state['water']} / {targets['water']} мл (~{round(state['water']/250, 1)} стак.)", size=15, weight=ft.FontWeight.BOLD, color="#38bdf8"),
                    ], expand=True, spacing=2),
                    ft.Row([
                        make_btn("-250", lambda e: change_water(-250), bg="#334155", fg="white", pad=8),
                        make_btn("+250 мл", lambda e: change_water(250), bg="#0284c7", fg="white", pad=8),
                    ], spacing=6)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.ProgressBar(value=water_pct, color="#38bdf8", bgcolor="#0f172a", height=5)
            ], spacing=8)
        )

        meal_cards = []
        for m_key, m_title in MEAL_TYPES:
            items = state["meals"].get(m_key, [])
            m_kcal = round(sum(i["kcal"] * i["grams"] / 100.0 for i in items))
            m_p = round(sum(i["p"] * i["grams"] / 100.0 for i in items))
            m_f = round(sum(i["f"] * i["grams"] / 100.0 for i in items))
            m_c = round(sum(i["c"] * i["grams"] / 100.0 for i in items))

            rows = []
            for idx, item in enumerate(items):
                item_kcal = round(item["kcal"] * item["grams"] / 100.0)
                step = item.get("unit_g", 25) if item.get("unit_name") in ("шт.", "ломтик", "кус.", "ст. л.", "скуп", "сырок") else 25
                step_label = "1шт" if item.get("unit_name") in ("шт.", "сырок") else f"{step}г"

                rows.append(
                    ft.Container(
                        bgcolor="#0f172a",
                        border_radius=12,
                        padding=10,
                        content=ft.Row([
                            ft.Column([
                                ft.Text(
                                    f"{item['emoji']} {item['name']}",
                                    size=13, weight=ft.FontWeight.W_600,
                                    max_lines=1, overflow=ft.TextOverflow.ELLIPSIS
                                ),
                                ft.Text(
                                    f"{format_units(item, item['grams'])}  •  {item_kcal} ккал",
                                    size=11, color="#10b981", weight=ft.FontWeight.W_500
                                ),
                            ], expand=True, spacing=2),
                            ft.Row([
                                make_btn(f"-{step_label}", lambda e, mk=m_key, i=idx, s=step: adjust_item_grams(mk, i, -s), bg="#1e293b", fg="white", pad=6, size=10),
                                make_btn(f"+{step_label}", lambda e, mk=m_key, i=idx, s=step: adjust_item_grams(mk, i, s), bg="#1e293b", fg="#10b981", pad=6, size=10),
                                make_btn("✕", lambda e, mk=m_key, i=idx: remove_item(mk, i), bg="#1e293b", fg="#f43f5e", pad=6, size=10),
                            ], spacing=4)
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                    )
                )

            if not rows:
                rows.append(
                    ft.Text("Пусто — выбери готовый рацион или добавь продукты", size=12, color="#64748b")
                )

            meal_cards.append(
                ft.Container(
                    bgcolor="#1e293b",
                    border_radius=18,
                    padding=14,
                    content=ft.Column([
                        ft.Row([
                            ft.Column([
                                ft.Text(m_title, size=15, weight=ft.FontWeight.BOLD),
                                ft.Text(f"Б: {m_p}г • Ж: {m_f}г • У: {m_c}г", size=11, color="#94a3b8"),
                            ], expand=True, spacing=1),
                            ft.Text(f"{m_kcal} ккал", size=14, color="#10b981", weight=ft.FontWeight.BOLD),
                            make_btn("+ Еда", lambda e, mk=m_key: jump_to_add_food(mk), bg="#10b981", fg="#0f172a", pad=7, size=11)
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        ft.Column(rows, spacing=6)
                    ], spacing=10)
                )
            )

        return [
            summary_card,
            water_card,
            ft.Row([
                make_btn("✨ Подобрать готовый рацион", lambda e: set_tab(1), bg="#10b981", fg="#0f172a", expand=True, pad=10),
                make_btn("Очистить", clear_day, bg="#334155", fg="#f43f5e", pad=10),
            ], spacing=8),
            *meal_cards
        ]

    # ================= ВКЛАДКА 2: ГОТОВЫЕ РАЦИОНЫ =================
    def build_rations_controls():
        targets = calc_targets()
        user_goal = int(state["goal"])
        foods_map = {f["id"]: f for f in get_all_foods()}

        goal_names = {
            -20: "Похудение (-20%)",
            -10: "Мягкий дефицит (-10%)",
            0: "Поддержание веса (0%)",
            15: "Набор массы (+15%)"
        }

        header_banner = ft.Container(
            bgcolor="#1e293b",
            border_radius=18,
            padding=14,
            content=ft.Column([
                ft.Text("Умный подбор рациона SyrokFit", size=16, weight=ft.FontWeight.BOLD),
                ft.Text(
                    f"Твоя цель: {goal_names.get(user_goal, 'Баланс')} • Норма: {targets['kcal']} ккал",
                    size=12, color="#10b981", weight=ft.FontWeight.W_600
                ),
                ft.Text(
                    "Нажми зелёную кнопку, и программа сама пересчитает граммы и штуки каждого продукта под твою норму!",
                    size=11, color="#94a3b8"
                ),
            ], spacing=4)
        )

        sorted_templates = sorted(
            RATION_TEMPLATES,
            key=lambda t: (0 if user_goal in t["goals"] else 1)
        )

        cards = []
        for tpl in sorted_templates:
            is_recommended = user_goal in tpl["goals"]

            base_kcal = 0.0
            preview_lines = []
            for m_key, m_title in MEAL_TYPES:
                pairs = tpl["items"].get(m_key, [])
                names = []
                for fid, g in pairs:
                    if fid in foods_map:
                        fd = foods_map[fid]
                        base_kcal += fd["kcal"] * (g / 100.0)
                        names.append(f"{fd['name']} ({format_units(fd, g)})")
                if names:
                    preview_lines.append(
                        ft.Text(
                            f"{m_title}: " + ", ".join(names),
                            size=11, color="#cbd5e1",
                            max_lines=2, overflow=ft.TextOverflow.ELLIPSIS
                        )
                    )

            badge = ft.Container(
                bgcolor="#10b981" if is_recommended else "#334155",
                border_radius=8,
                padding=6,
                content=ft.Text(
                    "★ Рекомендуем под твою цель" if is_recommended else f"База ~{round(base_kcal)} ккал",
                    size=10,
                    weight=ft.FontWeight.BOLD,
                    color="#0f172a" if is_recommended else "#94a3b8"
                )
            )

            cards.append(
                ft.Container(
                    bgcolor="#1e293b",
                    border_radius=18,
                    padding=14,
                    content=ft.Column([
                        ft.Row([badge], alignment=ft.MainAxisAlignment.START),
                        ft.Text(tpl["title"], size=15, weight=ft.FontWeight.BOLD),
                        ft.Text(tpl["desc"], size=12, color="#94a3b8"),
                        ft.Container(
                            bgcolor="#0f172a",
                            border_radius=12,
                            padding=10,
                            content=ft.Column(preview_lines, spacing=4)
                        ),
                        ft.Row([
                            make_btn(
                                f"⚡ Пересчитать под {targets['kcal']} ккал",
                                lambda e, t=tpl: apply_ration_template(t, True),
                                bg="#10b981", fg="#0f172a", expand=True, pad=10
                            ),
                            make_btn(
                                "Базовый",
                                lambda e, t=tpl: apply_ration_template(t, False),
                                bg="#334155", fg="white", pad=10
                            ),
                        ], spacing=8)
                    ], spacing=8)
                )
            )

        return [header_banner, *cards]

    # ================= ВКЛАДКА 3: ПРОДУКТЫ =================
    selected_food_cat = "Все"
    food_status_msg = "Выбери категорию и нажми на кнопку порции"

    new_food_name = ft.TextField(hint_text="Свой продукт (назв.)", expand=True, bgcolor="#0f172a", border_radius=10, text_size=12)
    new_food_p = ft.TextField(hint_text="Б", width=52, bgcolor="#0f172a", border_radius=10, text_size=12)
    new_food_f = ft.TextField(hint_text="Ж", width=52, bgcolor="#0f172a", border_radius=10, text_size=12)
    new_food_c = ft.TextField(hint_text="У", width=52, bgcolor="#0f172a", border_radius=10, text_size=12)

    def build_foods_controls():
        nonlocal selected_food_cat, food_status_msg

        def select_meal(meal_key):
            state["active_meal"] = meal_key
            save_state()
            render_current_tab()

        def select_category(cat):
            nonlocal selected_food_cat
            selected_food_cat = cat
            render_current_tab()

        def create_custom_food(e):
            nonlocal food_status_msg
            name_val = (new_food_name.value or "").strip()
            if not name_val:
                food_status_msg = "⚠️ Введи название своего продукта"
                render_current_tab()
                return
            try:
                p_v = float((new_food_p.value or "0").replace(",", "."))
                f_v = float((new_food_f.value or "0").replace(",", "."))
                c_v = float((new_food_c.value or "0").replace(",", "."))
            except ValueError:
                food_status_msg = "⚠️ БЖУ должны быть числами"
                render_current_tab()
                return

            kcal_v = round(p_v * 4 + f_v * 9 + c_v * 4)
            custom_item = {
                "id": f"cust_{len(state['custom_foods']) + 1}",
                "name": name_val,
                "cat": "Все",
                "emoji": "🍽️",
                "kcal": kcal_v,
                "p": p_v,
                "f": f_v,
                "c": c_v,
                "unit_g": 100,
                "unit_name": "порц."
            }
            state["custom_foods"].insert(0, custom_item)
            save_state()
            new_food_name.value = new_food_p.value = new_food_f.value = new_food_c.value = ""
            selected_food_cat = "Все"
            food_status_msg = f"✅ Продукт «{name_val}» ({kcal_v} ккал) сохранён в базу!"
            render_current_tab()

        def add_food_to_meal(food, grams):
            nonlocal food_status_msg
            m_key = state["active_meal"]
            for existing in state["meals"][m_key]:
                if existing["id"] == food["id"]:
                    existing["grams"] += grams
                    break
            else:
                state["meals"][m_key].append({
                    "id": food["id"],
                    "name": food["name"],
                    "emoji": food["emoji"],
                    "grams": grams,
                    "kcal": food["kcal"],
                    "p": food["p"],
                    "f": food["f"],
                    "c": food["c"],
                    "unit_g": food.get("unit_g", 0),
                    "unit_name": food.get("unit_name", "")
                })
            save_state()
            food_status_msg = f"✅ Добавлено: {food['name']} ({format_units(food, grams)})"
            render_current_tab()

        meal_selector = ft.Row([
            make_btn(
                title.split()[1],
                lambda e, k=key: select_meal(k),
                bg="#10b981" if state["active_meal"] == key else "#1e293b",
                fg="#0f172a" if state["active_meal"] == key else "white",
                expand=True, pad=8, size=11
            )
            for key, title in MEAL_TYPES
        ], spacing=6)

        cat_row_1 = ft.Row([
            make_btn(
                c,
                lambda e, cat_name=c: select_category(cat_name),
                bg="#10b981" if c == selected_food_cat else "#1e293b",
                fg="#0f172a" if c == selected_food_cat else "#cbd5e1",
                expand=True, pad=7, size=11
            )
            for c in ["Все", "Мясо", "Рыба", "Молочные"]
        ], spacing=6)

        cat_row_2 = ft.Row([
            make_btn(
                c,
                lambda e, cat_name=c: select_category(cat_name),
                bg="#10b981" if c == selected_food_cat else "#1e293b",
                fg="#0f172a" if c == selected_food_cat else "#cbd5e1",
                expand=True, pad=7, size=11
            )
            for c in ["Крупы", "Овощи/Фрукты", "Жиры/Спорт"]
        ], spacing=6)

        custom_food_card = ft.Container(
            bgcolor="#1e293b",
            border_radius=14,
            padding=10,
            content=ft.Column([
                ft.Text("➕ Добавить свой продукт (на 100 г):", size=11, color="#94a3b8", weight=ft.FontWeight.BOLD),
                ft.Row([new_food_name, new_food_p, new_food_f, new_food_c], spacing=6),
                make_btn("Сохранить в базу", create_custom_food, bg="#334155", fg="#10b981", pad=8, size=11)
            ], spacing=6)
        )

        food_cards = []
        for food in get_all_foods():
            if selected_food_cat != "Все" and food.get("cat") != selected_food_cat:
                continue

            ug = food.get("unit_g", 100)
            uname = food.get("unit_name", "")
            unit_hint = f"1 {uname} ≈ {ug} г" if (ug and uname) else "на 100 г"

            btn1_grams = ug if ug else 50
            btn1_label = f"+1 {uname} ({ug}г)" if (ug and uname) else "+50г"

            food_cards.append(
                ft.Container(
                    bgcolor="#1e293b",
                    border_radius=14,
                    padding=12,
                    content=ft.Row([
                        ft.Column([
                            ft.Text(
                                f"{food['emoji']} {food['name']}",
                                size=13, weight=ft.FontWeight.BOLD,
                                max_lines=1, overflow=ft.TextOverflow.ELLIPSIS
                            ),
                            ft.Text(
                                f"{unit_hint}  •  100г: {food['kcal']} ккал (Б:{food['p']} Ж:{food['f']} У:{food['c']})",
                                size=11, color="#94a3b8"
                            ),
                        ], expand=True, spacing=2),
                        ft.Row([
                            make_btn(btn1_label, lambda e, f=food, g=btn1_grams: add_food_to_meal(f, g), bg="#10b981", fg="#0f172a", pad=7, size=10),
                            make_btn("+100г", lambda e, f=food: add_food_to_meal(f, 100), bg="#0f172a", fg="#10b981", pad=7, size=10),
                        ], spacing=5)
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                )
            )

        return [
            ft.Container(
                bgcolor="#1e293b",
                border_radius=12,
                padding=10,
                content=ft.Text(food_status_msg, size=12, color="#10b981", weight=ft.FontWeight.BOLD)
            ),
            meal_selector,
            cat_row_1,
            cat_row_2,
            custom_food_card,
            *food_cards
        ]

    # ================= ВКЛАДКА 4: ПРОФИЛЬ =================
    def build_profile_controls():
        targets = calc_targets()

        def update_param(key, val):
            state[key] = val
            save_state()
            render_current_tab()

        age_label = ft.Text(f"Возраст: {int(state['age'])} лет", size=13, weight=ft.FontWeight.BOLD)
        weight_label = ft.Text(f"Вес: {int(state['weight'])} кг", size=13, weight=ft.FontWeight.BOLD)
        height_label = ft.Text(f"Рост: {int(state['height'])} см", size=13, weight=ft.FontWeight.BOLD)

        def on_age_slide(e):
            age_label.value = f"Возраст: {int(e.control.value)} лет"
            page.update()

        def on_weight_slide(e):
            weight_label.value = f"Вес: {int(e.control.value)} кг"
            page.update()

        def on_height_slide(e):
            height_label.value = f"Рост: {int(e.control.value)} см"
            page.update()

        bmi = targets["bmi"]
        if bmi < 18.5:
            bmi_status = ("Дефицит массы", "#38bdf8")
        elif bmi < 25:
            bmi_status = ("Нормальный вес", "#10b981")
        elif bmi < 30:
            bmi_status = ("Избыточный вес", "#fbbf24")
        else:
            bmi_status = ("Ожирение", "#f43f5e")

        cur_act = float(state["activity"])
        cur_goal = int(state["goal"])
        cur_macro = state.get("macro_preset", "balanced")

        return [
            ft.Container(
                bgcolor="#1e293b",
                border_radius=18,
                padding=16,
                content=ft.Column([
                    ft.Row([
                        ft.Column([
                            ft.Text("Твоя целевая норма", size=12, color="#94a3b8"),
                            ft.Text(f"🔥 {targets['kcal']} ккал", size=24, weight=ft.FontWeight.BOLD, color="#10b981"),
                        ], expand=True),
                        ft.Container(
                            bgcolor="#0f172a", border_radius=12, padding=10,
                            content=ft.Column([
                                ft.Text(f"ИМТ: {bmi}", size=13, weight=ft.FontWeight.BOLD),
                                ft.Text(bmi_status[0], size=10, color=bmi_status[1]),
                            ], spacing=2)
                        )
                    ]),
                    ft.Text(
                        f"Белки: {targets['p']} г  •  Жиры: {targets['f']} г  •  Углеводы: {targets['c']} г",
                        size=13, weight=ft.FontWeight.W_600
                    ),
                    ft.Text(
                        f"Базовый обмен (BMR): {targets['bmr']} ккал • Вода: {targets['water']} мл",
                        size=11, color="#94a3b8"
                    ),
                ], spacing=6)
            ),
            ft.Container(
                bgcolor="#1e293b",
                border_radius=18,
                padding=16,
                content=ft.Column([
                    ft.Row([
                        make_btn(
                            "👨 Мужчина",
                            lambda e: update_param("gender", "male"),
                            bg="#10b981" if state["gender"] == "male" else "#0f172a",
                            fg="#0f172a" if state["gender"] == "male" else "white",
                            expand=True, pad=9
                        ),
                        make_btn(
                            "👩 Женщина",
                            lambda e: update_param("gender", "female"),
                            bg="#10b981" if state["gender"] == "female" else "#0f172a",
                            fg="#0f172a" if state["gender"] == "female" else "white",
                            expand=True, pad=9
                        ),
                    ], spacing=8),
                    age_label,
                    ft.Slider(min=14, max=80, divisions=66, value=float(state["age"]), active_color="#10b981", on_change=on_age_slide, on_change_end=lambda e: update_param("age", int(e.control.value))),
                    weight_label,
                    ft.Slider(min=40, max=140, divisions=100, value=float(state["weight"]), active_color="#10b981", on_change=on_weight_slide, on_change_end=lambda e: update_param("weight", int(e.control.value))),
                    height_label,
                    ft.Slider(min=140, max=210, divisions=70, value=float(state["height"]), active_color="#10b981", on_change=on_height_slide, on_change_end=lambda e: update_param("height", int(e.control.value))),

                    ft.Text("Уровень активности:", size=12, color="#94a3b8"),
                    ft.Row([
                        make_btn("Сидячий (1.2)", lambda e: update_param("activity", 1.2), bg="#10b981" if abs(cur_act - 1.2) < 0.01 else "#0f172a", fg="#0f172a" if abs(cur_act - 1.2) < 0.01 else "white", expand=True, pad=8, size=11),
                        make_btn("1-3 трен. (1.375)", lambda e: update_param("activity", 1.375), bg="#10b981" if abs(cur_act - 1.375) < 0.01 else "#0f172a", fg="#0f172a" if abs(cur_act - 1.375) < 0.01 else "white", expand=True, pad=8, size=11),
                    ], spacing=6),
                    ft.Row([
                        make_btn("3-5 трен. (1.55)", lambda e: update_param("activity", 1.55), bg="#10b981" if abs(cur_act - 1.55) < 0.01 else "#0f172a", fg="#0f172a" if abs(cur_act - 1.55) < 0.01 else "white", expand=True, pad=8, size=11),
                        make_btn("6-7 трен. (1.725)", lambda e: update_param("activity", 1.725), bg="#10b981" if abs(cur_act - 1.725) < 0.01 else "#0f172a", fg="#0f172a" if abs(cur_act - 1.725) < 0.01 else "white", expand=True, pad=8, size=11),
                    ], spacing=6),

                    ft.Text("Твоя цель:", size=12, color="#94a3b8"),
                    ft.Row([
                        make_btn("Сушка -20%", lambda e: update_param("goal", -20), bg="#10b981" if cur_goal == -20 else "#0f172a", fg="#0f172a" if cur_goal == -20 else "white", expand=True, pad=8, size=11),
                        make_btn("Дефицит -10%", lambda e: update_param("goal", -10), bg="#10b981" if cur_goal == -10 else "#0f172a", fg="#0f172a" if cur_goal == -10 else "white", expand=True, pad=8, size=11),
                    ], spacing=6),
                    ft.Row([
                        make_btn("Баланс 0%", lambda e: update_param("goal", 0), bg="#10b981" if cur_goal == 0 else "#0f172a", fg="#0f172a" if cur_goal == 0 else "white", expand=True, pad=8, size=11),
                        make_btn("Масса +15%", lambda e: update_param("goal", 15), bg="#10b981" if cur_goal == 15 else "#0f172a", fg="#0f172a" if cur_goal == 15 else "white", expand=True, pad=8, size=11),
                    ], spacing=6),

                    ft.Text("Профиль макронутриентов (Б/Ж/У):", size=12, color="#94a3b8"),
                    ft.Row([
                        make_btn("Баланс 30/30/40", lambda e: update_param("macro_preset", "balanced"), bg="#10b981" if cur_macro == "balanced" else "#0f172a", fg="#0f172a" if cur_macro == "balanced" else "white", expand=True, pad=8, size=11),
                        make_btn("Белковый 35/25/40", lambda e: update_param("macro_preset", "high_protein"), bg="#10b981" if cur_macro == "high_protein" else "#0f172a", fg="#0f172a" if cur_macro == "high_protein" else "white", expand=True, pad=8, size=11),
                    ], spacing=6),
                    ft.Row([
                        make_btn("Спорт 25/25/50", lambda e: update_param("macro_preset", "athletic"), bg="#10b981" if cur_macro == "athletic" else "#0f172a", fg="#0f172a" if cur_macro == "athletic" else "white", expand=True, pad=8, size=11),
                        make_btn("Низкоугл. 35/45/20", lambda e: update_param("macro_preset", "low_carb"), bg="#10b981" if cur_macro == "low_carb" else "#0f172a", fg="#0f172a" if cur_macro == "low_carb" else "white", expand=True, pad=8, size=11),
                    ], spacing=6),
                ], spacing=8)
            )
        ]

    current_tab_index = 0

    def render_current_tab():
        if current_tab_index == 0:
            main_scroll.controls = build_diary_controls()
        elif current_tab_index == 1:
            main_scroll.controls = build_rations_controls()
        elif current_tab_index == 2:
            main_scroll.controls = build_foods_controls()
        else:
            main_scroll.controls = build_profile_controls()
        page.update()

    def set_tab(idx):
        nonlocal current_tab_index
        current_tab_index = idx
        update_bottom_nav()
        render_current_tab()

    bottom_nav = ft.Container(bgcolor="#1e293b", padding=10, border_radius=16)

    def update_bottom_nav():
        tabs = [
            (0, "📊 Дневник"),
            (1, "🍱 Рационы"),
            (2, "🥗 Продукты"),
            (3, "⚙️ Профиль"),
        ]
        bottom_nav.content = ft.Row([
            make_btn(
                title,
                lambda e, i=idx: set_tab(i),
                bg="#10b981" if current_tab_index == idx else "#0f172a",
                fg="#0f172a" if current_tab_index == idx else "#cbd5e1",
                expand=True, pad=9, radius=12, size=11
            )
            for idx, title in tabs
        ], spacing=6)

    update_bottom_nav()

    app_layout = ft.Container(
        expand=True,
        bgcolor="#0f172a",
        padding=12,
        content=ft.Column([
            top_bar,
            main_scroll,
            bottom_nav
        ], expand=True, spacing=10)
    )

    page.add(app_layout)
    render_current_tab()


if __name__ == "__main__":
    # Запускает нативное приложение (на ПК и на Android)
    ft.run(main)
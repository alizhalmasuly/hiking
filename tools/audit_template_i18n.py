"""Report literal Django template translations missing from kk/en catalogs."""
import re
import ast
from pathlib import Path

from compile_catalogs import parse

ROOT = Path(__file__).resolve().parents[1]
pattern = re.compile(r"\{%\s*trans\s+(['\"])(.*?)\1(?:\s+as\s+\w+)?\s*%\}")
messages = set()
unwrapped = []
for template in (ROOT / "templates").rglob("*.html"):
    source = template.read_text(encoding="utf-8")
    messages.update(pattern.findall(source))
    visible = re.sub(r"\{%.*?%\}|\{\{.*?\}\}", " ", source, flags=re.DOTALL)
    visible = re.sub(r"<[^>]*>", "\n", visible)
    for text in visible.splitlines():
        text = " ".join(text.split())
        if text and re.search(r"[А-Яа-яЁёӘәҒғҚқҢңӨөҰұҮүҺһІі]", text):
            unwrapped.append((template.relative_to(ROOT), text))
# Each regex result includes its quoting character and source string.
messages = {message for _, message in messages}
messages.update([
    "Алматы и окрестности", "Алматинская область", "Июнь — сентябрь", "1 день", "2 дня", "3 дня и больше", "8–14 км",
    "Живописный маршрут в горах Заилийского Алатау. Подготовьтесь к высоте, переменчивой погоде и красивым панорамам.",
    "Проверьте прогноз, возьмите воду и сообщите близким свой маршрут.", "Кок-Жайляу", "Большой Алматинский пик", "Пик Фурманова", "Кумбель", "Шымбулак", "Пик Молодёжный", "Бутаковское ущелье",
    "Треккинговые ботинки", "Непромокаемая куртка", "Термобельё", "Перчатки", "Шапка", "Карта маршрута", "Компас", "GPS / офлайн-карта", "Вода 2 л", "Перекус", "Аптечка", "Фонарик", "Power bank", "Свисток", "Палатка", "Спальный мешок", "Спальный коврик",
    "Рассвет над Кок-Жайляу", "Первый подъём на Фурмановку", "Тропа к Большому Алматинскому пику", "Тихое утро в Бутаковке", "Летний маршрут на Кумбель",
    "Вышли рано утром, чтобы пройти большую часть маршрута в прохладе. Тропа открывала всё новые виды на город и снежные вершины. Берите воду, проверяйте погоду и не торопитесь на высоте.",
    "Скачайте офлайн-карту и возьмите дополнительный слой одежды.", "Ботинки, ветровка, вода, аптечка", "Спасибо за полезный маршрут! Беру на заметку.",
    "Переменная облачность", "Лёгкий дождь", "Ясно", "Завтра", "Послезавтра",
])
failed = False
for language in ("en", "kk"):
    catalog_path = ROOT / "locale" / language / "LC_MESSAGES" / "django.po"
    catalog = parse(catalog_path)
    msgids = [ast.literal_eval(line[6:]) for line in catalog_path.read_text(encoding="utf-8").splitlines() if line.startswith("msgid ")]
    duplicates = sorted({msgid for msgid in msgids if msgids.count(msgid) > 1 and msgid})
    missing = sorted(messages - set(catalog))
    print(f"{language}: {len(messages) - len(missing)}/{len(messages)} UI and demo strings translated")
    for message in missing:
        print(f"  MISSING: {message.encode('unicode_escape').decode('ascii')}")
    for duplicate in duplicates:
        print(f"  DUPLICATE: {duplicate.encode('unicode_escape').decode('ascii')}")
    failed |= bool(missing or duplicates)
if failed:
    raise SystemExit(1)
if unwrapped:
    print("Untranslated literal template text:")
    for template, text in unwrapped:
        print(f"  {template}: {text.encode('unicode_escape').decode('ascii')}")
    raise SystemExit(1)

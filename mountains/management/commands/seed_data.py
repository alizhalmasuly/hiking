from datetime import date
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from mountains.models import Mountain
from hikes.models import Equipment
from community.models import HikingStory, Comment
class Command(BaseCommand):
    help = "Load sample Kazakhstan mountains, equipment and stories"
    def handle(self, *args, **options):
        records = [
            ("Кок-Жайляу", "kok-zhailau", 2251, "easy", "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=1200&q=85"),
            ("Пик Фурманова", "furmanovka", 3053, "moderate", "https://images.unsplash.com/photo-1454496522488-7a8e488e8606?auto=format&fit=crop&w=1200&q=85"),
            ("Большой Алматинский пик", "big-almaty-peak", 3681, "hard", "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=1200&q=85"),
            ("Кумбель", "kumbel", 3200, "moderate", "https://images.unsplash.com/photo-1464278533981-50106e6176b1?auto=format&fit=crop&w=1200&q=85"),
            ("Шымбулак", "shymbulak", 2260, "easy", "https://images.unsplash.com/photo-1519681393784-d120267933ba?auto=format&fit=crop&w=1200&q=85"),
            ("Пик Молодёжный", "molodezhny", 4147, "hard", "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=1200&q=85"),
            ("Бутаковское ущелье", "butakovka", 2200, "easy", "https://images.unsplash.com/photo-1470770841072-f978cf4d019e?auto=format&fit=crop&w=1200&q=85"),
        ]
        mountains = []
        for name, slug, altitude, difficulty, image in records:
            obj, _ = Mountain.objects.get_or_create(slug=slug, defaults={"name": name, "altitude": altitude, "difficulty": difficulty, "distance": "8–14 км", "description": f"Живописный маршрут в горах Заилийского Алатау. Подготовьтесь к высоте, переменчивой погоде и красивым панорамам.", "safety": "Проверьте прогноз, возьмите воду и сообщите близким свой маршрут.", "image_url": image, "featured": True})
            mountains.append(obj)
        items = [("Треккинговые ботинки", "Одежда"), ("Непромокаемая куртка", "Одежда"), ("Термобельё", "Одежда"), ("Перчатки", "Одежда"), ("Шапка", "Одежда"), ("Карта маршрута", "Навигация"), ("Компас", "Навигация"), ("GPS / офлайн-карта", "Навигация"), ("Вода 2 л", "Еда и вода"), ("Перекус", "Еда и вода"), ("Аптечка", "Безопасность"), ("Фонарик", "Безопасность"), ("Power bank", "Безопасность"), ("Свисток", "Безопасность"), ("Палатка", "Кемпинг"), ("Спальный мешок", "Кемпинг")]
        for name, category in items: Equipment.objects.get_or_create(name=name, defaults={"category": category})
        user, _ = User.objects.get_or_create(username="trailguide", defaults={"first_name": "Алия"})
        user.set_password("trailguide123"); user.save()
        titles = ["Рассвет над Кок-Жайляу", "Первый подъём на Фурмановку", "Тропа к Большому Алматинскому пику", "Тихое утро в Бутаковке", "Летний маршрут на Кумбель"]
        for idx, title in enumerate(titles):
            story, created = HikingStory.objects.get_or_create(title=title, defaults={"author": user, "mountain": mountains[idx], "hike_date": date(2025, 7, 12-idx), "difficulty": "Средний", "description": "Вышли рано утром, чтобы пройти большую часть маршрута в прохладе. Тропа открывала всё новые виды на город и снежные вершины. Берите воду, проверяйте погоду и не торопитесь на высоте.", "tips": "Скачайте офлайн-карту и возьмите дополнительный слой одежды.", "equipment_used": "Ботинки, ветровка, вода, аптечка", "cover_url": mountains[idx].image_url})
            if created:
                Comment.objects.create(story=story, author=user, text="Спасибо за полезный маршрут! Беру на заметку.")
        self.stdout.write(self.style.SUCCESS("Sample mountains, equipment and stories are ready. Demo login: trailguide / trailguide123"))

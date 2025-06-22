from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Yacht(models.Model):
    # Основные поля
    name = models.CharField(max_length=100)
    description = models.TextField()
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    main_photo = models.ImageField(upload_to='media/yachts/', blank=True, null=True)

    location = models.CharField(max_length=100, blank=True, null=True)
    latitude = models.DecimalField(max_digits=25, decimal_places=20, blank=True, null=True)  # Широта
    longitude = models.DecimalField(max_digits=25, decimal_places=20, blank=True, null=True)  # Долгота
    
    # Тоннаж
    displacement = models.CharField(max_length=100, blank=True, null=True)  # Водоизмещение
    fuel_capacity = models.PositiveIntegerField(blank=True, null=True)  # Запас топлива
    water_capacity = models.PositiveIntegerField(blank=True, null=True)  # Запас пресной воды

    # Пассажировместимость
    max_passengers = models.PositiveIntegerField(blank=True, null=True)  # Макс пассажиров
    cabins = models.PositiveIntegerField(blank=True, null=True)  # Кол-во кают
    guest_beds = models.PositiveIntegerField(blank=True, null=True)  # Спальных мест для гостей
    bathrooms = models.PositiveIntegerField(blank=True, null=True)  # Санузлы
    crew = models.PositiveIntegerField(blank=True, null=True)  # Экипаж

    # Размеры
    length = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)  # Длина
    power = models.PositiveIntegerField(blank=True, null=True)  # Мощность двигателя

    # Классификация
    # seaworthiness_class = models.CharField(max_length=50, blank=True, null=True)  # Класс мореходности CE
    # hull_type = models.CharField(max_length=100, blank=True, null=True)  # Тип корпуса
    # hull_material = models.CharField(max_length=100, blank=True, null=True)  # Материал корпуса
    # design_style = models.CharField(max_length=100, blank=True, null=True)  # Дизайн
    # concept = models.CharField(max_length=100, blank=True, null=True)  # Концепция

    # # Данные производителя
    # shipyard = models.CharField(max_length=100, blank=True, null=True)  # Верфь
    # country = models.CharField(max_length=100, blank=True, null=True)  # Страна
    # series = models.CharField(max_length=100, blank=True, null=True)  # Серия
    # model_name = models.CharField(max_length=100, blank=True, null=True)  # Модель
    # release_period = models.CharField(max_length=50, blank=True, null=True)  # Период выпуска

    def __str__(self):
        return self.name

class YachtPhoto(models.Model):
    yacht = models.ForeignKey(Yacht, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='yachts/photos/')
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Фото для {self.yacht.name}"

class Booking(models.Model):
    yacht = models.ForeignKey(Yacht, on_delete=models.CASCADE, related_name='bookings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    is_cancelled = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} бронировал {self.yacht.name}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Профиль {self.user.username}"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    UserProfile.objects.get_or_create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

# Create your models here.

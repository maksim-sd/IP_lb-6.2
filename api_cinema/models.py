from django.db import models
from django.contrib.auth.models import User


class Genre(models.Model):
    name = models.CharField(max_length=20, verbose_name="Название")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"
        

class Movie(models.Model):
    name = models.CharField(max_length=60, verbose_name="Название")
    relese_date = models.DateField(verbose_name="Дата выхода")
    description = models.CharField(max_length=600, verbose_name="Описание")
    duration = models.IntegerField(verbose_name="Продолжительность")
    age_limit = models.IntegerField(verbose_name="Возрастное ограничение")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Кино"
        verbose_name_plural = "Кино"
        

class MovieGenre(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name="Кино")
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, verbose_name="Жанр")

    class Meta:
        verbose_name = "Жанр кино"
        verbose_name_plural = "Жанр кино"
        
        
class Hall(models.Model):
    name = models.CharField(max_length=20, verbose_name="Название")
    number_rows = models.IntegerField(verbose_name="Количество рядов")
    number_places = models.IntegerField(verbose_name="Количество мест в ряду")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Зал"
        verbose_name_plural = "Залы"
        

class Seance(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name="Кино")
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, verbose_name="Зал")
    date_and_time = models.DateTimeField(verbose_name="Дата и время сеанса")
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Стоимость")
    
    def __str__(self):
        return self.movie.name + " " + self.date_and_time.strftime("%d.%m.%Y %H:%M")
    
    class Meta:
        verbose_name = "Сеанс"
        verbose_name_plural = "Сеансы"
        

class TicketStatus(models.Model):
    name = models.CharField(max_length=20, verbose_name="Название")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Статус билета"
        verbose_name_plural = "Статусы билета"
        

class Ticket(models.Model):
    seance = models.ForeignKey(Seance, on_delete=models.CASCADE, verbose_name="Сеанс")
    client = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Клиент")
    row = models.IntegerField(verbose_name="Ряд")
    place = models.IntegerField(verbose_name="Место")
    status = models.ForeignKey(TicketStatus, on_delete=models.CASCADE, verbose_name="Статус билета")
    
    class Meta:
        verbose_name = "Билет"
        verbose_name_plural = "Билеты"

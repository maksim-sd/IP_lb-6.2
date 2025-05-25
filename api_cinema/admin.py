from django.contrib import admin
from .models import *
from django.contrib import admin


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "relese_date", "duration", "age_limit"]
    
    
@admin.register(MovieGenre)
class MovieGenreAdmin(admin.ModelAdmin):
    list_display = ["id", "movie", "genre"]
    

@admin.register(Hall)
class HallAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "number_rows", "number_places"]
    
    
@admin.register(Seance)
class SeanceAdmin(admin.ModelAdmin):
    list_display = ["id", "movie", "hall", "date_and_time", "price"]
    

@admin.register(TicketStatus)
class TicketStatusAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ["id", "seance", "client", "row", "place", "status"]
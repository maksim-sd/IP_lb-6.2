from ninja import Query
from ninja.main import NinjaAPI
from ninja.errors import HttpError
from ninja.security import HttpBasicAuth
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from typing import List
from .models import *
from .shemas import *

api = NinjaAPI(csrf=True)


class BasicAuth(HttpBasicAuth):
    def authenticate(self, request, username, password):
        return authenticate(username=username, password=password)


@api.get("genres/view", response=List[GenreOut], summary="Показать жанры")
def genres_view(request):
    return Genre.objects.all()

@api.get("genre/view", response=GenreOut, summary="Показать определенный жанр")
def genre_view(request, id:int = Query(description="Код жанра")):
    return get_object_or_404(Genre, id=id)

@api.post("movie/add", auth=BasicAuth(), summary="Добавить кино")
def movie_add(request, playload: MovieIn):
    if not request.auth.groups.filter(name="Администратор").exists():
        return api.create_response(request, {"message": "Не достаточно прав"}, status=403)
    movie = Movie.objects.create(**playload.dict())
    return {"message": f"Кино успешно добавлено. Код кино: {movie.id}"}

@api.get("movies/view", response=List[MovieOut], summary="Показать все кино")
def movies_view(request):
    return Movie.objects.all()

@api.get("movie/view", response=MovieOut, summary="Показать определенное кино")
def movie_view(request, id:int = Query(description="Код кино")):
    return get_object_or_404(Movie, id=id)

@api.get("movie/genres/view", response=List[MovieGenreOutGenre], summary="Показать жанры определенного кино")
def movie_genres_view(request, id:int = Query(description="Код кино")):
    movie = get_object_or_404(Movie, id=id)
    return MovieGenre.objects.filter(movie=movie)

@api.get("movies/filter/genre", response=List[MovieGenreOutMovie], summary="Покать кино определенного жанра")
def movies_filter_genre(request, id:int = Query(description="Код жанра")):
    genre = get_object_or_404(Genre, id=id)
    return MovieGenre.objects.filter(genre=genre)

@api.patch("movie/update", auth=BasicAuth(), summary="Обновить кино")
def movie_update(request, playload: MovieIn, id:int = Query(description="Код кино")):
    if not request.auth.groups.filter(name="Администратор").exists():
        return api.create_response(request, {"message": "Не достаточно прав"}, status=403)
    movie = get_object_or_404(Movie, id=id)
    for att, value in playload.dict.items():
        setattr(movie, att, value)
    movie.save()
    return {"message": "Кино успешно обновлено"}

@api.delete("movie/delete", auth=BasicAuth(), summary="Удалить кино")
def movie_delete(request, id:int = Query(description="Код кино")):
    if not request.auth.groups.filter(name="Администратор").exists():
        return api.create_response(request, {"message": "Не достаточно прав"}, status=403)
    return get_object_or_404(Movie, id=id).delete()

@api.get("halls/view", response=List[HallOut], summary="Показать залы")
def halls_view(request):
    return Hall.objects.all()

@api.get("hall/view", response=HallOut, summary="Показать определенный зал")
def hall_view(request, id:int = Query(description="Код зала")):
    return get_object_or_404(Hall, id=id)

@api.post("seance/add", auth=BasicAuth(), summary="Добавить сеанс")
def seance_add(request, playload: SeanceIn):
    if not request.auth.groups.filter(name="Администратор").exists():
        return api.create_response(request, {"message": "Не достаточно прав"}, status=403)
    seance = Seance.objects.create(**playload.dict())
    return {"message": f"Сеанс успешно добавлен. Код сеанса: {seance.id}"}

@api.get("seances/view", response=List[SeanceOut], summary="Показать сеансы")
def seances_view(request):
    return Seance.objects.all()

@api.get("seance/view", response=SeanceOut, summary="Показать определенный сеанс")
def seance_view(request, id:int = Query(description="Код сеанса")):
    return get_object_or_404(Seance, id=id)

@api.get("seance/filter/genre", response=List[SeanceOut], summary="Показать сеансы определенного жанра")
def seance_filter_genre(request, id:int = Query(description="Код жанра")):
    genre = get_object_or_404(Genre, id=id)
    movie = Movie.objects.filter(moviegenre__genre=genre)
    return Seance.objects.filter(movie__in = movie)

@api.get("seance/filter/date", response=List[SeanceOut], summary="Показать сеансы на указанную дату")
def seance_filter_date(request, date:date = Query(description="Дата")):
    return Seance.objects.filter(date_and_time__date = date)

@api.get("seance/tickets/view", auth=BasicAuth(), response=List[TicketOut], summary="Показать все оформленные билеты на сеанс")
def seance_ticket_view(request, id:int = Query(description="Код сеанса")):
    if not request.auth.groups.filter(name="Администратор").exists():
        return api.create_response(request, {"message": "Не достаточно прав"}, status=403)
    seance = get_object_or_404(Seance, id=id)
    return Ticket.objects.filter(seance=seance)

@api.patch("seance/update", auth=BasicAuth(), summary="Обновить сеанс")
def seance_update(request, playload: SeanceIn, id:int = Query(description="Код сеанса")):
    if not request.auth.groups.filter(name="Администратор").exists():
        return api.create_response(request, {"message": "Не достаточно прав"}, status=403)
    seance = get_object_or_404(Seance, id=id)
    for att, value in playload.dict.items():
        setattr(seance, att, value)
    seance.save()
    return {"message": "Сеанс успешно обновлен"}

@api.delete("seance/delete", auth=BasicAuth(), summary="Удалить сеанс")
def seance_delete(request, id:int = Query(description="Код сеанса")):
    if not request.auth.groups.filter(name="Администратор").exists():
        return api.create_response(request, {"message": "Не достаточно прав"}, status=403)
    return get_object_or_404(Seance, id=id).delete()

@api.get("ticket/statuses/view", response=List[TicketStatusOut], summary="Показать статусы билета")
def ticket_statuses_view(request):
    return TicketStatus.objects.all()

@api.get("ticket/status/view", response=TicketStatusOut, summary="Показать определенный статус билета")
def ticket_status_view(request, id:int = Query(description="Код статуса билета")):
    return get_object_or_404(TicketStatus, id=id)

@api.post("ticket/add", auth=BasicAuth(), summary="Забронировать билет")
def ticket_add(request, playload: TicketIn):
    status = get_object_or_404(TicketStatus, id=1)
    client = request.auth
    ticket = Ticket.objects.create(**playload.dict(), client=client, status=status)
    return {"message": f"Билет успешно забронирован. Код билета: {ticket.id}"}

@api.patch("ticket/status/update", auth=BasicAuth(), summary="Изменить статус билета")
def ticket_status_update(request, id_ticket:int = Query(description="Код билета"), id_status:int = Query(description="Код статуса билета")):
    ticket = get_object_or_404(Ticket, id=id_ticket)
    status = get_object_or_404(TicketStatus, id=id_status)
    ticket.status = status
    ticket.save()
    return {"message": "Статус билета успешно изменен"}

@api.delete("ticket/delete", auth=BasicAuth(), summary="Удалить билет")
def ticket_delete(request, id:int = Query(description="Код билета")):
    get_object_or_404(Ticket, id=id).delete()
    return {"message": "Билет был успешно удален"}

@api.get("ticket/view", auth=BasicAuth(), response=TicketOut, summary="Показать определенный билет")
def ticket_view(request, id:int = Query(description="Код билета")):
    return get_object_or_404(Ticket, id=id)



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

# def auth_group(name):
#     def decorator(func):
#         def wrapper(request, *args, **kwargs):
#             if not request.auth.groups.filter(name=name).exists():
#                 return api.create_response(request, {"message": "Не достаточно прав"}, status=403)
#             return func(request, *args, **kwargs)
#         return wrapper
#     return decorator

@api.post("registration", summary="Регистрация", tags=["Пользователь"])
def post_registration(request, playload: ClientIn):
    if User.objects.filter(username=playload.username).exists():
        return api.create_response(request, {"message": "Пользователь уже зарегистрирован!"}, status=409)
    User.objects.create(**playload.dict())
    return {"message": "Пользователь успешно зарегистрирован"}

@api.post("ticket", auth=BasicAuth(), summary="Забронировать билет", tags=["Пользователь"])
def post_ticket(request, playload: TicketIn):
    status = get_object_or_404(TicketStatus, id=1)
    client = request.auth
    seance = get_object_or_404(Seance, id=playload.seance_id)
    status_seance = get_object_or_404(SeanceStatus, id=3)
    if (seance.hall.number_places < playload.place or playload.place < 1) or \
        (seance.hall.number_rows < playload.row or playload.row < 1):
        return api.create_response(request, {"message": "Данное место отсутствует"}, status=400)
    if seance.status == status_seance:
        return api.create_response(request, {"message": "Сеан уже завершён"}, status=400)
    if Ticket.objects.filter(row=playload.row, place=playload.place, seance=seance).exclude(status_id=3).exists():
        return api.create_response(request, {"message": "На данное место уже забронирован билет"}, status=400)
    ticket = Ticket.objects.create(**playload.dict(), client=client, status=status)
    return {"message": f"Билет успешно забронирован. Код билета: {ticket.id}"}

@api.get("user/ticket", response=List[TicketOut], auth=BasicAuth(), summary="Показать мои билеты", tags=["Пользователь"])
def get_user_ticket(request):
    return Ticket.objects.filter(client=request.auth)

@api.get("genres", response=List[GenreOut], auth=BasicAuth(), summary="Показать все жанры", tags=["Жанр"])
def get_all_genres(request):
    if not request.auth.groups.filter(name="Администратор").exists():
        return api.create_response(request, {"message": "Не достаточно прав"}, status=403)
    return Genre.objects.all()

@api.get("genre/{id}", response=GenreOut, auth=BasicAuth(), summary="Показать определенный жанр", tags=["Жанр"])
def get_genre(request, id:int):
    if not request.auth.groups.filter(name="Администратор").exists():
        return api.create_response(request, {"message": "Не достаточно прав"}, status=403)
    return get_object_or_404(Genre, id=id)

@api.get("movies", response=List[MovieOut], summary="Показать все кино", tags=["Кино"])
def get_movies(request):
    return Movie.objects.all()

@api.post("movie", auth=BasicAuth(), summary="Добавить кино", tags=["Кино"])
def post_movie(request, playload: MovieIn):
    if not request.auth.groups.filter(name="Администратор").exists():
        return api.create_response(request, {"message": "Не достаточно прав"}, status=403)
    movie = Movie.objects.create(**playload.dict())
    return {"message": f"Кино успешно добавлено. Код кино: {movie.id}"}

@api.get("movie/{id}", response=MovieOut, summary="Показать определенное кино", tags=["Кино"])
def get_movie(request, id:int):
    return get_object_or_404(Movie, id=id)

@api.patch("movie/{id}", auth=BasicAuth(), summary="Обновить кино", tags=["Кино"])
def patch_movie(request, playload: MovieIn, id:int):
    if not request.auth.groups.filter(name="Администратор").exists():
        return api.create_response(request, {"message": "Не достаточно прав"}, status=403)
    movie = get_object_or_404(Movie, id=id)
    for att, value in playload.dict().items():
        setattr(movie, att, value)
    movie.save()
    return {"message": "Кино успешно обновлено"}

@api.delete("movie/{id}", auth=BasicAuth(), summary="Удалить кино", tags=["Кино"])
def delete_movie(request, id:int):
    if not request.auth.groups.filter(name="Администратор").exists():
        return api.create_response(request, {"message": "Не достаточно прав"}, status=403)
    get_object_or_404(Movie, id=id).delete()
    return {"message": "Кино успешно удалено"}

@api.get("genres/movie/{id}", response=List[MovieGenreOutGenre], summary="Показать жанры определенного кино", tags=["Кино"])
def get_genres_movie(request, id:int):
    movie = get_object_or_404(Movie, id=id)
    return MovieGenre.objects.filter(movie=movie)

@api.get("movies/genre/{id}", response=List[MovieGenreOutMovie], summary="Покать кино определенного жанра", tags=["Кино"])
def get_movies_genre(request, id:int):
    genre = get_object_or_404(Genre, id=id)
    return MovieGenre.objects.filter(genre=genre)

@api.get("halls", response=List[HallOut], auth=BasicAuth(), summary="Показать все залы", tags=["Зал"])
def get_all_halls(request):
    if not request.auth.groups.filter(name="Администратор").exists():
        return api.create_response(request, {"message": "Не достаточно прав"}, status=403)
    return Hall.objects.all()

@api.get("hall/{id}", response=HallOut, auth=BasicAuth(), summary="Показать определенный зал", tags=["Зал"])
def get_hall(request, id:int):
    if not request.auth.groups.filter(name="Администратор").exists():
        return api.create_response(request, {"message": "Не достаточно прав"}, status=403)
    return get_object_or_404(Hall, id=id)

@api.get("seances", response=List[SeanceOut], summary="Показать все сеансы", tags=["Сеанс"])
def get_all_seances(request):
    return Seance.objects.all()

@api.post("seance", auth=BasicAuth(), summary="Добавить сеанс", tags=["Сеанс"])
def post_seance(request, playload: SeanceIn):
    if not request.auth.groups.filter(name="Администратор").exists():
        return api.create_response(request, {"message": "Не достаточно прав"}, status=403)
    seance = Seance.objects.create(**playload.dict())
    return {"message": f"Сеанс успешно добавлен. Код сеанса: {seance.id}"}

@api.get("seance/{id}", response=SeanceOut, summary="Показать определенный сеанс", tags=["Сеанс"])
def get_seance(request, id:int):
    return get_object_or_404(Seance, id=id)

@api.patch("seance", auth=BasicAuth(), summary="Обновить сеанс", tags=["Сеанс"])
def patch_seance(request, playload: SeanceIn, id:int):
    if not request.auth.groups.filter(name="Администратор").exists():
        return api.create_response(request, {"message": "Не достаточно прав"}, status=403)
    seance = get_object_or_404(Seance, id=id)
    for att, value in playload.dict().items():
        setattr(seance, att, value)
    seance.save()
    return {"message": "Сеанс успешно обновлен"}

@api.delete("seance", auth=BasicAuth(), summary="Удалить сеанс", tags=["Сеанс"])
def delete_seance(request, id:int):
    if not request.auth.groups.filter(name="Администратор").exists():
        return api.create_response(request, {"message": "Не достаточно прав"}, status=403)
    get_object_or_404(Seance, id=id).delete()
    return {"message": "Сеанс успешно удален"}

@api.get("seance/filter/", response=List[SeanceOut], summary="Отфильтровать сеансы", tags=["Сеанс"])
def seance_filter_genre(request, id_genre:int = Query(None, description="Код жанра"), date:date = Query(None, description="Дата")):
    seances = Seance.objects.all()
    if id_genre is not None:
        genre = get_object_or_404(Genre, id=id_genre)
        movie = Movie.objects.filter(moviegenre__genre=genre)
        seances = seances.filter(movie__in = movie)
    if date is not None:
        seances = seances.filter(date_and_time__date = date)
    return seances

@api.get("statuses/seance", auth=BasicAuth(), response=List[SeanceStatusOut], summary="Показать возможные статусы сеанса", tags=["Сеанс"])
def get_statuses_seance(request):
    if not request.auth.groups.filter(name="Администратор").exists():
        return api.create_response(request, {"message": "Не достаточно прав"}, status=403)
    return SeanceStatus.objects.all()

@api.patch("seance/{id_seance}/status/{id_status}", auth=BasicAuth(), response=List[SeanceStatusOut], summary="Изменить статус сеанса", tags=["Сеанс"])
def get_statuses_seance(request, id_seance:int, id_status:int):
    if not request.auth.groups.filter(name="Администратор").exists():
        return api.create_response(request, {"message": "Не достаточно прав"}, status=403)
    status = get_object_or_404(SeanceStatus, id=id_status)
    seance = get_object_or_404(Seance, id=id_seance)
    seance.status = status
    seance.save()
    return {"message": "Статус сеанса успешно изменен"}

@api.get("seance/{id}/tickets", auth=BasicAuth(), response=List[TicketOut], summary="Показать все оформленные билеты на сеанс", tags=["Билет"])
def get_seance_tickets(request, id:int):
    if not request.auth.groups.filter(name="Администратор").exists():
        return api.create_response(request, {"message": "Не достаточно прав"}, status=403)
    seance = get_object_or_404(Seance, id=id)
    return Ticket.objects.filter(seance=seance)

@api.get("ticket/{id}", auth=BasicAuth(), response=TicketOut, summary="Показать определенный билет", tags=["Билет"])
def get_ticket(request, id:int):
    if not request.auth.groups.filter(name="Администратор").exists():
        return api.create_response(request, {"message": "Не достаточно прав"}, status=403)
    return get_object_or_404(Ticket, id=id)

@api.get("statuses/ticket", response=List[TicketStatusOut], auth=BasicAuth(), summary="Показать возможные статусы билета", tags=["Билет"])
def get_statuses_ticket(request):
    if not request.auth.groups.filter(name="Администратор").exists():
        return api.create_response(request, {"message": "Не достаточно прав"}, status=403)
    return TicketStatus.objects.all()

@api.patch("ticket/{id_ticket}/status/{id_status}", auth=BasicAuth(), summary="Изменить статус билета", tags=["Билет"])
def patch_ticket_status(request, id_ticket:int, id_status:int):
    if not request.auth.groups.filter(name="Администратор").exists():
        return api.create_response(request, {"message": "Не достаточно прав"}, status=403)
    ticket = get_object_or_404(Ticket, id=id_ticket)
    status = get_object_or_404(TicketStatus, id=id_status)
    ticket.status = status
    ticket.save()
    return {"message": "Статус билета успешно изменен"}
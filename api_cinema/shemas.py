from ninja import Schema
from datetime import datetime, date


class GenreOut(Schema):
    id: int
    name: str
    
    
class MovieIn(Schema):
    name: str
    relese_date: date
    description: str
    duration: int
    age_limit: int
    
    
class MovieOut(Schema):
    id: int
    name: str
    relese_date: date
    description: str
    duration: int
    age_limit: int
    
    
class MovieGenreIn(Schema):
    movie_id: int
    genre_id: int
    

class MovieGenreOutGenre(Schema):
    genre: GenreOut

    
class MovieGenreOutMovie(Schema):
    movie: MovieOut
    
    
class HallOut(Schema):
    name: str
    number_rows: int
    number_places: int


class SeanceIn(Schema):
    movie_id: int
    hall_id: int
    date_and_time: datetime
    price: int
    
    
class SeanceOut(Schema):
    id: int
    movie: MovieOut
    hall: HallOut
    date_and_time: datetime
    price: int
    
    
class TicketStatusOut(Schema):
    id: int
    name: str
    

class ClientOut(Schema):
    id: int
    username: str
    email: str


class TicketIn(Schema):
    seance_id: int
    row: int
    place: int
    

class TicketOut(Schema):
    id: int
    seance: SeanceOut
    client: ClientOut
    row: int
    place: int
    status: TicketStatusOut
    

    


import sqlite3
from collections import Counter


class Netflix:

    def __init__(self, path):
        self.path = path

    def create_connection(self):
        """
        Подключение к базе данных Netflix
        """
        with sqlite3.connect(self.path) as connection:
            cursor = connection.cursor()
            return cursor

    def search_film(self, title):
        """
        Поиск фильма по названию (самого свежего)
        """
        cursor = self.create_connection()
        sqlite_query = (f"""SELECT title, country, release_year, listed_in, description
            FROM '{self.path.split('.')[0]}'
            WHERE title LIKE '%{title}%' AND "type" = 'Movie'
            ORDER BY release_year DESC LIMIT 1""")
        cursor.execute(sqlite_query)
        executed_query = cursor.fetchone()
        result = {"title": executed_query[0], "country": executed_query[1], "release_year": executed_query[2],
                  "genre": executed_query[3], "description": executed_query[4]}
        return result

    def search_film_year(self, year_1, year_2):
        """
        Поиск фильмов по диапазону лет
        """
        cursor = self.create_connection()
        sqlite_query = (f"""SELECT title, release_year
            FROM '{self.path.split('.')[0]}'
            WHERE release_year BETWEEN '{year_1}' AND '{year_2}' LIMIT 100 """)
        cursor.execute(sqlite_query)
        executed_query = cursor.fetchall()
        result = []
        for item in executed_query:
            result.append({"title": item[0], "release_year": item[1]})

        return result

    def search_film_rating(self, rating):
        """
        Поиск по возрастному рейтингу
        """
        rating_group = {"children": "'G'", "family": "'G', 'PG', 'PG-13'", "adult": "'R', 'NC-17'"}
        cursor = self.create_connection()
        sqlite_query = (f"""SELECT title, rating, description 
            FROM '{self.path.split('.')[0]}'
            WHERE rating in ({rating_group[rating]}) """)
        cursor.execute(sqlite_query)
        executed_query = cursor.fetchall()
        result = []
        for item in executed_query:
            result.append({"title": item[0], "rating": item[1], "description": item[2]})

        return result

    def search_film_genre(self, genre):
        """
        Принимает название жанра в качестве аргумента и возвращает 10 самых свежих фильмов в формате json
        """
        cursor = self.create_connection()
        sqlite_query = (f"""SELECT title, description 
            FROM '{self.path.split('.')[0]}'
            WHERE listed_in LIKE '%{genre}%'
            ORDER BY release_year DESC LIMIT 10""")
        cursor.execute(sqlite_query)
        executed_query = cursor.fetchall()
        result = []
        for item in executed_query:
            result.append({"title": item[0], "description": item[1]})

        return result

    def search_film_actors(self, actor_1, actor_2):
        """
        Принимает в качестве аргумента имена двух актеров, сохраняет всех актеров
        из колонки cast и возвращает список тех, кто играет с ними в паре больше 2 раз
        """
        cursor = self.create_connection()
        sqlite_query = (f"""SELECT `cast`
            FROM '{self.path.split('.')[0]}'
            WHERE `cast` LIKE '%{actor_1}%' AND `cast` LIKE '%{actor_2}%' """)
        cursor.execute(sqlite_query)
        executed_query = cursor.fetchall()
        actors_list = []
        for cast in executed_query:
            actors_list.extend(cast[0].split(', '))
            actors_list.remove(actor_1)
            actors_list.remove(actor_2)
        result = []
        for actor, count in Counter(actors_list).items():
            if count > 2:
                result.append(actor)
        return result

    def search_film_parameters(self, movie_type, release_year, genre):
        """
        Принимает тип картины (фильм или сериал), год выпуска и ее жанр и получаeт
        на выходе список названий картин с их описаниями
        """
        cursor = self.create_connection()
        sqlite_query = (f"""SELECT title, description 
            FROM '{self.path.split('.')[0]}'
            WHERE `type` = '{movie_type}' AND release_year = {release_year} AND listed_in LIKE '%{genre}%' """)
        cursor.execute(sqlite_query)
        executed_query = cursor.fetchall()
        result = []
        for item in executed_query:
            result.append({"title": item[0], "description": item[1]})

        return result

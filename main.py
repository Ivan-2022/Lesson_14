from flask import Flask, jsonify
from Netflix import Netflix


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['JSON_SORT_KEYS'] = False

netflix = Netflix("netflix.db")


@app.route("/movie/<title>")
def get_film_name(title):
    film_name = netflix.search_film(title)
    return jsonify(film_name)


@app.route("/movie/<int:year_1>/to/<int:year_2>")
def get_film_year(year_1, year_2):
    films = netflix.search_film_year(year_1, year_2)
    return jsonify(films)


@app.route("/rating/<category>")
def get_film_rating(category):
    films = netflix.search_film_rating(category)
    return jsonify(films)


@app.route("/genre/<genre>")
def get_film_genre(genre):
    films = netflix.search_film_genre(genre)
    return jsonify(films)


# films = netflix.search_film_parameters('Movie', 2021, 'Drama')
# print(films)

# actors = netflix.search_film_actors('Jack Black', 'Dustin Hoffman')
# print(actors)

if __name__ == '__main__':
    app.run()

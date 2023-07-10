from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from editform import Edit
from newmovie import NewMovie
import requests

db = SQLAlchemy()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'

app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
db.__init__(app)
Bootstrap5(app=app)

API_KEY = "a2fdc00159fc5ada5717fe5d88b23058"
API_READ_ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJhMmZkYzAwMTU5ZmM1YWRhNTcxN2ZlNWQ4OGIyMzA1OCIsInN1YiI6IjY0YTAwYTFhYzM5MGM1MDE0ZTNjMGZmZSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.ICqS1tlbNHFxVDWXCk6-v6eqmMKqylIbuELwCO66"
MOVIE_URL = "https://api.themoviedb.org/3/search/movie"


class Movie(db.Model):
    movie_id = db.Column(db.Integer, primary_key=True)
    movie_title = db.Column(db.String(250), nullable=False)
    movie_year = db.Column(db.Integer, nullable=False)
    movie_description = db.Column(db.String(500), nullable=False)
    movie_rating = db.Column(db.Float, nullable=True)
    movie_ranking = db.Column(db.Integer, nullable=True)
    movie_review = db.Column(db.String(400), nullable=True)
    movie_img_url = db.Column(db.String(250), nullable=False)


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    with app.app_context():
        result = db.session.execute(db.select(Movie).order_by(Movie.movie_rating))
        all_movies = result.scalars().all()
    for i in range(len(all_movies)):
        all_movies[i].movie_ranking = len(all_movies) - i
    return render_template("index.html", movies=all_movies)


@app.route("/delete/<title>", methods=["POST", "GET"])
def delete(title):
    with app.app_context():
        movie_to_delete = db.session.execute(db.select(Movie).where(Movie.movie_title == title)).scalar()
        db.session.delete(movie_to_delete)
        db.session.commit()
    return redirect(url_for("home"))


@app.route("/update/<title>", methods=["POST", "GET"])
def update(title):
    form_data = Edit(request.form)
    if request.method == "POST" and form_data.validate_on_submit():
        movie_to_update = db.session.execute(db.select(Movie).where(Movie.movie_title == title)).scalar()
        new_rating = form_data.rating.data
        new_review = form_data.review.data
        movie_to_update.movie_rating = new_rating
        movie_to_update.movie_review = new_review
        db.session.commit()
        return redirect(url_for("home"))
    return render_template('edit.html', form=form_data, title=title)


@app.route("/add", methods=["POST", "GET"])
def add():
    form_data = NewMovie(request.form)

    if request.method == "POST" and form_data.validate_on_submit():
        title = form_data.movie_title.data
        import requests

        url = "https://api.themoviedb.org/3/search/movie"
        param = {
            "query": title,
            "api_key": API_KEY,
        }
        headers = {
            "accept": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJhMmZkYzAwMTU5ZmM1YWRhNTcxN2ZlNWQ4OGIyMzA1OCIsInN1YiI6IjY0YTAwYTFhYzM5MGM1MDE0ZTNjMGZmZSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.ICqS1tlbNHFxVDWXCk6-v6eqmMKqylIbuELwCO66WXU"
        }

        response = requests.get(url=url, params=param, headers=headers)
        movies_data = response.json()["results"]

        return render_template("select.html", movies=movies_data)
    return render_template("add.html", form=form_data)


@app.route("/select")
def select():
    param = {
        "api_key": API_KEY,
        "language": "en-US"
    }
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJhMmZkYzAwMTU5ZmM1YWRhNTcxN2ZlNWQ4OGIyMzA1OCIsInN1YiI6IjY0YTAwYTFhYzM5MGM1MDE0ZTNjMGZmZSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.ICqS1tlbNHFxVDWXCk6-v6eqmMKqylIbuELwCO66WXU"
    }
    id = request.args.get("id")

    url = "https://api.themoviedb.org/3/movie"
    response = requests.get(url=f"{url}/{id}", params=param, headers=headers).json()


    try:
        title = response["original_title"]
        release_date = response["release_date"].split("-")[0]
        description = response["overview"]
        poster_path = response["poster_path"]
        print(poster_path)
        with app.app_context():
            new_movie = Movie(
                movie_title=title,
                movie_year=release_date,
                movie_description=description,
                movie_img_url=f"https://image.tmdb.org/t/p/original{poster_path}"
            )
            db.session.add(new_movie)
            db.session.commit()
    except KeyError and TypeError:
        return redirect(url_for("home"))
    else:
        return redirect(url_for("home"))


if __name__ == '__main__':
    app.run(debug=True)

import os
from flask import Flask,request,jsonify
from flask_restful import Api,Resource
from flask_sqlalchemy import SQLAlchemy
from http import HTTPStatus
from flask_migrate import Migrate

class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://root:1234@localhost/moviedatabase'

class Development_Config(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://root:1234@localhost/moviedatabase'

class Production_Config(Config):
    uri=os.environ.get("DATABASE_URL")
    if uri and uri.startswith("postgres://"):
        uri=uri.replace("postgres://","postgresql://",1)
    SQLALCHEMY_DATABASE_URI = uri

env=os.environ.get("ENV","Development") #here development is default or get the environment

if env=="Production":
    config_str=Production_Config
else:
    config_str = Development_Config

app=Flask(__name__)

app.config.from_object(config_str)
api=Api(app)

#connection
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:welcome$1234@localhost/moviedatabase'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://root:1234@localhost/moviedatabase'
db=SQLAlchemy(app)
migrate=Migrate(app,db)

# class User(db.Model):
#     id=db.Column(db.Integer,primary_key=True)
#     name=db.Column(db.String(50),unique=True,nullable=False)
#     email=db.Column(db.String(50),unique=True,nullable=False)

# class Profile(db.Model):
#     id=db.Column(db.Integer,primary_key=True)
#     name=db.Column(db.String(50),unique=True,nullable=False)
#     email=db.Column(db.String(50),unique=True,nullable=False)

class movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # this is the primary key
    title = db.Column(db.String(80), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    genre = db.Column(db.String(80), nullable=False)

    @staticmethod
    def add_movie(title,year,genre):
        new_movie=movie(title=title,year=year,genre=genre)
        db.session.add(new_movie)
        db.session.commit()


    @staticmethod
    def get_movies():
         #mov=movie.query.all().first()
         return (movie.query.all())


    @staticmethod
    def get_one_movie(id):
        return (movie.query.filter_by(id=id).first())

    @staticmethod
    def delete_movie_by_id(id):
        result=(movie.query.filter_by(id=id).delete())
        db.session.commit()
        return result

    @staticmethod
    def update_data_by_id(id,title,year,genre):

        movie_data=movie.query.filter_by(id=id).first()
        movie_data.title=title
        movie_data.year=year
        movie_data.genre=genre
        db.session.commit()






class all_movies(Resource):
    def post(self):
        data=request.get_json()
        print(data)
        movie.add_movie(title=data["title"],year=data["year"],
                        genre=data["genre"])
        return ""

    def get(self):
        data=movie.get_movies()
        print(data)
        # for i in data:
        #     print(i.title)
        movie_list=[]
        for i in data:
            movie_list.append({"title":i.title,"year":i.year,"genre":i.genre})
        return jsonify(movie_list)



class one_movie(Resource):
    def get(self, id):
        data = movie.get_one_movie(id)
        print(data)
        if data!=None:
            res = []
            res.append({"id":data.id,"title": data.title, "year": data.year, "genre": data.genre})
            return jsonify((res),HTTPStatus.OK)
        else:
            return {'measage':"No Id found","status":HTTPStatus.NOT_FOUND}

    def delete(self,id):
        data= movie.delete_movie_by_id(id)
        new_data=movie.get_movies()
        print(data)
        movie_list = []
        if data:
            for i in new_data:
                movie_list.append({"title": i.title, "year": i.year, "genre": i.genre})
            return jsonify((movie_list),HTTPStatus.OK)

        else:
            return {'measage':"No Id found","status":HTTPStatus.NOT_FOUND}

    def put(self,id):
        data1=movie.get_one_movie(id)
        if data1:
            data = request.get_json()
            print(data)
            movie.update_data_by_id(id=id,title=data["title"], year=data["year"],
                            genre=data["genre"])
            return {'message':"Updated",'status':HTTPStatus.OK}
        else:
            return {'message':"No such ID",'status':HTTPStatus.NOT_FOUND}









api.add_resource(all_movies,"/movies")
api.add_resource(one_movie,"/movies/<int:id>")
if __name__=="__main__":
    app.run()


# class Cast(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     actor_name = db.Column(db.String(50), unique=True, nullable=False)
#     role = db.Column(db.String(50), unique=True, nullable=False)

"""this is python console commands"""
# from flask_sqlalchem import Profile
# admin=Profile(name='admin',email='admin@example.com')
# db.session.add(admin)  ####Important
# db.session.commit()      ####Important
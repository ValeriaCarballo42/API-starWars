"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planet, Favorite
# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints


@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)


@app.route('/people', methods=['GET'])
def get_all_people():
    todos_los_personajes = People.query.all()
    resultado = [personaje.serialize() for personaje in todos_los_personajes]
    return jsonify(resultado), 200


@app.route('/planets', methods=['GET'])
def get_all_planets():
    todos_los_planetas = Planet.query.all()
    resultado = [planeta.serialize() for planeta in todos_los_planetas]
    return jsonify(resultado), 200


@app.route('/people/<int:people_id>', methods=['GET'])
def get_one_person(people_id):
    personaje = People.query.get(people_id)

    if personaje is None:
        return jsonify({"msg": "Personaje no encontrado"}), 404
    return jsonify(personaje.serialize()), 200


@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_one_planet(planet_id):
    planeta = Planet.query.get(planet_id)

    if planeta is None:
        return jsonify({"msj": "Planeta no encontrado"}), 404
    return jsonify(planeta.serialize()), 200


@app.route('/users', methods=['GET'])
def get_all_users():
    todos_los_usuarios = User.query.all()
    resultado = [usuario.serialize() for usuario in todos_los_usuarios]
    return jsonify(resultado), 200


@app.route('/users/favorites', methods=['GET'])
def get_user_favorites():
    user_id = 1

    favoritos = Favorite.query.filter_by(user_id=user_id).all()
    resultado = [favorito.serialize() for favorito in favoritos]

    return jsonify(resultado), 200


@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_people(people_id):
    user_id = 1

    nuevo_favorito = Favorite(user_id=user_id, people_id=people_id)
    db.session.add(nuevo_favorito)
    db.session.commit()

    return jsonify(nuevo_favorito.serialize()), 201


@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    user_id = 1

    nuevo_favorito = Favorite(user_id=user_id, planet_id=planet_id)
    db.session.add(nuevo_favorito)
    db.session.commit()

    return jsonify(nuevo_favorito.serialize()), 201


@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(people_id):
    user_id = 1

    favorito_a_eliminar = Favorite.query.filter_by(
        user_id=user_id, people_id=people_id).first()

    if favorito_a_eliminar is None:
        return jsonify({"msg": "Favorito no encontrado"}), 404
    else:
        db.session.delete(favorito_a_eliminar)
        db.session.commit()
        return jsonify({"msg": "Favorito eliminado correctamente"}), 200


@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    user_id = 1

    favorito_a_eliminar = Favorite.query.filter_by(
        user_id=user_id, planet_id=planet_id).first()

    if favorito_a_eliminar is None:
        return jsonify({"msg": "Favorito no encontrado"}), 404
    else:
        db.session.delete(favorito_a_eliminar)
        db.session.commit()
        return jsonify({"msg": "Favorito eliminado correctamente"}), 200
    

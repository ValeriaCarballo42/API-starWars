from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)


    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class People(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(60), unique=False, nullable=False)
    height: Mapped[str] = mapped_column(String(20), nullable=True)
    mass: Mapped[str] = mapped_column(String(20), nullable=True)
    hair_color: Mapped[str] = mapped_column(String(20), nullable=True)
    skin_color: Mapped[str] = mapped_column(String(20), nullable=True)
    eye_color: Mapped[str] = mapped_column(String(20), nullable=True)
    birth_year: Mapped[str] = mapped_column(String(20), nullable=True)
    gender: Mapped[str] = mapped_column(String(20), nullable=True)


    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color,
            "birth_year": self.birth_year,
            "gender": self.gender
        }


class Planet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(60), unique=False, nullable=False)
    climate: Mapped[str] = mapped_column(String(20), nullable=True)
    terrain: Mapped[str] = mapped_column(String(20), nullable=True)
    diameter: Mapped[str] = mapped_column(String(20), nullable=True)
    gravity: Mapped[str] = mapped_column(String(20), nullable=True)
    population: Mapped[str] = mapped_column(String(20), nullable=True)
    orbital_period: Mapped[str] = mapped_column(String(20), nullable=True)
    rotation_period: Mapped[str] = mapped_column(String(20), nullable=True)
    surface_water: Mapped[str] = mapped_column(String(20), nullable=True)


    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "terrain": self.terrain,
            "diameter": self.diameter,
            "gravity": self.gravity,
            "population": self.population,
            "orbital_period": self.orbital_period,
            "rotation_period": self.rotation_period,
            "surface_water": self.surface_water
        }


class Favorite(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id:  Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    people_id: Mapped[int] = mapped_column(ForeignKey('people.id'), nullable=True)
    planet_id: Mapped[int] = mapped_column(ForeignKey('planet.id'), nullable=True)


    def serialize(self):
        return {
           "id": self.id,
           "user_id": self.user_id,
           "people_id": self.people_id,
           "planet_id": self.planet_id
        }

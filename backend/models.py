from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, nullable=False)
    genre = Column(String, nullable=False)
    director = Column(String, nullable=True)
    actors = Column(String, nullable=True)
    description = Column(String)
    year = Column(Integer)
    rating = Column(Float, default=0.0)

    reviews = relationship("Review", back_populates="movie")

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    movie_id = Column(Integer, ForeignKey("movies.id"))
    user = Column(String, nullable=False)
    score = Column(Float, nullable=False)
    comment = Column(String)

    movie = relationship("Movie", back_populates="reviews")

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    photo = Column(String(250))

class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    title = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
    items =relationship('Item', backref="categoryOfitem", lazy='dynamic')

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'title': self.title,
            'id': self.id,
            'items': [i.serialize for i in self.items]
        }

class Item(Base):
    __tablename__ = 'item'

    title = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
    nutritions =relationship('Nutritions', backref="nutritionsOfitem", lazy='dynamic')

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'category_id': self.category_id,
            'title': self.title,
            'description': self.description,
            'id': self.id,
            'nutritions': [i.serialize for i in self.nutritions]
        }

class Nutritions(Base):
    __tablename__ = 'nutritions'

    id = Column(Integer, primary_key=True)
    energy = Column(String(250), nullable=False)
    calories = Column(String(250), nullable=False)
    fat = Column(String(250), nullable=False)
    saturatedFat = Column(String(250), nullable=False)
    carbohydrate = Column(String(250), nullable=False)
    sugar = Column(String(250), nullable=False)
    dietaryFiber = Column(String(250), nullable=False)
    protein = Column(String(250), nullable=False)
    cholesterol = Column(String(250), nullable=False)
    sodium = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
    item_id =  Column(Integer, ForeignKey('item.id'))
    item = relationship(Item)


    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'energy' : self.energy,
            'calories' : self.calories,
            'fat' : self.fat,
            'saturatedFat' : self.saturatedFat,
            'carbohydrate' : self.carbohydrate,
            'sugar' : self.sugar,
            'dietaryFiber' : self.dietaryFiber,
            'protein' : self.protein,
            'cholesterol' : self.cholesterol,
            'sodium' : self.sodium,
        }

engine = create_engine('sqlite:///recipes.db')


Base.metadata.create_all(engine)
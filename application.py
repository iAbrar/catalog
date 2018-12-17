from flask import Flask
app = Flask(__name__)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Category, Base, Item, User

engine = create_engine('sqlite:///recipes.db?check_same_thread=False')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
st commit by calling
# session.rollback()
session = DBSession()


# Show all categories
@app.route('/')
@app.route('/catalog/')
def showCategories():
    return "All categories"

# Show all recipes
@app.route('/catalog/<int:category_id>/recipes/')
def showRecipes():
    return "All recipes"

# create a recipy
@app.route('/catalog/<int:category_id>/recipes/new/')
def newRecipy():
    return " recipy name"

# edit specific recipy
@app.route('/catalog/<int:category_id>/recipy/<int:recipy_id>/edit/')
def editRecipy():
    return " recipy editing"

# delete specific recipy
@app.route('/catalog/<int:category_id>/recipy/<int:recipy_id>/delete/')
def deleteRecipy():
    return " recipy deleted"


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)

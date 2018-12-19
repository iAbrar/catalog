from flask import Flask, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Category, Base, Item, User

app = Flask(__name__)


engine = create_engine('sqlite:///recipes.db?check_same_thread=False')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# session.rollback()
session = DBSession()


# Show all categories
@app.route('/')
@app.route('/catalog/')
def showCategories():
    categories = session.query(Category).all()
    items = session.query(Item).all()

    return render_template('publichome.html', categories=categories, items=items)

# Show all recipes
@app.route('/catalog/<int:category_id>/recipes/')
def showRecipes(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(category_id=category_id).all()

    return render_template('category.html', category=category, items=items)

# Show one recipy
@app.route('/catalog/<int:category_id>/recipes/<int:recipy_id>/')
def showRecipy(category_id,recipy_id):
    category = session.query(Category).filter_by(id=category_id).one()
    item = session.query(Item).filter_by(id=recipy_id).one()

    return render_template('category.html', category=category, items=items)
# create a recipy
@app.route('/catalog/<int:category_id>/recipes/new/')
def newRecipy(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    return render_template('new.html', category_id=category_id)

# edit specific recipy
@app.route('/catalog/<int:category_id>/recipy/<int:recipy_id>/edit/')
def editRecipy(category_id,recipy_id):
    category = session.query(Category).filter_by(id=category_id).one()
    item = session.query(Item).filter_by(id=recipy_id).one()
    return render_template('edit.html', category=category, item=item)

# delete specific recipy
@app.route('/catalog/<int:category_id>/recipy/<int:recipy_id>/delete/')
def deleteRecipy(category_id,recipy_id):
    category = session.query(Category).filter_by(id=category_id).one()
    item = session.query(Item).filter_by(id=recipy_id).one()
    return render_template('delete.html', item=item)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)

from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Category, Base, Item, User

from flask import session as login_session
import random, string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)


engine = create_engine('sqlite:///recipes.db?check_same_thread=False')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# session.rollback()
session = DBSession()


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return  render_template('login.html', STATE=state)

# JSON APIs to view the catalog
@app.route('/catalog/JSON')
def showCategoriesJSON():
    categories = session.query(Category).all()
    return jsonify(categories=[i.serialize for i in categories])

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

    return render_template('recipy.html', category=category, item=item)
# create a recipy
@app.route('/catalog/<int:category_id>/recipes/new/',methods=['GET','POST'])
def newRecipy(category_id):
    if request.method == 'POST':
        newItem = Item(title = request.form['name'],description = request.form['description'],category_id=category_id)
        session.add(newItem)
        session.commit()
        flash("new  recipy %s created!" %(newItem.title))
        return redirect(url_for('showRecipes',category_id=category_id))
    else:
        return render_template('new.html', category_id=category_id)

# edit specific recipy
@app.route('/catalog/<int:category_id>/recipy/<int:recipy_id>/edit/',methods=['GET','POST'])
def editRecipy(category_id,recipy_id):
    editedItem = session.query(Item).filter_by(id=recipy_id).one()

    if request.method == 'POST':
        if request.form['title']:
            editedItem.title = request.form['title']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['meal']:
            if request.form['meal'] == "Breakfast":
                editedItem.category_id=1
            elif request.form['meal'] == "Lunch":
                editedItem.category_id=2
            else:
                editedItem.category_id=3
        session.add(editedItem)
        session.commit()
        flash("Recipy %s Successfully Edited!" %(editedItem.title))
        return redirect(url_for('showRecipes',category_id=editedItem.category_id))
    else:
        return render_template('edit.html', category_id=category_id, recipy_id=recipy_id, item =editedItem)

# delete specific recipy
@app.route('/catalog/<int:category_id>/recipy/<int:recipy_id>/delete/', methods =['GET','POST'])
def deleteRecipy(category_id,recipy_id):
    deletedItem = session.query(Item).filter_by(id=recipy_id).one()
    if request.method == 'POST':
        session.delete(deletedItem)
        session.commit()
        flash('Recipy Successfully Deleted')
        return redirect(url_for('showRecipes', category_id=category_id))
    return render_template('delete.html', item=deletedItem)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)

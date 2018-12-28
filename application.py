from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Category, Base, Item, User, Nutritions

from flask import session as login_session
import random, string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Catalog Application"


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

@app.route('/gconnect', methods=['POST'])
def gconnect():
     # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
# Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    # ADD PROVIDER TO LOGIN SESSION
    login_session['provider'] = 'google'

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], photo=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None



@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        flash("you are Successfully disconnected")
        return redirect(url_for('showCategories'))

    else:
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response

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
    items = session.query(Item).limit(4)
    print(categories)
    for i in items:
        print(i)
    if 'username' not in login_session:
        return render_template('index.html', categories=categories, items=items)
    else:
        return render_template('home.html', categories=categories, items=items)

# Show all recipes
@app.route('/catalog/<int:category_id>/recipes/')
def showRecipes(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(category_id=category_id).all()
    if 'username' not in login_session:
        return render_template('publiccategory.html', category=category, items=items)
    else:
        return render_template('category.html', category=category, items=items)

# Show one recipe
@app.route('/catalog/<int:category_id>/recipes/<int:recipe_id>/')
def showrecipe(category_id,recipe_id):
    category = session.query(Category).filter_by(id=category_id).one()
    item = session.query(Item).filter_by(id=recipe_id).one()
    if 'username' not in login_session:
        return render_template('publicrecipe.html', category=category, item=item)
    else:
        return render_template('recipe.html', category=category, item=item)
# create a recipe
@app.route('/catalog/<int:category_id>/recipes/new/',methods=['GET','POST'])
def newrecipe(category_id):
    if 'username' not in login_session:
        return redirect('/login')

    if request.method == 'POST':
        nutritions1 = [Nutritions(energy = request.form['energy'],calories = request.form['calories'],
                    fat = request.form['fat'],saturatedFat = request.form['s-fat'],
                    carbohydrate = request.form['carbs'],sugar = request.form['sugar'],
                    dietaryFiber = request.form['fibers'],protein = request.form['protein'],
                    cholesterol = request.form['chol'],sodium = request.form['sodium'])]

        newItem = Item(title = request.form['name'],description = request.form['description'],
                        ingredients = request.form['ingredients'], instructions = request.form['instructions'],
                        difficulty = request.form['difficulty'], serves = request.form['serves'],
                        preparingTime = request.form['p-time'], cookingTime = request.form['c-time'],
                        nutritions=nutritions1,picture=request.form['image'],
                        category_id=category_id,  user_id=login_session['user_id'])
        session.add(newItem)
        session.commit()
        flash("new  recipe %s created!" %(newItem.title))
        return redirect(url_for('showRecipes',category_id=category_id))
    else:
        return render_template('new.html', category_id=category_id)

# edit specific recipe
@app.route('/catalog/<int:category_id>/recipe/<int:recipe_id>/edit/',methods=['GET','POST'])
def editrecipe(category_id,recipe_id):
    editedItem = session.query(Item).filter_by(id=recipe_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if editedItem.user_id != login_session['user_id']:
        return """<script>function myFunction() {alert('You are not authorized to edit this recipe. Please create your own recipe in order to edit.');
         window.location.href = '/catalog/"""+str(category_id)+"/recipes/';}</script><body onload='myFunction()''>"""
        return redirect(url_for('showCategories'))
    if request.method == 'POST':
        if request.form['title']:
            editedItem.title = request.form['title']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['categories']:
            editedItem.category_id = request.form['categories']

        session.add(editedItem)
        session.commit()
        flash("recipe %s Successfully Edited!" %(editedItem.title))
        return redirect(url_for('showRecipes',category_id=editedItem.category_id))
    else:
        return render_template('edit.html', category_id=category_id, recipe_id=recipe_id, item =editedItem)

# delete specific recipe
@app.route('/catalog/<int:category_id>/recipe/<int:recipe_id>/delete/', methods =['GET','POST'])
def deleterecipe(category_id,recipe_id):
    deletedItem = session.query(Item).filter_by(id=recipe_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if deletedItem.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized to delete this recipe. Please create your own recipe in order to delete.');window.location.href = '/catalog/"""+str(category_id)+"/recipes/'}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        session.delete(deletedItem)
        session.commit()
        flash('recipe Successfully Deleted')
        return redirect(url_for('showRecipes', category_id=category_id))
    return render_template('delete.html', item=deletedItem)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)

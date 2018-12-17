from flask import Flask
app = Flask(__name__)

# Show all categories
@app.route('/')
@app.route('/catalog/')
def showCategories():
    return "All categories"

# Show all recipes
@app.route('/catalog/category/recipes/')
def showRecipes():
    return "All recipes"

# Show specific recipy
@app.route('/catalog/category/recipy/')
def showRecipy():
    return " recipy name"

# edit specific recipy
@app.route('/catalog/category/recipy/edit/')
def editRecipy():
    return " recipy editing"

# delete specific recipy
@app.route('/catalog/category/recipy/delete/')
def deleteRecipy():
    return " recipy deleted"


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)

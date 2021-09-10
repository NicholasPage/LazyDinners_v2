#!flask/bin/python
"""Now let's build from a JSON in s3. Did someone say stateful?"""
import random
import json
import boto3

from flask import Flask, jsonify, request, abort, make_response

app = Flask(__name__)

my_bucket = 'lazydinners'
my_key = 'allrecipes.json'

s3 = boto3.client('s3')

object = s3.get_object(Bucket = my_bucket, Key = my_key)
object_data = json.loads(object['Body'].read())

data = []
data += object_data

recipes = data


@app.route('/recipe/api/v2.0/recipe/allrecipes', methods=['GET'])
def Get_Allrecipes():
    """Return all recipes"""
    return jsonify(recipes)

	
@app.route('/recipe/api/v2.0/recipe/recipeoftheday', methods=['GET'])
def Get_Recipeoftheday():
    """Return a random recipe"""
	#Example
	#curl -X GET http://localhost:5000/recipe/api/v1.0/recipe/recipeoftheday
    recipe = random.choice(recipes)
    return jsonify({'Meal of the day': recipe['name']}, {'Ingredients': recipe['ingredients']}, {'Side Ideas': recipe['side_ideas']}, {'Difficulty Level': recipe['difficulty']})

	
@app.route('/recipe/api/v2.0/newrecipe', methods=['POST'])
def Create_Recipe():
    """Adds a recipe to the list"""
	#Example
	#curl -H "Content-Type: application/json" -X POST -d '{"name":"recipename","ingredients":"ingredient1, ingredient2, ingredient3","side_ideas":"idea1, idea2, idea3","difficulty":"difficultylevel"}' http://localhost:5000/recipe/api/v1.0/newrecipe
    if not request.json or not "name" in request.json or not "ingredients" in request.json or not "side_ideas" in request.json or not "difficulty" in request.json:
        abort(400)
    recipe = {
        "name": request.json.get("name", ""),
        "ingredients": request.json.get("ingredients", ""),
	"side_ideas": request.json.get("side_ideas", ""),
	"difficulty": request.json.get("difficulty", "")
    }
    recipes.append(recipe)

    newrecipes = json.dumps(recipes)

    s3.put_object(Body = newrecipes, Bucket = my_bucket, Key = my_key)
    return jsonify({'Succesffuly added the recipe ': recipe["name"]}), 201


if __name__ == '__main__':
    app.run(debug=True)

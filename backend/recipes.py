
from flask import Flask, request, jsonify
from flask_restx import Resource, Namespace, fields
from models import Recipe
from flask_jwt_extended import jwt_required


recipe_ns=Namespace('recipe', description="A namespece recipes")

#serilize to JSON. We will use this to take the SQL Alchemy output and change it to JSON
recipe_model=recipe_ns.model(
    "Recipe",
    {
        "id":fields.Integer(),
        "title":fields.String(),
        "description":fields.String()
    }
)

@recipe_ns.route('/hello')
class HelloResource(Resource):
    #testing hello world
    # GET
    def get(self):
        
        return {"message": "Hello World"}
          

@recipe_ns.route('/recipes')
class RecipesResource(Resource):
    
    # marshal_list_with Takes your data object and applies the field filtering. 
    # The marshalling can work on single objects, dicts, or lists of objects.

    # GET ALL
    @recipe_ns.marshal_list_with(recipe_model)
    def get(self):
        """Get all recipes """
        recipes=Recipe.query.all() # Returns full list of recipes as SQL Alchemo object. Then we'll convert to JSON
        return recipes

    #POST
    @recipe_ns.marshal_with(recipe_model)
    @recipe_ns.expect(recipe_model)
    @jwt_required() # protects the route
    def post(self):
        """Create a new recipe"""
        data=request.get_json()
        new_recipe=Recipe(
            title=data.get('title'),
            description=data.get('description')
        )
        new_recipe.save() #saves to the database (references the models.py file for save under the 'Recipe' class)
        
        return new_recipe, 201


@recipe_ns.route('/recipe/<int:id>')
class RecipeResource(Resource):
    #GET BY ID
    @recipe_ns.marshal_with(recipe_model)
    def get(self,id):
        """Get a recipe by id"""
        recipe=Recipe.query.get_or_404(id)

        return recipe

    #PUT BY ID
    @recipe_ns.marshal_with(recipe_model)
    @jwt_required() # protects the route
    def put(self,id):
        """Update Recipe by id"""
        recipe_to_update=Recipe.query.get_or_404(id)

        data=request.get_json()

        recipe_to_update.update(data.get('title'), data.get('description')) #saves to the database (references the models.py file for save under the 'Recipe' class)
        
        return recipe_to_update, 201


    #DELETE BY ID
    @recipe_ns.marshal_with(recipe_model)
    @jwt_required() # protects the route
    def delete(self,id):
        """Delete recipe by id"""
        recipe_to_delete=Recipe.query.get_or_404(id)

        recipe_to_delete.delete()
        
        return recipe_to_delete, 201


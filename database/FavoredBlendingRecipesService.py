from typing import List
from database.models import FavoredBlendingRecipes
from database.connection import db

class FavoredBlendingRecipesService:
    collection = db['FavoredBlendingRecipes']

    @classmethod
    async def create(cls, favored_blending_recipe: FavoredBlendingRecipes) -> FavoredBlendingRecipes:
        favored_blending_recipe_dict = favored_blending_recipe.dict()
        await cls.collection.insert_one(favored_blending_recipe_dict)
        return favored_blending_recipe

    @classmethod
    async def read(cls, favored_blend_id: str) -> FavoredBlendingRecipes:
        favored_blending_recipe = await cls.collection.find_one({"favored_blend_id": favored_blend_id})
        return FavoredBlendingRecipes(**favored_blending_recipe) if favored_blending_recipe else None

    @classmethod
    async def read_by_user_id(cls, user_id: str) -> List[FavoredBlendingRecipes]:
        favored_blending_recipes = await cls.collection.find({"user_id": user_id}).to_list(length=100)
        return [FavoredBlendingRecipes(**favored_blending_recipe) for favored_blending_recipe in favored_blending_recipes]

    @classmethod
    async def update(cls, favored_blend_id: str, favored_blending_recipe: FavoredBlendingRecipes) -> FavoredBlendingRecipes:
        favored_blending_recipe_dict = favored_blending_recipe.dict()
        await cls.collection.replace_one({"favored_blend_id": favored_blend_id}, favored_blending_recipe_dict)
        return await cls.read(favored_blend_id)

    @classmethod
    async def delete(cls, favored_blend_id: str) -> None:
        await cls.collection.delete_one({"favored_blend_id": favored_blend_id})

    @classmethod
    async def delete_by_user_id(cls, user_id: str) -> None:
        await cls.collection.delete_many({"user_id": user_id})
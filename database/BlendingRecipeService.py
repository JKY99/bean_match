from typing import List
from database.models import BlendingRecipe
from database.connection import db

# 블렌딩 레시피에 대한 CRUD 연산을 수행하는 BlendingRecipeService 클래스입니다.
class BlendingRecipeService:
    collection = db['BlendingRecipes']

    @classmethod
    async def create(cls, blending_recipe: BlendingRecipe) -> BlendingRecipe:
        blending_recipe_dict = blending_recipe.dict()
        await cls.collection.insert_one(blending_recipe_dict)
        return blending_recipe

    @classmethod
    async def read(cls, blend_id: str) -> BlendingRecipe:
        blending_recipe = await cls.collection.find_one({"blend_id": blend_id})
        return BlendingRecipe(**blending_recipe) if blending_recipe else None

    @classmethod
    async def read_all(cls) -> List[BlendingRecipe]:
        blending_recipes = await cls.collection.find().to_list(length=100)
        return [BlendingRecipe(**blending_recipe) for blending_recipe in blending_recipes]

    @classmethod
    async def update(cls, blend_id: str, blending_recipe: BlendingRecipe) -> BlendingRecipe:
        await cls.collection.replace_one({"blend_id": blend_id}, blending_recipe.dict())
        return await cls.read(blending_recipe.blend_id)

    @classmethod
    async def delete(cls, blend_id: str) -> None:
        await cls.collection.delete_one({"blend_id": blend_id})
from typing import List
from database.models import FavoredBean
from database.connection import db

class FavoredBeanService:
    collection = db['FavoredBeans']

    @classmethod
    async def create(cls, favored_bean: FavoredBean) -> FavoredBean:
        favored_bean_dict = favored_bean.dict()
        await cls.collection.insert_one(favored_bean_dict)
        return favored_bean

    @classmethod
    async def read(cls, favored_bean_id: str) -> FavoredBean:
        favored_bean = await cls.collection.find_one({"favored_bean_id": favored_bean_id})
        return FavoredBean(**favored_bean) if favored_bean else None

    @classmethod
    async def read_by_user_id(cls, user_id: str) -> List[FavoredBean]:
        favored_beans = await cls.collection.find({"user_id": user_id}).to_list(length=100)
        return [FavoredBean(**favored_bean) for favored_bean in favored_beans]

    @classmethod
    async def read_all(cls) -> List[FavoredBean]:
        favored_beans = await cls.collection.find().to_list(length=100)
        return [FavoredBean(**favored_bean) for favored_bean in favored_beans]

    @classmethod
    async def update(cls, favored_bean_id: str, favored_bean: FavoredBean) -> FavoredBean:
        await cls.collection.replace_one({"favored_bean_id": favored_bean_id}, favored_bean.dict())
        return await cls.read(favored_bean.favored_bean_id)
    
    @classmethod
    async def delete(cls, favored_bean_id: str) -> bool:
        result = await cls.collection.delete_one({"favored_bean_id": favored_bean_id})
        return result.deleted_count > 0

    @classmethod
    async def delete_by_user_id(cls, user_id: str) -> bool:
        result = await cls.collection.delete_many({"user_id": user_id})
        return result.deleted_count > 0

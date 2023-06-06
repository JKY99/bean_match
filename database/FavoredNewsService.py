from typing import List
from database.models import FavoredNews
from database.connection import db

class FavoredNewsService:
    collection = db['FavoredNews']

    @classmethod
    async def create(cls, favored_news: FavoredNews) -> FavoredNews:
        favored_news_dict = favored_news.dict()
        await cls.collection.insert_one(favored_news_dict)
        return favored_news

    @classmethod
    async def read(cls, favored_news_id: str) -> FavoredNews:
        favored_news = await cls.collection.find_one({"favored_news_id": favored_news_id})
        return FavoredNews(**favored_news) if favored_news else None

    @classmethod
    async def read_by_user_id(cls, user_id: str) -> List[FavoredNews]:
        favored_news_list = await cls.collection.find({"user_id": user_id}).to_list(length=100)
        return [FavoredNews(**favored_news) for favored_news in favored_news_list]

    @classmethod
    async def update(cls, favored_news_id: str, favored_news: FavoredNews) -> FavoredNews:
        favored_news_dict = favored_news.dict()
        await cls.collection.replace_one({"favored_news_id": favored_news_id}, favored_news_dict)
        return await cls.read(favored_news_id)

    @classmethod
    async def delete(cls, favored_news_id: str) -> None:
        await cls.collection.delete_one({"favored_news_id": favored_news_id})

    @classmethod
    async def delete_by_user_id(cls, user_id: str) -> None:
        await cls.collection.delete_many({"user_id": user_id})

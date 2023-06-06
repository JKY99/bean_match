from typing import List
from database.models import News
from database.connection import db

class NewsService:
    collection = db['News']

    @classmethod
    async def create(cls, news: News) -> News:
        news_dict = news.dict()
        await cls.collection.insert_one(news_dict)
        return news

    @classmethod
    async def read(cls, news_id: str) -> News:
        news = await cls.collection.find_one({"news_id": news_id})
        return News(**news) if news else None

    @classmethod
    async def read_by_user_id(cls, user_id: str) -> List[News]:
        news_items = await cls.collection.find({"user_id": user_id}).to_list(length=100)
        return [News(**news) for news in news_items]

    @classmethod
    async def update(cls, news_id: str, news: News) -> News:
        news_dict = news.dict()
        await cls.collection.replace_one({"news_id": news_id}, news_dict)
        return await cls.read(news_id)

    @classmethod
    async def delete(cls, news_id: str) -> None:
        await cls.collection.delete_one({"news_id": news_id})

    @classmethod
    async def delete_by_user_id(cls, user_id: str) -> None:
        await cls.collection.delete_many({"user_id": user_id})
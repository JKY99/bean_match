from typing import List
from database.models import Bean
from database.connection import db

# 원두에 대한 CRUD 연산을 수행하는 BeanService 클래스입니다.
class BeanService:
    collection = db['Beans']

    @classmethod
    async def create(cls, bean: Bean) -> Bean:
        bean_dict = bean.dict()
        await cls.collection.insert_one(bean_dict)
        return bean

    @classmethod
    async def read(cls, bean_id: str) -> Bean:
        bean = await cls.collection.find_one({"bean_id": bean_id})
        return Bean(**bean) if bean else None

    @classmethod
    async def read_all(cls) -> List[Bean]:
        beans = await cls.collection.find().to_list(length=100)
        return [Bean(**bean) for bean in beans]

    @classmethod
    async def update(cls, bean_id: str, bean: Bean) -> Bean:
        await cls.collection.replace_one({"bean_id": bean_id}, bean.dict())
        return await cls.read(bean.bean_id)

    @classmethod
    async def delete(cls, bean_id: str) -> None:
        await cls.collection.delete_one({"bean_id": bean_id})
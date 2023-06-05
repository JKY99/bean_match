from typing import List
from database.models import Beverage
from database.connection import db

class BeverageService:
    collection = db['Beverages']

    @classmethod
    async def create(cls, beverage: Beverage) -> Beverage:
        beverage_dict = beverage.dict()
        await cls.collection.insert_one(beverage_dict)
        return beverage

    @classmethod
    async def read(cls, beverage_id: str) -> Beverage:
        beverage = await cls.collection.find_one({"beverage_id": beverage_id})
        return Beverage(**beverage) if beverage else None

    @classmethod
    async def read_all(cls) -> List[Beverage]:
        beverages = await cls.collection.find().to_list(length=100)
        return [Beverage(**beverage) for beverage in beverages]

    @classmethod
    async def update(cls, beverage_id: str, beverage: Beverage) -> Beverage:
        await cls.collection.replace_one({"beverage_id": beverage_id}, beverage.dict())
        return await cls.read(beverage.beverage_id)

    @classmethod
    async def delete(cls, beverage_id: str) -> bool:
        result = await cls.collection.delete_one({"beverage_id": beverage_id})
        return result.deleted_count > 0

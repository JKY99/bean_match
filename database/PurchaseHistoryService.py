from database.models import PurchaseHistory
from database.connection import db
from typing import List
from fastapi.encoders import jsonable_encoder

class PurchaseHistoryService:
    collection = db['PurchaseHistories']

    @classmethod
    async def create(cls, purchase_history: PurchaseHistory) -> PurchaseHistory:
        purchase_history_dict = jsonable_encoder(purchase_history)
        result = await cls.collection.insert_one(purchase_history_dict)
        new_purchase_history = await cls.collection.find_one({"_id": result.inserted_id})
        return PurchaseHistory(**new_purchase_history)

    @classmethod
    async def read_by_purchase_id(cls, purchase_id: str) -> PurchaseHistory:
        purchase_history = await cls.collection.find_one({"purchase_id": purchase_id})
        return PurchaseHistory(**purchase_history) if purchase_history else None

    @classmethod
    async def read_by_user_id(cls, user_id: str) -> List[PurchaseHistory]:
        purchase_histories = await cls.collection.find({"user_id": user_id}).to_list(length=100)
        return [PurchaseHistory(**purchase_history) for purchase_history in purchase_histories]

    @classmethod
    async def update_by_purchase_id(cls, purchase_id: str, purchase_history: PurchaseHistory) -> PurchaseHistory:
        await cls.collection.replace_one({"purchase_id": purchase_id}, jsonable_encoder(purchase_history))
        return await cls.read_by_purchase_id(purchase_id)

    @classmethod
    async def delete_by_purchase_id(cls, purchase_id: str) -> bool:
        delete_result = await cls.collection.delete_one({"purchase_id": purchase_id})
        return bool(delete_result.deleted_count)

    @classmethod
    async def delete_by_user_id(cls, user_id: str) -> bool:
        delete_result = await cls.collection.delete_many({"user_id": user_id})
        return bool(delete_result.deleted_count)

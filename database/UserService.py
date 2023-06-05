from typing import List
from fastapi.encoders import jsonable_encoder
from database.models import User
from database.connection import db

class UserService:
    collection = db['Users']

    @classmethod
    async def create(cls, user: User) -> User:
        user_dict = jsonable_encoder(user)
        new_user = await cls.collection.insert_one(user_dict)
        created_user = await cls.collection.find_one({"_id": new_user.inserted_id})
        return User(**created_user)

    @classmethod
    async def read(cls, user_id: str) -> User:
        user = await cls.collection.find_one({"_id": user_id})
        if user:
            return User(**user)
        return None

    @classmethod
    async def read_all(cls) -> List[User]:
        users = await cls.collection.find().to_list(length=100)
        return [User(**user) for user in users]

    @classmethod
    async def update(cls, user_id: str, user: User) -> User:
        user_dict = jsonable_encoder(user)
        await cls.collection.replace_one({"_id": user_id}, user_dict)
        updated_user = await cls.collection.find_one({"_id": user_id})
        if updated_user:
            return User(**updated_user)
        return None

    @classmethod
    async def delete(cls, user_id: str) -> None:
        delete_result = await cls.collection.delete_one({"_id": user_id})
        if delete_result.deleted_count:
            return True
        return False

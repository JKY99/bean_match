from typing import List
from fastapi.encoders import jsonable_encoder
from database.models import UserPreference
from database.connection import db

class UserPreferenceService:
    collection = db['UserPreferences']

    @classmethod
    async def create(cls, preference: UserPreference) -> UserPreference:
        preference_dict = jsonable_encoder(preference)
        new_preference = await cls.collection.insert_one(preference_dict)
        created_preference = await cls.collection.find_one({"preference_id": preference.preference_id})
        return UserPreference(**created_preference)

    @classmethod
    async def read_by_preference_id(cls, preference_id: str) -> UserPreference:
        preference = await cls.collection.find_one({"preference_id": preference_id})
        if preference:
            return UserPreference(**preference)
        return None

    @classmethod
    async def read_by_user_id(cls, user_id: str) -> List[UserPreference]:
        preferences = await cls.collection.find({"user_id": user_id}).to_list(length=100)
        return [UserPreference(**preference) for preference in preferences]

    @classmethod
    async def update_by_preference_id(cls, preference_id: str, preference: UserPreference) -> UserPreference:
        preference_dict = jsonable_encoder(preference)
        await cls.collection.replace_one({"preference_id": preference_id}, preference_dict)
        updated_preference = await cls.collection.find_one({"preference_id": preference_id})
        if updated_preference:
            return UserPreference(**updated_preference)
        return None

    @classmethod
    async def update_by_user_id(cls, user_id: str, preference: UserPreference) -> List[UserPreference]:
        preference_dict = jsonable_encoder(preference)
        await cls.collection.update_many({"user_id": user_id}, {"$set": preference_dict})
        updated_preferences = await cls.collection.find({"user_id": user_id}).to_list(length=100)
        return [UserPreference(**preference) for preference in updated_preferences]

    @classmethod
    async def delete_by_preference_id(cls, preference_id: str) -> None:
        delete_result = await cls.collection.delete_one({"preference_id": preference_id})
        if delete_result.deleted_count:
            return True
        return False

    @classmethod
    async def delete_by_user_id(cls, user_id: str) -> None:
        delete_result = await cls.collection.delete_many({"user_id": user_id})
        if delete_result.deleted_count:
            return True
        return False

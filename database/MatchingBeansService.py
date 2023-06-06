from typing import List
from database.models import Bean
from database.connection import db
from numpy import dot
from numpy.linalg import norm

class MatchingBeansService:
    beans = db['Beans']
    user_preferences = db['UserPreferences']

    @staticmethod
    def one_hot_encode(value: str, categories: List[str]) -> List[int]:
        return [1 if category == value else 0 for category in categories]

    @staticmethod
    def cosine_similarity(a: List[int], b: List[int]) -> float:
        return dot(a, b) / (norm(a) * norm(b))

    @classmethod
    async def match_beans(cls, user_id: str) -> List[Bean]:
        all_origins = ['Brazil', 'Colombia', 'Ethiopia', 'Kenya', 'Costa Rica', 'Guatemala', 'Yemen', 'India', 'Vietnam']
        all_processes = ['Natural', 'Washed', 'Honey', 'Pulped Natural', 'Wet-hulled', 'Semi-washed']

        bean_list = await cls.beans.find().to_list(length=1000)
        user_preference = await cls.user_preferences.find_one({'user_id': user_id})

        if not user_preference:
            return None

        user_vector = [
            user_preference['preferred_acidity_level'],
            user_preference['preferred_bitterness_level'],
            user_preference['preferred_body_level'],
            user_preference['preferred_sweetness_level']
        ]
        user_vector += cls.one_hot_encode(user_preference['preferred_origin'], all_origins)
        user_vector += cls.one_hot_encode(user_preference['preferred_process'], all_processes)

        result_list = []

        for bean in bean_list:
            bean_vector = [
                bean['acidity_level'],
                bean['bitterness_level'],
                bean['body_level'],
                bean['sweetness_level']
            ]
            bean_vector += cls.one_hot_encode(bean['origin'], all_origins)
            bean_vector += cls.one_hot_encode(bean['process'], all_processes)

            similarity = cls.cosine_similarity(user_vector, bean_vector)
            result_list.append((bean, similarity))  # 원두 자체를 리스트에 추가

        result_list.sort(key=lambda x: x[1], reverse=True)

        return [bean for bean, _ in result_list]  # 원두 자체를 반환
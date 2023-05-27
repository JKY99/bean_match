from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv, find_dotenv
from datetime import datetime
from models import *
import os
import asyncio
from typing import List
from numpy import dot
from numpy.linalg import norm

load_dotenv(find_dotenv())

password = os.environ.get("MONGODB_PWD")

uri = f"mongodb+srv://admin:{1234}@recommend.wg2l4em.mongodb.net/?retryWrites=true&w=majority"

client = AsyncIOMotorClient(uri)


# 데이터베이스를 선택합니다.
db = client.BeanRecommendationsDB

async def find_user_by_id(user_id):
    users = db.Users
    user_list = await users.find_one({'user_id': user_id})
    return user_list

async def find_all_beans():
    beans = db.Beans
    bean_list = await beans.find().to_list(length=1000)
    return bean_list

async def find_bean_by_name(bean_name):
    beans = db.Beans
    bean = await beans.find_one({'name': bean_name})
    return bean

async def find_bean_by_id(bean_id):
    beans = db.Beans
    bean = await beans.find_one({'bean_id': bean_id})
    return bean

async def find_user_preference(user_id):
    user_preferences = db.UserPreferences
    user_preference = await user_preferences.find_one({'user_id': user_id})
    return user_preference

async def post_create_user(user):
    if await db.Users.find_one({"user_id": user.user_id}):
        raise HTTPException(status_code=400, detail="User already registered")

    user.created_at = datetime.now()  # 계정 생성 날짜 설정
    user.updated_at = datetime.now()  # 계정 정보 수정 날짜 설정

    user_obj = user.dict()
    result = await db.Users.insert_one(user_obj)
    return result

async def post_create_preference(pref: UserPreference):
    if await db.UserPreferences.find_one({"preference_id": pref.preference_id}):
        raise HTTPException(status_code=400, detail="Preference already exists")

    pref.created_at = datetime.now()  # 선호도 정보 생성 날짜 설정
    pref.updated_at = datetime.now()  # 선호도 정보 수정 날짜 설정

    pref_obj = pref.dict()
    result = await db.UserPreferences.insert_one(pref_obj)
    return result.inserted_id


def one_hot_encode(value: str, categories: List[str]) -> List[int]:
    return [1 if category == value else 0 for category in categories]

# 코사인 유사도 계산 함수
def cosine_similarity(a: List[int], b: List[int]) -> float:
    return dot(a, b) / (norm(a) * norm(b))

all_origins = ['Brazil', 'Colombia', 'Ethiopia', 'Kenya', 'Costa Rica', 'Guatemala', 'Yemen', 'India', 'Vietnam']
all_processes = ['Natural', 'Washed', 'Honey', 'Pulped Natural', 'Wet-hulled', 'Semi-washed']

async def match_beans(user_id: str) -> List[Bean]:
    beans = db.Beans
    user_preferences = db.UserPreferences

    bean_list = await beans.find().to_list(length=1000)
    user_preference = await user_preferences.find_one({'user_id': user_id})

    if not user_preference:
        return None

    user_vector = [
        user_preference['preferred_acidity_level'],
        user_preference['preferred_bitterness_level'],
        user_preference['preferred_body_level'],
        user_preference['preferred_sweetness_level']
    ]
    user_vector += one_hot_encode(user_preference['preferred_origin'], all_origins)
    user_vector += one_hot_encode(user_preference['preferred_process'], all_processes)

    result_list = []

    for bean in bean_list:
        bean_vector = [
            bean['acidity_level'],
            bean['bitterness_level'],
            bean['body_level'],
            bean['sweetness_level']
        ]
        bean_vector += one_hot_encode(bean['origin'], all_origins)
        bean_vector += one_hot_encode(bean['process'], all_processes)

        similarity = cosine_similarity(user_vector, bean_vector)
        result_list.append((bean, similarity))  # 원두 자체를 리스트에 추가

    result_list.sort(key=lambda x: x[1], reverse=True)

    return [bean for bean, _ in result_list]  # 원두 자체를 반환


# print(asyncio.run(match_beans("23234")))
# print(asyncio.run(find_bean_by_id("34009")))
# print(asyncio.run(find_all_beans()))
# print(asyncio.run(find_user_preference("23234")))

# #----------------------사용자 선호도 정보 랜덤 생성-------------------------
# from faker import Faker
# from pydantic import ValidationError
# from random import randint

# fake = Faker()  # Faker 인스턴스 생성

# # # 원두 가공 방식 선택지
# processes = ['Natural', 'Washed', 'Honey', 'Pulped Natural', 'Wet-hulled', 'Semi-washed']

# # # 원두 로스팅 레벨 선택지
# roast_levels = ['Light', 'Medium', 'Medium-Dark', 'Dark']

# # # 원두 원산지 선택지
# origins = ['Brazil', 'Colombia', 'Ethiopia', 'Kenya', 'Costa Rica', 'Guatemala', 'Yemen', 'India', 'Vietnam']

# # # 원두 맛 프로파일 선택지
# flavor_profiles_choices = ['Chocolatey', 'Fruity', 'Nutty', 'Floral', 'Spicy', 'Sweet', 'Winey', 'Citrus', 'Caramel', 'Buttery', 'Sour', 'Earthy']

# async def get_random_beans_ids(n):
#     beans = db.Beans
#     sample_beans = await beans.aggregate([{"$sample": {"size": n}}]).to_list(n)
#     return [bean['bean_id'] for bean in sample_beans]

# async def create_user_preference(user):
#     preferences = db.UserPreferences  # Preferences 컬렉션

#     preferred_beverage_ids = await get_random_beans_ids(3)  # 선호 음료 ID
#     preferred_beans_ids = await get_random_beans_ids(3)  # 선호 원두 ID

#     user_preference = {
#         "preference_id": fake.unique.random_number(digits=5),
#         "user_id": user['user_id'],
#         "preferred_beverage_ids": preferred_beverage_ids,
#         "preferred_beans_ids": preferred_beans_ids,
#         "preferred_process": fake.random_element(elements=processes),
#         "preferred_origin": fake.random_element(elements=origins),
#         "preferred_roast": fake.random_element(elements=roast_levels),
#         "preferred_acidity_level": randint(1, 5),
#         "preferred_bitterness_level": randint(1, 5),
#         "preferred_body_level": randint(1, 5),
#         "preferred_sweetness_level": randint(1, 5),
#         "preferred_flavor_profiles": ", ".join(fake.random_elements(elements=flavor_profiles_choices, length=3, unique=True)),
#         "created_at": datetime.now(),
#         "updated_at": datetime.now(),
#     }

#     # 생성된 데이터가 UserPreference 모델에 맞는지 검사
#     try:
#         user_preference_model = UserPreference(**user_preference)
#     except ValidationError as e:
#         print(f"Error: {e}")
#         return

#     # DB에 UserPreference 문서 생성
#     await preferences.insert_one(user_preference_model.dict())

# async def generate_user_preferences():
#     users = db.Users
#     all_users = await users.find().to_list(1000)  # 모든 사용자 가져오기
#     for user in all_users:
#         await create_user_preference(user)

# # UserPreference 문서 생성
# loop = asyncio.get_event_loop()
# loop.run_until_complete(generate_user_preferences())

# # ---------------------------원두 정보 랜덤 생성---------------------------
# from faker import Faker
# from pydantic import ValidationError
# from random import randint

# fake = Faker()  # Faker 인스턴스 생성

# async def create_bean(bean):
#     # Bean 컬렉션에 Bean 문서를 생성하는 함수
#     beans = db.Beans
#     await beans.insert_one(bean.dict())


# # 원두 가공 방식 선택지
# processes = ['Natural', 'Washed', 'Honey', 'Pulped Natural', 'Wet-hulled', 'Semi-washed']

# # 원두 로스팅 레벨 선택지
# roast_levels = ['Light', 'Medium', 'Medium-Dark', 'Dark']

# # 원두 원산지 선택지
# origins = ['Brazil', 'Colombia', 'Ethiopia', 'Kenya', 'Costa Rica', 'Guatemala', 'Yemen', 'India', 'Vietnam']

# # 원두 특징 선택지
# features = ['Chocolatey', 'Fruity', 'Nutty', 'Floral', 'Spicy', 'Sweet', 'Winey', 'Citrus', 'Caramel', 'Buttery']

# # 원두 맛 프로파일 선택지
# flavor_profiles_choices = ['Chocolatey', 'Fruity', 'Nutty', 'Floral', 'Spicy', 'Sweet', 'Winey', 'Citrus', 'Caramel', 'Buttery', 'Sour', 'Earthy']

# unique_flavor_profiles = []
# unique_bean_names = []

# async def generate_beans(n):
#     # n 개의 랜덤한 Bean 문서를 생성하는 함수
#     for _ in range(n):
#         origin = fake.random_element(elements=origins)  # 실제 원두 원산지 반영
#         process = fake.random_element(elements=processes)  # 실제 원두 가공 방식 반영
#         feature = fake.random_element(elements=features)  # 실제 원두 특징 반영

#         # 원두 이름 생성
#         bean_name = f"{origin} {process} {feature}"
#         if bean_name in unique_bean_names:
#             continue
#         else:
#             unique_bean_names.append(bean_name)

#         # 원두 맛 프로파일 생성
#         flavor_profiles = ", ".join(fake.random_elements(elements=flavor_profiles_choices, length=3, unique=True))
#         if flavor_profiles in unique_flavor_profiles:
#             continue
#         else:
#             unique_flavor_profiles.append(flavor_profiles)

#         bean = {
#             "bean_id": fake.unique.random_number(digits=5),
#             "bean_name": bean_name,
#             "bean_img_url": fake.image_url(),
#             "process": fake.random_element(elements=processes),  # 실제 원두 가공 방식 반영
#             "origin": fake.random_element(elements=origins),  # 실제 원두 원산지 반영
#             "roast": fake.random_element(elements=roast_levels),  # 실제 원두 로스팅 레벨 반영
#             "acidity_level": randint(1, 5),  # 1~5 사이의 값
#             "bitterness_level": randint(1, 5),  # 1~5 사이의 값
#             "body_level": randint(1, 5),  # 1~5 사이의 값
#             "sweetness_level": randint(1, 5),  # 1~5 사이의 값
#             "flavor_profiles": flavor_profiles,
#             "description": fake.text(),
#             "created_at": datetime.now(),
#             "updated_at": datetime.now(),
#         }

#         # 생성된 데이터가 Bean 모델에 맞는지 검사
#         try:
#             bean_model = Bean(**bean)
#         except ValidationError as e:
#             print(f"Error: {e}")
#             continue

#         # DB에 Bean 문서 생성
#         await create_bean(bean_model)


# # 100개의 Bean 문서 생성
# loop = asyncio.get_event_loop()
# loop.run_until_complete(generate_beans(100))


#---------------------- 사용자 정보 랜덤 생성------------------------
# from faker import Faker
# from pydantic import ValidationError
# from models import User

# fake = Faker()  # Faker 인스턴스 생성

# async def create_user(user):
#     # User 컬렉션에 User 문서를 생성하는 함수
#     users = db.Users
#     await users.insert_one(user.dict())

# async def generate_users(n):
#     # n 개의 랜덤한 User 문서를 생성하는 함수
#     for _ in range(n):
#         user_id = fake.unique.random_number(digits=5)  # user_id 생성
#         user = {
#             "_id": user_id,  # MongoDB에서 요구하는 _id 필드
#             "user_id": user_id,
#             "username": fake.name(),
#             "email": fake.email(),  
#             "age": fake.random_int(min=18, max=90),
#             "gender": fake.random_element(elements=('M', 'F')),
#             "created_at": datetime.now(),
#             "updated_at": datetime.now(),
#         }

#         # 생성된 데이터가 User 모델에 맞는지 검사
#         try:
#             user_model = User(**user)
#         except ValidationError as e:
#             print(f"Error: {e}")
#             continue

#         # DB에 User 문서 생성
#         await create_user(user_model)

# # 100개의 User 문서 생성
# loop = asyncio.get_event_loop()
# loop.run_until_complete(generate_users(100))
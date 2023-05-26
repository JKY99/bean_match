from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv, find_dotenv
from datetime import datetime
from models import *
import os
import asyncio

load_dotenv(find_dotenv())

password = os.environ.get("MONGODB_PWD")

uri = f"mongodb+srv://admin:{1234}@recommend.wg2l4em.mongodb.net/?retryWrites=true&w=majority"

client = AsyncIOMotorClient(uri)


# 데이터베이스를 선택합니다.
db = client.BeanRecommendationsDB

async def find_all_beans():
    beans = db.Beans
    bean_list = await beans.find().to_list(length=1000)
    return bean_list

async def find_bean(bean_name):
    beans = db.Beans
    bean = await beans.find_one({'name': bean_name})
    return bean



#---------------------------원두 정보 랜덤 생성---------------------------
from faker import Faker
from pydantic import ValidationError
from random import randint

fake = Faker()  # Faker 인스턴스 생성

async def create_bean(bean):
    # Bean 컬렉션에 Bean 문서를 생성하는 함수
    beans = db.Beans
    await beans.insert_one(bean.dict())


# 원두 가공 방식 선택지
processes = ['Natural', 'Washed', 'Honey', 'Pulped Natural', 'Wet-hulled', 'Semi-washed']

# 원두 로스팅 레벨 선택지
roast_levels = ['Light', 'Medium', 'Medium-Dark', 'Dark']

# 원두 원산지 선택지
origins = ['Brazil', 'Colombia', 'Ethiopia', 'Kenya', 'Costa Rica', 'Guatemala', 'Yemen', 'India', 'Vietnam']

# 원두 특징 선택지
features = ['Chocolatey', 'Fruity', 'Nutty', 'Floral', 'Spicy', 'Sweet', 'Winey', 'Citrus', 'Caramel', 'Buttery']

# 원두 맛 프로파일 선택지
flavor_profiles_choices = ['Chocolatey', 'Fruity', 'Nutty', 'Floral', 'Spicy', 'Sweet', 'Winey', 'Citrus', 'Caramel', 'Buttery', 'Sour', 'Earthy']

unique_flavor_profiles = []
unique_bean_names = []

async def generate_beans(n):
    # n 개의 랜덤한 Bean 문서를 생성하는 함수
    for _ in range(n):
        origin = fake.random_element(elements=origins)  # 실제 원두 원산지 반영
        process = fake.random_element(elements=processes)  # 실제 원두 가공 방식 반영
        feature = fake.random_element(elements=features)  # 실제 원두 특징 반영

        # 원두 이름 생성
        bean_name = f"{origin} {process} {feature}"
        if bean_name in unique_bean_names:
            continue
        else:
            unique_bean_names.append(bean_name)

        # 원두 맛 프로파일 생성
        flavor_profiles = ", ".join(fake.random_elements(elements=flavor_profiles_choices, length=3, unique=True))
        if flavor_profiles in unique_flavor_profiles:
            continue
        else:
            unique_flavor_profiles.append(flavor_profiles)

        bean = {
            "_id": fake.unique.random_number(digits=5),
            "bean_name": bean_name,
            "bean_img_url": fake.image_url(),
            "process": fake.random_element(elements=processes),  # 실제 원두 가공 방식 반영
            "origin": fake.random_element(elements=origins),  # 실제 원두 원산지 반영
            "roast_level": fake.random_element(elements=roast_levels),  # 실제 원두 로스팅 레벨 반영
            "acidity_level": randint(0, 5),  # 0~5 사이의 값
            "bitterness_level": randint(0, 5),  # 0~5 사이의 값
            "body_level": randint(0, 5),  # 0~5 사이의 값
            "sweetness": randint(0, 5),  # 0~5 사이의 값
            "flavor_profiles": flavor_profiles,
            "description": fake.text(),
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }

        # 생성된 데이터가 Bean 모델에 맞는지 검사
        try:
            bean_model = Bean(**bean)
        except ValidationError as e:
            print(f"Error: {e}")
            continue

        # DB에 Bean 문서 생성
        await create_bean(bean_model)


# 100개의 Bean 문서 생성
loop = asyncio.get_event_loop()
loop.run_until_complete(generate_beans(100))


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
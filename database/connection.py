from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv, find_dotenv
# import os

load_dotenv(find_dotenv())

# password = os.environ.get("MONGODB_PWD")
uri = f"mongodb+srv://admin:{1234}@recommend.wg2l4em.mongodb.net/?retryWrites=true&w=majority"
client = AsyncIOMotorClient(uri)

# 데이터베이스를 선택합니다.
db = client.BeanRecommendationsDB
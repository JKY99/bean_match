from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv, find_dotenv
from datetime import datetime
from models import *
import os
from typing import List

# 환경 변수를 로드합니다.
load_dotenv(find_dotenv())

# 환경 변수에서 비밀번호를 얻습니다.
password = os.environ.get("MONGODB_PWD")

# MongoDB URI를 정의합니다.
uri = f"mongodb+srv://admin:{password}@recommend.wg2l4em.mongodb.net/?retryWrites=true&w=majority"

# MongoDB 클라이언트를 생성합니다.
client = AsyncIOMotorClient(uri)

# 데이터베이스를 선택합니다.
db = client.BeanRecommendationsDB

# 글로벌 컬렉션 변수를 정의합니다.
# 이 변수는 MongoDB 데이터베이스 내의 FavoredBeans 컬렉션을 나타냅니다.
FavoredBeans = db.FavoredBeans


# 새로운 찜한 원두를 생성하는 비동기 함수입니다.
# 이 함수는 먼저 데이터베이스에서 같은 ID를 가진 원두가 이미 있는지 확인합니다. 
# 만약 이미 존재한다면, HTTP 오류를 발생시킵니다.
# 그렇지 않다면, 원두 정보를 데이터베이스에 추가합니다.
async def post_create_favoredBean(favoredBean):
    if await FavoredBeans.find_one({"favored_bean_id": favoredBean.favoredBean_id}):
        raise HTTPException(status_code=400, detail="FavoredBean already registered")

    favoredBean.created_at = datetime.now()  # 생성 날짜 설정
    favoredBean.updated_at = datetime.now()  # 정보 수정 날짜 설정

    favoredBean_obj = favoredBean.dict()
    result = await FavoredBeans.insert_one(favoredBean_obj)
    return result

# 사용자 ID를 기준으로 찜한 원두를 검색하는 비동기 함수입니다.
# 이 함수는 데이터베이스에서 사용자 ID에 해당하는 모든 찜한 원두를 찾습니다.
# 찜한 원두가 없다면, HTTP 오류를 발생시킵니다.
async def get_favoredBeans_by_user(user_id: str):
    favored_beans = await FavoredBeans.find({"user_id": user_id}).to_list(length=100)
    if not favored_beans:
        raise HTTPException(status_code=404, detail="FavoredBeans not found")

    return favored_beans

# 찜한 원두 정보를 업데이트하는 비동기 함수입니다.
# 이 함수는 먼저 데이터베이스에서 해당 ID의 찜한 원두가 존재하는지 확인합니다.
# 찜한 원두가 없다면, HTTP 오류를 발생시킵니다.
# 찜한 원두가 있다면, 해당 원두 정보를 업데이트합니다.
async def put_update_favoredBean(favored_bean_id: str, favoredBean: FavoredBean):
    if not await FavoredBeans.find_one({"favored_bean_id": favored_bean_id}):
        raise HTTPException(status_code=400, detail="FavoredBean not found")

    favoredBean.updated_at = datetime.now()

    favoredBean_obj = favoredBean.dict()
    result = await FavoredBeans.update_one(
        {"favored_bean_id": favored_bean_id},
        {"$set": favoredBean_obj}
    )
    
    if result.acknowledged:
        return {"result": "FavoredBean updated"}
    else:
        raise HTTPException(status_code=500, detail="Unknown error occurred.")
    
# 찜한 원두를 삭제하는 비동기 함수입니다.
# 이 함수는 먼저 데이터베이스에서 해당 ID의 찜한 원두를 찾습니다.
# 찜한 원두가 없다면, HTTP 오류를 발생시킵니다.
# 찜한 원두가 있다면, 해당 원두를 데이터베이스에서 삭제합니다.
async def delete_favoredBean(favored_bean_id: str):
    favored_bean = await FavoredBeans.find_one({"favored_bean_id": favored_bean_id})
    if favored_bean is None:
        raise HTTPException(status_code=404, detail="FavoredBean not found")

    result = await FavoredBeans.delete_one({"favored_bean_id": favored_bean_id})

    return result

from typing import List, Tuple
from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from models import *
from database import *

app = FastAPI()

# app.mount("/", StaticFiles(directory="public", html = True), name="static")

@app.get("/")
def hello():
    return {"msg":"hello"}

# 모든 원두 정보를 조회합니다.  ex) /beans/all
@app.get("/beans/all", response_model=List[Bean])
async def get_all_beans():
    result = await find_all_beans()
    return result

# 모든 음료 정보를 조회합니다.  ex) /beverages/all
@app.get("/beverages/all", response_model=List[Bean])
async def get_all_beverages():
    result = await find_all_beverage()
    return result

# # from bson import json_util
# @app.get("/beans/all_", response_model={"beans":List[Bean]})
# async def get_all_beans_():
#     result = await find_all_beans()
#     return {"beans":result}

# 사용자 정보를 id로 조회합니다.   ex) /users?user_id=1234
@app.get("/user_id/id/{user_id}", response_model=User)
async def get_user_by_id(user_id: str):
    result = await find_user_by_id(user_id)
    return result

# 원두 정보를 name으로 조회합니다.   ex) /beans?bean_name=abcd
@app.get("/beans/name/{bean_name}", response_model=Bean)
async def get_bean_by_name(bean_name: str):
    result = await find_bean_by_name(bean_name)
    return result

# 원두 정보를 id로 조회합니다.   ex) /beans?bean_id=1234
@app.get("/beans/id/{bean_id}", response_model=Bean)
async def get_bean_by_id(bean_id: str):
    result = await find_bean_by_id(bean_id)
    return result

# 사용자 선호도 정보를 user_id로 조회합니다.   ex) /user_preference/?user_id=23234
@app.get("/user_preference/", response_model=UserPreference)
async def get_user_preference_by_user_id(user_id: str = Query(...)):
    result = await find_user_preference(user_id)
    return result

# 사용자 추천 원두를 user_id로 조회합니다.   ex) /match_beans/?user_id=23234
@app.get("/match_beans/", response_model=List[Bean])
async def get_match_beans_by_user_id(user_id: str = Query(...)):
    result = await match_beans(user_id)
    return result

# 이미지 파일 반환하기 ex) /data/img/abcd.jpg
@app.get("/data/img/{filename}")
async def get_image(filename: str):
    return FileResponse(path=f"data/img/{filename}", media_type="image/jpeg")

# 사용자 정보 생성하기 ex) /users/
@app.post("/users/")
async def create_user(user: User):
    if await post_create_user(user):
        result = {"msg":"o"}
    else:
        result = {"msg":"x"}
    return result

# 사용자 정보 생성하기 ex) /preferences/
@app.post("/preferences/")
async def create_preference(pref: UserPreference):
    if await post_create_preference(pref):
        result = {"msg":"o"}
    else:
        result = {"msg":"x"}
    return result
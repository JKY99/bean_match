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

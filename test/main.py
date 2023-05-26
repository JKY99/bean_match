# 필요한 모듈들을 import합니다.
from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
from models import *
from database import *

# FastAPI 인스턴스를 생성합니다.
app = FastAPI()

# 메인 페이지입니다. "Hello" 메시지를 반환합니다.
@app.get("/")
def hello():
    return {"msg": "Hello"}

# 모든 원두 정보를 조회하는 endpoint입니다. 예를 들어, "/beans/all"로 접근하면 모든 원두 정보를 반환합니다.
@app.get("/beans/all", response_model=List[Bean])
async def get_all_beans():
    # 모든 원두 정보를 데이터베이스에서 찾아 반환합니다.
    result = await find_all_beans()
    return result

# 특정 원두의 정보를 조회하는 endpoint입니다. 예를 들어, "/beans?bean_name=abcd"로 접근하면 "abcd"라는 이름의 원두 정보를 반환합니다.
@app.get("/beans/", response_model=Bean)
async def get_bean_by_name(bean_name: str = Query(...)):
    # 특정 원두 정보를 데이터베이스에서 찾아 반환합니다.
    result = await find_bean(bean_name)
    return result

# # 웹서버의 data/img 디렉토리에서 특정 이미지 파일을 반환하는 endpoint입니다. 예를 들어, "/data/img/abcd.jpg"로 접근하면 "abcd.jpg" 이미지를 반환합니다.
# @app.get("/data/img/{filename}")
# async def get_image(filename: str):
#     # 해당 파일을 응답으로 반환합니다.
#     return FileResponse(path=f"data/img/{filename}", media_type="image/jpeg")

from anyio import Path
from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
from models import *
from database import *

app = FastAPI()

@app.get("/")
def hello():
    return {"msg","hello"}

# 모든 원두 정보를 조회합니다.  ex) /beans/all
@app.get("/beans/all", response_model=List[Bean])
async def get_all_beans():
    result = await find_all_beans()
    return result

# 원두 정보를 조회합니다.   ex) /beans?bean_name=abcd
@app.get("/beans/", response_model=Bean)
async def get_bean_by_name(bean_name: str = Query(...)):
    result = await find_bean(bean_name)
    return result

# 이미지 파일 반환하기 ex) /data/img/abcd.jpg
@app.get("/data/img/{filename}")
async def get_image(filename: str = Path(...)):
    return FileResponse(path=f"data/img/{filename}", media_type="image/jpeg")
from typing import List, Tuple
from fastapi import FastAPI, Query, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from database.models import *
from database.database import *
from database.favoredBean import *

app = FastAPI()

# app.mount("/", StaticFiles(directory="public", html = True), name="static")

# -------------------------- User ------------------------------
@app.post("/users", response_model=User)
async def create_user(user: User) -> User:
    return await UserService.create(user)

@app.get("/users/{user_id}", response_model=User)
async def read_user(user_id: str) -> User:
    user = await UserService.read(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/users", response_model=List[User])
async def read_all_users() -> List[User]:
    return await UserService.read_all()

@app.put("/users/{user_id}", response_model=User)
async def update_user(user_id: str, user: User) -> User:
    return await UserService.update(user_id, user)

@app.delete("/users/{user_id}")
async def delete_user(user_id: str):
    await UserService.delete(user_id)
    return {"detail": "User deleted"}
# -------------------------- User ------------------------------
# -------------------------- UserPreference ------------------------------
@app.post("/preference/", response_model=UserPreference)
async def create_preference(preference: UserPreference):
    return await UserPreferenceService.create(preference)

@app.get("/preference/{preference_id}", response_model=UserPreference)
async def read_preference_by_id(preference_id: str):
    preference = await UserPreferenceService.read_by_preference_id(preference_id)
    if preference is None:
        raise HTTPException(status_code=404, detail="Preference not found")
    return preference

@app.get("/preference/user/{user_id}", response_model=List[UserPreference])
async def read_preference_by_user(user_id: str):
    preferences = await UserPreferenceService.read_by_user_id(user_id)
    if preferences is None:
        raise HTTPException(status_code=404, detail="Preferences not found")
    return preferences

@app.put("/preference/{preference_id}", response_model=UserPreference)
async def update_preference_by_id(preference_id: str, preference: UserPreference):
    updated_preference = await UserPreferenceService.update_by_preference_id(preference_id, preference)
    if updated_preference is None:
        raise HTTPException(status_code=404, detail="Preference not found")
    return updated_preference

@app.put("/preference/user/{user_id}", response_model=List[UserPreference])
async def update_preference_by_user(user_id: str, preference: UserPreference):
    updated_preferences = await UserPreferenceService.update_by_user_id(user_id, preference)
    if updated_preferences is None:
        raise HTTPException(status_code=404, detail="Preferences not found")
    return updated_preferences

@app.delete("/preference/{preference_id}")
async def delete_preference_by_id(preference_id: str):
    deleted = await UserPreferenceService.delete_by_preference_id(preference_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Preference not found")
    return {"message": "Preference has been deleted"}

@app.delete("/preference/user/{user_id}")
async def delete_preference_by_user(user_id: str):
    deleted = await UserPreferenceService.delete_by_user_id(user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Preferences not found")
    return {"message": "Preferences have been deleted"}
# -------------------------- UserPreference ------------------------------
# -------------------------- UserPreference ------------------------------
# -------------------------- UserPreference ------------------------------



# 이미지 파일 반환하기 ex) /data/img/abcd.jpg
@app.get("/data/img/{filename}")
async def get_image(filename: str):
    return FileResponse(path=f"data/img/{filename}", media_type="image/jpeg")

# # 모든 원두 정보를 조회합니다.  ex) /beans/all
# @app.get("/beans/all", response_model=List[Bean])
# async def get_all_beans():
#     result = await find_all_beans()
#     return result

# # 모든 음료 정보를 조회합니다.  ex) /beverages/all
# @app.get("/beverages/all", response_model=List[Beverage])
# async def get_all_beverages():
#     result = await find_all_beverage()
#     return result

# # 모든 블렌딩 레시피 정보를 조회합니다.  ex) /blending_recipes/all
# @app.get("/blending_recipes/all", response_model=List[BlendingRecipe])
# async def get_all_blending_recipes():
#     result = await find_all_blending_recipe()
#     return result

# # 사용자 정보를 id로 조회합니다.   ex) /users?user_id=1234
# @app.get("/user_id/id/{user_id}", response_model=User)
# async def get_user_by_id(user_id: str):
#     result = await find_user_by_id(user_id)
#     return result

# # 원두 정보를 name으로 조회합니다.   ex) /beans?bean_name=abcd
# @app.get("/beans/name/{bean_name}", response_model=Bean)
# async def get_bean_by_name(bean_name: str):
#     result = await find_bean_by_name(bean_name)
#     return result

# # 원두 정보를 id로 조회합니다.   ex) /beans?bean_id=1234
# @app.get("/beans/id/{bean_id}", response_model=Bean)
# async def get_bean_by_id(bean_id: str):
#     result = await find_bean_by_id(bean_id)
#     return result

# # 사용자 선호도 정보를 user_id로 조회합니다.   ex) /user_preference/?user_id=23234
# @app.get("/user_preference/", response_model=UserPreference)
# async def get_user_preference_by_user_id(user_id: str = Query(...)):
#     result = await find_user_preference(user_id)
#     return result

# # 사용자 추천 원두를 user_id로 조회합니다.   ex) /match_beans/?user_id=23234
# @app.get("/match_beans/", response_model=List[Bean])
# async def get_match_beans_by_user_id(user_id: str = Query(...)):
#     result = await match_beans(user_id)
#     return result


# # 사용자 정보 생성하기 ex) /users/
# @app.post("/users/")
# async def create_user(user: User):
#     if await post_create_user(user):
#         result = {"msg":"o"}
#     else:
#         result = {"msg":"x"}
#     return result

# # 사용자 정보 생성하기 ex) /preferences/
# @app.post("/preferences/")
# async def create_preference(pref: UserPreference):
#     if await post_create_preference(pref):
#         result = {"msg":"o"}
#     else:
#         result = {"msg":"x"}
#     return result

# # 찜 정보 생성하기 ex) /preferences/
# @app.post("/preferences/")
# async def create_preference(pref: UserPreference):
#     if await post_create_preference(pref):
#         result = {"msg":"o"}
#     else:
#         result = {"msg":"x"}
#     return result

# # 찜 정보 수정하기 ex) /preferences/
# @app.post("/preferences/")
# async def create_preference(pref: UserPreference):
#     if await post_create_preference(pref):
#         result = {"msg":"o"}
#     else:
#         result = {"msg":"x"}
#     return result

# # 찜 정보 삭제하기 ex) /preferences/
# @app.post("/preferences/")
# async def create_preference(pref: UserPreference):
#     if await post_create_preference(pref):
#         result = {"msg":"o"}
#     else:
#         result = {"msg":"x"}
#     return result

# #----------------------------------------찜 원두 시작----------------------------------------------------#
# # 찜한 원두 정보 생성 API (POST 방식)
# @app.post("/favoredBeans")
# async def create_favoredBean(favoredBean: FavoredBean):
#     try:
#         result = await post_create_favoredBean(favoredBean)
#         return {"msg": "o"}
#     except:
#         raise HTTPException(status_code=400, detail="Failed to create favoredBean.")

# # 사용자 ID를 기준으로 찜한 원두 검색 API (GET 방식)
# @app.get("/favoredBeans/{user_id}")
# async def read_favoredBeans_by_user(user_id: str):
#     try:
#         favored_beans = await get_favoredBeans_by_user(user_id)
#         return favored_beans
#     except:
#         raise HTTPException(status_code=404, detail="Failed to get favoredBeans by user id.")

# # 찜한 원두 정보 수정 API (PUT 방식)
# @app.put("/favoredBeans/{favored_bean_id}")
# async def update_favoredBean(favored_bean_id: str, favoredBean: FavoredBean):
#     try:
#         result = await put_update_favoredBean(favored_bean_id, favoredBean)
#         return {"msg": "o"}
#     except:
#         raise HTTPException(status_code=400, detail="Failed to update favoredBean.")

# # 찜한 원두 정보 삭제 API (DELETE 방식)
# @app.delete("/favoredBeans/{favored_bean_id}")
# async def remove_favoredBean(favored_bean_id: str):
#     try:
#         result = await delete_favoredBean(favored_bean_id)
#         return {"msg": "o"}
#     except:
#         raise HTTPException(status_code=404, detail="Failed to delete favoredBean.")
# #----------------------------------------찜 원두 끝----------------------------------------------------#
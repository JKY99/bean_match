from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

# 사용자 정보를 위한 클래스
class User(BaseModel):
    user_id: str   # 사용자 ID (Primary Key)
    username: str  # 사용자 이름
    email: str  # 사용자 이메일
    age: int  # 사용자 나이
    gender: str  # 사용자 성별
    created_at: datetime  # 계정 생성 날짜
    updated_at: datetime  # 계정 정보 수정 날짜

# 사용자 선호도 정보를 위한 클래스
class UserPreference(BaseModel):
    preference_id: str   # 선호도 ID (Primary Key)
    user_id: str  # 사용자 ID
    preferred_beverage_ids: List[str]  # 선호 음료 ID
    preferred_beans_ids: List[str]  # 선호 원두 ID
    preferred_process: str  # 선호 가공 방식
    preferred_origin: str  # 선호 원산지
    preferred_roast: str  # 선호 로스팅 정도
    preferred_acidity_level: int  # 선호 산도 정도
    preferred_bitterness_level: int  # 선호 쓴맛 정도
    preferred_body_level: int  # 선호 바디 정도
    preferred_sweetness_level: int  # 선호 단맛 정도
    preferred_flavor_profiles: str  # 선호 맛 프로파일
    created_at: datetime  # 선호도 정보 생성 날짜
    updated_at: datetime  # 선호도 정보 수정 날짜

# 구매 이력을 위한 클래스
class PurchaseHistory(BaseModel):
    purchase_id: str   # 구매 이력 ID (Primary Key)
    user_id: str  # 사용자 ID
    bean_id: str  # 원두 ID
    purchase_date: datetime  # 구매 날짜
    purchase_quantity: int  # 구매 수량
    purchase_price: float  # 구매 가격

# 원두 정보를 위한 클래스
class Bean(BaseModel):
    bean_id: str   # 원두 ID (Primary Key)
    bean_name: str  # 원두 이름
    bean_img_url: str  # 원두 이미지 URL
    process: str  # 가공 방식
    origin: str  # 원산지
    roast: str  # 로스팅 정도
    acidity_level: int  # 산도 정도
    bitterness_level: int  # 쓴맛 정도
    body_level: int  # 바디 정도
    sweetness_level: int  # 단맛 정도
    flavor_profiles: str  # 맛 프로파일
    description: str  # 원두 설명
    created_at: datetime  # 원두 정보 생성 날짜
    updated_at: datetime  # 원두 정보 수정 날짜

# 블렌딩 레시피를 위한 클래스
class BlendingRecipe(BaseModel):
    blend_id: str   # 블렌딩 레시피 ID (Primary Key)
    blend_name: str  # 블렌딩 레시피 이름
    blend_list: List[dict]  # 블렌딩 레시피에 사용된 원두들의 ID리스트와 비율 
    description: str  # 블렌딩 레시피 설명 
    created_at: datetime  # 블렌딩 레시피 정보 등록 날짜
    updated_at: datetime  # 블렌딩 레시피 정보 수정 날짜

# 음료 정보를 위한 클래스
class Beverage(BaseModel):
    beverage_id: str   # 음료 ID (Primary Key)
    beverage_name: str  # 음료 이름
    description: str  # 음료 설명
    created_at: datetime  # 음료 정보 등록 날짜
    updated_at: datetime  # 음료 정보 수정 날짜

# 찜한 원두를 위한 클래스
class FavoredBean(BaseModel):
    favored_bean_id: str   # 원두 찜 ID (Primary Key)
    user_id: str  # 사용자 ID
    bean_id: str  # 원두 ID
    created_at: datetime  # 원두 찜 정보 등록 날짜
    updated_at: datetime  # 원두 찜 정보 수정 날짜

# 찜한 블렌딩 레시피를 위한 클래스
class FavoredBlendingRecipes(BaseModel):
    favored_blend_id: str   # 블렌딩 레시피 찜 ID (Primary Key)
    user_id: str  # 사용자 ID
    blend_id: str  # 블렌딩 레시피 ID
    created_at: datetime  # 블렌딩 레시피 찜 정보 등록 날짜
    updated_at: datetime  # 블렌딩 레시피 찜 정보 수정 날짜

# 뉴스 페이지를 위한 클래스
class News(BaseModel):
    news_id: str   # 뉴스 ID (Primary Key)
    news_title: str  # 뉴스 제목
    news_content: str  # 뉴스 내용
    news_url: str  # 뉴스 URL
    created_at: datetime  # 뉴스 등록 날짜
    updated_at: datetime  # 뉴스 정보 수정 날짜

# 찜한 뉴스 페이지를 위한 클래스
class FavoredNews(BaseModel):
    favored_news_id: str   # 찜한 뉴스 ID (Primary Key)
    user_id: str  # 사용자 ID
    news_id: str  # 뉴스 ID
    created_at: datetime  # 뉴스 찜 정보 등록 날짜
    updated_at: datetime  # 뉴스 찜 정보 수정 날짜

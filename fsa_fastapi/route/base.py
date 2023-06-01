from fastapi import APIRouter

from route import route_users, route_login, route_product, route_ingredient, route_diet

api_router = APIRouter()
api_router.include_router(route_users.router, prefix="/users", tags=["users"])
api_router.include_router(route_login.router, prefix="/login", tags=["login"])
api_router.include_router(route_product.router, prefix="/product", tags=["product"])
api_router.include_router(route_ingredient.router, prefix="/ingredient", tags=["ingredient"])
api_router.include_router(route_diet.router, prefix="/diet", tags=["diet"])

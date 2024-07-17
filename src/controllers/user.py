from fastapi import APIRouter

from src.models.decorated_response import APIResponse
from src.service import user
user_route = APIRouter(tags=["users"])


@user_route.get("/all-users")
def get_users():
    """Get all 
    """
    return


@user_route.get("/load-users", tags=["User"],
                summary="trigger user",
                response_model=APIResponse,
                responses={200: {}, 404: {}})
def trigger_user_loading_script():
    """Trigger user script for loading data from CSV file to DB"""
    user.data_loader()
    return

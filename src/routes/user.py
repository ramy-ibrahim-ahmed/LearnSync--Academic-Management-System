from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import UserModel, CourseModel
from ..schemas.user import User, UserCreate
from ..schemas.course import Course
from ..helpers.database import get_db

router = APIRouter()


@router.get("/users", response_model=List[User], status_code=status.HTTP_200_OK)
async def get_users(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    user_model = UserModel(db_client=db)
    users = await user_model.read_users(skip=skip, limit=limit)
    return users


@router.post("/users", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_or_get_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    user_model = UserModel(db_client=db)
    db_user = await user_model.read_user_by_email(email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User {user.email} already exists!",
        )
    return await user_model.create_user(user=user)


@router.get("/users/{user_id}", response_model=User, status_code=status.HTTP_200_OK)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user_model = UserModel(db_client=db)
    user = await user_model.read_user_by_id(user_id=user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found!",
        )
    return user


@router.get("/users/{user_id}/courses", response_model=List[Course])
async def get_user_courses(user_id: int, db: AsyncSession = Depends(get_db)):
    course_model = CourseModel(db_client=db)
    courses = await course_model.read_user_courses(user_id=user_id)
    return courses

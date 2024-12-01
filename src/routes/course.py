from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..schemas.course import Course, CourseCreate
from ..models import CourseModel
from ..helpers.database import get_db

router = APIRouter()


@router.get("/courses", response_model=List[Course])
async def get_courses(db: AsyncSession = Depends(get_db)):
    course_model = CourseModel(db_client=db)
    courses = await course_model.read_courses()
    return courses


@router.post("/courses", response_model=Course)
async def create_new_course(course: CourseCreate, db: AsyncSession = Depends(get_db)):
    course_model = CourseModel(db_client=db)
    return await course_model.create_course(course=course)


@router.get("/courses/{course_id}")
async def get_course(course_id: int, db: AsyncSession = Depends(get_db)):
    course_model = CourseModel(db_client=db)
    course = await course_model.read_course_by_id(course_id=course_id)
    if course is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Course with ID {course_id} is not found!",
        )
    return course

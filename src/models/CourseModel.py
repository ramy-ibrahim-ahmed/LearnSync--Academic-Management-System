from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from .db_schemas.course import Course
from ..schemas.course import CourseCreate


class CourseModel:
    def __init__(self, db_client: AsyncSession):
        self.db_client = db_client

    async def read_course_by_id(self, course_id: int):
        result = await self.db_client.execute(
            select(Course).filter(Course.id == course_id)
        )
        return result.scalar_one_or_none()

    async def read_courses(self):
        result = await self.db_client.execute(select(Course))
        return result.scalars().all()

    async def read_user_courses(self, user_id: int):
        result = await self.db_client.execute(
            select(Course).filter(Course.user_id == user_id)
        )
        return result.scalars().all()

    async def create_course(self, course: CourseCreate):
        db_course = Course(
            title=course.title,
            description=course.description,
            user_id=course.user_id,
        )
        self.db_client.add(db_course)
        await self.db_client.commit()
        await self.db_client.refresh(db_course)
        return db_course

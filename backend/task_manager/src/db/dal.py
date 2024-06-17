from datetime import datetime
from src.db.models import Task, TaskUser, User
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.api.utils import Paginator


class TaskDAL:
    def __init__(self, session: AsyncSession, user_id: int):
        self.session = session
        self.user_id = user_id

    async def get_all_tasks(self, is_completed: bool
                            , paginator_params: Paginator):
        query = (
            select(Task)
            .join(TaskUser)
            .where(TaskUser.user_id == self.user_id)
            .offset((paginator_params.page - 1) * paginator_params.n)
            .limit(paginator_params.n)
        )

        if is_completed is not None:
            query = query.filter(Task.is_completed == is_completed)

        result = await self.session.execute(query)
        tasks = result.scalars().all()
        return {'success': True, 'data': tasks}

    async def get_count_by_completed(self, completed: bool):
        query = (
            select(Task)
            .join(TaskUser)
            .where(TaskUser.user_id == self.user_id)
        )
        if completed is not None:
            query = query.filter(Task.is_completed == completed)

        result = await self.session.execute(query)
        tasks = result.scalars().all()
        return {'success': True, 'count': len(tasks)}

    async def add_task_for_user(self, title: str, target_date: datetime):
        if target_date.tzinfo is not None:
            target_date = target_date.replace(tzinfo=None)

        task = Task(title=title, target_date=target_date)
        self.session.add(task)
        await self.session.flush()
        query = select(User).filter(User.id == self.user_id)
        result = await self.session.execute(query)
        user = result.scalars().first()
        if not user:
            return {'success': False}
        task_user = TaskUser(task_id=task.id, user_id=self.user_id)
        self.session.add(task_user)
        await self.session.flush()
        await self.session.commit()
        return {'success': True}

    async def update_task_for_user(self, **kwargs):
        if 'target_date' in kwargs:
            if kwargs['target_date'] is not None:
                kwargs['target_date'] = kwargs['target_date'].replace(tzinfo=None)

        result = await self.session.execute(select(User).filter_by(id=self.user_id))
        user = result.scalars().first()

        if not user:
            return {'success': False}

        result = await self.session.execute(select(Task).filter_by(id=kwargs['task_id']))
        task = result.scalars().first()

        if not task:
            return {'success': False}

        for key, value in kwargs.items():
            if hasattr(task, key) & (value is not None):
                setattr(task, key, value)

        await self.session.commit()
        return {'success': True}

    async def delete_task_for_user(self, task_id: int):
        result = await self.session.execute(
            select(TaskUser).filter_by(user_id=self.user_id, task_id=task_id)
        )
        task_user = result.scalars().first()

        if not task_user:
            return {'success': False}

        await self.session.delete(task_user)

        task = await self.session.get(Task, task_id)
        if task:
            await self.session.delete(task)

        await self.session.commit()
        return {'success': True}

    async def get_task_by_id(self, task_id: int, user_id: int):
        result = await self.session.execute(
            select(TaskUser).filter_by(user_id=user_id, task_id=task_id)
        )
        task = result.scalars().first()
        task_info = await self.session.execute(select(Task).filter_by(id=task.task_id))
        task = task_info.scalars().first()
        return {'success': True, 'data': task}

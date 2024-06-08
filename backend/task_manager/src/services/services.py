from datetime import datetime
from src.db.database import async_session_maker
from src.api.utils import Paginator
from src.db.dal import TaskDAL


class TaskService:
    def __init__(self, user_id: int):
        self.user_id = user_id

    async def get_all_tasks(self, is_completed: bool, paginator_params: Paginator):
        async with async_session_maker() as session:
            try:
                return await TaskDAL(session, self.user_id).get_all_tasks(is_completed, paginator_params)
            except Exception as e:
                print(e)
                return {'success': False, 'data': None}

    async def get_tasks_by_completed(self, completed: bool, paginator_params: Paginator):
        async with async_session_maker() as session:
            try:
                return await TaskDAL(session, self.user_id).get_tasks_by_completed(completed, paginator_params)
            except Exception as e:
                print(e)
                return {'success': False, 'data': None}

    async def add_task_for_user(self, title: str, target_date: datetime):
        async with async_session_maker() as session:
            try:
                return await TaskDAL(session, self.user_id).add_task_for_user(title, target_date)
            except Exception as e:
                print(e)
                return {'success': False, 'data': None}

    async def update_task_for_user(self, **kwargs):
        async with async_session_maker() as session:
            try:
                print(kwargs)
                return await TaskDAL(session, self.user_id).update_task_for_user(**kwargs)
            except Exception as e:
                print(e)
                return {'success': False, 'data': None}

    async def delete_task_for_user(self, task_id: int):
        async with async_session_maker() as session:
            try:
                return await TaskDAL(session, self.user_id).delete_task_for_user(task_id)
            except Exception as e:
                print(e)
                return {'success': False, 'data': None}

    async def get_count_by_completed(self, completed: bool):
        async with async_session_maker() as session:
            try:
                return await TaskDAL(session, self.user_id).get_count_by_completed(completed)
            except Exception as e:
                print(e)
                return {'success': False, 'count': None}

    async def get_task_by_id(self, task_id: int):
        try:
            async with async_session_maker() as session:
                return await TaskDAL(session, self.user_id).get_task_by_id(task_id, self.user_id)
        except Exception as e:
            print(e)
            return {'success': False, 'data': None}

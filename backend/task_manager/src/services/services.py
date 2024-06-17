from datetime import datetime
from src.db.database import async_session_maker
from src.api.utils import Paginator
from src.db.dal import TaskDAL


class TaskService:
    def __init__(self, user_id: int, session):
        self.user_id = user_id
        self.session = session

    async def get_all_tasks(self, is_completed: bool, paginator_params: Paginator):
        try:
            return await TaskDAL(self.session, self.user_id).get_all_tasks(is_completed, paginator_params)
        except Exception as e:
            print(e)
            return {'success': False, 'data': None}

    async def add_task_for_user(self, title: str, target_date: datetime):
        try:
            return await TaskDAL(self.session, self.user_id).add_task_for_user(title, target_date)
        except Exception as e:
            print(e)
            return {'success': False}

    async def update_task_for_user(self, **kwargs):
        try:
            return await TaskDAL(self.session, self.user_id).update_task_for_user(**kwargs)
        except Exception as e:
            print(e)
            return {'success': False}

    async def delete_task_for_user(self, task_id: int):
        try:
            return await TaskDAL(self.session, self.user_id).delete_task_for_user(task_id)
        except Exception as e:
            print(e)
            return {'success': False}

    async def get_count_by_completed(self, completed: bool):
        try:
            return await TaskDAL(self.session, self.user_id).get_count_by_completed(completed)
        except Exception as e:
            print(e)
            return {'success': False, 'count': None}

    async def get_task_by_id(self, task_id: int):
        try:
            return await TaskDAL(self.session, self.user_id).get_task_by_id(task_id, self.user_id)
        except Exception as e:
            print(e)
            return {'success': False, 'data': None}

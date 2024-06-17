import pytest
from src.api.utils import Paginator
from datetime import datetime

paginator = Paginator()


async def test_add_task(task_service):
    response = await task_service.add_task_for_user("test", datetime.now())
    assert response["success"] is True


async def test_all_task(task_service):
    response = await task_service.get_all_tasks(None, paginator)
    assert len(response) >= 0


async def test_task_count(task_service):
    response = await task_service.get_count_by_completed(False)
    assert response["count"] >= 0


async def test_update_is_completed_task(task_service):
    response = await task_service.update_task_for_user(is_completed=True, task_id=1)
    assert response["success"] is True


async def test_update_target_date_task(task_service):
    response = await task_service.update_task_for_user(
        target_date=datetime.now(), task_id=1
    )
    assert response["success"] is True


async def test_update_title_task(task_service):
    response = await task_service.update_task_for_user(title="test2", task_id=1)
    assert response["success"] is True


async def test_update_task_not_valid_task_id(task_service):
    response = await task_service.update_task_for_user(is_completed=False, task_id=2)
    assert response["success"] is False


async def test_update_not_valid_is_completed(task_service):
    response = await task_service.update_task_for_user(is_completed=None, task_id=1)
    assert response["success"] is True


async def test_update_not_valid_target_date(task_service):
    response = await task_service.update_task_for_user(target_date=None, task_id=1)
    assert response["success"] is True


async def test_update_not_valid_title(task_service):
    response = await task_service.update_task_for_user(title=None, task_id=1)
    assert response["success"] is True


async def test_delete_task(task_service):
    response = await task_service.delete_task_for_user(task_id=1)
    assert response["success"] is True


async def test_delete_task_not_valid_task_id(task_service):
    response = await task_service.delete_task_for_user(task_id=2)
    assert response["success"] is False

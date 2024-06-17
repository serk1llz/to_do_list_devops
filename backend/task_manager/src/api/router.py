from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi_users import FastAPIUsers
from src.api.auth import auth_backend
from src.api.schemas import Task, TaskDelete, TaskPatch, TaskPOST
from src.api.user_manager import get_user_manager
from src.api.utils import Paginator
from src.db.database import async_session_maker
from src.db.models import User
from src.services.services import TaskService

router = APIRouter(prefix="/task", tags=["task"])

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user()


@router.get("/count")
async def count_completed(
    is_completed: bool = None, user: User = Depends(current_user)
):
    try:
        async with async_session_maker() as session:
            result = await TaskService(user.id, session).get_count_by_completed(
                is_completed
            )
            if result["success"]:
                return {"count": result["count"]}
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST, content="Not valid data"
            )
    except Exception as e:
        print(e)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content="Internal Server Error",
        )


@router.delete("/delete/{task_id}")
async def delete_task_for_user(task_id: int, user: User = Depends(current_user)):
    try:
        async with async_session_maker() as session:
            result = await TaskService(user.id, session).delete_task_for_user(task_id)
            if result["success"]:
                return JSONResponse(status_code=status.HTTP_200_OK, content="Success")
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST, content="Not valid data"
            )
    except Exception as e:
        print(e)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content="Internal Server Error",
        )


@router.get("/{task_id}")
async def get_task_by_id(task_id: int, user: User = Depends(current_user)):
    try:
        async with async_session_maker() as session:
            result = await TaskService(user.id, session).get_task_by_id(task_id)
            if (result["success"]) & (result["data"] is not None):
                return Task.model_validate(result["data"], from_attributes=True)
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST, content="Not valid data"
            )
    except Exception as e:
        print(e)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content="Internal Server Error",
        )


@router.get("/")
async def get_all_tasks(
    is_completed: bool = None,
    user: User = Depends(current_user),
    paginator: Paginator = Depends(),
):
    try:
        async with async_session_maker() as session:
            result = await TaskService(user.id, session).get_all_tasks(
                is_completed, paginator
            )
            if (result["success"]) & (result["data"] is not None):
                output_tasks = [
                    Task.model_validate(task, from_attributes=True)
                    for task in result["data"]
                ]
                return output_tasks
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST, content="Not valid data"
            )
    except Exception as e:
        print(e)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content="Internal Server Error",
        )


@router.post("/add")
async def add_task_for_user(params: TaskPOST, user: User = Depends(current_user)):
    try:
        async with async_session_maker() as session:
            result = await TaskService(user.id, session).add_task_for_user(
                params.title, params.target_date
            )
            if result["success"] is True:
                return JSONResponse(status_code=status.HTTP_200_OK, content="Success")
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST, content="Not valid data"
            )
    except Exception as e:
        print(e)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content="Internal Server Error",
        )


@router.patch("/update")
async def update_task_for_user(params: TaskPatch, user: User = Depends(current_user)):
    try:
        async with async_session_maker() as session:
            result = await TaskService(user.id, session).update_task_for_user(
                **params.dict()
            )
            if result["success"]:
                return JSONResponse(status_code=status.HTTP_200_OK, content="Success")
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST, content="Not valid data"
            )
    except Exception as e:
        print(e)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content="Internal Server Error",
        )

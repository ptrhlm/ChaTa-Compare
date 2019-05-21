from fastapi import APIRouter

from app.api.api_v1.endpoints import (chart, report, survey, survey_tasks,
                                      token, user, utils)

api_router = APIRouter()
api_router.include_router(token.router)
api_router.include_router(user.router)
api_router.include_router(utils.router)
api_router.include_router(chart.router)
api_router.include_router(survey.router)
api_router.include_router(survey_tasks.router)
api_router.include_router(report.router)

# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base  # noqa
from app.db_models.user import User  # noqa
from app.db_models.answer import Answer
from app.db_models.chart import Chart
from app.db_models.criterion import Criterion
from app.db_models.report import Report
from app.db_models.survey import Survey
from app.db_models.task import Task

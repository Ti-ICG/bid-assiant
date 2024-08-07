from sqlalchemy.ext.declarative import declarative_base

import thcloud.db as db
import thcloud.models as models
from thcloud.models import Article

models.BaseModel.metadata.create_all(bind=db.engine)

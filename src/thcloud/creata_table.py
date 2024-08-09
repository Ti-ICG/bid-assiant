from sqlalchemy.ext.declarative import declarative_base

import thcloud.db as db
import thcloud.models as models

models.BaseModel.metadata.create_all(bind=db.engine)

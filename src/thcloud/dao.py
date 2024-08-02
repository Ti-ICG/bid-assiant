from typing import Generic, List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from thcloud.models import (
    Bid_catalog,
    Bid_catalog_content,
    Requirement_analysis,
    Requirement_analysis_detail,
    Response_indicator,
    Response_indicator_detail,
    Scheme,
    System_framework,
    System_framework_detail,
)
from thcloud.schemas import (
    CreateBidCatalog,
    CreateBidCatalogContent,
    CreateRequirementAnalysis,
    CreateRequirementAnalysisDetail,
    CreateResponseIndicator,
    CreateResponseIndicatorDetail,
    CreateSchema,
    CreateScheme,
    CreateSystemFramework,
    ModelType,
    UpdateBidCatalog,
    UpdateBidCatalogContent,
    UpdateRequirementAnalysis,
    UpdateRequirementAnalysisDetail,
    UpdateResponseIndicator,
    UpdateResponseIndicatorDetail,
    UpdateSchema,
    UpdateScheme,
    UpdateSystemFramework,
)


class BaseDAO(Generic[ModelType, CreateSchema, UpdateSchema]):
    model: ModelType

    def get(self, session: Session, offset=0, limit=10) -> List[ModelType]:
        result = session.query(self.model).offset(offset).limit(limit).all()
        return result

    def get_by_id(
        self,
        session: Session,
        pk: int,
    ) -> ModelType:
        return session.query(self.model).get(pk)

    def create(self, session: Session, obj_in: CreateSchema) -> ModelType:
        """Create"""
        obj = self.model(**jsonable_encoder(obj_in))
        session.add(obj)
        session.commit()
        return obj

    def patch(self, session: Session, pk: int, obj_in: UpdateSchema) -> ModelType:
        """Patch"""
        obj = self.get_by_id(session, pk)
        update_data = obj_in.dict(exclude_unset=True)
        for key, val in update_data.items():
            setattr(obj, key, val)
        session.add(obj)
        session.commit()
        session.refresh(obj)
        return obj

    def delete(self, session: Session, pk: int) -> None:
        """Delete"""
        obj = self.get_by_id(session, pk)
        session.delete(obj)
        session.commit()

    def count(self, session: Session):
        return session.query(self.model).count()


class SchemeDAO(BaseDAO[Scheme, CreateScheme, UpdateScheme]):
    model = Scheme


class RequirementAnalysisDAO(
    BaseDAO[Requirement_analysis, CreateRequirementAnalysis, UpdateRequirementAnalysis]
):
    model = Requirement_analysis


class RequirementAnalysisDetailDAO(
    BaseDAO[
        Requirement_analysis_detail,
        CreateRequirementAnalysisDetail,
        UpdateRequirementAnalysisDetail,
    ]
):
    model = Requirement_analysis_detail


class SystemFrameworkDAO(
    BaseDAO[System_framework, CreateSystemFramework, UpdateSystemFramework]
):
    model = System_framework


class SystemFrameworkDAO(
    BaseDAO[System_framework, CreateSystemFramework, UpdateSystemFramework]
):
    model = System_framework


# class SystemFrameworkDetailDAO(BaseDAO[System_framework_detail,CreateSystemFrameworkDetail,UpdateSystemFrameworkDetail]):
#     model = System_framework_detail


class ResponseIndicatorDAO(
    BaseDAO[Response_indicator, CreateResponseIndicator, UpdateResponseIndicator]
):
    model = Response_indicator


class ResponseIndicatorDetailDAO(
    BaseDAO[
        Response_indicator_detail,
        CreateResponseIndicatorDetail,
        UpdateResponseIndicatorDetail,
    ]
):
    model = Response_indicator_detail


class BidCatalogDAO(BaseDAO[Bid_catalog, CreateBidCatalog, UpdateBidCatalog]):
    model = Bid_catalog


class BidCatalogContentDAO(
    BaseDAO[Bid_catalog_content, CreateBidCatalogContent, UpdateBidCatalogContent]
):
    model = Bid_catalog_content

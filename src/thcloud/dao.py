from typing import Generic, List
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy import text
from thcloud.models import (
    Bid_catalog,
    Bid_catalog_content,
    Catalog_prompt,
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
    CreateCatalogPrompt,
    CreateRequirementAnalysis,
    CreateRequirementAnalysisDetail,
    CreateResponseIndicator,
    CreateResponseIndicatorDetail,
    CreateSchema,
    CreateScheme,
    CreateSystemFramework,
    CreateSystemFrameworkDetail,
    ModelType,
    UpdateBidCatalog,
    UpdateBidCatalogContent,
    UpdateCatalogPrompt,
    UpdateRequirementAnalysis,
    UpdateRequirementAnalysisDetail,
    UpdateResponseIndicator,
    UpdateResponseIndicatorDetail,
    UpdateSchema,
    UpdateScheme,
    UpdateSystemFramework,
    UpdateSystemFrameworkDetail,
)


class BaseDAO(Generic[ModelType, CreateSchema, UpdateSchema]):
    model: ModelType

    def get(self, session: Session, offset=0, limit=10) -> List[ModelType]:
        result = session.query(self.model).offset(offset).limit(limit).all()
        return result

    def get_all_by_id(
        self,
        session: Session,
        pk: int,
    ) -> List[ModelType]:
        return session.query(self.model).filter(self.model.scheme_id == pk).all()

    def get_by_scheme_id(
        self,
        session: Session,
        pk: int,
    ) -> List[ModelType]:
        return session.query(self.model).filter(self.model.scheme_id == pk).first()

    def get_by_id(
        self,
        session: Session,
        pk: int,
    ) -> ModelType:
        return session.query(self.model).get(pk)

    def get_detail(
        self,
        session: Session,
        pk: int,
    ) -> ModelType:

        requirement_content = session.execute(
            text(
                "select id,requirement_content from requirement_analysis where scheme_id = :id"
            ),
            params={"id": pk},
        ).first()
        if requirement_content is not None:
            requirement_id = requirement_content[0]
            requirement_content = requirement_content[1]
        else:
            requirement_content = ""
        framework_content = session.execute(
            text(
                "select id,framework_content from system_framework where scheme_id = :id"
            ),
            params={"id": pk},
        ).first()
        if framework_content is not None:
            framework_id = framework_content[0]
            framework_content = framework_content[1]
        else:
            framework_content = ""
        indicator_content = session.execute(
            text(
                "select id,indicator_content from response_indicators where scheme_id = :id"
            ),
            params={"id": pk},
        ).first()
        if indicator_content is not None:
            indicator_id = indicator_content[0]
            indicator_content = indicator_content[1]
        else:
            indicator_content = ""
        file_url = session.query(self.model).get(pk)
        if file_url is not None:
            file_url = file_url.file_path_url
        else:
            raise HTTPException(status_code=404, detail="Bidfile is not exists")

        response = {
            "requirement_id": requirement_id,
            "requirement_content": requirement_content,
            "framework_id": framework_id,
            "framework_content": framework_content,
            "indicator_id": indicator_id,
            "indicator_content": indicator_content,
            "file_url": file_url,
        }

        return response

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


class SystemFrameworkDetailDAO(BaseDAO[System_framework_detail,CreateSystemFrameworkDetail,UpdateSystemFrameworkDetail]):
    model = System_framework_detail


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


class CatalogPromptDAO(
    BaseDAO[Catalog_prompt, CreateCatalogPrompt, UpdateCatalogPrompt]
):
    model = Catalog_prompt


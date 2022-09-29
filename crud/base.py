from datetime import datetime
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import UUID4, BaseModel

from sql_app.database import Base, db
from core.utils import validate_uuid4

# Define custom types for SQLAlchemy model, and Pydantic schemas
ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """Base class that can be extend by other action classes.
           Provides basic CRUD and listing operations.

        :param model: The SQLAlchemy model
        :type model: Type[ModelType]
        """
        self.model = model


    def get(self, id: UUID4) -> Optional[ModelType]:
        if not validate_uuid4(id):
            return None
        return db.query(self.model).filter(self.model.id == id).first()

    def create(self, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        try:
            db.commit()
        except:
            db.rollback()
            raise HTTPException(status_code=503, detail="Error writing to DB")
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]],
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        try:
            db.commit()
        except:
            db.rollback()
            raise HTTPException(status_code=503, detail="Error writing to DB")
        db.refresh(db_obj)
        return db_obj

    def delete(self, id: UUID4) -> ModelType:
        if not validate_uuid4(id):
            return None
        obj = db.query(self.model).get(id)
        db.delete(obj)
        try:
            db.commit()
        except:
            db.rollback()
            raise HTTPException(status_code=503, detail="Error writing to DB")
        return obj

    def soft_delete(self, db_obj: ModelType) -> ModelType:
        setattr(db_obj, "deleted_at", datetime.now())
        db.add(db_obj)
        try:
            db.commit()
        except:
            db.rollback()
            raise HTTPException(status_code=503, detail="Error writing to DB")
        db.refresh(db_obj)
        return db_obj

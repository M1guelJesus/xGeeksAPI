from typing import Optional, List
from dateutil import parser
from pydantic import UUID4
from crud.base import CRUDBase
from models import Meeting
from schemas import MeetingCreate, MeetingUpdate
from sql_app.database import db
from core.utils import validate_uuid4


class CRUDMeeting(CRUDBase[Meeting, MeetingCreate, MeetingUpdate]):
    def get_by_interviewer_id(self, interviewer_id: UUID4) -> Optional[Meeting]:
        if not validate_uuid4(interviewer_id):
            return None
        return db.query(self.model).filter(self.model.interviewer_id == interviewer_id).all()

    def create_multiple(self, obj_in: List[MeetingCreate]):
        aux = [dict(interviewer_id=obj.interviewer_id, date=parser.parse(obj.date)) for obj in obj_in]
        db.bulk_insert_mappings(Meeting, aux)
        try:
            db.commit()
        except:
            db.rollback()
            raise HTTPException(status_code=503, detail=[{"error": "Error writing to DB"}])
        return None

    def update_candidate(self, db_obj: Meeting, candidate_id: UUID4):
        if candidate_id is not None and not validate_uuid4(candidate_id):
            return None
        db_obj.candidate_id = candidate_id
        try:
            db.commit()
        except:
            db.rollback()
            raise HTTPException(status_code=503, detail=[{"error": "Error writing to DB"}])
        db.refresh(db_obj)
        return db_obj

    def delete(self, id: UUID4, interviewer_id: UUID4) -> Meeting:
        if not validate_uuid4(id):
            return None
        if not validate_uuid4(interviewer_id):
            return None
        obj = db.query(self.model).get(id)
        if obj.interviewer_id != interviewer_id:
            raise HTTPException(status_code=403, detail=[{"permissions": "Insufficient permissions."}])

        db.delete(obj)
        try:
            db.commit()
        except:
            db.rollback()
            raise HTTPException(status_code=503, detail=[{"error": "Error writing to DB"}])
        return obj


meeting = CRUDMeeting(Meeting)

from fastapi import APIRouter, Depends
from pydantic import UUID4
from pydantic import BaseModel

import crud
from core.auth import get_active_user, verify_role
from schemas import Meeting, MeetingCreate, MeetingUpdate, User
from typing import List

meeting_router = APIRouter(prefix="/meetings", tags=["Meeting"])


class Ids(BaseModel):
    id: str


@meeting_router.get("/{interviewer_id}", response_model=List[Meeting], name="Returns all meetings of the interviewer")
async def get_meetings_interviewer(interviewer_id: str, current_user: User = Depends(get_active_user)):
    """
    get_meetings_interviewer get from the BD a list with all meetings of the interviewer

    :param interviewer_id: id of the interviewer
    :param current_user: forces the user to be logged and saves its information
    :return: List with all meetings of the interviewer
    """
    await verify_role(current_user, ["INTERVIEWER", "CANDIDATE"])

    return crud.meeting.get_by_interviewer_id(interviewer_id=interviewer_id)


@meeting_router.post("", response_model=List[Meeting], name="Creates multiple meetings opportunities")
async def create_meetings_opportunities(meetings: List[MeetingCreate], current_user: User = Depends(get_active_user)):
    """
    create_meetings_opportunities creates multiple meetings opportunities for the interviewer

    :param meetings: list of all the meetings opportunities to create
    :param current_user: forces the user to be logged and saves its information
    :return: List with all meetings of the interviewer
    """
    await verify_role(current_user, ["INTERVIEWER"])

    if len(meetings) == 0:
        raise HTTPException(status_code=400, detail=[{"empty": "emptyList"}])

    crud.meeting.create_multiple(obj_in=meetings)

    return crud.meeting.get_by_interviewer_id(interviewer_id=meetings[0].interviewer_id)


@meeting_router.patch("/{meeting_id}", response_model=Meeting, name="Creates multiple meetings opportunities")
async def update_meeting(meeting_id: str, meeting_in: MeetingUpdate, current_user: User = Depends(get_active_user)):
    """
    update_meeting creates multiple meetings opportunities for the interviewer

    :param meeting_id: str with the ID of the Meeting that will be updated
    :param meeting_in: MeetingUpdate object with the candidate_id to add or null to remove it
    :param current_user: forces the user to be logged and saves its information
    :return: Meeting object updated
    """
    await verify_role(current_user, ["CANDIDATE"])

    meeting: Optional[Meeting] = crud.meeting.get(id=meeting_id)

    if meeting is None:
        raise HTTPException(status_code=404, detail=[{"meetings": "meetingNotFound"}])

    return crud.meeting.update_candidate(db_obj=meeting, candidate_id=meeting_in.candidate_id)


# In the HTTP Delete method the body is irrelevant and as we want to send the list of ids to delete in the body we need to use POST
@meeting_router.post("/delete", response_model=List[Meeting], name="Deletes multiple meetings opportunities")
async def delete_meetings_opportunities(meetings: List[Ids], current_user: User = Depends(get_active_user)):
    """
    delete_meetings_opportunities deletes multiple meetings opportunities for the interviewer, even if a meeting was agended
    In the HTTP Delete method the body is irrelevant and as we want to send the list of ids to delete in the body we need to use POST

    :param meetings: list of UUID4s of all the meetings to delete
    :param current_user: forces the user to be logged and saves its information
    :return: List of all the deleted meetings
    """
    await verify_role(current_user, ["INTERVIEWER"])

    deleted_meetings: List[Meeting] = []

    for meeting in meetings:
        deleted_meetings.append(crud.meeting.delete(id=meeting.id, interviewer_id=current_user.id))

    return deleted_meetings
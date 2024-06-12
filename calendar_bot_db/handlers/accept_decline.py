import logging

from aiogram import Router, F
from aiogram.types import CallbackQuery

from calendar_bot_db.models.crud_meetings import accept_decline_invite


logger = logging.getLogger(__name__)

router = Router(name="accept_decline_invite_router")


@router.callback_query(F.data.startswith("accepted_by_"))
async def get_accept_invite(callback: CallbackQuery):
    await callback.answer()
    data = callback.data.replace("accepted_by_", "")
    participant_id, meeting_id = map(int, data.split("_meeting_"))
    await accept_decline_invite(participant_id, meeting_id, accept=True)
    await callback.message.answer("Вы приняли приглашение.")


@router.callback_query(F.data.startswith("declined_by_"))
async def get_decline_invite(callback: CallbackQuery):
    await callback.answer()
    data = callback.data.replace("declined_by_", "")
    participant_id, meeting_id = map(int, data.split("_meeting_"))
    await accept_decline_invite(participant_id, meeting_id, decline=True)
    await callback.message.answer("Вы отклонили приглашение.")

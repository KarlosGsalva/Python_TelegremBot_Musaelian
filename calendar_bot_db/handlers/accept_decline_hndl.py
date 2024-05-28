import logging

from aiogram import Router, F
from aiogram.filters import StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager

from calendar_bot_db.models import crud_sqla_core as db
from calendar_bot_db.models import crud_meetings as dbm
from calendar_bot_db.models.crud_meetings import accept_decline_invite
from calendar_bot_db.services import convert_str_to_time
from calendar_bot_db.states import FSMCreateMeeting
from calendar_bot_db.lexicon import WARNING_TEXTS as WTEXT

import calendar_bot_db.keyboards as kb


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


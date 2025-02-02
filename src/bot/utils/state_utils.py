from typing import Any

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove

from src.bot.resources import sres
from src.bot.resources.constants import TempStorageDataKeys
from src.bot.states import MainStates
from src.bot.views.base.models import View


async def cancel_current_action(msg: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state and current_state.startswith(MainStates.__name__):
        await msg.answer(text=sres.CANCEL.NO_ACTIONS)
        return

    await msg.answer(text=sres.CANCEL.SUCCESS)
    await set_global_state(msg, state, new_state=MainStates.Main)


async def set_global_state(
        msg: Message,
        state: FSMContext,
        new_state: State | StatesGroup | None = MainStates.Main,
        view: View = View.for_state(text=sres.DEFAULT.SELECT_ACTION, reply_markup=ReplyKeyboardRemove()),
) -> Message:
    if (not isinstance(msg, Message) or not isinstance(state, FSMContext)
            or not isinstance(new_state, State | StatesGroup | None)):
        raise ValueError(f"Invalid arg types: msg={type(msg)}, state={type(state)}, new_state={type(new_state)}")

    await clear_temp_data(state)
    await state.set_state(new_state)
    return await view.answer_view(msg)


async def clear_temp_data(state: FSMContext) -> dict[str, Any]:
    if not isinstance(state, FSMContext):
        raise ValueError(f"Invalid arg types: state={type(state)}")

    data = await state.get_data()
    for i in list(TempStorageDataKeys):
        data.pop(i, None)
    await state.set_data(data)

    return data


async def update_temp_data(state: FSMContext, key: TempStorageDataKeys, value: Any) -> dict[str, Any]:
    if not isinstance(state, FSMContext) or not isinstance(key, TempStorageDataKeys):
        raise ValueError(f"Invalid arg types: state={type(state)}, key={type(key)}")

    return await state.update_data({key: value})


async def get_temp_data(state: FSMContext, key: TempStorageDataKeys) -> Any:
    if not isinstance(state, FSMContext) or not isinstance(key, TempStorageDataKeys):
        raise ValueError(f"Invalid arg types: state={type(state)}, key={type(key)}")

    data = await state.get_data()
    try:
        value = data[key]
        return value
    except KeyError as e:
        raise KeyError(f"The temp data key '{key}' was not found in the state data") from e


async def get_temp_data_or_default(state: FSMContext, key: TempStorageDataKeys, default: Any | None = None) -> Any:
    if not isinstance(state, FSMContext) or not isinstance(key, TempStorageDataKeys):
        raise ValueError(f"Invalid arg types: state={type(state)}, key={type(key)}")

    return await state.get_value(key, default)


async def unknown_error(msg: Message, state: FSMContext):
    if not isinstance(msg, Message) or not isinstance(state, FSMContext):
        raise ValueError(f"Invalid arg types: msg={type(msg)}, state={type(state)}")

    await msg.answer(sres.ERRORS.UNEXPECTED)
    await cancel_current_action(msg, state)


async def unknown_error_for_callback(callback: CallbackQuery, state: FSMContext):
    # Probably `state` will be useful in the future
    if not isinstance(callback, CallbackQuery) or not isinstance(state, FSMContext):
        raise ValueError(f"Invalid arg types: callback={type(callback)}, state={type(state)}")

    await callback.answer(sres.ERRORS.UNEXPECTED)

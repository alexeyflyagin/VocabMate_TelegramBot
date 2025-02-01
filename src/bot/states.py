from aiogram.fsm.state import StatesGroup, State


class MainStates(StatesGroup):
    Main = State()


class NewCardGroupStates(StatesGroup):
    Title = State()

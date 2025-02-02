from aiogram.fsm.state import StatesGroup, State


class MainStates(StatesGroup):
    Main = State()


class NewCardGroupStates(StatesGroup):
    Title = State()


class NewCardItemStates(StatesGroup):
    Term = State()
    Definition = State()


class TrainingStates(StatesGroup):
    Start = State()
    Term = State()
    Definition = State()

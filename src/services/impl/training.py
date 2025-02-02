import random
from datetime import datetime

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.dao import dao_card_group, dao_training, dao_card_item, dao_training_level
from src.data.models import CardItemOrm, TrainingOrm, TrainingLevelOrm
from src.data.session_manager import SessionManager
from src.loggers import service_logger
from src.services.exceptions import VocabMateAPIError, VocabMateDatabaseError, VocabMateNotFoundError, \
    VocabMateUnprocessableEntityError
from src.services.models.entities import CardItemEntity, CardGroupEntity
from src.services.models.training import StartTrainingRequest, StartTrainingResponse, TrainingLevelData, \
    AnswerLevelRequest, AnswerLevelResponse
from src.services.utils import raise_e_if_none


class TrainingService:

    def __init__(self, session_manager: SessionManager):
        self.session_manager = session_manager

    @staticmethod
    async def __create_levels(s: AsyncSession, training: TrainingOrm, cards: tuple[CardItemOrm, ...]) -> list[
        TrainingLevelOrm]:
        levels = []
        for card in cards:
            number_of = random.randint(2, 3)
            for i in range(number_of):
                level = await dao_training_level.create(s, training.id, card.id)
                levels.append(level)
        return levels

    async def start_training(self, data: StartTrainingRequest) -> StartTrainingResponse:
        """
        Use to start a training by the selected card group.

        :param data:

        :raises VocabMateNotFoundError: If the card group was not found
        :raises VocabMateBadRequestError: If the card group doesn't have cards
        :raises VocabMateDatabaseError:
        :raises VocabMateAPIError:
        """
        try:
            async with self.session_manager.session as s:
                card_group = await dao_card_group.get_by_id(s, id_=data.card_group_id, with_for_update=True)
                raise_e_if_none(card_group,
                                e=VocabMateNotFoundError(f"The card group (id={data.card_group_id}) was not found"))
                cards = await dao_card_item.get_by_group_id(s, card_group.id, with_for_update=True)

                if len(cards) == 0:
                    raise VocabMateUnprocessableEntityError(f"The card group (id={card_group.id}) is empty")

                await dao_training.delete_all(s)
                new_training = await dao_training.create(s, data.card_group_id)
                levels = await self.__create_levels(s, training=new_training, cards=cards)

                card_group_entity = CardGroupEntity.model_validate(card_group)
                response = StartTrainingResponse(training_id=new_training.id, total_levels=len(levels),
                                                 card_group=card_group_entity)
                await s.commit()
                return response
        except (VocabMateNotFoundError, VocabMateUnprocessableEntityError) as e:
            service_logger.debug(e)
            raise
        except SQLAlchemyError as e:
            service_logger.error(e)
            raise VocabMateDatabaseError(e)
        except Exception as e:
            service_logger.exception(e)
            raise VocabMateAPIError(f'An unexpected error occurred: {e}')

    async def get_current_level(self, training_id: int) -> TrainingLevelData:
        """
        Use to get a current level of the training.

        :raises VocabMateNotFoundError: If the training was not found
        :raises VocabMateDatabaseError:
        :raises VocabMateAPIError:
        """
        try:
            async with self.session_manager.session as s:
                training = await dao_training.get_by_id(s, training_id)
                raise_e_if_none(training, e=VocabMateNotFoundError(f"The training (id={training_id}) was not found"))
                t_levels = await dao_training_level.get_total_count_by_training_id(s, training_id)
                t_ans = await dao_training_level.get_total_answered_by_training_id(s, training_id)
                t_ans_wrong = await dao_training_level.get_total_answered_by_training_id(s, training_id, False)
                card_group = await dao_card_group.get_by_id(s, training.card_group_id)
                card_group_entity = CardGroupEntity.model_validate(card_group)
                if t_ans == t_levels:
                    return TrainingLevelData(level_id=None, training_id=training_id, total_answered=t_ans,
                                             total_answered_wrong=t_ans_wrong, total_levels=t_levels,
                                             is_completed=True, card_item=None, card_group=card_group_entity)

                if training.current_level_id:
                    level = await dao_training_level.get_by_id(s, training.current_level_id, with_for_update=True)
                else:
                    level = await dao_training_level.get_random_not_answered_by_training_id(s, training_id,
                                                                                            with_for_update=True)
                    training.current_level_id = level.id
                card_item = await dao_card_item.get_by_id(s, level.card_item_id)

                card_item_entity = CardItemEntity.model_validate(card_item)
                response = TrainingLevelData(training_id=training_id, total_answered=t_ans,
                                             total_answered_wrong=t_ans_wrong, total_levels=t_levels,
                                             is_completed=False, card_item=card_item_entity, level_id=level.id,
                                             card_group=card_group_entity)
                await s.commit()
                return response
        except VocabMateNotFoundError as e:
            service_logger.debug(e)
            raise
        except SQLAlchemyError as e:
            service_logger.error(e)
            raise VocabMateDatabaseError(e)
        except Exception as e:
            service_logger.exception(e)
            raise VocabMateAPIError(f'An unexpected error occurred: {e}')

    async def answer_level(self, data: AnswerLevelRequest) -> AnswerLevelResponse:
        """
        Use to answer your current learning level.

        :raises VocabMateNotFoundError: If the training was not found
        :raises VocabMateUnprocessableEntityError: If the current level was not found
        :raises VocabMateDatabaseError:
        :raises VocabMateAPIError:
        """
        try:
            async with self.session_manager.session as s:
                training = await dao_training.get_by_id(s, data.training_id, with_for_update=True)
                raise_e_if_none(training,
                                e=VocabMateNotFoundError(f"The training (id={data.training_id}) was not found"))

                if training.current_level_id is None:
                    raise VocabMateUnprocessableEntityError(f"The current level was not found")

                current_level = await dao_training_level.get_by_id(s, training.current_level_id, with_for_update=True)
                current_level.answer_is_right = data.is_right
                current_level.answered_at = datetime.now()
                current_level_card = await dao_card_item.get_by_id(s, current_level.card_item_id, with_for_update=True)

                level = await dao_training_level.get_random_not_answered_by_training_id(s, training.id,
                                                                                        with_for_update=True)
                training.current_level_id = level.id if level else None

                total_added = 0
                if not data.is_right:
                    total_added = random.randint(2, 3)
                    for i in range(total_added):
                        await dao_training_level.create(s, training.id, current_level_card.id)

                card_entity = CardItemEntity.model_validate(current_level_card)
                response = AnswerLevelResponse(training_id=training.id, total_added=total_added, card_item=card_entity)
                await s.commit()
                return response
        except VocabMateNotFoundError as e:
            service_logger.debug(e)
            raise
        except VocabMateUnprocessableEntityError as e:
            service_logger.error(e)
            raise
        except SQLAlchemyError as e:
            service_logger.error(e)
            raise VocabMateDatabaseError(e)
        except Exception as e:
            service_logger.exception(e)
            raise VocabMateAPIError(f'An unexpected error occurred: {e}')

    async def finish_training(self, training_id: int) -> TrainingLevelData:
        """
        Use to finish and delete a learning.

        :raises VocabMateNotFoundError: If the training was not found
        :raises VocabMateDatabaseError:
        :raises VocabMateAPIError:
        """
        try:
            async with self.session_manager.session as s:
                training = await dao_training.get_by_id(s, training_id, with_for_update=True)
                raise_e_if_none(training,
                                e=VocabMateNotFoundError(f"The training (id={training_id}) was not found"))
                card_group = await dao_card_group.get_by_id(s, training.card_group_id)
                t_levels = await dao_training_level.get_total_count_by_training_id(s, training_id)
                t_ans = await dao_training_level.get_total_answered_by_training_id(s, training_id)
                t_ans_wrong = await dao_training_level.get_total_answered_by_training_id(s, training_id, False)

                card_group_entity = CardGroupEntity.model_validate(card_group)
                response = TrainingLevelData(level_id=None, training_id=training_id, total_answered=t_ans,
                                             total_answered_wrong=t_ans_wrong, total_levels=t_levels, is_completed=True,
                                             card_item=None, card_group=card_group_entity)
                await dao_training.delete(s, training)
                await s.commit()
                return response
        except VocabMateNotFoundError as e:
            service_logger.debug(e)
            raise
        except SQLAlchemyError as e:
            service_logger.error(e)
            raise VocabMateDatabaseError(e)
        except Exception as e:
            service_logger.exception(e)
            raise VocabMateAPIError(f'An unexpected error occurred: {e}')

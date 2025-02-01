from sqlalchemy.exc import SQLAlchemyError

from src.dao import dao_card_group, dao_word_card
from src.data.session_manager import SessionManager
from src.loggers import service_logger
from src.services.exceptions import VocabMateAPIError, VocabMateDatabaseError, VocabMateNotFoundError
from src.services.models.entities import WordCardEntity
from src.services.models.word_card import AddWordCardRequest
from src.services.utils import raise_e_if_none


class WordCardService:

    def __init__(self, session_manager: SessionManager):
        self.session_manager = session_manager

    async def add_word_card(self, data: AddWordCardRequest) -> WordCardEntity:
        """
        Use to add the new word card to card group.

        :param data:

        :return: The created word card entity

        :raises VocabMateNotFoundError: If the card group was not found
        :raises VocabMateDatabaseError:
        :raises VocabMateAPIError:
        """
        try:
            async with self.session_manager.session as s:
                card_group = await dao_card_group.get_by_id(s, id_=data.group_id)
                raise_e_if_none(card_group,
                                e=VocabMateNotFoundError(f"The card group (id={data.group_id}) was not found"))
                new_word = await dao_word_card.create(s, group_id=data.group_id, word=data.word, pos=data.pos,
                                                      translations=data.translation, transcription=data.transcription)
                entity = WordCardEntity.model_validate(new_word)
                await s.commit()
                return entity
        except VocabMateNotFoundError as e:
            service_logger.debug(e)
            raise
        except SQLAlchemyError as e:
            service_logger.error(e)
            raise VocabMateDatabaseError(e)
        except Exception as e:
            service_logger.exception(e)
            raise VocabMateAPIError(f'An unexpected error occurred: {e}')

    async def get_word_card(self, id_: int) -> WordCardEntity:
        """
        Use to get the word card from a card group.

        :param id_: The ID of the word card

        :raises VocabMateNotFoundError: If the word card was not found
        :raises VocabMateDatabaseError:
        :raises VocabMateAPIError:
        """
        try:
            async with self.session_manager.session as s:
                word_card = await dao_word_card.get_by_id(s, id_=id_)
                raise_e_if_none(word_card, e=VocabMateNotFoundError(f"If the word card (id={id_}) was not found"))
                entity = WordCardEntity.model_validate(word_card)
                return entity
        except VocabMateNotFoundError as e:
            service_logger.debug(e)
            raise
        except SQLAlchemyError as e:
            service_logger.error(e)
            raise VocabMateDatabaseError(e)
        except Exception as e:
            service_logger.exception(e)
            raise VocabMateAPIError(f'An unexpected error occurred: {e}')

    async def remove_word_card(self, id_: int):
        """
        Use to remove the word card from a card group.

        :param id_: The ID of the word card

        :raises VocabMateNotFoundError: If the word card was not found
        :raises VocabMateDatabaseError:
        :raises VocabMateAPIError:
        """
        try:
            async with self.session_manager.session as s:
                word_card = await dao_word_card.get_by_id(s, id_=id_, with_for_update=True)
                raise_e_if_none(word_card, e=VocabMateNotFoundError(f"If the word card (id={id_}) was not found"))
                await dao_card_group.delete(s, word_card)
                await s.commit()
        except VocabMateNotFoundError as e:
            service_logger.debug(e)
            raise
        except SQLAlchemyError as e:
            service_logger.error(e)
            raise VocabMateDatabaseError(e)
        except Exception as e:
            service_logger.exception(e)
            raise VocabMateAPIError(f'An unexpected error occurred: {e}')

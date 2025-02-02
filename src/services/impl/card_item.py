from sqlalchemy.exc import SQLAlchemyError

from src.dao import dao_card_group, dao_card_item
from src.data.session_manager import SessionManager
from src.loggers import service_logger
from src.services.exceptions import VocabMateAPIError, VocabMateDatabaseError, VocabMateNotFoundError
from src.services.models.card_item import AddCardItemRequest
from src.services.models.entities import CardItemEntity
from src.services.utils import raise_e_if_none


class CardItemService:

    def __init__(self, session_manager: SessionManager):
        self.session_manager = session_manager

    async def add_card_item(self, data: AddCardItemRequest) -> CardItemEntity:
        """
        Use to add the new card item to card group.

        :param data:

        :return: The created card item entity

        :raises VocabMateNotFoundError: If the card group was not found
        :raises VocabMateDatabaseError:
        :raises VocabMateAPIError:
        """
        try:
            async with self.session_manager.session as s:
                card_group = await dao_card_group.get_by_id(s, id_=data.group_id)
                raise_e_if_none(card_group,
                                e=VocabMateNotFoundError(f"The card group (id={data.group_id}) was not found"))
                new_card = await dao_card_item.create(s, group_id=data.group_id, term=data.term,
                                                      definition=data.definition)
                entity = CardItemEntity.model_validate(new_card)
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

    async def get_card_item(self, id_: int) -> CardItemEntity:
        """
        Use to get the card item from a card group.

        :param id_: The ID of the card item

        :raises VocabMateNotFoundError: If the card item was not found
        :raises VocabMateDatabaseError:
        :raises VocabMateAPIError:
        """
        try:
            async with self.session_manager.session as s:
                card_item = await dao_card_item.get_by_id(s, id_=id_)
                raise_e_if_none(card_item, e=VocabMateNotFoundError(f"If the card item (id={id_}) was not found"))
                entity = CardItemEntity.model_validate(card_item)
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

    async def remove_card_item(self, id_: int):
        """
        Use to remove the card item from a card group.

        :param id_: The ID of the card item

        :raises VocabMateNotFoundError: If the card item was not found
        :raises VocabMateDatabaseError:
        :raises VocabMateAPIError:
        """
        try:
            async with self.session_manager.session as s:
                card_item = await dao_card_item.get_by_id(s, id_=id_, with_for_update=True)
                raise_e_if_none(card_item, e=VocabMateNotFoundError(f"If the card item (id={id_}) was not found"))
                await dao_card_group.delete(s, card_item)
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

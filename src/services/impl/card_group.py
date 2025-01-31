from sqlalchemy.exc import SQLAlchemyError

from src.dao import dao_card_group
from src.data.session_manager import SessionManager
from src.loggers import service_logger
from src.services.exceptions import VocabMateAPIError, VocabMateDatabaseError, VocabMateNotFoundError
from src.services.models.card_group import CreateCardGroupRequest
from src.services.models.entities import CardGroupEntity
from src.services.utils import raise_e_if_none


class CardGroupService:

    def __init__(self, session_manager: SessionManager):
        self.session_manager = session_manager

    async def create_card_group(self, data: CreateCardGroupRequest) -> CardGroupEntity:
        """
        Use to create the card group.

        :param data:

        :return: The created card group entity

        :raises VocabMateDatabaseError:
        :raises VocabMateAPIError:
        """
        try:
            async with self.session_manager.session as s:
                created_group = await dao_card_group.create(s, title=data.title)
                entity = CardGroupEntity.model_validate(created_group)
                await s.commit()
                return entity
        except SQLAlchemyError as e:
            service_logger.error(e)
            raise VocabMateDatabaseError(e)
        except Exception as e:
            service_logger.exception(e)
            raise VocabMateAPIError(f'An unexpected error occurred: {e}')

    async def delete_card_group(self, id_: int):
        """
        Use to delete the card group by `ID`.

        :param id_: The card group's ID

        :raises VocabMateNotFoundError: If the card group was not found
        :raises VocabMateDatabaseError:
        :raises VocabMateAPIError:
        """
        try:
            async with self.session_manager.session as s:
                card_group = await dao_card_group.get_by_id(s, id_=id_, with_for_update=True)
                raise_e_if_none(card_group, e=VocabMateNotFoundError(f"If the card group (id={id_}) was not found"))
                await dao_card_group.delete(s, card_group)
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

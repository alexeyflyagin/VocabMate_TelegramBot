import math

from sqlalchemy.exc import SQLAlchemyError

from src.dao import dao_card_group, dao_word_card
from src.data.session_manager import SessionManager
from src.loggers import service_logger
from src.services.exceptions import VocabMateAPIError, VocabMateDatabaseError, VocabMateNotFoundError
from src.services.models.card_group import CreateCardGroupRequest, GetCardGroupsRequest, GetCardGroupsResponse
from src.services.models.entities import CardGroupEntity, WordCardEntity
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
                entity.cards = []
                await s.commit()
                return entity
        except SQLAlchemyError as e:
            service_logger.error(e)
            raise VocabMateDatabaseError(e)
        except Exception as e:
            service_logger.exception(e)
            raise VocabMateAPIError(f'An unexpected error occurred: {e}')

    async def get_card_group(self, id_: int) -> CardGroupEntity:
        """
        Use to get the card group by `ID`.

        :param id_: The ID of the card group

        :return: The CardGroupEntity that includes the `cards` field

        :raises VocabMateNotFoundError: If the card group was not found
        :raises VocabMateDatabaseError:
        :raises VocabMateAPIError:
        """
        try:
            async with self.session_manager.session as s:
                card_group = await dao_card_group.get_by_id(s, id_=id_, with_for_update=True)
                raise_e_if_none(card_group, e=VocabMateNotFoundError(f"If the card group (id={id_}) was not found"))
                entity = CardGroupEntity.model_validate(card_group)
                word_cards = await dao_word_card.get_by_group_id(s, group_id=id_)
                word_cards_entities = [WordCardEntity.model_validate(i) for i in word_cards]
                entity.cards = word_cards_entities
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

    async def get_groups(self, data: GetCardGroupsRequest) -> GetCardGroupsResponse:
        """
        Get the card group list by pages.

        :raises VocabMateDatabaseError:
        :raises VocabMateAPIError:
        """
        try:
            async with self.session_manager.session as s:
                total_items = await dao_card_group.get_total_count(s)
                total_pages = math.ceil(total_items / data.limit)

                if total_pages and data.loop_pages and data.page not in range(total_pages):
                    data.page = data.page % total_pages

                card_groups = await dao_card_group.get_page(s, limit=data.limit, page=data.page)
                items = []
                for i in card_groups:
                    entity = CardGroupEntity.model_validate(i)
                    cards = await dao_word_card.get_by_group_id(s, i.id)
                    entity.cards = [WordCardEntity.model_validate(i) for i in cards]
                    items.append(entity)

                res = GetCardGroupsResponse(total_items=total_items, page=data.page, total_pages=total_pages,
                                            limit=data.limit, items=items)
                return res
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

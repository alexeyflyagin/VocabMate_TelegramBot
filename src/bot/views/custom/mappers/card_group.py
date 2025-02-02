from src.bot.views.custom.models.card_group import CardGroupViewData, DeleteCardGroupViewData, CardGroupItemData, \
    CardGroupPageListViewData, CardPageListOfCardGroupViewData, CardItemData
from src.services.models.card_group import GetCardGroupsResponse
from src.services.models.card_item import GetCardsOfCardGroupResponse
from src.services.models.entities import CardGroupEntity, CardItemEntity


def vd__card_group__from__entity(entity: CardGroupEntity) -> CardGroupViewData:
    if not isinstance(entity, CardGroupEntity):
        raise ValueError(f"Invalid type of entity. Args: entity={type(entity)}")

    if entity.cards is None:
        raise ValueError(f"Invalid entity. The `cards` field must not be None")

    return CardGroupViewData(
        card_group_id=entity.id,
        created_at=entity.created_at,
        title=entity.title,
        card_labels=[i.term for i in entity.cards],
    )


def vd__delete_card_group__from__entity(entity: CardGroupEntity) -> DeleteCardGroupViewData:
    if not isinstance(entity, CardGroupEntity):
        raise ValueError(f"Invalid type of entity. Args: entity={type(entity)}")

    if entity.cards is None:
        raise ValueError(f"Invalid entity. The `cards` field must not be None")

    return DeleteCardGroupViewData(
        card_group_id=entity.id,
        title=entity.title,
        total_cards=len(entity.cards),
    )


def card_group_item_data_list__from__entities(entities: list[CardGroupEntity]) -> list[CardGroupItemData]:
    items = []
    for entity in entities:
        item = CardGroupItemData(card_group_id=entity.id, created_at=entity.created_at, title=entity.title,
                                 card_labels=[i.term for i in entity.cards])
        items.append(item)
    return items


def card_item_data_list__from__entities(entities: list[CardItemEntity]) -> list[CardItemData]:
    items = []
    for entity in entities:
        item = CardItemData(card_item_id=entity.id, created_at=entity.created_at, term=entity.term,
                            definition=entity.definition)
        items.append(item)
    return items


def vd__card_group_page_list__from__get_card_groups_response(
        response: GetCardGroupsResponse
) -> CardGroupPageListViewData:
    return CardGroupPageListViewData(total_items=response.total_items, page=response.page,
                                     total_pages=response.total_pages, limit=response.limit,
                                     items=card_group_item_data_list__from__entities(response.items))


def vd__card_page_list_of_card_group__from__get_cards_of_card_group_response(
        response: GetCardsOfCardGroupResponse
) -> CardPageListOfCardGroupViewData:
    return CardPageListOfCardGroupViewData(total_items=response.total_items, page=response.page,
                                           total_pages=response.total_pages, limit=response.limit,
                                           card_group_title=response.card_group.title,
                                           card_group_id=response.card_group.id,
                                           items=card_item_data_list__from__entities(response.items))

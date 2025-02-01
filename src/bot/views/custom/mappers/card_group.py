from src.bot.views.custom.models.card_group import CardGroupViewData, DeleteCardGroupViewData, ItemData, \
    CardGroupPageOfListViewData
from src.services.models.card_group import GetCardGroupsResponse
from src.services.models.entities import CardGroupEntity


def vd__card_group__from__entity(entity: CardGroupEntity) -> CardGroupViewData:
    if not isinstance(entity, CardGroupEntity):
        raise ValueError(f"Invalid type of entity. Args: entity={type(entity)}")

    if entity.cards is None:
        raise ValueError(f"Invalid entity. The `cards` field must not be None")

    return CardGroupViewData(
        card_group_id=entity.id,
        date_create=entity.date_create,
        title=entity.title,
        card_labels=[i.word for i in entity.cards]
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


def item_data_list__from__entities(entities: list[CardGroupEntity]) -> list[ItemData]:
    items = []
    for entity in entities:
        item = ItemData(card_group_id=entity.id, date_create=entity.date_create, title=entity.title,
                        card_labels=[i.word for i in entity.cards])
        items.append(item)
    return items


def vd__card_group_page_of_list__from__get_card_groups_response(
        response: GetCardGroupsResponse
) -> CardGroupPageOfListViewData:
    return CardGroupPageOfListViewData(total_items=response.total_items, page=response.page,
                                       total_pages=response.total_pages, limit=response.limit,
                                       items=item_data_list__from__entities(response.items))

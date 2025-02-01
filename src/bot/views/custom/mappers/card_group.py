from src.bot.views.custom.models.card_group import CardGroupViewData, DeleteCardGroupViewData
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

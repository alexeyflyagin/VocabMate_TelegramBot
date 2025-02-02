from textwrap import dedent


class DEFAULT:
    FIELD_PLACEHOLDER = '-'
    TEMPORARILY_UNAVAILABLE = "This feature is temporarily unavailable."
    UNEXPECTED_ACTION = "The action is not recognized"
    SELECT_ACTION = "Select action."

    class BTN:
        ADD = "+ Add"
        BACK = "« Back"
        PREVIOUS_SYM = "«"
        PAGE_COUNTER = "{current} / {total}"
        NEXT_SYM = "»"


class AUTH:
    WELCOME = """Welcome *{first_name}*!"""


class CANCEL:
    NO_ACTIONS = """No action right now."""
    SUCCESS = """👌 The action has been canceled."""


class BTN:
    ADD_NEW_CARD = "+ Add new card"
    CONFIRM = "Yes, that's right!"
    CANCEL = "Cancel"
    DELETE = "Delete"
    CARDS = "Cards"
    BACK_TO_LIST = "« Back to list"


class ERRORS:
    UNEXPECTED = """Ops! An unexpected error occurred."""
    ACCESS_ERROR = "😔 Sorry, *it's a private bot!* You don't have access to this bot!"


class CARD_GROUP_LIST:
    ITEM = """*({btn_label})*  {title}"""

    VIEW = dedent("""\
    The list of *your card groups*:
    —
    {items}
    —
    """)

    VIEW__NO_ITEMS = dedent("""\
        The list or card groups still is empty.
        
        Add the first card group to start 👇
    """)


class CARD_GROUP:
    SHORT_LIST__ITEM = """•  {card_content}"""
    SHORT_LIST__MORE_ONE = """_(1 more item...)_"""
    SHORT_LIST__MORE = "_({more_counter} more items...)_"""
    SHORT_LIST__NO_ITEM_PLACEHOLDER = """_There are no cards yet..._"""

    VIEW = dedent("""\
    Card Group  #{id}
    *{title}*
    
    *Created at:*  {created_at}
    —
    {items_short_list}
    """)

    NOT_FOUND_ERROR = """Ops! The card group #{id} was not found."""

    class DELETE:
        DELETE_CONFIRMATION_VIEW = dedent("""\
        *Delete '{title}' card group.*

        Are you really want to delete it?
        """)

        DELETE_CONFIRMATION_WITH_CARDS_VIEW = dedent("""\
        *Delete '{title}' card group.*
        All {cards_counter} card(s) will be deleted.

        Are you really want to delete it?
        """)

        SUCCESS = """✅ The card group #{id} has been successfully deleted!"""

    class CARDS:
        ITEM = """*({btn_label})*  {term}"""

        VIEW = dedent("""\
        The list of *card items* from
        *{card_group_title}*:
        —
        {items}
        —
        """)

        VIEW__NO_ITEMS = dedent("""\
        The list of *card items* from
        *{card_group_title}*:
        —
        _No items..._
        —
        Add the first card item to start 👇
        """)


class NEW_CARD_GROUP:
    ENTER_TITLE = dedent("""\
    Alright, a *new card group*. How are we going to call it? Please *choose a title* for your card group.
    
    Use /cancel to cancel this operation.
    """)

    ENTER_TITLE__MP = dedent("""Type a title...""")

    SUCCESS = dedent("""
    ✅ New card group successfully created! 
    Use /newcardgroup to create more.
    """)


class NEW_CARD_ITEM:
    ENTER_TERM__MP = dedent("""Type a term...""")
    ENTER_DEFINITION__MP = dedent("""Type a definition...""")

    ENTER_TERM = dedent("""\
    Alright, a *new card item*. Please *enter a term* for your card.
    Use /cancel to cancel this operation.
    """)

    ENTER_DEFINITION = dedent("""\
    Good! Please *enter a definition* for your your term.
    Use /cancel to cancel this operation.
    """)

    SUCCESS = dedent("""
    ✅ New card successfully created and added to '{title}' card group!
    """)


class CHECK:
    class ERROR:
        CONTENT_TYPE = "🤨 Hmm... The message has unexpected content. Please try again..."

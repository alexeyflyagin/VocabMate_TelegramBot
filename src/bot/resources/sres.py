from textwrap import dedent


class DEFAULT:
    FIELD_PLACEHOLDER = '-'
    TEMPORARILY_UNAVAILABLE = "This feature is temporarily unavailable."

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
    CONFIRM = "Yes, that's right!"
    CANCEL = "Cancel"
    DELETE = "Delete"
    CARDS = "Cards"


class ERRORS:
    UNEXPECTED = """Ops! An unexpected error occurred."""
    ACCESS_ERROR = "😔 Sorry, *it's a private bot!* You don't have access to this bot!"


class CARD_GROUP_LIST:
    ITEM = """*{btn_label}*  {title}"""

    VIEW = dedent("""\
    The list of your card groups:
    —
    {items}
    —
    """)

    VIEW__NO_ITEMS = dedent("""\
        The list or card groups still is empty.
        
        Add the first card group to start 👇
    """)


class CARD_GROUP:
    SHORT_LIST__ITEM = """• {card_content}"""
    SHORT_LIST__MORE = """{more_counter} more items..."""
    SHORT_LIST__NO_ITEM_PLACEHOLDER = """_There are no cards yet..._"""

    VIEW = dedent("""\
    Card Group  #{id}
    *{title}*
    
    *Created at:*  {created_at}
    —
    {items_short_list}
    """)

    NOT_FOUND_ERROR = """Card group #{id} was not found."""

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


class NEW_CARD_GROUP:
    ENTER_TITLE = dedent("""\
    Alright, a new card group. How are we going to call it? Please *choose a title* for your card group.
    
    Use /cancel to cancel this operation.
    """)

    SUCCESS = dedent("""
    ✅ New card group successfully created! 
    Use /newcardgroup to create more.
    """)


class CHECK:
    class ERROR:
        CONTENT_TYPE = "🤨 Hmm... The message has unexpected content. Please try again..."

from datetime import datetime
from enum import StrEnum


class FormatType(StrEnum):
    STANDARD = "%Y-%m-%d %H:%M:%S"


def date_format(dt: datetime, format_type: FormatType = FormatType.STANDARD) -> str:
    return dt.strftime(format_type)

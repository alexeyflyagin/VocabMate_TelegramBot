class VocabMateAPIError(Exception):
    pass


class VocabMateDatabaseError(VocabMateAPIError):
    def __init__(self, e: Exception):
        super().__init__(f'Database error occurred: {e}')


class VocabMateNotFoundError(VocabMateAPIError):
    pass


class VocabMateUnprocessableEntityError(VocabMateAPIError):
    pass

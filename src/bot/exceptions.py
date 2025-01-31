class VocabBot(Exception):
    pass


class InvalidTrustedUserId(VocabBot):
    def __init__(self, user_id: int):
        super().__init__(f'Someone tried to access a bot with an untrusted id (id={user_id})')

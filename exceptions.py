class SendMessageExept(Exception):
    """Cообщение не отправлено."""
    pass


class TokenError(ValueError):
    """Token Error exception class."""


class APIConnectError(Exception):
    """API connect error exception class"""


class APIStatusError(Exception):
    """API response error exception class"""


class TelegramBotError(Exception):
    """Telegram bot error exception class"""


class JSONConversionError(Exception):
    """Json error exception class"""

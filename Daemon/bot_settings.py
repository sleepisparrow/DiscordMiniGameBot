from dataclasses import dataclass
import logging


@dataclass
class BotSettings:
    """Bot settings"""
    test_server: list[int] | None
    token: str
    logger_settings: int


def get_test_settings(token: str):
    """Get test bot settings"""
    return BotSettings(
        test_server=None,
        token=token,
        logger_settings=logging.DEBUG
    )


def get_main_settings(token: str):
    """Get test bot settings"""
    return BotSettings(
        test_server=None,
        token=token,
        logger_settings=logging.WARNING
    )

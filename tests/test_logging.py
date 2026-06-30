"""Tests for logging configuration."""

import logging

from bookstai.logging import configure_logging


def test_configure_logging_default_info() -> None:
    configure_logging(verbose=False)
    assert logging.getLogger().level == logging.INFO


def test_configure_logging_verbose_debug() -> None:
    configure_logging(verbose=True)
    assert logging.getLogger().level == logging.DEBUG


def test_configure_logging_does_not_duplicate_handlers() -> None:
    root = logging.getLogger()
    before = len(root.handlers)
    configure_logging(verbose=False)
    configure_logging(verbose=False)
    assert len(root.handlers) == before or len(root.handlers) == 1

from logging import DEBUG, INFO
from os import getenv

from structlog import (
    configure,
    get_logger,
    make_filtering_bound_logger,
    stdlib,
)
from structlog import (
    dev as structlog_dev,
)

logger: stdlib.BoundLogger = get_logger()


def set_up_custom_logging() -> None:
    """Setup custom logging for the application."""
    level = INFO
    if getenv("INPUT_DEBUG", "false").lower() == "true":
        level = DEBUG
    if getenv("CI"):
        configure(
            processors=[
                structlog_dev.ConsoleRenderer(
                    exception_formatter=structlog_dev.plain_traceback
                ),
            ],
            wrapper_class=make_filtering_bound_logger(level),
        )
    else:
        configure(wrapper_class=make_filtering_bound_logger(level))

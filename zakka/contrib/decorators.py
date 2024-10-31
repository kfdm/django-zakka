import logging
from functools import wraps

logger = logging.getLogger(__name__)


def skip_raw(func):
    """
    For many pre_save/post_save signals, we want to skip actions when loading a
    raw value from a fixture. This allows us to more consistantly handle those cases.
    """

    @wraps(func)
    def _wrapper(*, raw=False, instance, **kwargs):
        if raw:
            logger.debug("Skipping %s:%s for raw %s", __name__, func.__name__, instance)
            return
        else:
            logger.debug("Running %s:%s for %s", __name__, func.__name__, instance)
            return func(raw=raw, instance=instance, **kwargs)

    return _wrapper

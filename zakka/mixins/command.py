import logging

logging.basicConfig(level=logging.WARNING)


class LoggingMixin:
    def execute(self, *args, **options):
        logging.root.setLevel(
            {
                0: logging.ERROR,
                1: logging.WARNING,
                2: logging.INFO,
                3: logging.DEBUG,
            }.get(options["verbosity"])
        )
        return super().execute(*args, **options)

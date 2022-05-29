import json

import django.test
from django.conf import settings


class TestCase(django.test.TestCase):
    def json_data(self, *path, base_dir=settings.BASE_DIR):
        path = base_dir.joinpath(*path)
        with path.open() as fp:
            return json.load(fp)

    def raw_data(self, *path, base_dir=settings.BASE_DIR):
        with path.open() as fp:
            return fp.read()

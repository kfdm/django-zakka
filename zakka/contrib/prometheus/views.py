import prometheus_client
from prometheus_client.core import InfoMetricFamily

from django.http import HttpResponse
from django.views.generic import View

try:
    from importlib.metadata import version
except ImportError:
    from importlib_metadata import version


class Metrics(View):
    info_metric_name = "zakka_build_info"
    info_metric_metadata = "zakka"

    default_collectors = [
        prometheus_client.PlatformCollector,
    ]

    def __init__(self):
        self.registry = prometheus_client.CollectorRegistry(auto_describe=True)
        for collector in self.default_collectors:
            collector(registry=self.registry)
        self.registry.register(self)

    def get_info_metric(self):
        yield InfoMetricFamily(
            self.info_metric_name,
            "Deployment Information",
            value={"version": version(self.info_metric_metadata)},
        )

    def get(self, request, *args, **kwargs):
        return HttpResponse(
            prometheus_client.generate_latest(self.registry),
            content_type=prometheus_client.CONTENT_TYPE_LATEST,
        )

    def collect(self):
        # https://github.com/prometheus/client_python#custom-collectors
        yield from self.get_info_metric()

from tempfile import TemporaryDirectory
from unittest import TestCase

from app.clients.k8s.settings import K8SSettings
from app.pydantic_yaml import from_yaml, to_yaml
from app.settings import PrometheusSettings, Settings


class PyDanticYamlTest(TestCase):
    def test_dump_load_settings(self):
        expected = Settings(
            k8s=K8SSettings(incluster=True, context=None),
            prometheus=PrometheusSettings(endpoint_port=8080),
        )
        with TemporaryDirectory("-pydantic", "test") as tmpdir:
            yaml_file = f"{tmpdir}/test.yaml"
            to_yaml(yaml_file, expected)
            actual = from_yaml(yaml_file, Settings)

        self.assertEqual(expected, actual)

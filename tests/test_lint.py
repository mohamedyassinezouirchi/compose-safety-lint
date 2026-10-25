import unittest
from compose_safety_lint import lint_document, main
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
import io

class ComposeSafetyLintTests(unittest.TestCase):
    def test_detects_privileged_and_socket(self):
        data = {"services": {"api": {
            "privileged": True, "read_only": True,
            "volumes": ["/var/run/docker.sock:/var/run/docker.sock"]
        }}}
        codes = {i["rule"] for i in lint_document(data)}
        self.assertEqual(codes, {"CSL001", "CSL002"})

    def test_detects_host_and_capability(self):
        data = {"services": {"worker": {
            "network_mode": "host", "pid": "host", "cap_add": ["SYS_ADMIN"],
            "security_opt": ["seccomp:unconfined"], "read_only": True
        }}}
        self.assertEqual(len(lint_document(data)), 4)

    def test_read_only_warning(self):
        codes = {i["rule"] for i in lint_document({"services": {"web": {"image": "nginx"}}})}
        self.assertEqual(codes, {"CSL007"})

    def test_safe_example(self):
        doc = {"services": {"web": {"image": "nginx", "read_only": True}}}
        self.assertEqual(lint_document(doc), [])

    def test_invalid_services(self):
        with self.assertRaises(ValueError):
            lint_document({"services": []})

    def test_cli_with_yaml(self):
        with TemporaryDirectory() as temp:
            path = Path(temp) / "compose.yml"
            path.write_text("services:\n  web:\n    image: nginx\n    read_only: true\n", encoding="utf-8")
            with patch("sys.stdout", new_callable=io.StringIO):
                self.assertEqual(main([str(path)]), 0)

if __name__ == "__main__":
    unittest.main()

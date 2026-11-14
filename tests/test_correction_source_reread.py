import ast
import importlib.util
import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CHECKER_PATH = (
    REPO_ROOT
    / "evidence/wave-20261009-correction-01/source-reread"
    / "check-source-reread-correction-01.py"
)
RECEIPT_PATH = CHECKER_PATH.parent / "source-byte-reread-CORRECTION-01.json"
AUTHENTICATION_PATH = (
    REPO_ROOT
    / "evidence/wave-20261009-correction-01/serialized-admission-03"
    / "cache-authentication-20261010.json"
)


def load_checker():
    spec = importlib.util.spec_from_file_location("correction_source_reread", CHECKER_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class CorrectionSourceRereadCheckerTests(unittest.TestCase):
    def setUp(self):
        self.checker = load_checker()
        self.receipt = json.loads(RECEIPT_PATH.read_text(encoding="utf-8"))
        self.authentication = json.loads(
            AUTHENTICATION_PATH.read_text(encoding="utf-8")
        )

    def test_checker_uses_no_optimization_strippable_asserts(self):
        tree = ast.parse(CHECKER_PATH.read_text(encoding="utf-8"))
        self.assertFalse(
            any(isinstance(node, ast.Assert) for node in ast.walk(tree)),
            "checker must not use assertions that python -O removes",
        )

    def test_declared_bindings_reject_tampering(self):
        mutations = [
            ("cache authentication status", lambda data: data["cache_binding"].__setitem__("authentication_status", "UNAUTHENTICATED")),
            ("inventory digest", lambda data: data["cache_binding"].__setitem__("inventory_digest", "0" * 64)),
            ("git blob sha", lambda data: data["source_binding"].__setitem__("git_blob_sha", "0" * 40)),
            ("retrieval status", lambda data: data["source_binding"].__setitem__("retrieval_status", "MISSING")),
            ("A before integration", lambda data: data["integration_binding"].__setitem__("A_before_worker_integration", "0" * 40)),
            ("A after worker integration", lambda data: data["integration_binding"].__setitem__("A_after_worker_integration", "0" * 40)),
            ("exclusive root identity", lambda data: data["integration_binding"].__setitem__("exclusive_root_tree_identity", "UNKNOWN")),
        ]
        for expected_message, mutate in mutations:
            with self.subTest(expected_message=expected_message):
                candidate = json.loads(json.dumps(self.receipt))
                mutate(candidate)
                with self.assertRaisesRegex(ValueError, expected_message):
                    self.checker.validate_declared_bindings(
                        candidate, self.authentication, REPO_ROOT
                    )


if __name__ == "__main__":
    unittest.main()

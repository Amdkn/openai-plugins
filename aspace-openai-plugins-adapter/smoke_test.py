#!/usr/bin/env python3
"""Smoke tests for the aspace-openai-plugins-adapter (D12 clean-room).

Standard library only. Offline by construction: no network call is made
(the suite also asserts the adapter imports no network module), and every
fixture is generated in a scratch directory — no upstream file is read.
Run: python3 aspace-openai-plugins-adapter/smoke_test.py
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
MOCK = HERE / "mock_plugin.py"

FORBIDDEN_IMPORTS = ("socket", "urllib", "http.client", "http.server",
                     "requests", "httpx", "aiohttp")


class AdapterSmokeTest(unittest.TestCase):
    def test_contract_is_valid_json(self):
        contract = json.loads((HERE / "contract.json").read_text(encoding="utf-8"))
        self.assertEqual(contract["adapter"]["name"], "aspace-openai-plugins-adapter")
        self.assertEqual(contract["adapter"]["version"], "0.1.0")
        self.assertEqual(contract["upstream"]["frozen_commit"],
                         "d420d13051bffe4543ed39e30fa46b87148e47dd")
        self.assertIsNone(contract["id"])  # D12: no address before the 13e judgment
        self.assertEqual(contract["clean_room"]["regime"],
                         "D12 (D-N048) — reference only, clean-room adaptation")

    def test_manifest_command_prints_valid_manifest(self):
        out = subprocess.run([sys.executable, str(MOCK), "manifest"],
                             capture_output=True, text=True, timeout=30)
        self.assertEqual(out.returncode, 0, out.stderr)
        manifest = json.loads(out.stdout)
        self.assertEqual(manifest["name"], "aspace-example")
        self.assertEqual(manifest["version"], "0.1.0")
        self.assertIn("interface", manifest)
        self.assertEqual(manifest["interface"]["displayName"], "A'Space Example")

    def test_validate_accepts_minimal_manifest(self):
        sys.path.insert(0, str(HERE))
        try:
            import mock_plugin as mp
        finally:
            sys.path.pop(0)
        with tempfile.TemporaryDirectory() as tmp:
            plugin_dir = Path(tmp) / "aspace-example"
            manifest_dir = plugin_dir / ".codex-plugin"
            manifest_dir.mkdir(parents=True)
            (manifest_dir / "plugin.json").write_text(
                json.dumps(mp.minimal_manifest("aspace-example")), encoding="utf-8")
            self.assertEqual(mp.validate_plugin_dir(plugin_dir), [])

    def test_validate_rejects_missing_manifest(self):
        sys.path.insert(0, str(HERE))
        try:
            import mock_plugin as mp
        finally:
            sys.path.pop(0)
        with tempfile.TemporaryDirectory() as tmp:
            errors = mp.validate_plugin_dir(Path(tmp) / "empty-plugin")
            self.assertTrue(any("missing manifest" in e for e in errors))

    def test_validate_rejects_bad_json(self):
        sys.path.insert(0, str(HERE))
        try:
            import mock_plugin as mp
        finally:
            sys.path.pop(0)
        with tempfile.TemporaryDirectory() as tmp:
            plugin_dir = Path(tmp) / "bad-plugin"
            manifest_dir = plugin_dir / ".codex-plugin"
            manifest_dir.mkdir(parents=True)
            (manifest_dir / "plugin.json").write_text("{not json", encoding="utf-8")
            errors = mp.validate_plugin_dir(plugin_dir)
            self.assertTrue(any("not valid JSON" in e for e in errors))

    def test_env_reports_offline(self):
        out = subprocess.run([sys.executable, str(MOCK), "env"],
                             capture_output=True, text=True, timeout=30)
        self.assertEqual(out.returncode, 0, out.stderr)
        env = json.loads(out.stdout)
        self.assertEqual(env["DO_NOT_TRACK"], "1")
        self.assertIn("no socket/urllib/http", env["ASPACE_ADAPTER_NETWORK"])

    def test_adapter_imports_no_network_module(self):
        source = (HERE / "mock_plugin.py").read_text(encoding="utf-8")
        for forbidden in FORBIDDEN_IMPORTS:
            self.assertNotIn(f"import {forbidden}", source)
            self.assertNotIn(f"from {forbidden}", source)

    def test_no_upstream_content_in_adapter(self):
        # The adapter must not embed upstream text: every payload file is
        # small and carries only A'Space wording. (Blob-level proof is done
        # by Ryan against the gel tree; this is the local guard.) The test
        # file itself is excluded: it holds the guard literals by design.
        for name in ("contract.json", "mock_plugin.py", "README.md"):
            text = (HERE / name).read_text(encoding="utf-8")
            self.assertNotIn("bradautomates", text)
            self.assertNotIn("api.githubcopilot.com", text)
            self.assertNotIn("mcp.figma.com", text)


if __name__ == "__main__":
    unittest.main(verbosity=2)

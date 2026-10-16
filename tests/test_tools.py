"""Safety checks run locally with fake networking; no UHEM jobs are submitted."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("uhem_check", ROOT / "scripts/uhem-check.py")
doctor = importlib.util.module_from_spec(spec)
spec.loader.exec_module(doctor)


def successful_result():
    checks = {name: {"returncode": 0, "stdout": "", "stderr": ""}
              for name in ("project", "partitions", "nodes", "my_jobs", "modules")}
    checks["project"]["stdout"] = (
        " demo Kullanilan-CpuSaat(CpuHour-Usage):2,588/148,204 (%1),  Disk:242/1,124 GB (%21).\n"
        "other Kullanilan-CpuSaat(CpuHour-Usage):0/50,000 (%0),  Disk:0/50 GB (%0).\n")
    return {"hostname": "altay.example", "user": "demo", "checks": checks}


class CheckTests(unittest.TestCase):
    def test_quota_and_multiple_projects(self):
        result = doctor.summarize(successful_result())
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["projects"][0]["remaining_core_hours"], 145616)
        self.assertEqual(result["projects"][1]["total_core_hours"], 50000)
        self.assertEqual(result["jobs_submitted"], 0)

    def test_failed_required_check_is_partial(self):
        data = successful_result()
        data["checks"]["nodes"]["returncode"] = 1
        result = doctor.summarize(data)
        self.assertEqual(result["status"], "PARTIAL")
        self.assertIn("nodes", result["failed_checks"])

    def test_missing_required_check_is_partial(self):
        data = successful_result()
        del data["checks"]["modules"]
        self.assertIn("modules", doctor.summarize(data)["failed_checks"])

    def test_unrecognized_quota_is_not_zero_or_pass(self):
        data = successful_result()
        data["checks"]["project"]["stdout"] = "changed output format"
        result = doctor.summarize(data)
        self.assertEqual(result["status"], "PARTIAL")
        self.assertIn("quota_not_parsed", result["failed_checks"])
        self.assertEqual(result["projects"], [])

    def test_malformed_check_is_partial(self):
        data = successful_result()
        data["checks"]["project"] = None
        self.assertEqual(doctor.summarize(data)["status"], "PARTIAL")

    def test_invalid_response_rejected(self):
        for data in ([], {}, {"checks": []}):
            with self.subTest(data=data), self.assertRaises(ValueError):
                doctor.summarize(data)

    def test_host_injection_and_options_rejected(self):
        for host in ("-oProxyCommand=bad", "demo;touch x", "a b", "user@host", "$(id)", ""):
            with self.subTest(host=host), self.assertRaises(ValueError):
                doctor.ssh_command(host)

    def test_ssh_does_not_disable_host_verification(self):
        command = doctor.ssh_command("UHEM_Nanoparticle")
        self.assertIn("StrictHostKeyChecking=yes", command)
        self.assertIn("BatchMode=yes", command)
        self.assertEqual(command[-3:], ["UHEM_Nanoparticle", "python3", "-"])

    def test_report_private_and_never_overwritten(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "private" / "report.json"
            doctor.save_report(path, {"test": True})
            self.assertEqual(path.stat().st_mode & 0o777, 0o600)
            self.assertEqual(path.parent.stat().st_mode & 0o777, 0o700)
            original = path.read_bytes()
            with self.assertRaises(FileExistsError):
                doctor.save_report(path, {})
            self.assertEqual(path.read_bytes(), original)

    def test_report_symlink_not_followed(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "original"
            target.write_text("preserve")
            link = Path(directory) / "report.json"
            link.symlink_to(target)
            with self.assertRaises(FileExistsError):
                doctor.save_report(link, {})
            self.assertEqual(target.read_text(), "preserve")


FAKE_COMMAND = '''import json,os,pathlib,sys
name=pathlib.Path(sys.argv[0]).name
directory=pathlib.Path(os.environ["FAKE_DIR"])
with (directory/"calls.jsonl").open("a") as stream:
 stream.write(json.dumps([name]+sys.argv[1:])+"\\n")
if name=="systemctl":
 if sys.argv[1]=="is-active":
  sys.exit(0 if os.environ.get("FAKE_ACTIVE","1")=="1" or (directory/"started").exists() else 3)
 if sys.argv[1]=="start":
  if os.environ.get("FAKE_START_FAIL")=="1": sys.exit(1)
  (directory/"started").touch()
elif name=="dig":
 print(os.environ.get("FAKE_DNS","10.128.2.9"))
elif name=="ip":
 print("10.128.2.9 dev "+os.environ.get("FAKE_ROUTE","tun-uhem")+" src 10.128.1.1")
elif name=="nc":
 print("CONNECTED")
 if os.environ.get("FAKE_ECHO_STDIN")=="1": print(sys.stdin.read())
'''


class ProxyTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.directory = Path(self.temporary.name)
        for name in ("systemctl", "dig", "ip", "nc", "sleep"):
            path = self.directory / name
            path.write_text("#!" + sys.executable + "\n" + FAKE_COMMAND)
            path.chmod(0o755)
        self.environment = os.environ.copy()
        for name in list(self.environment):
            if name.startswith(("UHEM_", "FAKE_")):
                del self.environment[name]
        self.environment.update(PATH=str(self.directory) + os.pathsep + os.defpath,
                                FAKE_DIR=str(self.directory))
        self.addCleanup(self.temporary.cleanup)

    def run_proxy(self, *args, stdin_data=None, **overrides):
        environment = self.environment.copy()
        environment.update(overrides)
        return subprocess.run(["bash", str(ROOT / "scripts/uhem-proxy.sh"), *args],
                              env=environment, input=stdin_data, capture_output=True, text=True, timeout=20)

    def calls(self):
        path = self.directory / "calls.jsonl"
        return [json.loads(line) for line in path.read_text().splitlines()] if path.exists() else []

    def test_rejects_arbitrary_target_before_any_commands(self):
        for args in (("example.com", "22"), ("altay.uhem.itu.edu.tr", "80"), ("-x", "22"), ()):
            self.assertEqual(self.run_proxy(*args).returncode, 2)
        self.assertEqual(self.calls(), [])

    def test_rejects_invalid_settings_before_any_commands(self):
        for overrides in ({"UHEM_VPN_SERVICE": "--bad.service"},
                          {"UHEM_VPN_SERVICE": "bad;id.service"},
                          {"UHEM_TUN_DEVICE": "tun0;id"},
                          {"UHEM_VPN_DNS": "8.8.8.8"},
                          {"UHEM_VPN_DNS": "10.128.999.1"}):
            self.assertEqual(self.run_proxy("altay.uhem.itu.edu.tr", "22", **overrides).returncode, 2)
        self.assertEqual(self.calls(), [])

    def test_correct_route_connects_without_idle_timeout(self):
        result = self.run_proxy("altay.uhem.itu.edu.tr", "22")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.calls()[-1], ["nc", "10.128.2.9", "22"])
        self.assertFalse(any(call[0] == "systemctl" and call[1] == "start" for call in self.calls()))

    def test_only_named_service_started(self):
        result = self.run_proxy("altay.uhem.itu.edu.tr", "22", FAKE_ACTIVE="0",
                                UHEM_VPN_SERVICE="mine-uhem.service")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(["systemctl", "start", "mine-uhem.service"], self.calls())
        self.assertFalse(any(call[0] in ("pkill", "kill", "ip") and "delete" in call for call in self.calls()))

    def test_proxy_preserves_ssh_stdin(self):
        payload = "SSH-2.0-local-test\noriginal-client-bytes\n"
        result = self.run_proxy("altay.uhem.itu.edu.tr", "22", stdin_data=payload, FAKE_ECHO_STDIN="1")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(payload, result.stdout)

    def test_start_failure_does_not_connect(self):
        result = self.run_proxy("altay.uhem.itu.edu.tr", "22", FAKE_ACTIVE="0", FAKE_START_FAIL="1")
        self.assertEqual(result.returncode, 1)
        self.assertFalse(any(call[0] == "nc" for call in self.calls()))

    def test_wrong_tunnel_rejected(self):
        result = self.run_proxy("altay.uhem.itu.edu.tr", "22", FAKE_ROUTE="tun-unrelated")
        self.assertEqual(result.returncode, 1)
        self.assertFalse(any(call[0] == "nc" for call in self.calls()))

    def test_public_dns_answer_rejected_without_fallback(self):
        result = self.run_proxy("altay.uhem.itu.edu.tr", "22", FAKE_DNS="203.0.113.9")
        self.assertEqual(result.returncode, 1)
        self.assertTrue(all("@10.128.5.2" in call for call in self.calls() if call[0] == "dig"))
        self.assertFalse(any(call[0] in ("ip", "nc") for call in self.calls()))

    def test_invalid_octet_rejected(self):
        result = self.run_proxy("altay.uhem.itu.edu.tr", "22", FAKE_DNS="10.128.999.1")
        self.assertEqual(result.returncode, 1)
        self.assertFalse(any(call[0] == "nc" for call in self.calls()))

    def test_custom_tunnel_and_internal_dns(self):
        result = self.run_proxy("altay.uhem.itu.edu.tr", "22", UHEM_TUN_DEVICE="tun-my-uhem",
                                FAKE_ROUTE="tun-my-uhem", UHEM_VPN_DNS="10.128.5.3")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("@10.128.5.3", next(call for call in self.calls() if call[0] == "dig"))


class InstallTests(unittest.TestCase):
    def run_installer(self, prefix):
        return subprocess.run(["sh", str(ROOT / "scripts/install-local-tools.sh"), "--prefix", str(prefix)],
                              capture_output=True, text=True, timeout=10)

    def test_install_and_idempotence(self):
        with tempfile.TemporaryDirectory() as directory:
            self.assertEqual(self.run_installer(directory).returncode, 0)
            installed = Path(directory) / "bin/uhem-check"
            self.assertEqual(installed.read_bytes(), (ROOT / "scripts/uhem-check.py").read_bytes())
            self.assertTrue(os.access(installed, os.X_OK))
            self.assertEqual(self.run_installer(directory).returncode, 0)

    def test_conflict_is_preserved(self):
        with tempfile.TemporaryDirectory() as directory:
            installed = Path(directory) / "bin/uhem-check"
            installed.parent.mkdir()
            installed.write_text("existing tool")
            self.assertEqual(self.run_installer(directory).returncode, 1)
            self.assertEqual(installed.read_text(), "existing tool")

    def test_symlink_is_preserved(self):
        with tempfile.TemporaryDirectory() as directory:
            installed = Path(directory) / "bin/uhem-check"
            installed.parent.mkdir()
            original = Path(directory) / "original"
            original.write_text("existing tool")
            installed.symlink_to(original)
            self.assertEqual(self.run_installer(directory).returncode, 1)
            self.assertTrue(installed.is_symlink())
            self.assertEqual(original.read_text(), "existing tool")


if __name__ == "__main__":
    unittest.main()

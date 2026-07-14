#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "templates" / "trip-lifecycle" / "checks" / "trip_contract.py"


class TripLifecycleContractTests(unittest.TestCase):
    def run_checker(self, *args: str) -> subprocess.CompletedProcess[str]:
        if args[0] == "release" and "--expected-issue" not in args:
            args = (*args, "--expected-issue", "OPE-305")
        return subprocess.run(
            [sys.executable, str(CHECKER), *args],
            capture_output=True,
            text=True,
            timeout=10,
        )

    def make_ringer(self, temp: str) -> Path:
        ringer = Path(temp) / "ringer.py"
        ringer.write_text("import sys\nsys.exit(0 if sys.argv[1:] else 1)\n", encoding="utf-8")
        return ringer

    def manifest_args(self, manifest: Path, issue: str = "OPE-305") -> tuple[str, ...]:
        return (
            "manifest", "--manifest", str(manifest), "--ringer", str(self.make_ringer(str(manifest.parent))),
            "--expected-run-name", "ope-305-trip-protocol", "--expected-issue", issue,
        )

    def release_args(self, package: Path, repo: Path, command: str, issue: str = "OPE-305") -> tuple[str, ...]:
        return (
            "release", "--package", str(package), "--repo", str(repo),
            "--expected-run-name", "ope-305-trip-protocol", "--expected-issue", issue,
            "--verify-command", command,
        )

    def make_repo(self, temp: str) -> Path:
        repo = Path(temp) / "repo"
        repo.mkdir()
        subprocess.run(["git", "init", "-q", str(repo)], check=True)
        (repo / "tracked.txt").write_text("before\n", encoding="utf-8")
        subprocess.run(["git", "-C", str(repo), "add", "tracked.txt"], check=True)
        subprocess.run(
            [
                "git", "-C", str(repo), "-c", "user.name=Test", "-c", "user.email=test@example.com",
                "-c", "commit.gpgSign=false",
                "commit", "-qm", "initial",
            ],
            check=True,
        )
        return repo

    def test_manifest_accepts_a_verified_phase_round(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            manifest = Path(temp) / "manifest.json"
            manifest.write_text(
                json.dumps(
                    {
                        "run_name": "ope-305-trip-protocol",
                        "workdir": str(Path(temp) / "work"),
                        "max_parallel": 1,
                        "trip": {
                            "issue": "OPE-305",
                            "phase": "review",
                            "plan_version": 2,
                        },
                        "tasks": [
                            {
                                "key": "review-protocol",
                                "task_type": "code-review",
                                "spec": (
                                    "Review the approved implementation against its exact Plan, inspect the real diff, "
                                    "run the declared checks, and write only the required review artifact."
                                ),
                                "check": "python3 trip_contract.py review --report review.md",
                                "expect_files": ["review.md"],
                                "verified": "the review artifact has an allowed deterministic verdict",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            result = self.run_checker(*self.manifest_args(manifest))

        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("PASS [manifest_contract]", result.stdout)

    def test_manifest_rejects_a_drifted_run_name(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            manifest = Path(temp) / "manifest.json"
            manifest.write_text(
                json.dumps(
                    {
                        "run_name": "ope-305-review",
                        "trip": {"issue": "OPE-305", "phase": "review", "plan_version": 1},
                        "tasks": [{"key": "review", "task_type": "review", "spec": "x", "check": "x", "expect_files": ["review.md"], "verified": "x"}],
                    }
                ),
                encoding="utf-8",
            )
            result = self.run_checker(*self.manifest_args(manifest))

        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        self.assertIn("FAIL [run_name_mismatch]", result.stdout)

    def test_manifest_lints_instead_of_parsing_its_phase_check(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            manifest = Path(temp) / "manifest.json"
            manifest.write_text(
                json.dumps(
                    {
                        "run_name": "ope-305-trip-protocol",
                        "trip": {"issue": "OPE-305", "phase": "review", "plan_version": 1},
                        "tasks": [
                            {
                                "key": "review",
                                "task_type": "review",
                                "spec": "x",
                                "check": "python3 trip_contract.py review --report review.md && true # plan-declared",
                                "expect_files": ["review.md"],
                                "verified": "x",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            result = self.run_checker(*self.manifest_args(manifest))

        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_manifest_rejects_a_mismatched_issue(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            manifest = Path(temp) / "manifest.json"
            manifest.write_text(json.dumps({
                "run_name": "ope-305-trip-protocol",
                "trip": {"issue": "OPE-999", "phase": "review", "plan_version": 1},
                "tasks": [{"key": "review", "task_type": "review", "spec": "x", "check": "python3 -c 'pass'", "expect_files": ["review.md"], "verified": "x"}],
            }), encoding="utf-8")
            result = self.run_checker(*self.manifest_args(manifest))
        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        self.assertIn("FAIL [issue_mismatch]", result.stdout)

    def test_manifest_fails_when_ringer_lint_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            manifest = Path(temp) / "manifest.json"
            manifest.write_text(json.dumps({
                "run_name": "ope-305-trip-protocol",
                "trip": {"issue": "OPE-305", "phase": "review", "plan_version": 1},
                "tasks": [{"key": "review", "task_type": "review", "spec": "x", "check": "python3 -c 'pass'", "expect_files": ["review.md"], "verified": "x"}],
            }), encoding="utf-8")
            ringer = self.make_ringer(temp)
            ringer.write_text("import sys\nsys.exit(1)\n", encoding="utf-8")
            result = self.run_checker(
                "manifest", "--manifest", str(manifest), "--ringer", str(ringer),
                "--expected-run-name", "ope-305-trip-protocol", "--expected-issue", "OPE-305",
            )
        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        self.assertIn("FAIL [ringer_lint_failed]", result.stdout)

    def test_review_accepts_an_allowed_deterministic_verdict(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            report = Path(temp) / "review.md"
            report.write_text(
                """# TRIP Review

## Summary
- The implementation matches the approved Plan.

## Findings
No blocking findings.

## Verification
- Command: `python3 tests/test_trip_lifecycle.py`
- Result: pass

## Verdict
Verdict: APPROVED
""",
                encoding="utf-8",
            )

            result = self.run_checker("review", "--report", str(report))

        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("PASS [review_contract]: APPROVED", result.stdout)

    def test_review_rejects_prose_after_the_verdict(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            report = Path(temp) / "review.md"
            report.write_text(
                """# TRIP Review

## Summary
The implementation is ready.

## Findings
No blocking findings.

## Verification
- Command: `python3 tests/test_trip_lifecycle.py`
- Result: pass

## Verdict
Verdict: APPROVED
Approval is conditional on another undocumented check.
""",
                encoding="utf-8",
            )

            result = self.run_checker("review", "--report", str(report))

        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        self.assertIn("FAIL [verdict_not_final]", result.stdout)

    def test_review_rejects_a_title_after_prose(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            report = Path(temp) / "review.md"
            report.write_text(
                """Preface that must not precede the review title.

# TRIP Review

## Summary
The implementation is ready.

## Findings
No blocking findings.

## Verification
- Command: `python3 tests/test_trip_lifecycle.py`
- Result: pass

## Verdict
Verdict: APPROVED
""",
                encoding="utf-8",
            )

            result = self.run_checker("review", "--report", str(report))

        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        self.assertIn("FAIL [missing_title]", result.stdout)

    def test_review_rejects_misplaced_verification_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            report = Path(temp) / "review.md"
            report.write_text(
                """# TRIP Review

## Summary
- Command: `python3 tests/test_trip_lifecycle.py`
- Result: pass

## Findings
No blocking findings.

## Verification

## Verdict
Verdict: APPROVED
""",
                encoding="utf-8",
            )
            result = self.run_checker("review", "--report", str(report))

        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        self.assertIn("FAIL [missing_command]", result.stdout)

    def test_review_rejects_misplaced_evidence_even_with_valid_verification(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            report = Path(temp) / "review.md"
            report.write_text(
                """# TRIP Review

## Summary
- Command: false
- Result: pass

## Findings
No blocking findings.

## Verification
- Command: `python3 tests/test_trip_lifecycle.py`
- Result: pass

## Verdict
Verdict: APPROVED
""",
                encoding="utf-8",
            )
            result = self.run_checker("review", "--report", str(report))

        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        self.assertIn("FAIL [misplaced_verification_evidence]", result.stdout)

    def test_review_rejects_failed_evidence_for_approved(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            report = Path(temp) / "review.md"
            report.write_text("""# TRIP Review

## Summary
Ready.

## Findings
None.

## Verification
- Command: false
- Result: fail
- Command: true
- Result: pass

## Verdict
Verdict: APPROVED
""", encoding="utf-8")
            result = self.run_checker("review", "--report", str(report))
        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        self.assertIn("FAIL [approved_nonpass_result]", result.stdout)

    def test_review_rejects_orphan_verification_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            report = Path(temp) / "review.md"
            report.write_text("""# TRIP Review

## Summary
Ready.

## Findings
None.

## Verification
- Result: pass

## Verdict
Verdict: REQUEST_CHANGES
""", encoding="utf-8")
            result = self.run_checker("review", "--report", str(report))
        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        self.assertIn("FAIL [malformed_verification_evidence]", result.stdout)

    def test_release_accepts_evidence_with_pending_side_effects(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repo = self.make_repo(temp)
            (repo / "tracked.txt").write_text("after\n", encoding="utf-8")
            (repo / "untracked.txt").write_text("new\n", encoding="utf-8")
            package = Path(temp) / "release.json"
            package.write_text(
                json.dumps(
                    {
                        "ope_issue": "OPE-305",
                        "run_name": "ope-305-trip-protocol",
                        "plan_version": 2,
                        "commit_message": "feat: add native TRIP protocol",
                        "changed_files": [
                            "tracked.txt",
                            "untracked.txt",
                        ],
                        "verification": [
                            {
                                "command": f"{sys.executable} -c 'pass'",
                                "result": "pass",
                            }
                        ],
                        "side_effects": [
                            {"name": "commit", "status": "pending"},
                            {"name": "push", "status": "pending"},
                            {"name": "pr", "status": "pending"},
                        ],
                    }
                ),
                encoding="utf-8",
            )

            result = self.run_checker(
                "release", "--package", str(package), "--repo", str(repo),
                "--expected-run-name", "ope-305-trip-protocol",
                "--verify-command", f"{sys.executable} -c 'pass'",
            )

        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("PASS [release_contract]: 3 side effects pending", result.stdout)

    def test_release_rejects_unreported_or_nonexistent_changes(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repo = self.make_repo(temp)
            (repo / "tracked.txt").write_text("after\n", encoding="utf-8")
            (repo / "untracked.txt").write_text("new\n", encoding="utf-8")
            package = Path(temp) / "release.json"
            package.write_text(json.dumps({
                "ope_issue": "OPE-305", "run_name": "ope-305-trip-protocol", "plan_version": 1,
                "commit_message": "test", "changed_files": ["does-not-exist.txt"],
                "verification": [{"command": f"{sys.executable} -c 'pass'", "result": "pass"}],
                "side_effects": [{"name": "commit", "status": "pending"}],
            }), encoding="utf-8")
            result = self.run_checker(
                "release", "--package", str(package), "--repo", str(repo),
                "--expected-run-name", "ope-305-trip-protocol",
                "--verify-command", f"{sys.executable} -c 'pass'",
            )

        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        self.assertIn("FAIL [changed_files_mismatch]", result.stdout)

    def test_release_uses_the_net_diff_from_head(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repo = self.make_repo(temp)
            (repo / "tracked.txt").write_text("staged\n", encoding="utf-8")
            subprocess.run(["git", "-C", str(repo), "add", "tracked.txt"], check=True)
            (repo / "tracked.txt").write_text("before\n", encoding="utf-8")
            package = Path(temp) / "release.json"
            package.write_text(json.dumps({
                "ope_issue": "OPE-305", "run_name": "ope-305-trip-protocol", "plan_version": 1,
                "commit_message": "test", "changed_files": ["tracked.txt"],
                "verification": [{"command": f"{sys.executable} -c 'pass'", "result": "pass"}],
                "side_effects": [{"name": "commit", "status": "pending"}],
            }), encoding="utf-8")
            result = self.run_checker(
                "release", "--package", str(package), "--repo", str(repo),
                "--expected-run-name", "ope-305-trip-protocol",
                "--verify-command", f"{sys.executable} -c 'pass'",
            )

        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        self.assertIn("FAIL [changed_files_mismatch]", result.stdout)

    def test_release_executes_a_command_claimed_as_pass(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repo = self.make_repo(temp)
            (repo / "tracked.txt").write_text("after\n", encoding="utf-8")
            package = Path(temp) / "release.json"
            package.write_text(json.dumps({
                "ope_issue": "OPE-305", "run_name": "ope-305-trip-protocol", "plan_version": 1,
                "commit_message": "test", "changed_files": ["tracked.txt"],
                "verification": [{"command": "false", "result": "pass"}],
                "side_effects": [{"name": "commit", "status": "pending"}],
            }), encoding="utf-8")
            result = self.run_checker(
                "release", "--package", str(package), "--repo", str(repo),
                "--expected-run-name", "ope-305-trip-protocol", "--verify-command", "false",
            )

        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        self.assertIn("FAIL [verification_command_failed]", result.stdout)

    def test_release_times_out_a_slow_verify_command(self) -> None:
        slow = f"{sys.executable} -c 'import time; time.sleep(5)'"
        with tempfile.TemporaryDirectory() as temp:
            repo = self.make_repo(temp)
            (repo / "tracked.txt").write_text("after\n", encoding="utf-8")
            package = Path(temp) / "release.json"
            package.write_text(json.dumps({
                "ope_issue": "OPE-305", "run_name": "ope-305-trip-protocol", "plan_version": 1,
                "commit_message": "test", "changed_files": ["tracked.txt"],
                "verification": [{"command": slow, "result": "pass"}],
                "side_effects": [{"name": "commit", "status": "pending"}],
            }), encoding="utf-8")
            result = self.run_checker(
                "release", "--package", str(package), "--repo", str(repo),
                "--expected-run-name", "ope-305-trip-protocol",
                "--verify-command", slow, "--verify-timeout", "1",
            )

        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        self.assertIn("FAIL [verification_timeout]", result.stdout)
        self.assertIn("timed out after 1s", result.stdout)

    def test_release_rejects_missing_verification_result(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repo = self.make_repo(temp)
            (repo / "tracked.txt").write_text("after\n", encoding="utf-8")
            package = Path(temp) / "release.json"
            package.write_text(json.dumps({
                "ope_issue": "OPE-305", "run_name": "ope-305-trip-protocol", "plan_version": 1,
                "commit_message": "test", "changed_files": ["tracked.txt"],
                "verification": [{"command": f"{sys.executable} -c 'pass'"}],
                "side_effects": [{"name": "commit", "status": "pending"}],
            }), encoding="utf-8")
            result = self.run_checker(
                "release", "--package", str(package), "--repo", str(repo),
                "--expected-run-name", "ope-305-trip-protocol",
                "--verify-command", f"{sys.executable} -c 'pass'",
            )

        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        self.assertIn("FAIL [invalid_verification_result]", result.stdout)

    def test_release_rejects_a_nonpass_verification_result(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repo = self.make_repo(temp)
            (repo / "tracked.txt").write_text("after\n", encoding="utf-8")
            package = Path(temp) / "release.json"
            package.write_text(json.dumps({
                "ope_issue": "OPE-305", "run_name": "ope-305-trip-protocol", "plan_version": 1,
                "commit_message": "test", "changed_files": ["tracked.txt"],
                "verification": [{"command": f"{sys.executable} -c 'pass'", "result": "fail"}],
                "side_effects": [{"name": "commit", "status": "pending"}],
            }), encoding="utf-8")
            result = self.run_checker(
                "release", "--package", str(package), "--repo", str(repo),
                "--expected-run-name", "ope-305-trip-protocol",
                "--verify-command", f"{sys.executable} -c 'pass'",
            )

        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        self.assertIn("FAIL [invalid_verification_result]", result.stdout)

    def test_release_rejects_a_mismatched_issue(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repo = self.make_repo(temp)
            (repo / "tracked.txt").write_text("after\n", encoding="utf-8")
            package = Path(temp) / "release.json"
            command = f"{sys.executable} -c 'pass'"
            package.write_text(json.dumps({
                "ope_issue": "OPE-999", "run_name": "ope-305-trip-protocol", "plan_version": 1,
                "commit_message": "test", "changed_files": ["tracked.txt"],
                "verification": [{"command": command, "result": "pass"}],
                "side_effects": [{"name": "commit", "status": "pending"}],
            }), encoding="utf-8")
            result = self.run_checker(*self.release_args(package, repo, command))
        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        self.assertIn("FAIL [issue_mismatch]", result.stdout)

    def test_release_round_trips_special_git_paths(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repo = self.make_repo(temp)
            (repo / "tracked.txt").write_text("after\n", encoding="utf-8")
            names = ["line\nbreak.txt", "tab\tname.txt", 'quote"name.txt', r"slash\\name.txt", "café.txt"]
            for name in names:
                (repo / name).write_text("new\n", encoding="utf-8")
            package = Path(temp) / "release.json"
            command = f"{sys.executable} -c 'pass'"
            package.write_text(json.dumps({
                "ope_issue": "OPE-305", "run_name": "ope-305-trip-protocol", "plan_version": 1,
                "commit_message": "test", "changed_files": ["tracked.txt", *names],
                "verification": [{"command": command, "result": "pass"}],
                "side_effects": [{"name": "commit", "status": "pending"}],
            }), encoding="utf-8")
            result = self.run_checker(*self.release_args(package, repo, command))
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python3
"""Validate native TRIP lifecycle artifacts composed from Ringer manifests."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

TRIP_PHASES = ("plan", "implement", "review", "release")
REVIEW_VERDICTS = ("APPROVED", "REQUEST_CHANGES", "NEEDS_REWORK")
REVIEW_HEADINGS = ("Summary", "Findings", "Verification", "Verdict")
ISSUE_RE = re.compile(r"^OPE-\d+$")


def fail(name: str, detail: str) -> str:
    return f"FAIL [{name}]: {detail}"


def nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate_manifest(path: Path, ringer: Path, expected_run_name: str, expected_issue: str) -> list[str]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return [fail("missing_manifest", f"{path} does not exist")]
    except json.JSONDecodeError as exc:
        return [fail("invalid_json", f"{path} is not valid JSON: {exc}")]

    if not isinstance(data, dict):
        return [fail("invalid_manifest", "manifest root must be a JSON object")]

    failures: list[str] = []
    trip = data.get("trip")
    if not isinstance(trip, dict):
        return [fail("missing_trip", "manifest must contain a trip object")]

    issue = trip.get("issue")
    if not nonempty_string(issue) or not ISSUE_RE.fullmatch(issue.strip()):
        failures.append(fail("invalid_issue", "trip.issue must be an OPE issue key such as OPE-305"))
    elif issue != expected_issue:
        failures.append(fail("issue_mismatch", "trip.issue must exactly equal --expected-issue"))

    phase = trip.get("phase")
    if phase not in TRIP_PHASES:
        failures.append(fail("invalid_phase", f"trip.phase must be one of: {', '.join(TRIP_PHASES)}"))

    plan_version = trip.get("plan_version")
    if isinstance(plan_version, bool) or not isinstance(plan_version, int) or plan_version < 1:
        failures.append(fail("invalid_plan_version", "trip.plan_version must be a positive integer"))

    run_name = data.get("run_name")
    if not nonempty_string(run_name):
        failures.append(fail("invalid_run_name", "run_name must be a non-empty string"))
    elif run_name != expected_run_name:
        failures.append(fail("run_name_mismatch", "run_name must exactly equal --expected-run-name"))
    elif run_name != expected_issue.lower() and not run_name.startswith(expected_issue.lower() + "-"):
        failures.append(fail("run_name_issue_mismatch", "run_name must be the expected issue or start with it"))

    # Execute ringer directly: it is a #!/bin/sh polyglot that self-selects a
    # supported Python; running it via sys.executable bypasses that and makes
    # the lint verdict depend on the checker's own interpreter.
    try:
        lint = subprocess.run(
            [str(ringer.resolve()), "lint", str(path)],
            capture_output=True,
            text=True,
            timeout=60,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        failures.append(fail("ringer_lint_failed", f"cannot lint manifest: {exc}"))
    else:
        if lint.returncode:
            failures.append(fail("ringer_lint_failed", "Ringer lint rejected the manifest"))

    tasks = data.get("tasks")
    if not isinstance(tasks, list) or not tasks:
        failures.append(fail("invalid_tasks", "tasks must be a non-empty list"))
        return failures

    for index, task in enumerate(tasks, start=1):
        if not isinstance(task, dict):
            failures.append(fail("invalid_task", f"task {index} must be a JSON object"))
            continue
        key = task.get("key") if nonempty_string(task.get("key")) else f"#{index}"
        for field in ("spec", "check", "verified", "task_type"):
            if not nonempty_string(task.get(field)):
                failures.append(fail("missing_task_field", f"task {key}: {field} must be a non-empty string"))
        expect_files = task.get("expect_files")
        if (
            not isinstance(expect_files, list)
            or not expect_files
            or not all(nonempty_string(item) for item in expect_files)
        ):
            failures.append(
                fail("invalid_expect_files", f"task {key}: expect_files must be a non-empty list of strings")
            )

    return failures


def validate_review(path: Path) -> tuple[list[str], str]:
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return [fail("missing_review", f"{path} does not exist")], ""
    if not text.strip():
        return [fail("empty_review", f"{path} is empty")], ""

    failures: list[str] = []
    nonempty_lines = [line.strip() for line in text.splitlines() if line.strip()]
    if not re.fullmatch(r"#\s+TRIP Review", nonempty_lines[0], re.IGNORECASE):
        failures.append(fail("missing_title", "review must start with '# TRIP Review'"))
    sections = re.findall(r"^##\s+(.+?)\s*$", text, re.MULTILINE)
    if tuple(sections) != REVIEW_HEADINGS:
        failures.append(
            fail(
                "invalid_sections",
                "level-two headings must be exactly: Summary, Findings, Verification, Verdict",
            )
        )

    verification = ""
    verification_match = re.search(
        r"^##\s+Verification\s*$\n(.*?)(?=^##\s+|\Z)", text, re.MULTILINE | re.DOTALL
    )
    if verification_match:
        verification = verification_match.group(1)
    evidence_outside_verification = text[: verification_match.start()] + text[verification_match.end() :] if verification_match else text
    if re.search(r"^\s*[-*]?\s*(?:Command|Result):", evidence_outside_verification, re.IGNORECASE | re.MULTILINE):
        failures.append(
            fail("misplaced_verification_evidence", "Command and Result evidence must appear only in Verification")
        )
    evidence_lines = [line.strip() for line in verification.splitlines() if line.strip()]
    results: list[str] = []
    if not evidence_lines:
        failures.append(fail("missing_command", "Verification must cite at least one executed command"))
    else:
        for index in range(0, len(evidence_lines), 2):
            command = re.fullmatch(r"[-*]?\s*Command:\s*(\S.*)", evidence_lines[index], re.IGNORECASE)
            result = (
                re.fullmatch(r"[-*]?\s*Result:\s*(\S.*)", evidence_lines[index + 1], re.IGNORECASE)
                if index + 1 < len(evidence_lines)
                else None
            )
            if not command or not result:
                failures.append(fail("malformed_verification_evidence", "Verification must contain immediate Command/Result pairs"))
                break
            results.append(result.group(1))

    verdicts = re.findall(
        rf"^Verdict:\s*({'|'.join(REVIEW_VERDICTS)})\s*$",
        text,
        re.MULTILINE,
    )
    if len(verdicts) != 1:
        failures.append(
            fail(
                "invalid_verdict",
                "review must contain exactly one verdict: APPROVED, REQUEST_CHANGES, or NEEDS_REWORK",
            )
        )
    elif nonempty_lines[-1] != f"Verdict: {verdicts[0]}":
        failures.append(fail("verdict_not_final", "the verdict must be the final non-empty line"))
    elif verdicts[0] == "APPROVED" and any(result != "pass" for result in results):
        failures.append(fail("approved_nonpass_result", "APPROVED requires every Verification result to be exactly pass"))
    return failures, verdicts[0] if len(verdicts) == 1 else ""


def tracked_and_untracked_changes(repo: Path) -> tuple[list[str], Path | None, str | None]:
    try:
        root = subprocess.run(
            ["git", "-C", str(repo), "rev-parse", "--show-toplevel"],
            capture_output=True,
            timeout=10,
            check=True,
        ).stdout
        root = os.fsdecode(root).strip()
        names: set[str] = set()
        for command in (
            ["diff", "--name-only", "-z", "HEAD"],
            ["ls-files", "--others", "--exclude-standard", "-z"],
        ):
            result = subprocess.run(
                ["git", "-C", root, *command],
                capture_output=True,
                timeout=10,
                check=True,
            )
            names.update(os.fsdecode(item) for item in result.stdout.split(b"\0") if item)
    except (OSError, subprocess.SubprocessError) as exc:
        return [], None, str(exc)
    return sorted(names), Path(root), None


def validate_release(
    path: Path,
    repo: Path,
    expected_run_name: str,
    expected_issue: str,
    verify_commands: list[str],
    verify_timeout: int = 600,
) -> tuple[list[str], int]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return [fail("missing_release", f"{path} does not exist")], 0
    except json.JSONDecodeError as exc:
        return [fail("invalid_json", f"{path} is not valid JSON: {exc}")], 0
    if not isinstance(data, dict):
        return [fail("invalid_release", "release package root must be a JSON object")], 0

    failures: list[str] = []
    issue = data.get("ope_issue")
    if not nonempty_string(issue) or not ISSUE_RE.fullmatch(issue.strip()):
        failures.append(fail("invalid_issue", "ope_issue must be an OPE issue key such as OPE-305"))
    elif issue != expected_issue:
        failures.append(fail("issue_mismatch", "ope_issue must exactly equal --expected-issue"))
    run_name = data.get("run_name")
    if not nonempty_string(run_name):
        failures.append(fail("invalid_run_name", "run_name must be a non-empty string"))
    elif run_name != expected_run_name:
        failures.append(fail("run_name_mismatch", "run_name must exactly equal --expected-run-name"))
    elif run_name != expected_issue.lower() and not run_name.startswith(expected_issue.lower() + "-"):
        failures.append(fail("run_name_issue_mismatch", "run_name must be the expected issue or start with it"))

    plan_version = data.get("plan_version")
    if isinstance(plan_version, bool) or not isinstance(plan_version, int) or plan_version < 1:
        failures.append(fail("invalid_plan_version", "plan_version must be a positive integer"))
    if not nonempty_string(data.get("commit_message")):
        failures.append(fail("missing_commit_message", "commit_message must be a non-empty string"))

    changed_files = data.get("changed_files")
    if (
        not isinstance(changed_files, list)
        or not changed_files
        or not all(nonempty_string(item) for item in changed_files)
    ):
        failures.append(fail("invalid_changed_files", "changed_files must be a non-empty list of strings"))
    else:
        actual_changes, repo_root, error = tracked_and_untracked_changes(repo)
        if error:
            failures.append(fail("invalid_repo", f"cannot inspect --repo {repo}: {error}"))
        elif set(changed_files) != set(actual_changes) or len(changed_files) != len(set(changed_files)):
            failures.append(
                fail(
                    "changed_files_mismatch",
                    f"changed_files must equal Git changes in {repo_root}: {', '.join(actual_changes) or '(none)'}",
                )
            )

    verification = data.get("verification")
    if not isinstance(verification, list) or not verification:
        failures.append(fail("missing_verification", "verification must contain at least one executed check"))
    else:
        package_commands: list[str] = []
        for index, item in enumerate(verification, start=1):
            if not isinstance(item, dict) or not nonempty_string(item.get("command")):
                failures.append(fail("invalid_verification", f"verification {index} must name a command"))
                continue
            if item.get("result") != "pass":
                failures.append(fail("invalid_verification_result", f"verification {index} result must be exactly 'pass'"))
            package_commands.append(item["command"])
        if package_commands != verify_commands:
            failures.append(
                fail("verification_commands_mismatch", "verification commands must exactly match --verify-command")
            )
        elif package_commands == verify_commands:
            for command in verify_commands:
                try:
                    result = subprocess.run(
                        command,
                        shell=True,
                        cwd=repo,
                        capture_output=True,
                        text=True,
                        timeout=verify_timeout,
                    )
                except subprocess.TimeoutExpired:
                    failures.append(fail("verification_timeout", f"command timed out after {verify_timeout}s: {command}"))
                    continue
                if result.returncode:
                    failures.append(
                        fail(
                            "verification_command_failed",
                            f"command exited {result.returncode}: {command}",
                        )
                    )

    side_effects = data.get("side_effects")
    pending_count = len(side_effects) if isinstance(side_effects, list) else 0
    if not isinstance(side_effects, list) or not side_effects:
        failures.append(fail("missing_side_effects", "side_effects must list at least one pending OE action"))
    else:
        names: list[str] = []
        for index, item in enumerate(side_effects, start=1):
            if not isinstance(item, dict) or not nonempty_string(item.get("name")):
                failures.append(fail("invalid_side_effect", f"side effect {index} must name an action"))
                continue
            name = item["name"].strip()
            names.append(name)
            if not re.fullmatch(r"[a-z][a-z0-9_-]*", name):
                failures.append(fail("invalid_side_effect", f"side effect name is not a stable slug: {name!r}"))
            if item.get("status") != "pending":
                failures.append(
                    fail("side_effect_not_pending", f"side effect {name!r} must remain pending for OE")
                )
        if len(names) != len(set(names)):
            failures.append(fail("duplicate_side_effect", "side effect names must be unique checkpoints"))
    return failures, pending_count


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Ringer TRIP lifecycle contracts.")
    subparsers = parser.add_subparsers(dest="mode", required=True)

    manifest = subparsers.add_parser("manifest")
    manifest.add_argument("--manifest", required=True, type=Path)
    manifest.add_argument("--ringer", required=True, type=Path)
    manifest.add_argument("--expected-run-name", required=True)
    manifest.add_argument("--expected-issue", required=True)

    review = subparsers.add_parser("review")
    review.add_argument("--report", required=True, type=Path)

    release = subparsers.add_parser("release")
    release.add_argument("--package", required=True, type=Path)
    release.add_argument("--repo", required=True, type=Path)
    release.add_argument("--expected-run-name", required=True)
    release.add_argument("--expected-issue", required=True)
    release.add_argument("--verify-command", action="append", required=True)
    release.add_argument("--verify-timeout", type=int, default=600, help="seconds allowed per verify command")

    args = parser.parse_args()
    if args.mode == "manifest":
        failures = validate_manifest(args.manifest, args.ringer, args.expected_run_name, args.expected_issue)
        pass_message = "PASS [manifest_contract]: manifest identifies one verified TRIP phase round"
    elif args.mode == "review":
        failures, verdict = validate_review(args.report)
        pass_message = f"PASS [review_contract]: {verdict}"
    else:
        failures, pending_count = validate_release(
            args.package, args.repo, args.expected_run_name, args.expected_issue, args.verify_command,
            verify_timeout=args.verify_timeout,
        )
        pass_message = f"PASS [release_contract]: {pending_count} side effects pending"
    if failures:
        for item in failures:
            print(item)
        return 1
    print(pass_message)
    return 0


if __name__ == "__main__":
    sys.exit(main())

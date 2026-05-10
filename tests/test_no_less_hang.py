"""Verify that `less` and pager-using commands do not hang in a new session.

The common issue: when a new subprocess/session is created without a TTY,
invoking `less` (or commands that default to using `less` as a pager)
will block waiting for interactive input that never comes.

The fix: ensure environment variables are set to prevent pager hangs:
- PAGER=cat      — use cat as the default pager
- GIT_PAGER=cat  — use cat for git commands
- LESS=-RFQ      — quit-if-one-screen, raw-control-chars, quiet
"""

import os
import subprocess
import time


def _base_env() -> dict[str, str]:
    """Return a copy of the current environment with pager-safe overrides."""
    env = os.environ.copy()
    env.setdefault("PAGER", "cat")
    env.setdefault("GIT_PAGER", "cat")
    env.setdefault("LESS", "-RFQ")
    return env


def _run_with_timeout(
    args: list[str],
    timeout: float = 5.0,
    env: dict[str, str] | None = None,
    input: bytes | None = None,
) -> subprocess.CompletedProcess:
    """Run a command and assert it finishes within *timeout* seconds."""
    return subprocess.run(
        args,
        capture_output=True,
        timeout=timeout,
        env=env or _base_env(),
        input=input,
    )


# --- less behaviour -------------------------------------------------------


class TestLessNoHang:
    """Verify `less` does not hang when invoked in a non-interactive session."""

    def test_less_flag_F_exits_cleanly(self):
        """`less -F` (quit-if-one-screen) should exit without user input."""
        proc = _run_with_timeout(["less", "-F"], input=b"short content\n")
        assert proc.returncode == 0

    def test_less_with_env_QUIT_immediately(self):
        """`LESS=-F` environment makes bare `less` quit on short output."""
        env = _base_env()
        env["LESS"] = "-F"
        proc = _run_with_timeout(["less"], input=b"short content\n", env=env)
        assert proc.returncode == 0

    def test_less_empty_input_exits(self):
        """`less -F` with empty input should not hang."""
        proc = _run_with_timeout(["less", "-F"], input=b"")
        assert proc.returncode == 0


# --- git pager behaviour --------------------------------------------------


class TestGitPagerNoHang:
    """Verify git commands that use a pager do not hang."""

    def test_git_log_no_pager(self):
        """`git --no-pager log` should never hang."""
        proc = _run_with_timeout(["git", "--no-pager", "log", "--oneline", "-1"])
        assert proc.returncode == 0
        assert len(proc.stdout) > 0

    def test_git_log_with_pager_cat(self):
        """`git log` with GIT_PAGER=cat should not hang."""
        env = _base_env()
        env["GIT_PAGER"] = "cat"
        proc = _run_with_timeout(["git", "log", "--oneline", "-1"], env=env)
        assert proc.returncode == 0
        assert len(proc.stdout) > 0

    def test_git_diff_with_pager_cat(self):
        """`git diff` with GIT_PAGER=cat should not hang."""
        env = _base_env()
        env["GIT_PAGER"] = "cat"
        proc = _run_with_timeout(["git", "diff", "HEAD"], env=env)
        assert proc.returncode == 0


# --- environment defaults -------------------------------------------------


class TestPagerEnvironmentDefaults:
    """Verify the pager-safe environment variables are present."""

    def test_pager_env_set(self):
        """PAGER should be set to a non-interactive value in the base env."""
        env = _base_env()
        assert env.get("PAGER") in ("cat", "less -F", "less -RFQ")

    def test_git_pager_env_set(self):
        """GIT_PAGER should be set to a non-interactive value in the base env."""
        env = _base_env()
        assert env.get("GIT_PAGER") in ("cat", "less -F", "less -RFQ")

    def test_less_env_set(self):
        """LESS should contain flags that prevent hangs (-F or -q or -Q)."""
        env = _base_env()
        less_val = env.get("LESS", "")
        # At least one of the quit-early/quit-on-eof flags should be present
        assert any(flag in less_val for flag in ("F", "q", "Q")), (
            f"LESS={less_val!r} lacks a quit-early flag (F/q/Q)"
        )


# --- subshell integration test -------------------------------------------


class TestNewSessionNoHang:
    """Integration test: a fresh subprocess session should not hang on pagers."""

    def test_subshell_git_log(self):
        """A subshell running `git log` with safe env should complete quickly."""
        env = _base_env()
        start = time.monotonic()
        proc = subprocess.run(
            ["bash", "-c", "git log --oneline -1"],
            capture_output=True,
            timeout=5,
            env=env,
        )
        elapsed = time.monotonic() - start
        assert proc.returncode == 0
        assert elapsed < 4.0, f"git log took {elapsed:.1f}s — possible pager hang"

    def test_subshell_echo_pipe_less(self):
        """A subshell piping to `less -F` should complete quickly."""
        env = _base_env()
        start = time.monotonic()
        proc = subprocess.run(
            ["bash", "-c", "echo hello | less -F"],
            capture_output=True,
            timeout=5,
            env=env,
        )
        elapsed = time.monotonic() - start
        assert proc.returncode == 0
        assert elapsed < 4.0, f"less -F took {elapsed:.1f}s — possible hang"

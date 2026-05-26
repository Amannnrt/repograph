import subprocess

from repograph.core.models import (
    GitMetadata,
)


def run_git_command(
    repo_path: str,
    args: list[str],
) -> str:

    result = subprocess.run(
        ["git", *args],
        cwd=repo_path,
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        return ""

    return result.stdout.strip()


def get_file_git_metadata(
    *,
    repo_path: str,
    relative_file_path: str,
) -> GitMetadata:

    latest_commit = run_git_command(
        repo_path,
        [
            "log",
            "-1",
            "--pretty=format:%H|%an|%ad|%s",
            "--",
            relative_file_path,
        ],
    )

    if not latest_commit:
        return GitMetadata()

    parts = latest_commit.split(
        "|",
        maxsplit=3,
    )

    if len(parts) != 4:
        return GitMetadata()

    (
        commit_hash,
        author,
        timestamp,
        message,
    ) = parts

    commit_count = run_git_command(
        repo_path,
        [
            "rev-list",
            "--count",
            "HEAD",
            "--",
            relative_file_path,
        ],
    )

    try:
        change_frequency = int(
            commit_count
        )
    except ValueError:
        change_frequency = 0

    return GitMetadata(
        commit_hash=commit_hash,
        author=author,
        commit_message=message,
        commit_timestamp=timestamp,
        change_frequency=change_frequency,
    )

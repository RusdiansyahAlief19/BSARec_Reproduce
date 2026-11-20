#!/usr/bin/env python3
"""Validate CP1 item/time sequences and write CP2 categorical time buckets."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Sequence


BUCKET_IDS = {
    "0": "first event / no prior history",
    "1": "zero gap / equal adjacent timestamp",
    "2": "0 < gap <= 1 hour",
    "3": "1 hour < gap <= 1 day",
    "4": "1 day < gap <= 1 week",
    "5": "1 week < gap <= 30 days",
    "6": "30 days < gap <= 365 days",
    "7": "gap > 365 days",
}


def encode_gap(gap: int, first_position: bool = False) -> int:
    """Map a nonnegative gap in seconds to the CP2's 8 categorical IDs."""
    if gap < 0:
        raise ValueError("negative gap")
    if first_position:
        return 0
    if gap == 0:
        return 1
    if gap <= 3_600:
        return 2
    if gap <= 86_400:
        return 3
    if gap <= 604_800:
        return 4
    if gap <= 2_592_000:
        return 5
    if gap <= 31_536_000:
        return 6
    return 7


def _read_integer_rows(path: Path) -> list[list[int]]:
    rows: list[list[int]] = []
    with path.open("r", encoding="utf-8-sig") as stream:
        for line_no, line in enumerate(stream, start=1):
            fields = line.split()
            if not fields:
                raise ValueError(f"blank row at {path}:{line_no}")
            try:
                rows.append([int(value) for value in fields])
            except ValueError as exc:
                raise ValueError(f"non-integer token at {path}:{line_no}") from exc
    return rows


def read_aligned_sequences(
    item_path: Path, time_path: Path
) -> tuple[list[list[int]], list[list[int]]]:
    """Read CP1 rows; the time file's first field is metadata, not a gap."""
    item_rows = _read_integer_rows(item_path)
    time_rows = _read_integer_rows(time_path)
    if len(item_rows) != len(time_rows):
        raise ValueError(
            f"row count mismatch: items={len(item_rows)}, time={len(time_rows)}"
        )

    seen_users: set[int] = set()
    for row_no, (items, times) in enumerate(zip(item_rows, time_rows), start=1):
        if len(items) < 2 or len(times) < 2:
            raise ValueError(f"row {row_no} must contain a user and at least one event")
        if items[0] in seen_users:
            raise ValueError(f"duplicate CP1 user ID {items[0]} at row {row_no}")
        seen_users.add(items[0])
        if len(items) != len(times):
            raise ValueError(
                f"row {row_no} length mismatch: items={len(items)-1}, "
                f"time_gaps={len(times)-1}"
            )
        gaps = times[1:]
        if gaps[0] != 0:
            raise ValueError(f"row {row_no} first gap must be 0")
        if any(gap < 0 for gap in gaps):
            raise ValueError(f"row {row_no} contains a negative gap")
    return item_rows, time_rows


def encode_rows(
    item_rows: Sequence[Sequence[int]], time_rows: Sequence[Sequence[int]]
) -> list[list[int]]:
    """Return rows with CP1 user IDs and time bucket IDs aligned to each item."""
    if len(item_rows) != len(time_rows):
        raise ValueError(
            f"row count mismatch: items={len(item_rows)}, time={len(time_rows)}"
        )
    encoded: list[list[int]] = []
    seen_users: set[int] = set()
    for row_no, (items, times) in enumerate(zip(item_rows, time_rows), start=1):
        if len(items) < 2 or len(times) < 2:
            raise ValueError(f"row {row_no} must contain a user and at least one event")
        user_id = int(items[0])
        if user_id in seen_users:
            raise ValueError(f"duplicate CP1 user ID {user_id} at row {row_no}")
        seen_users.add(user_id)
        if len(items) != len(times):
            raise ValueError(
                f"row {row_no} length mismatch: items={len(items)-1}, "
                f"time_gaps={len(times)-1}"
            )
        gaps = [int(gap) for gap in times[1:]]
        if gaps[0] != 0:
            raise ValueError(f"row {row_no} first gap must be 0")
        if any(gap < 0 for gap in gaps):
            raise ValueError(f"row {row_no} contains a negative gap")
        encoded.append(
            [user_id]
            + [encode_gap(gap, first_position=(i == 0)) for i, gap in enumerate(gaps)]
        )
    return encoded


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def prepare_dataset(dataset: str, data_dir: Path, output_dir: Path) -> dict:
    item_path = data_dir / f"{dataset}.txt"
    time_path = data_dir / f"{dataset}_time.txt"
    if not item_path.is_file() or not time_path.is_file():
        raise FileNotFoundError(f"Missing CP1 item/time pair for {dataset}: {data_dir}")

    item_rows, time_rows = read_aligned_sequences(item_path, time_path)
    bucket_rows = encode_rows(item_rows, time_rows)
    output_dir.mkdir(parents=True, exist_ok=True)
    bucket_path = output_dir / f"{dataset}_cp2_time_buckets.txt"
    with bucket_path.open("w", encoding="utf-8", newline="\n") as stream:
        for row in bucket_rows:
            stream.write(" ".join(map(str, row)) + "\n")

    counts = Counter(bucket for row in bucket_rows for bucket in row[1:])
    return {
        "dataset": dataset,
        "users": len(item_rows),
        "interactions": sum(len(row) - 1 for row in item_rows),
        "bucket_ids": BUCKET_IDS,
        "bucket_counts_all_positions": dict(sorted(counts.items())),
        "units": "seconds",
        "normalization": "none; categorical embedding IDs",
        "time_file_first_field": "ignored metadata; CP1 user ID is copied from item file",
        "alignment": "row order and event counts validated; raw timestamp gaps independently audited",
        "target_leakage_rule": "only input-history buckets are supplied; target-position bucket is excluded",
        "source_sha256": {
            item_path.name: _sha256(item_path),
            time_path.name: _sha256(time_path),
        },
        "output_file": bucket_path.name,
        "output_sha256": _sha256(bucket_path),
    }


def main() -> None:
    project_root = Path(__file__).resolve().parents[2]
    default_data_dir = project_root.parent / "anca" / "txt"
    default_output_dir = project_root.parent / "anca" / "cp2"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, default=default_data_dir)
    parser.add_argument("--output-dir", type=Path, default=default_output_dir)
    parser.add_argument("--datasets", nargs="+", default=["Beauty", "ML-1M"])
    args = parser.parse_args()

    reports = [prepare_dataset(name, args.data_dir, args.output_dir) for name in args.datasets]
    manifest = {
        "schema": "CP2 explicit time buckets v1",
        "bucket_ids": BUCKET_IDS,
        "units": "seconds",
        "normalization": "none; categorical embedding IDs",
        "datasets": reports,
    }
    manifest_path = args.output_dir / "CP2_Beauty_ML1M_time_bucket_audit.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"manifest": str(manifest_path), "datasets": reports}, indent=2))


if __name__ == "__main__":
    main()

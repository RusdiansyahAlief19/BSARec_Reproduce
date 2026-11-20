import tempfile
import unittest
from pathlib import Path

from scripts.prepare_cp2_time_buckets import encode_gap, encode_rows, read_aligned_sequences


class TimeBucketTests(unittest.TestCase):
    def test_bucket_boundaries_follow_explicit_cp2_scheme(self):
        self.assertEqual(
            [encode_gap(gap, first_position=(i == 0)) for i, gap in enumerate(
                [0, 0, 1, 3600, 3601, 86400, 86401, 604800, 604801,
                 2592000, 2592001, 31536000, 31536001]
            )],
            [0, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7],
        )

    def test_time_metadata_is_dropped_and_cp1_user_id_is_preserved(self):
        item_rows = [[1, 10, 11, 12], [2, 20, 21]]
        time_rows = [[5585, 0, 0, 3601], [17505, 0, 86400]]
        self.assertEqual(encode_rows(item_rows, time_rows), [[1, 0, 1, 3], [2, 0, 3]])

    def test_rejects_item_time_length_mismatch(self):
        with self.assertRaisesRegex(ValueError, "length mismatch"):
            encode_rows([[1, 10, 11]], [[5585, 0]])

    def test_rejects_negative_or_nonzero_first_gap(self):
        with self.assertRaisesRegex(ValueError, "first gap"):
            encode_rows([[1, 10, 11]], [[5585, 2, 3]])
        with self.assertRaisesRegex(ValueError, "negative gap"):
            encode_rows([[1, 10, 11]], [[5585, 0, -1]])

    def test_reads_rows_without_requiring_time_metadata_to_match_user_id(self):
        with tempfile.TemporaryDirectory() as tmp:
            item_path = Path(tmp) / "items.txt"
            time_path = Path(tmp) / "times.txt"
            item_path.write_text("1 10 11\n2 20\n", encoding="utf-8")
            time_path.write_text("5585 0 0\n17505 0\n", encoding="utf-8")
            self.assertEqual(read_aligned_sequences(item_path, time_path), ([[1, 10, 11], [2, 20]], [[5585, 0, 0], [17505, 0]]))


if __name__ == "__main__":
    unittest.main()

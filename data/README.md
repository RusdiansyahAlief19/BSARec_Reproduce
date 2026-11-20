# Data files

Datasets and generated sequence files are intentionally kept out of Git. Acquire source data from the official/distribution sources and follow their terms. For local CP2 preprocessing, place the CP1 item/time pairs under `../anca/txt` relative to the repository, or pass `--data-dir` and `--output-dir` to `scripts/CP2/prepare_cp2_time_buckets.py`.

Expected file pairs include `Beauty.txt` / `Beauty_time.txt` and `ML-1M.txt` / `ML-1M_time.txt`. The LastFM timestamp source records tagging events; it should not be interpreted as listening history without additional validation.

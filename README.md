# BSARec Reproduction and Time-Aware Extension

**Maintainer: Anca — Lab KC, FILKOM.** This repository preserves Anca's experiment notebooks, preprocessing audits, results, reports, and presentation artifacts for Checkpoint 1 and Checkpoint 2. Some historical working folders used a different name; repository ownership and organization follow Anca's project workspace.

This project reproduces selected BSARec/SASRec experiments and evaluates a time-bucket extension to BSARec. It does not redistribute upstream source code, datasets, or model checkpoints.

## Research question

Does adding categorical time-gap embeddings to BSARec improve next-item recommendation? CP2 compares vanilla BSARec and time-aware BSARec on Beauty and MovieLens-1M using the same dataset-specific hyperparameters and paired seeds (42, 43, 44). LastFM is documented and audited, but is not included in the CP2 paired training comparison.

## Main findings

### CP2 paired results

| Dataset | Metric | Vanilla mean | Time-aware mean | Relative change | Paired seeds higher |
| --- | --- | ---: | ---: | ---: | ---: |
| Beauty | HR@10 | 0.09797 | 0.09830 | +0.34% | 1/3 |
| Beauty | NDCG@10 | 0.05903 | 0.05937 | +0.56% | 2/3 |
| ML-1M | HR@10 | 0.26507 | 0.27710 | +4.54% | 3/3 |
| ML-1M | NDCG@10 | 0.14700 | 0.15410 | +4.83% | 3/3 |

Across the six reported metrics, Beauty has very small mean gains and mixed paired-seed directions; the evidence does not show a clear practical improvement. ML-1M improves on all six mean metrics, with 17 of 18 metric-by-seed deltas positive. This is preliminary evidence that the effect depends on the dataset. There are only three seeds, metrics are rounded in the source logs, and no statistical significance test is reported; do not describe these results as statistically significant or universally generalizable.

- Per-seed table: [`results/CP2/paired_by_seed.csv`](results/CP2/paired_by_seed.csv)
- Aggregate table: [`results/CP2/summary.csv`](results/CP2/summary.csv)
- Executed paired notebook: [`notebooks/CP2/CP2_Paired_BSARec_Vanilla_vs_Time_Beauty_ML1M_executed.ipynb`](notebooks/CP2/CP2_Paired_BSARec_Vanilla_vs_Time_Beauty_ML1M_executed.ipynb)
- Time-bucket audit: [`reports/CP2/Beauty_ML1M_time_bucket_audit.json`](reports/CP2/Beauty_ML1M_time_bucket_audit.json)

The CP2 time feature uses eight categorical IDs: first event, zero gap, then positive gaps up to 1 hour, 1 day, 1 week, 30 days, 365 days, and over 365 days. No numeric normalization is applied to bucket IDs. Only history-position buckets are passed to the model; the target-position bucket is excluded. The configuration is in [`configs/CP2/time_bucket_config.json`](configs/CP2/time_bucket_config.json).

### CP1 reproduction

CP1 covers BSARec and SASRec runs on Beauty, LastFM, and ML-1M. Beauty and LastFM have three-seed result tables; the archived ML-1M baseline has one seed and should be treated as descriptive. The Beauty ablations use one seed per setting. Full tables and caveats are documented in the result files and the CP1 report.

- CP1 report: [`reports/CP1/Laporan_Progres_CP1_BSARec.docx`](reports/CP1/Laporan_Progres_CP1_BSARec.docx)
- CP1 presentation: [`presentations/CP1/BSARec_CP1_3Datasets.pptx`](presentations/CP1/BSARec_CP1_3Datasets.pptx)
- Dataset-specific notebooks: [`notebooks/CP1/`](notebooks/CP1/)
- CP1 result tables: [`results/CP1/`](results/CP1/)

The paper's time-aware sequential recommendation literature predates this project (for example, TiSASRec). Therefore CP2 is framed as an empirical BSARec extension/evaluation, not as the first method to use time intervals.

## Dataset and preprocessing notes

- **Beauty:** Amazon review interactions with event timestamps, transformed into the CP1 item/time sequence format and audited for row alignment before CP2 bucket generation.
- **MovieLens-1M:** ratings ordered by their source timestamps; CP1 item/time sequences were checked for matching row order and counts before CP2 bucket generation.
- **LastFM:** the available HetRec timestamp field describes artist-tag events, not listening/scrobble events. Audit files also caution that structural alignment does not prove every per-event timestamp is semantically correct. LastFM was therefore kept out of the CP2 paired training scope while its temporal semantics and alignment remain a separate validation concern. This is a scope decision, not a claim that the dataset is invalid.

Raw and processed datasets are not committed because of licensing, size, and redistribution constraints. See [`data/README.md`](data/README.md) for the local data layout and setup expectations. CP2 preprocessing reports and LastFM audits are in [`reports/CP2/`](reports/CP2/); Colab notebooks are in [`notebooks/CP2/`](notebooks/CP2/).

## Experimental controls and limitations

- Within each dataset, vanilla and time-aware runs use matched seeds and the same model hyperparameters. Beauty: learning rate 0.0005, alpha 0.7, c 5, 1 attention head, 4 data-loader workers. ML-1M: learning rate 0.001, alpha 0.9, c 3, 2 heads, 2 workers. Confirmed commands are stored in the paired notebook.
- The worker count is a data-loading/runtime setting, not a model contribution. It is held fixed within each dataset's vanilla/time pair; Beauty and ML-1M use different counts, so cross-dataset score comparisons are descriptive. The repository records the run settings but not a controlled reason for the cross-dataset difference; do not present it as a worker ablation or an exact paper configuration.
- The CP2 paired CSV is assembled from preserved notebook outputs: vanilla and Beauty values are stored in the analysis cell; ML-1M time-aware values are read from saved run logs. The resulting values match the displayed test outputs. Keep the executed notebook and logs with any future exports.
- The paired results use three seeds only. There is no formal significance test, no bucket-boundary sensitivity analysis, and no evidence that gains generalize to other recommendation models or datasets.
- CP1 reproductions differ from the paper in software/runtime environments and some run configurations. The repository documents those differences instead of attributing unexplained gaps to one cause.

## Repository layout

| Path | Contents |
| --- | --- |
| `notebooks/CP1/` | CP1 Beauty, LastFM, and ML-1M notebooks |
| `notebooks/CP2/` | CP2 paired runs, executed outputs, and LastFM audit notebooks |
| `scripts/CP1/` | CP1 comparison, plotting, and run scripts |
| `scripts/CP2/` | Time-bucket preprocessing and embedding-export helpers |
| `results/CP1/`, `results/CP2/` | Tabular experiment outputs, separated by checkpoint |
| `logs/CP1/`, `logs/CP2/` | Available logs; CP2 seed-42 logs are labeled as pilot logs |
| `reports/CP1/`, `reports/CP2/` | Progress report and audit/report artifacts |
| `figures/CP1/` | CP1 ablation figure |
| `presentations/CP1/` | CP1 deck |
| `configs/CP2/` | Time-bucket configuration |

## Reproduce CP2 preprocessing

The default local input path is `../anca/txt` relative to this repository, matching Anca's workspace directory after its rename. Alternatively pass explicit paths:

```bash
python scripts/CP2/prepare_cp2_time_buckets.py --data-dir PATH_TO_CP1_ITEM_TIME_FILES --output-dir PATH_TO_LOCAL_OUTPUT
```

The script expects paired `<dataset>.txt` and `<dataset>_time.txt` files for each requested dataset. It validates sequence alignment, writes bucket files and a JSON manifest, and prints SHA-256 digests. Keep those generated data files outside Git.

To continue a Colab run, use the runnable paired notebook in `notebooks/CP2/`; the executed copy is for inspection and reporting. Avoid rerunning long training cells just to view stored output.

## Upstream and data sources

- BSARec upstream: <https://github.com/yehjin-shin/BSARec>
- Audited upstream commit used by the CP2 runtime: `c80bdc0f1a889b78fe9a27e2058389cc84caea84`
- BSARec paper: Shin et al., AAAI 2024, <https://arxiv.org/abs/2312.10325>
- Data sources: Amazon Reviews (Beauty), GroupLens MovieLens-1M, and HetRec 2011 Last.fm. Obtain data directly from their official/distribution sources and follow their terms.

The repository intentionally excludes raw data, processed sequence files, checkpoints, runtime outputs, credentials, and temporary presentation build files.

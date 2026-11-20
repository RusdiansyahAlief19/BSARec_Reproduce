# Notebook index

## CP1 — reproduction

| Notebook | Dataset / purpose | Notes |
| --- | --- | --- |
| `CP1/BSARec_Beauty.ipynb` | Beauty: baseline, author checkpoint evaluation, and ablation | Saved training outputs are retained; some execution counters are absent. |
| `CP1/BSARec_LastFM.ipynb` | LastFM: strict preprocessing audit and main BSARec/SASRec runs | Dataset previews are omitted from saved outputs. |
| `CP1/BSARec_LastFM_EksperimenTambahan.ipynb` | LastFM: additional 2-worker/W&B experiment | Descriptive supplement; not the controlled worker experiment. |
| `CP1/BSARec_dan_SASRec_ML_1M.ipynb` | ML-1M: one seed per model | Treat the result as descriptive. |

## CP2 — time-aware BSARec

| Notebook | Purpose | Notes |
| --- | --- | --- |
| `CP2/CP2_Paired_BSARec_Vanilla_vs_Time_Beauty_ML1M_template.ipynb` | Runnable paired comparison | Use this for new runs after reviewing setup and inputs. |
| `CP2/CP2_Paired_BSARec_Vanilla_vs_Time_Beauty_ML1M_executed.ipynb` | Preserved paired run outputs | Inspection/reporting copy; contains the run outputs associated with `results/CP2/`. |
| `CP2/CP2_Paired_BSARec_Vanilla_vs_Time_Beauty_ML1M_LabGPU.ipynb` | Lab GPU variant | Separate runtime notebook. |
| `CP2/CP2_TimeAware_BSARec_Beauty_ML1M.ipynb` | Time-aware training workflow | Earlier workflow. |
| `CP2/CP2_TimeAware_BSARec_Beauty_ML1M_executed.ipynb` | Saved earlier outputs | Keep distinct from the final paired results. |
| `CP2/LastFM/` | LastFM preprocessing, audit, and bucket preparation notebooks | LastFM was not included in the paired CP2 training results. |

Raw data and generated time-bucket sequence files are excluded from Git. The executed paired notebook contains a mixture of captured metrics and parsed logs in its final reporting cell; it should be retained with the paired CSVs for auditability.

# BSARec_Reproduce

Reproduksi paper **"An Attentive Inductive Bias for Sequential Recommendation beyond the Self-Attention"** (BSARec, Shin, Choi, Wi, dan Park, AAAI 2024; [arXiv:2312.10325](https://arxiv.org/abs/2312.10325)) pada dataset Amazon Beauty, untuk Checkpoint 1 probation Lab KC (Lab Sistem Cerdas), FILKOM, 2026. Tim: Anca dan Renno.

Repositori ini **tidak berisi ulang kode atau data upstream**. Isinya: skrip perbandingan dan plot kami, hasil dalam bentuk CSV, grafik, log training, dan patch kecil untuk logging W&B. Kode model dan data diambil dari repositori resmi penulis: <https://github.com/yehjin-shin/BSARec> (commit yang dipakai: **[ isi hash dari `git -C BSARec rev-parse HEAD` ]**).

## Ringkasan hasil (Beauty)

Angka rata-rata 3 seed (42, 43, 44), dibandingkan dengan Table 2 paper. Detail per seed ada di `results/`.

| Metrik | BSARec paper | BSARec kami | Gap | SASRec paper | SASRec kami | Gap |
| --- | --- | --- | --- | --- | --- | --- |
| HR@5 | 0,0736 | 0,0703 | -4,5% | 0,0340 | 0,0341 | +0,2% |
| NDCG@5 | 0,0523 | 0,0501 | -4,1% | 0,0221 | 0,0218 | -1,2% |
| HR@10 | 0,1008 | 0,0980 | -2,8% | 0,0531 | 0,0533 | +0,4% |
| NDCG@10 | 0,0611 | 0,0591 | -3,3% | 0,0283 | 0,0280 | -1,1% |
| HR@20 | 0,1373 | 0,1334 | -2,8% | 0,0823 | 0,0823 | 0,0% |
| NDCG@20 | 0,0703 | 0,0680 | -3,3% | 0,0356 | 0,0353 | -0,8% |

- Checkpoint resmi penulis (`BSARec_Beauty_best`) memberi angka yang sama persis dengan Table 2 paper, jadi evaluasi kami benar.
- BSARec hasil latihan kami konsisten 2,8% sampai 4,5% di bawah paper; penyebabnya **belum teruji** (dugaan: perbedaan versi library dan GPU, lihat bagian lingkungan).
- SASRec sangat sensitif terhadap seed (std HR@5 0,0035); rata-rata tiga seed hampir sama dengan paper.
- BSARec mengungguli SASRec 62% sampai 130% di reproduksi kami (paper: 67% sampai 137%).

### Ablasi alpha dan c (satu seed, 42)

![Ablasi](figures/ablasi_beauty.png)

Alpha besar lebih baik dan mendatar di 0.5 sampai 0.9; c terbaik di 5 sampai 7. Dengan satu seed per titik, hanya alpha = 0.1 dan c = 1 yang bedanya cukup jelas dari noise antar seed (std HR@20 sekitar 0,0013). Tabel lengkap: `results/ablation_alpha_beauty.csv` dan `results/ablation_c_beauty.csv`.

## Struktur repositori

| Folder | Isi |
| --- | --- |
| `scripts/` | `compare_with_paper.py` (tabel gap vs paper), `plot_ablation.py` (tabel dan grafik ablasi), `run_baselines.sh`, `run_ablation.sh` |
| `results/` | CSV hasil per seed, mean, std, dan gap terhadap paper; CSV ablasi |
| `figures/` | Grafik ablasi |
| `logs/` | Log training (`.log`) tiap run |
| `patches/` | Patch logging W&B untuk `main.py` upstream |
| `notebooks/` | Notebook Colab yang dipakai |

## Cara mereproduksi

1. Dari root repo ini, ambil kode upstream (jangan di-commit; sudah masuk .gitignore) dan siapkan environment (lihat README upstream; kami memakai pip di Colab, bukan `bsarec_env.yaml`):
   ```
   git clone https://github.com/yehjin-shin/BSARec
   cd BSARec/src
   ```
2. (Opsional) terapkan patch W&B: `git apply ../../patches/wandb_logging.patch`.
3. Jalankan `bash ../../scripts/run_baselines.sh` (BSARec dan SASRec, 3 seed) dan `bash ../../scripts/run_ablation.sh` (sapuan alpha dan c). Satu run BSARec di Beauty memakan sekitar 15 sampai 25 menit di Tesla T4.
4. Dari root repo ini: `python scripts/compare_with_paper.py` dan `python scripts/plot_ablation.py`.

## Lingkungan

| Komponen | Reproduksi kami | Paper |
| --- | --- | --- |
| GPU | Tesla T4 (Google Colab) | NVIDIA RTX 3090 |
| Python | 3.13.16 | 3.9.7 |
| PyTorch | 2.11.0 (CUDA 13.0) | 1.8.1 (CUDA 11.1) |
| NumPy / SciPy | 2.1.3 / 1.16.3 | 1.24.3 / 1.11.1 |

Eksperimen dicatat di Weights & Biases (project `bsarec-repro`): **[ tautan W&B bila dibuat publik ]**.

## Data dan lisensi

Repositori upstream menyertakan data di `src/data`. Kami **tidak** menyalinnya ke sini. Beauty berasal dari Amazon Reviews (McAuley dkk., 2015) melalui hasil pra-pemrosesan repositori FMLP-Rec; ML-1M dari GroupLens; LastFM dari HetRec 2011. Lisensi tiap dataset: **[ ringkasan dari tab Anca; verifikasi ulang ke sumber resmi ]**. Repositori upstream saat dicek tidak mencantumkan berkas lisensi, sehingga kode upstream tidak kami salin; cukup di-clone dari sumbernya.

## Keterbatasan

Ablasi hanya satu seed per titik; baseline hanya tiga seed; penyebab selisih BSARec dengan paper belum teruji; baseline kuat (DuoRec, FEARec) tidak direproduksi; nondeterminisme GPU dapat mengubah digit terakhir (contoh: NDCG@20 seed 42 bernilai 0,0683 dan 0,0682 pada dua run).

## Rujukan

Shin, Y., Choi, J., Wi, H., dan Park, N. (2024). An Attentive Inductive Bias for Sequential Recommendation beyond the Self-Attention. AAAI 2024.

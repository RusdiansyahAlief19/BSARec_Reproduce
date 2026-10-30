Notebook Colab yang disimpan di sini:

- `BSARec_Reproduce.ipynb`: reproduksi Beauty.
- `BSARec_LastFM_Final_Strict.ipynb`: preprocessing/audit dan enam run utama LastFM pada konfigurasi 4 worker. Preview output baris mentah dihapus dari salinan publik; kode sumber dan metrik tersimpan dipertahankan.
- `BSARec_LastFM_WandB_2workers.ipynb`: eksperimen tambahan LastFM 2 worker, W&B, ablasi, dan evaluasi checkpoint penulis. Gunakan sebagai catatan eksperimen tambahan, bukan sumber utama audit protokol. Ada beberapa output troubleshooting dari sesi Colab.
- `BSARec_dan_SASRec_ML_1M.ipynb`: eksperimen ML-1M seed 42; hasil hanya deskriptif dan konfigurasi worker kedua model berbeda.

Dataset mentah dan checkpoint model tidak di-commit. Sel training pada notebook dapat menjalankan training penuh; hindari “Run all” jika hanya ingin membaca output yang tersimpan. Sebelum menambahkan notebook lain, periksa output sel agar tidak memuat dataset mentah atau credential W&B.

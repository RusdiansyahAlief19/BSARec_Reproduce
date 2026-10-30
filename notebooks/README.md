Notebook Colab yang disimpan di sini:

| File | Dataset dan isi | Bukti eksekusi tersimpan |
| --- | --- | --- |
| `BSARec_Beauty.ipynb` | Beauty: checkpoint penulis, run utama, dan ablasi | Output log dan metrik ada, tetapi salinan ini tidak memuat output training BSARec seed 44. Sebagian sel juga tidak memiliki nomor eksekusi. |
| `BSARec_LastFM.ipynb` | LastFM: preprocessing dan enam run utama pada konfigurasi 4 worker | Keenam sel training memiliki nomor eksekusi dan output test. Preview baris dataset mentah dihapus dari output salinan publik. |
| `BSARec_LastFM_EksperimenTambahan.ipynb` | LastFM: eksperimen 2 worker dengan W&B, ablasi, dan evaluasi checkpoint penulis | Sel run dan tabel ringkasan memiliki output tersimpan; ini eksperimen tambahan, bukan audit utama. |
| `BSARec_dan_SASRec_ML_1M.ipynb` | MovieLens-1M: satu seed untuk tiap model | Log dan tabel metrik tersimpan, tetapi nomor eksekusi semua sel kosong pada salinan ini. |

Jadi, notebook LastFM utama sudah menunjukkan sel training yang benar-benar berjalan. Jika tersedia, tambahkan ekspor Colab Beauty yang mencakup output BSARec seed 44 dan ekspor Colab ML-1M dengan metadata eksekusi; tidak perlu melatih ulang hanya untuk mengganti nama file. Dataset mentah dan checkpoint model tidak di-commit. Sel training dapat menjalankan eksperimen penuh bila dieksekusi ulang; hindari “Run all” hanya untuk membaca output. Sebelum menambahkan notebook, pastikan outputnya tidak memuat dataset mentah atau credential W&B.

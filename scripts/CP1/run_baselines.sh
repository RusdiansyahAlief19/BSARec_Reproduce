#!/usr/bin/env bash
# BSARec dan SASRec di Beauty, 3 seed. Jalankan dari folder src/ repo upstream.
# Perintah mengikuti README upstream; cocokkan dengan perintah yang benar-benar dipakai di notebook.
set -e
for s in 42 43 44; do
  python main.py --data_name Beauty --lr 0.0005 --alpha 0.7 --c 5 --num_attention_heads 1 \
    --seed $s --train_name BSARec_Beauty_s${s}
  python main.py --model_type SASRec --data_name Beauty --num_attention_heads 1 \
    --seed $s --train_name SASRec_Beauty_s${s}
done
# Verifikasi checkpoint penulis (hasil harus sama dengan Table 2 paper):
# python main.py --data_name Beauty --alpha 0.7 --c 5 --num_attention_heads 1 \
#   --load_model BSARec_Beauty_best --do_eval

#!/usr/bin/env bash
# Sapuan ablasi BSARec di Beauty (seed 42). Jalankan dari folder src/ milik repo upstream
# (https://github.com/yehjin-shin/BSARec) yang sudah diberi patch W&B (lihat patches/).
set -e
for a in 0.1 0.3 0.5 0.9; do   # alpha, c=5 tetap (alpha=0.7, c=5 = baseline seed 42)
  python main.py --data_name Beauty --lr 0.0005 --alpha $a --c 5 --num_attention_heads 1 \
    --seed 42 --train_name BSARec_Beauty_a${a}_c5
done
for c in 1 3 7 9; do           # c, alpha=0.7 tetap
  python main.py --data_name Beauty --lr 0.0005 --alpha 0.7 --c $c --num_attention_heads 1 \
    --seed 42 --train_name BSARec_Beauty_a0.7_c${c}
done

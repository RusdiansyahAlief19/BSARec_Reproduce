# Tabel dan grafik ablasi alpha dan c di Beauty (seed 42). Angka diketik manual.
# Jalankan dari root repo: python scripts/plot_ablation.py  (menyimpan figures/ablasi_beauty.png)
import pandas as pd
import matplotlib.pyplot as plt

KEYS = ["HR@5", "NDCG@5", "HR@10", "NDCG@10", "HR@20", "NDCG@20"]

# urutan: HR@5, NDCG@5, HR@10, NDCG@10, HR@20, NDCG@20
alpha = {  # c = 5 tetap
    0.1: [0.0700, 0.0494, 0.0955, 0.0576, 0.1308, 0.0665],
    0.3: [0.0708, 0.0497, 0.0958, 0.0578, 0.1335, 0.0673],
    0.5: [0.0706, 0.0501, 0.0985, 0.0591, 0.1339, 0.0680],
    0.7: [0.0702, 0.0499, 0.0988, 0.0592, 0.1347, 0.0683],  # baseline seed 42
    0.9: [0.0709, 0.0501, 0.0989, 0.0590, 0.1348, 0.0681],
}
c_val = {  # alpha = 0.7 tetap
    1: [0.0681, 0.0486, 0.0945, 0.0571, 0.1285, 0.0656],
    3: [0.0694, 0.0497, 0.0967, 0.0585, 0.1316, 0.0673],
    5: [0.0702, 0.0499, 0.0988, 0.0592, 0.1347, 0.0683],  # baseline seed 42
    7: [0.0707, 0.0498, 0.0986, 0.0589, 0.1344, 0.0679],
    9: [0.0701, 0.0500, 0.0974, 0.0588, 0.1323, 0.0676],
}
BASE = alpha[0.7]
NOISE = 0.0013  # std HR@20 BSARec antar 3 seed (42, 43, 44)

def tabel(d, nama):
    df = pd.DataFrame(d, index=KEYS).T
    df.index.name = nama
    df["Gap HR@20 vs base (%)"] = (df["HR@20"] / BASE[4] - 1) * 100
    df["Gap NDCG@20 vs base (%)"] = (df["NDCG@20"] / BASE[5] - 1) * 100
    df["HR@20 beda > 1 std?"] = (df["HR@20"] - BASE[4]).abs() > NOISE
    return df

ta, tc = tabel(alpha, "alpha (c=5)"), tabel(c_val, "c (alpha=0.7)")
print(ta.round(4).to_string(), "\n")
print(tc.round(4).to_string())
print(f"\nCatatan: 1 seed per titik; selisih HR@20 di bawah ~{NOISE} (1 std antar seed) tidak bisa dibedakan dari noise; di atas {2*NOISE:.4f} (2 std) lebih meyakinkan.")

def panel(ax, df, xlabel, judul):
    x = range(len(df))
    ax.bar(x, df["NDCG@20"], color="#7aa7e0", label="NDCG@20")
    ax.set_ylim(df["NDCG@20"].min() * 0.97, df["NDCG@20"].max() * 1.02)
    ax.set_ylabel("NDCG@20"); ax.set_xlabel(xlabel); ax.set_title(judul)
    ax.set_xticks(list(x)); ax.set_xticklabels(df.index)
    ax2 = ax.twinx()
    ax2.plot(list(x), df["HR@20"], "o-", color="#d62728", label="HR@20")
    ax2.set_ylabel("HR@20")
    return ax, ax2

fig, axs = plt.subplots(1, 2, figsize=(11, 4))
panel(axs[0], ta, "alpha", "Sensitivitas alpha, Beauty (c=5)")
panel(axs[1], tc, "c", "Sensitivitas c, Beauty (alpha=0.7)")
fig.suptitle("Ablasi BSARec di Beauty (seed 42)")
plt.tight_layout()
import os; os.makedirs("figures", exist_ok=True); plt.savefig("figures/ablasi_beauty.png", dpi=150)
plt.close()

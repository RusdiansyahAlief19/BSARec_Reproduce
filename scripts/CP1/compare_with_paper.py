# Bandingkan hasil reproduksi Beauty (3 seed) dengan Table 2 paper.
# Semua angka diketik manual (tidak butuh file). Jalankan dari root repo: python scripts/compare_with_paper.py
import pandas as pd

pd.set_option("display.width", 220)
pd.set_option("display.max_columns", 30)

KEYS = ["HR@5", "NDCG@5", "HR@10", "NDCG@10", "HR@20", "NDCG@20"]

paper = {  # Table 2 paper, Beauty
    "BSARec": [0.0736, 0.0523, 0.1008, 0.0611, 0.1373, 0.0703],
    "SASRec": [0.0340, 0.0221, 0.0531, 0.0283, 0.0823, 0.0356],
}
hasilku = {  # hasil test akhir per seed (urutan: HR@5, NDCG@5, HR@10, NDCG@10, HR@20, NDCG@20)
    "BSARec": {"s42": [0.0702, 0.0499, 0.0988, 0.0592, 0.1347, 0.0683],
               "s43": [0.0709, 0.0507, 0.0994, 0.0599, 0.1334, 0.0684],
               "s44": [0.0698, 0.0498, 0.0957, 0.0581, 0.1322, 0.0673]},
    "SASRec": {"s42": [0.0302, 0.0192, 0.0503, 0.0256, 0.0800, 0.0331],
               "s43": [0.0350, 0.0222, 0.0542, 0.0284, 0.0823, 0.0355],
               "s44": [0.0370, 0.0241, 0.0554, 0.0300, 0.0846, 0.0373]},
}

hasil = {}
for model in paper:
    df = pd.DataFrame(hasilku[model], index=KEYS)
    seeds = list(df.columns)
    df.insert(0, "Paper", paper[model])
    df["Mean"] = df[seeds].mean(axis=1)
    df["Std"] = df[seeds].std(axis=1)
    for s in seeds:
        df[f"Gap {s} (%)"] = (df[s] - df["Paper"]) / df["Paper"] * 100
    df["Gap Mean (%)"] = (df["Mean"] - df["Paper"]) / df["Paper"] * 100
    hasil[model] = df
    print(f"\n=== {model} (Beauty), {len(seeds)} seed: {', '.join(seeds)} ===")
    print(df.round(4).to_string())

# Perbandingan keseluruhan: seberapa besar BSARec mengungguli SASRec (paper vs reproduksiku)
b, s = hasil["BSARec"], hasil["SASRec"]
ringkas = pd.DataFrame({
    "BSARec paper": b["Paper"], "BSARec mean": b["Mean"],
    "SASRec paper": s["Paper"], "SASRec mean": s["Mean"],
    "Naik vs SASRec, paper (%)": (b["Paper"] / s["Paper"] - 1) * 100,
    "Naik vs SASRec, aku (%)": (b["Mean"] / s["Mean"] - 1) * 100,
})
print("\n=== Ringkasan: BSARec vs SASRec ===")
print(ringkas.round(4).to_string())

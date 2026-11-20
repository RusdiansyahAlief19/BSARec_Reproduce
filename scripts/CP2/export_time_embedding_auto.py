import argparse
import json
import os
import pathlib
import sys

import torch
import matplotlib.pyplot as plt

def find_latest_checkpoint(results_dir: str) -> str:
    """Return the path of the most recent *.pt file in results_dir.
    Raises FileNotFoundError if none found.
    """
    pat = pathlib.Path(results_dir).glob("*.pt")
    ckpts = sorted(pat, key=lambda p: p.stat().st_mtime, reverse=True)
    if not ckpts:
        raise FileNotFoundError(f"No .pt checkpoint found in {results_dir}")
    return str(ckpts[0])

def load_embedding(ckpt_path: str, key: str = "time_embedding.weight"):
    state = torch.load(ckpt_path, map_location="cpu")
    if isinstance(state, dict) and "model_state_dict" in state:
        state = state["model_state_dict"]
    if key not in state:
        raise KeyError(f"Key {key} not found in checkpoint")
    return state[key].cpu().numpy()

def save_txt(arr, out_path: str):
    # space‑separated rows
    with open(out_path, "w", encoding="utf-8") as f:
        for row in arr:
            f.write(" ".join(map(str, row.tolist())) + "\n")

def save_json(arr, out_path: str):
    # convert to list of lists, replace NaN/Inf with 0 to keep valid JSON
    import numpy as np
    clean_arr = np.nan_to_num(arr, nan=0.0, posinf=0.0, neginf=0.0)
    data = clean_arr.tolist()
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def save_heatmap(arr, out_path: str):
    plt.figure(figsize=(8, 6))
    plt.imshow(arr, aspect="auto", cmap="viridis")
    plt.colorbar(label="Embedding value")
    plt.title("Time‑interval embedding heatmap")
    plt.xlabel("Embedding dimension")
    plt.ylabel("Time bucket")
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()

def show_preview(arr, rows: int = 5):
    import pandas as pd
    df = pd.DataFrame(arr[:rows])
    print("First {rows} buckets (each column is an embedding dimension):")
    print(df)

def main():
    parser = argparse.ArgumentParser(description="Export time‑interval embedding from the latest checkpoint.")
    parser.add_argument("--ckpt_path", type=str, default=None, help="Path to a checkpoint .pt file. If omitted, the newest file in results/ is used.")
    parser.add_argument("--out_dir", type=str, default="src", help="Directory where output files will be written.")
    parser.add_argument("--name", type=str, default="time_embedding", help="Base name for output files (txt/json/heatmap).")
    parser.add_argument("--show", action="store_true", help="Print a preview table of the first few rows.")
    parser.add_argument("--plot", action="store_true", help="Generate a heat‑map PNG image.")
    args = parser.parse_args()

    ckpt_path = args.ckpt_path or find_latest_checkpoint("results")
    embedding = load_embedding(ckpt_path)

    os.makedirs(args.out_dir, exist_ok=True)
    txt_path = os.path.join(args.out_dir, f"{args.name}.txt")
    json_path = os.path.join(args.out_dir, f"{args.name}.json")

    save_txt(embedding, txt_path)
    save_json(embedding, json_path)
    print(f"Saved TXT to {txt_path}\nSaved JSON to {json_path}")

    if args.plot:
        png_path = os.path.join(args.out_dir, f"{args.name}_heatmap.png")
        save_heatmap(embedding, png_path)
        print(f"Saved heat‑map PNG to {png_path}")

    if args.show:
        show_preview(embedding)

if __name__ == "__main__":
    main()

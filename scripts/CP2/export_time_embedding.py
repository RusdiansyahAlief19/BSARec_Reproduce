#!/usr/bin/env python
"""Export the learned time‑interval embedding from a trained BSARec checkpoint.

Usage:
    python export_time_embedding.py --ckpt_path /path/to/checkpoint.pt \
        --out_path /desired/output.{txt|json}

The script extracts the ``time_embedding`` weight matrix (shape ``[num_buckets, hidden_dim]``)
and writes it in a simple, GitHub‑friendly format:

* **TXT** – one line per bucket ``<bucket_id> <v1> <v2> ... <vD>``
* **JSON** – a dict ``{"0": [v1, v2, ...], "1": [...], ...}``

Both formats can be loaded later with ``np.loadtxt`` or ``json.load``.
"""

import argparse
import json
import os
import sys

import torch
import numpy as np

def load_checkpoint(ckpt_path: str):
    if not os.path.isfile(ckpt_path):
        raise FileNotFoundError(f"Checkpoint not found: {ckpt_path}")
    # ``torch.load`` works for both CPU and GPU checkpoints.
    ckpt = torch.load(ckpt_path, map_location="cpu")
    # The state dict may be stored under the key ``'model_state_dict'``
    # or directly as the checkpoint itself.
    if isinstance(ckpt, dict) and "model_state_dict" in ckpt:
        state_dict = ckpt["model_state_dict"]
    else:
        state_dict = ckpt
    return state_dict

def extract_time_embedding(state_dict: dict) -> np.ndarray:
    # Try common naming conventions.
    weight_key = None
    for candidate in [
        "time_embedding.weight",
        "model.time_embedding.weight",
        "module.time_embedding.weight",
        "time_embeddings",
    ]:
        if candidate in state_dict:
            weight_key = candidate
            break
    if weight_key is None:
        # Fallback: look for the only tensor with shape [8, *]
        matches = [k for k, v in state_dict.items() if isinstance(v, torch.Tensor) and v.dim() == 2 and v.size(0) == 8]
        if not matches:
            raise KeyError("Unable to locate time‑embedding tensor in checkpoint.")
        weight_key = matches[0]
        print(f"[Info] Using fallback key '{weight_key}' for time embedding.")
    tensor = state_dict[weight_key]
    return tensor.cpu().numpy()

def save_as_txt(emb: np.ndarray, out_path: str):
    with open(out_path, "w", encoding="utf-8") as f:
        for bucket_id, vec in enumerate(emb):
            line = "{} {}\n".format(bucket_id, " ".join(map(lambda x: f"{x:.6f}", vec)))
            f.write(line)

def save_as_json(emb: np.ndarray, out_path: str):
    data = {str(i): vec.tolist() for i, vec in enumerate(emb)}
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def main():
    parser = argparse.ArgumentParser(description="Export BSARec time‑interval embedding.")
    parser.add_argument("--ckpt_path", required=True, help="Path to the *.pt checkpoint file.")
    parser.add_argument("--out_path", required=True, help="Path for the exported file (must end with .txt or .json).")
    args = parser.parse_args()

    state_dict = load_checkpoint(args.ckpt_path)
    emb = extract_time_embedding(state_dict)
    if args.out_path.lower().endswith('.txt'):
        save_as_txt(emb, args.out_path)
    elif args.out_path.lower().endswith('.json'):
        save_as_json(emb, args.out_path)
    else:
        raise ValueError("Output file must end with .txt or .json")
    print(f"Time‑embedding ({emb.shape[0]} buckets × {emb.shape[1]} dim) saved to {args.out_path}")

if __name__ == "__main__":
    main()

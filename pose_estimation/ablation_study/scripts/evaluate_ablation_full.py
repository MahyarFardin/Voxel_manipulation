import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path

PROJECT_ROOT = Path(".").resolve().parent

OUT_DIR      = PROJECT_ROOT / "outputs/ablation_v2"
OUT_DIR.mkdir(parents=True, exist_ok=True)

METHODS = [
    ("GDino+MegaPose",  "results_gdino_megapose.json", "#4C72B0"),
    ("SAM2+MegaPose",   "results_sam2_megapose.json",  "#DD8452"),
    ("SAM3+MegaPose",   "results_sam3_megapose.json",  "#55A868"),
    ("YOLO+MegaPose",   "results_yolo_megapose.json",  "#C44E52"),
    ("GDino+FP",        "results_gdino_fp.json",       "#8172B2"),
    ("SAM2+FP",         "results_sam2_fp.json",        "#937860"),
    ("SAM3+FP",         "results_sam3_fp.json",        "#DA8BC3"),
    ("YOLO+FP",         "results_yolo_fp.json",        "#8C8C8C"),
]

OBJECTS_ORDER = ["lamp", "cone", "redcup", "bottle", "crackerbox", "deodorant"]

def load_results(json_name):
    path = OUT_DIR / json_name
    if not path.exists():
        print(f"  WARNING: {json_name} not found — method will show as missing")
        return {}
    with open(path) as f:
        return json.load(f).get("results", {})


raw = {name: load_results(fname) for name, fname, _ in METHODS}

rows = []
for name, fname, color in METHODS:
    results = raw[name]
    for obj in OBJECTS_ORDER:
        r = results.get(obj, {})
        status = r.get("status", "missing")
        if status == "success":
            rows.append({
                "method": name,
                "object": obj,
                "status": "success",
                "position_error_cm":  r["position_error_cm"],
                "rotation_error_deg": r["rotation_error_deg"],
                "add_cm":             r["add_cm"],
                "add_success":        100.0 if r["add_success"] else 0.0,
                "total_time_s":       r["total_time_s"],
                "detection_time_s":   r["detection_time_s"],
                "estimation_time_s":  r["estimation_time_s"],
            })
        else:
            rows.append({
                "method": name,
                "object": obj,
                "status": status,
                "position_error_cm":  np.nan,
                "rotation_error_deg": np.nan,
                "add_cm":             np.nan,
                "add_success":        np.nan,
                "total_time_s":       np.nan,
                "detection_time_s":   np.nan,
                "estimation_time_s":  np.nan,
            })

df = pd.DataFrame(rows)
METHOD_NAMES = [n for n, _, _ in METHODS]
METHOD_COLORS = {n: c for n, _, c in METHODS}

METRIC_LABELS = {
    "position_error_cm":  "Position Error (cm)   [lower = better]",
    "rotation_error_deg": "Rotation Error (°)    [lower = better]",
    "add_success":        "ADD Success (%)       [higher = better]",
    "total_time_s":       "Total Time (s)        [lower = better]",
}

print("\n" + "=" * 100)
print("ABLATION STUDY — FULL RESULTS (8 conditions × 6 objects)")
print("=" * 100)

for col, label in METRIC_LABELS.items():
    pivot = df.pivot(index="object", columns="method", values=col)
    pivot = pivot.reindex(index=OBJECTS_ORDER, columns=METHOD_NAMES)
    print(f"\n── {label} ──")
    print(pivot.to_string(float_format=lambda x: f"{x:.2f}"))

print("\n" + "=" * 100)
print("SUMMARY (mean over successfully estimated objects per method)")
print("=" * 100)
summary_rows = []
for name in METHOD_NAMES:
    sub = df[df["method"] == name]
    ok  = sub[sub["status"] == "success"]
    summary_rows.append({
        "Method":              name,
        "Detected":            (sub["status"] == "success").sum(),
        "Mean pos err (cm)":   ok["position_error_cm"].mean(),
        "Mean rot err (°)":    ok["rotation_error_deg"].mean(),
        "ADD success (%)":     ok["add_success"].mean(),
        "Mean time (s)":       ok["total_time_s"].mean(),
    })
summary_df = pd.DataFrame(summary_rows).set_index("Method")
print(summary_df.to_string(float_format=lambda x: f"{x:.2f}"))

csv_path = OUT_DIR / "comparison_table.csv"
df.to_csv(csv_path, index=False)
print(f"\nCSV saved → {csv_path}")

summary_csv = OUT_DIR / "comparison_summary.csv"
summary_df.to_csv(summary_csv)
print(f"Summary CSV saved → {summary_csv}")

BAR_W = 0.10
x     = np.arange(len(OBJECTS_ORDER))

def bar_plot(metric_col, ylabel, filename, title_suffix=""):
    fig, ax = plt.subplots(figsize=(16, 6))
    for k, name in enumerate(METHOD_NAMES):
        vals  = []
        hatch = None
        for obj in OBJECTS_ORDER:
            sub = df[(df["method"] == name) & (df["object"] == obj)]
            v   = sub[metric_col].values[0] if len(sub) > 0 else np.nan
            vals.append(v)
        bars = ax.bar(
            x + k * BAR_W, vals, BAR_W,
            label=name, color=METHOD_COLORS[name],
            alpha=0.85, edgecolor="white",
        )
        for bar, v in zip(bars, vals):
            if not np.isnan(v):
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    bar.get_height() + 0.2,
                    f"{v:.1f}",
                    ha="center", va="bottom", fontsize=6, rotation=90,
                )

    ax.set_xticks(x + BAR_W * (len(METHOD_NAMES) - 1) / 2)
    ax.set_xticklabels(OBJECTS_ORDER, fontsize=11)
    ax.set_ylabel(ylabel, fontsize=12)
    ax.set_title(f"{ylabel}{' — ' + title_suffix if title_suffix else ''}", fontsize=13)
    ax.legend(fontsize=8, ncol=4, loc="upper right")
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    path = OUT_DIR / filename
    fig.savefig(path, dpi=150)
    plt.close(fig)
    print(f"Saved → {path}")

bar_plot("position_error_cm",  "Position Error (cm)",    "plot_position_error.png")
bar_plot("rotation_error_deg", "Rotation Error (°)",     "plot_rotation_error.png")
bar_plot("add_success",        "ADD Success (%)",        "plot_add_success.png")
bar_plot("total_time_s",       "Total Runtime (s)",      "plot_runtime.png")

def make_heatmap():
    metrics = ["position_error_cm", "rotation_error_deg", "add_success", "total_time_s"]
    mlabels = ["Pos err (cm)", "Rot err (°)", "ADD % success", "Time (s)"]

    mat = np.full((len(METHOD_NAMES), len(metrics)), np.nan)
    for mi, name in enumerate(METHOD_NAMES):
        sub = df[(df["method"] == name) & (df["status"] == "success")]
        for mj, col in enumerate(metrics):
            mat[mi, mj] = sub[col].mean()

    mat_norm = np.full_like(mat, np.nan)
    for mj, col in enumerate(metrics):
        col_vals = mat[:, mj]
        valid    = col_vals[~np.isnan(col_vals)]
        if len(valid) == 0:
            continue
        lo, hi = valid.min(), valid.max()
        if hi == lo:
            mat_norm[:, mj] = 0.5
        else:
            if col == "add_success":
                mat_norm[:, mj] = (col_vals - lo) / (hi - lo)        # high = good
            else:
                mat_norm[:, mj] = 1 - (col_vals - lo) / (hi - lo)   # low = good

    fig, ax = plt.subplots(figsize=(10, 6))
    im = ax.imshow(mat_norm, cmap="RdYlGn", vmin=0, vmax=1, aspect="auto")

    ax.set_xticks(range(len(metrics)))
    ax.set_xticklabels(mlabels, fontsize=11)
    ax.set_yticks(range(len(METHOD_NAMES)))
    ax.set_yticklabels(METHOD_NAMES, fontsize=10)

    for mi in range(len(METHOD_NAMES)):
        for mj in range(len(metrics)):
            v = mat[mi, mj]
            txt = f"{v:.1f}" if not np.isnan(v) else "—"
            ax.text(mj, mi, txt, ha="center", va="center", fontsize=9,
                    color="black")

    fig.colorbar(im, ax=ax, label="Normalized score (green = better)")
    ax.set_title("Ablation Heatmap — all 8 conditions (mean over detected objects)", fontsize=12)
    fig.tight_layout()
    path = OUT_DIR / "plot_heatmap.png"
    fig.savefig(path, dpi=150)
    plt.close(fig)
    print(f"Saved → {path}")

make_heatmap()

def make_grouped_summary():
    mp_methods = ["GDino+MegaPose", "SAM2+MegaPose", "SAM3+MegaPose", "YOLO+MegaPose"]
    fp_methods = ["GDino+FP",       "SAM2+FP",       "SAM3+FP",       "YOLO+FP"]
    detectors  = ["GDino", "SAM2", "SAM3", "YOLO"]

    fig, axes = plt.subplots(1, 2, figsize=(14, 6), sharey=False)
    metrics   = [("position_error_cm", "Mean Position Error (cm)"),
                 ("add_success",       "Mean ADD Success (%)")]

    for ax, (col, ylabel) in zip(axes, metrics):
        mp_vals = []
        fp_vals = []
        for m_mp, m_fp in zip(mp_methods, fp_methods):
            mp_ok = df[(df["method"] == m_mp) & (df["status"] == "success")]
            fp_ok = df[(df["method"] == m_fp)  & (df["status"] == "success")]
            mp_vals.append(mp_ok[col].mean() if len(mp_ok) > 0 else np.nan)
            fp_vals.append(fp_ok[col].mean()  if len(fp_ok)  > 0 else np.nan)

        xi = np.arange(len(detectors))
        ax.bar(xi - 0.2, mp_vals, 0.38, label="MegaPose", color="#4C72B0", alpha=0.85)
        ax.bar(xi + 0.2, fp_vals, 0.38, label="FoundationPose", color="#C44E52", alpha=0.85)

        for i, (mv, fv) in enumerate(zip(mp_vals, fp_vals)):
            if not np.isnan(mv):
                ax.text(i - 0.2, mv + 0.3, f"{mv:.1f}", ha="center", fontsize=9)
            if not np.isnan(fv):
                ax.text(i + 0.2, fv + 0.3, f"{fv:.1f}", ha="center", fontsize=9)

        ax.set_xticks(xi)
        ax.set_xticklabels(detectors, fontsize=11)
        ax.set_ylabel(ylabel, fontsize=11)
        ax.set_title(ylabel, fontsize=12)
        ax.legend(fontsize=10)
        ax.grid(axis="y", alpha=0.3)

    fig.suptitle("MegaPose vs FoundationPose — grouped by detector", fontsize=13)
    fig.tight_layout()
    path = OUT_DIR / "plot_grouped_summary.png"
    fig.savefig(path, dpi=150)
    plt.close(fig)
    print(f"Saved → {path}")

make_grouped_summary()

print("\nDone. All outputs in:", OUT_DIR)

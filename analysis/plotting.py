from pathlib import Path
from matplotlib import pyplot as plt
import matplotlib.patches as mpatches

def save_subplot(fig, ax, path: str, pad: float = 0.05, include_extra_artists=()):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    bbox = ax.get_tightbbox(renderer, bbox_extra_artists=include_extra_artists)
    bbox_inches = bbox.transformed(fig.dpi_scale_trans.inverted())
    bbox_inches = bbox_inches.expanded(
        (bbox_inches.width + 2 * pad) / bbox_inches.width,
        (bbox_inches.height + 2 * pad) / bbox_inches.height,
    )
    fig.savefig(path, dpi=300, bbox_inches=bbox_inches)


def plot_hit_vs_stand(datasets, f_name:str, save_full=True, save_subplots=True):
    df = datasets[f_name]
    fig, plots = plt.subplots(3, 2, figsize=(15, 20))
    df["ev_diff"] = df["ev_hit"] - df["ev_stand"]
    color_map = {
        "Hit": "blue",
        "Stand": "red",
        "Double": "green",
        "Split": "purple"
    }
    plots[0,0].scatter(df["ten_density"], df["ev_diff"], s=10)
    plots[0,0].axhline(0, color="black")
    plots[0,0].set_xlabel("Ten density")
    plots[0,0].set_ylabel("EV(Hit) - EV(Stand)")
    plots[0,0].set_title("EV(Hit) - EV(Stand) vs ten density")

    plots[0,1].scatter(df["ace_density"], df["ev_diff"], s=10)
    plots[0,1].axhline(0, color="black")
    plots[0,1].set_xlabel("Ace density")
    plots[0,1].set_ylabel("EV(Hit) - EV(Stand)")
    plots[0,1].set_title("EV(Hit) - EV(Stand) vs ace density")

    colors = df["best_move"].map({
        "Hit": "blue",
        "Stand": "red",
        "Double": "green",
        "Split": "purple"
    })
    df["best_ev"] = df[["ev_hit", "ev_stand", "ev_double", "ev_split"]].max(axis=1)

    plots[1,0].scatter(df["ten_density"], df["best_ev"], c=colors, s=10)
    plots[1,0].set_xlabel("Ten density")
    plots[1,0].set_ylabel("Best EV")
    plots[1,0].set_title("Best move regions")
    legend_handles = [
        mpatches.Patch(color=color_map[k], label=k)
        for k in color_map
    ]
    legend_10 = plots[1,0].legend(handles=legend_handles)

    plots[1,1].plot(df["ten_density"], df["ev_double"], label="Double", color=color_map["Double"])
    plots[1,1].plot(df["ten_density"], df["ev_hit"], label="Hit", color=color_map["Hit"])
    plots[1,1].plot(df["ten_density"], df["ev_stand"], label="Stand", color=color_map["Stand"])
    plots[1,1].plot(df["ten_density"], df["ev_split"], label="Split", color=color_map["Split"])
    plots[1,1].set_xlabel("Ten density")
    plots[1,1].set_ylabel("EV")
    plots[1,1].set_title("EVs")
    legend_11 = plots[1,1].legend(handles=legend_handles)

    plots[2,0].scatter(df["ten_density"], df["ev_gap"], s=10)
    plots[2,0].set_xlabel("Ten density")
    plots[2,0].set_ylabel("EV gap")
    plots[2,0].set_title("Decision confidence")

    sc = plots[2,1].scatter(
        df["ten_density"],
        df["ace_density"],
        c=df["ev_diff"],
        cmap="viridis",
        s=40
    )
    cbar = fig.colorbar(sc, ax=plots[2,1])
    cbar.set_label("EV(Hit) - EV(Stand)")
    plots[2,1].set_xlabel("Ten density")
    plots[2,1].set_ylabel("Ace density")
    plots[2,1].set_title("EV difference by deck composition")

    if save_subplots:
        base = f"plots/{f_name}"
        save_subplot(fig, plots[0, 0], f"{base}_evdiff_vs_ten.pdf")
        save_subplot(fig, plots[0, 1], f"{base}_evdiff_vs_ace.pdf")
        save_subplot(fig, plots[1, 0], f"{base}_best_move_regions.pdf", include_extra_artists=(legend_10,))
        save_subplot(fig, plots[1, 1], f"{base}_evs.pdf", include_extra_artists=(legend_11,))
        save_subplot(fig, plots[2, 0], f"{base}_decision_confidence.pdf")
        save_subplot(fig, plots[2, 1], f"{base}_deck_composition.pdf", include_extra_artists=(cbar.ax,))

    if save_full:
        fig.savefig(
            f'plots/{f_name}.png',
            dpi=300,
            bbox_inches="tight"
        )
    plt.show()

def plot_hit_vs_double(datasets, f_name:str, save_full=True, save_subplots=True):
    df = datasets[f_name]
    fig, plots = plt.subplots(3, 2, figsize=(15, 20))
    df["ev_diff"] = df["ev_hit"] - df["ev_double"]
    color_map = {
        "Hit": "blue",
        "Stand": "red",
        "Double": "green",
        "Split": "purple"
    }

    plots[0,0].scatter(df["ten_density"], df["ev_diff"], s=10)
    plots[0,0].axhline(0, color="black")
    plots[0,0].set_xlabel("Ten density")
    plots[0,0].set_ylabel("EV(Hit) - EV(Double)")
    plots[0,0].set_title("EV(Hit) - EV(Double) vs ten density")

    plots[0,1].scatter(df["low_density"], df["ev_diff"], s=10)
    plots[0,1].axhline(0, color="black")
    plots[0,1].set_xlabel("Low density")
    plots[0,1].set_ylabel("EV(Hit) - EV(Double)")
    plots[0,1].set_title("EV(Hit) - EV(Double) vs low density")

    colors = df["best_move"].map({
        "Hit": "blue",
        "Stand": "red",
        "Double": "green",
        "Split": "purple"
    })
    df["best_ev"] = df[["ev_hit", "ev_stand", "ev_double", "ev_split"]].max(axis=1)

    plots[1,0].scatter(df["ten_density"], df["best_ev"], c=colors, s=10)
    plots[1,0].set_xlabel("Ten density")
    plots[1,0].set_ylabel("Best EV")
    plots[1,0].set_title("Best move regions")
    legend_handles = [
        mpatches.Patch(color=color_map[k], label=k)
        for k in color_map
    ]
    legend_10 = plots[1,0].legend(handles=legend_handles)

    plots[1,1].plot(df["ten_density"], df["ev_double"], label="Double", color=color_map["Double"])
    plots[1,1].plot(df["ten_density"], df["ev_hit"], label="Hit", color=color_map["Hit"])
    plots[1,1].plot(df["ten_density"], df["ev_stand"], label="Stand", color=color_map["Stand"])
    plots[1,1].plot(df["ten_density"], df["ev_split"], label="Split", color=color_map["Split"])
    plots[1,1].set_xlabel("Ten density")
    plots[1,1].set_ylabel("EV")
    legend_11 = plots[1,1].legend(handles=legend_handles)
    plots[1,1].set_title("EVs")

    plots[2,0].scatter(df["ten_density"], df["ev_gap"], s=10)
    plots[2,0].set_xlabel("Ten density")
    plots[2,0].set_ylabel("EV gap")
    plots[2,0].set_title("Decision confidence")

    sc = plots[2,1].scatter(
        df["ten_density"],
        df["ace_density"],
        c=df["ev_diff"],
        cmap="viridis",
        s=40
    )

    cbar = fig.colorbar(sc, ax=plots[2,1])
    cbar.set_label("EV(Hit) - EV(Double)")

    plots[2,1].set_xlabel("Ten density")
    plots[2,1].set_ylabel("Ace density")
    plots[2,1].set_title("EV difference by deck composition")

    if save_subplots:
        base = f"plots/{f_name}"
        save_subplot(fig, plots[0, 0], f"{base}_evdiff_vs_ten.pdf")
        save_subplot(fig, plots[0, 1], f"{base}_evdiff_vs_ace.pdf")
        save_subplot(fig, plots[1, 0], f"{base}_best_move_regions.pdf", include_extra_artists=(legend_10,))
        save_subplot(fig, plots[1, 1], f"{base}_evs.pdf", include_extra_artists=(legend_11,))
        save_subplot(fig, plots[2, 0], f"{base}_decision_confidence.pdf")
        save_subplot(fig, plots[2, 1], f"{base}_deck_composition.pdf", include_extra_artists=(cbar.ax,))

    if save_full:
        fig.savefig(
            f'plots/{f_name}.png',
            dpi=300,
            bbox_inches="tight"
        )
    plt.show()

def plot_hit_vs_stand_soft(datasets, f_name:str, save_full=True, save_subplots=True):
    df = datasets[f_name]
    fig, plots = plt.subplots(3, 2, figsize=(15, 20))
    df["ev_diff"] = df["ev_hit"] - df["ev_stand"]
    color_map = {
        "Hit": "blue",
        "Stand": "red",
        "Double": "green",
        "Split": "purple"
    }
    plots[0,0].scatter(df["ten_density"], df["ev_diff"], s=10)
    plots[0,0].axhline(0, color="black")
    plots[0,0].set_xlabel("Ten density")
    plots[0,0].set_ylabel("EV(Hit) - EV(Stand)")
    plots[0,0].set_title("EV(Hit) - EV(Stand) vs ten density")

    plots[0,1].scatter(df["ace_density"], df["ev_diff"], s=10)
    plots[0,1].axhline(0, color="black")
    plots[0,1].set_xlabel("Ace density")
    plots[0,1].set_ylabel("EV(Hit) - EV(Stand)")
    plots[0,1].set_title("EV(Hit) - EV(Stand) vs ace density")

    colors = df["best_move"].map({
        "Hit": "blue",
        "Stand": "red",
        "Double": "green",
        "Split": "purple"
    })
    df["best_ev"] = df[["ev_hit", "ev_stand", "ev_double", "ev_split"]].max(axis=1)

    plots[1,0].scatter(df["ten_density"], df["best_ev"], c=colors, s=10)
    plots[1,0].set_xlabel("Ten density")
    plots[1,0].set_ylabel("Best EV")
    plots[1,0].set_title("Best move regions")
    legend_handles = [
        mpatches.Patch(color=color_map[k], label=k)
        for k in color_map
    ]
    legend_10 = plots[1,0].legend(handles=legend_handles)

    plots[1,1].plot(df["ten_density"], df["ev_double"], label="Double", color=color_map["Double"])
    plots[1,1].plot(df["ten_density"], df["ev_hit"], label="Hit", color=color_map["Hit"])
    plots[1,1].plot(df["ten_density"], df["ev_stand"], label="Stand", color=color_map["Stand"])
    plots[1,1].plot(df["ten_density"], df["ev_split"], label="Split", color=color_map["Split"])
    plots[1,1].set_xlabel("Ten density")
    plots[1,1].set_ylabel("EV")
    legend_11 = plots[1,1].legend(handles=legend_handles)
    plots[1,1].set_title("EVs")

    plots[2,0].scatter(df["ace_density"], df["ev_gap"], s=10)
    plots[2,0].set_xlabel("Ace density")
    plots[2,0].set_ylabel("EV gap")
    plots[2,0].set_title("Decision confidence")

    sc = plots[2,1].scatter(
        df["ten_density"],
        df["ace_density"],
        c=df["ev_diff"],
        cmap="viridis",
        s=40
    )

    cbar = fig.colorbar(sc, ax=plots[2,1])
    cbar.set_label("EV(Hit) - EV(Stand)")

    plots[2,1].set_xlabel("Ten density")
    plots[2,1].set_ylabel("Ace density")
    plots[2,1].set_title("EV difference by deck composition")

    if save_subplots:
        base = f"plots/{f_name}"
        save_subplot(fig, plots[0, 0], f"{base}_evdiff_vs_ten.pdf")
        save_subplot(fig, plots[0, 1], f"{base}_evdiff_vs_ace.pdf")
        save_subplot(fig, plots[1, 0], f"{base}_best_move_regions.pdf", include_extra_artists=(legend_10,))
        save_subplot(fig, plots[1, 1], f"{base}_evs.pdf", include_extra_artists=(legend_11,))
        save_subplot(fig, plots[2, 0], f"{base}_decision_confidence.pdf")
        save_subplot(fig, plots[2, 1], f"{base}_deck_composition.pdf", include_extra_artists=(cbar.ax,))

    if save_full:
        fig.savefig(
            f'plots/{f_name}.png',
            dpi=300,
            bbox_inches="tight"
        )
    plt.show()


def plot_split(datasets, f_name:str, save_full=True, save_subplots=True):
    df = datasets[f_name]
    fig, plots = plt.subplots(3, 2, figsize=(15, 20))
    df["ev_diff_sns"] = df["ev_split"] - df["ev_stand"]
    df["ev_diff_snh"] = df["ev_split"] - df["ev_hit"]
    color_map = {
        "Hit": "blue",
        "Stand": "red",
        "Double": "green",
        "Split": "purple"
    }
    plots[0,0].scatter(df["ten_density"], df["ev_diff_sns"], s=10)
    plots[0,0].axhline(0, color="black")
    plots[0,0].set_xlabel("Ten density")
    plots[0,0].set_ylabel("EV(Split) - EV(Stand)")
    plots[0,0].set_title("EV(Split) - EV(Stand) vs ten density")

    plots[0,1].scatter(df["ten_density"], df["ev_diff_snh"], s=10)
    plots[0,1].axhline(0, color="black")
    plots[0,1].set_xlabel("Ten density")
    plots[0,1].set_ylabel("EV(Split) - EV(Hit)")
    plots[0,1].set_title("EV(Split) - EV(Hit) vs ten density")

    colors = df["best_move"].map({
        "Hit": "blue",
        "Stand": "red",
        "Double": "green",
        "Split": "purple"
    })
    df["best_ev"] = df[["ev_hit", "ev_stand", "ev_double", "ev_split"]].max(axis=1)

    plots[1,0].scatter(df["ten_density"], df["best_ev"], c=colors, s=10)
    plots[1,0].set_xlabel("Ten density")
    plots[1,0].set_ylabel("Best EV")
    plots[1,0].set_title("Best move regions")
    legend_handles = [
        mpatches.Patch(color=color_map[k], label=k)
        for k in color_map
    ]
    legend_10 = plots[1,0].legend(handles=legend_handles)

    plots[1,1].plot(df["ten_density"], df["ev_double"], label="Double", color=color_map["Double"])
    plots[1,1].plot(df["ten_density"], df["ev_hit"], label="Hit", color=color_map["Hit"])
    plots[1,1].plot(df["ten_density"], df["ev_stand"], label="Stand", color=color_map["Stand"])
    plots[1,1].plot(df["ten_density"], df["ev_split"], label="Split", color=color_map["Split"])
    plots[1,1].set_xlabel("Ten density")
    plots[1,1].set_ylabel("EV")
    legend_11 = plots[1,1].legend(handles=legend_handles)
    plots[1,1].set_title("EVs")

    sc = plots[2,0].scatter(
        df["ten_density"],
        df["ace_density"],
        c=df["ev_diff_sns"],
        cmap="viridis",
        s=40
    )

    cbar0 = fig.colorbar(sc, ax=plots[2,0])
    cbar0.set_label("EV(Split) - EV(Stand)")

    plots[2,0].set_xlabel("Ten density")
    plots[2,0].set_ylabel("Ace density")
    plots[2,0].set_title("EV difference (split and stand) by deck composition")


    sc = plots[2, 1].scatter(
        df["ten_density"],
        df["ace_density"],
        c=df["ev_diff_snh"],
        cmap="viridis",
        s=40
    )

    cbar1 = fig.colorbar(sc, ax=plots[2, 1])
    cbar1.set_label("EV(Split) - EV(Hit)")

    plots[2, 1].set_xlabel("Ten density")
    plots[2, 1].set_ylabel("Ace density")
    plots[2, 1].set_title("EV difference (split and hit) by deck composition")

    if save_subplots:
        base = f"plots/{f_name}"
        save_subplot(fig, plots[0, 0], f"{base}_evdiff_vs_ten.pdf")
        save_subplot(fig, plots[0, 1], f"{base}_evdiff_vs_ace.pdf")
        save_subplot(fig, plots[1, 0], f"{base}_best_move_regions.pdf", include_extra_artists=(legend_10,))
        save_subplot(fig, plots[1, 1], f"{base}_evs.pdf", include_extra_artists=(legend_11,))
        save_subplot(fig, plots[2, 0], f"plots/{f_name}_split_vs_stand_density.pdf", include_extra_artists=(cbar0.ax,))
        save_subplot(fig, plots[2, 1], f"plots/{f_name}_split_vs_hit_density.pdf", include_extra_artists=(cbar1.ax,))

    if save_full:
        fig.savefig(
            f'plots/{f_name}.png',
            dpi=300,
            bbox_inches="tight"
        )
    plt.show()


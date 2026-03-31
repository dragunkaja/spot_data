import matplotlib.pyplot as plt
import seaborn as sns
import textwrap


def plot_lollipop_top_songs(df_plot, title="Top Utwory"):
    plt.figure(figsize=(10, 8))
    df_plot = df_plot.sort_values('hours', ascending=True)

    plt.hlines(y=df_plot['song'], xmin=0, xmax=df_plot['hours'], color='grey', alpha=0.4)
    plt.scatter(df_plot['hours'], df_plot['song'], color='#1DB954', s=100)

    for i, (h, s) in enumerate(zip(df_plot['hours'], df_plot['streams'])):
        plt.text(h + 0.5, i, f"{int(s)}x", va='center', fontsize=10, fontweight='bold')

    plt.title(title, fontsize=16)
    sns.despine(left=True, bottom=True)
    plt.tight_layout()


def plot_dual_activity(df_all, df_hits):
    # Agregacja
    all_counts = df_all['hour'].value_counts().sort_index().reset_index(name='total')
    hit_counts = df_hits['hour'].value_counts().sort_index().reset_index(name='hits')

    fig, ax1 = plt.subplots(figsize=(15, 8))

    # Słupki
    sns.barplot(data=hit_counts, x='hour', y='hits', ax=ax1, palette='viridis', alpha=0.6, hue='hour', legend=False)

    # Linia
    ax2 = ax1.twinx()
    sns.lineplot(x=all_counts.index, y=all_counts['total'], ax=ax2, color='r', marker='o', label='Ogólna aktywność')

    ax1.set_title('Rozkład hitów na tle całkowitej aktywności', fontsize=16, fontweight='bold')
    ax2.grid(False)
    plt.tight_layout()
    return fig


def func_with_counts(pct, allvals):
    absolute = int(round(pct / 100. * sum(allvals)))
    return f"{pct:.1f}%\n({absolute:d})"


def plot_comparison_pies(powody_list, titles):
    fig, axes = plt.subplots(1, len(powody_list), figsize=(16, 8))
    for i, (powody, title) in enumerate(zip(powody_list, titles)):
        axes[i].pie(
            powody, labels=powody.index,
            autopct=lambda pct: func_with_counts(pct, powody),
            startangle=90, colors=sns.color_palette('pastel')
        )
        axes[i].set_title(title)
    plt.tight_layout()
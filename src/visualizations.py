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



def plot_top_artists_bar(df_plot):
    plt.figure(figsize=(12, 6))
    sns.set_style("whitegrid")

    ax = sns.barplot(data=df_plot, x='artist', y='hours', hue='artist', palette='viridis', legend=False)

    plt.title('Top Artyści', fontsize=16, fontweight='bold')
    plt.xlabel('')
    plt.ylabel('Godziny słuchania', fontsize=12)
    plt.xticks(rotation=45, ha='right')

    for container in ax.containers:
        ax.bar_label(container, fmt='%.0f h', padding=0)

    plt.tight_layout()
    plt.show()


def plot_songs_scatter(df_plot):
    plt.figure(figsize=(12, 8))
    sns.scatterplot(
        data=df_plot, x='streams', y='hours', size='hours',
        hue='song', legend=False, sizes=(100, 1000), palette='viridis', alpha=0.7
    )

    for i in range(len(df_plot)):
        plt.text(df_plot.streams.iloc[i] + 1, df_plot.hours.iloc[i] + 0.1,
                 df_plot.song.iloc[i], fontsize=9)

    plt.title('Relacja: Liczba odtworzeń vs Czas słuchania', fontsize=16)
    plt.xlabel('Liczba odtworzeń (x)', fontsize=12)
    plt.ylabel('Suma godzin (h)', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.show()


def plot_horizontal_lollipop(df_plot, x_col, y_col, label_col, title, color='#1DB954'):
    """Uniwersalna funkcja do wykresów Lollipop (poziomych)"""
    df_plot = df_plot.sort_values(x_col, ascending=True)

    plt.figure(figsize=(10, 8))
    plt.hlines(y=df_plot[y_col], xmin=0, xmax=df_plot[x_col], color='grey', alpha=0.4)
    plt.scatter(df_plot[x_col], df_plot[y_col], color=color, s=100, alpha=1)

    for i, val in enumerate(df_plot[x_col]):
        plt.text(val + (df_plot[x_col].max() * 0.02), i, f"{int(val)}{'x' if 'ilosc' in x_col else 'h'}",
                 va='center', fontsize=10, fontweight='bold')

    plt.title(title, fontsize=16)
    plt.xlabel(x_col)
    plt.ylabel('')
    sns.despine(left=True, bottom=True)
    plt.tight_layout()
    plt.show()
import pandas as pd
import numpy as np

def get_top_ranking(df, groupby_col, n):
    ranking = (df.groupby(str(groupby_col)).agg(
        ms_played=('ms_played', 'sum'),
        streams=('ms_played', 'count'),
    ).sort_values('ms_played', ascending=False).head(n).reset_index())
    ranking['hours']= (ranking['ms_played']/3600000).round(1)
    ranking.index = ranking.index +1
    return ranking

def get_fav_songs_for_top_artists(df, top_artists_df):
    fav_songs = (df.groupby(['artist', 'song'])['ms_played']
                 .sum()
                 .reset_index()
                 .sort_values(by='ms_played', ascending=False))
    fav_songs = fav_songs.drop_duplicates(subset=['artist'], keep='first')
    return pd.merge(top_artists_df, fav_songs, on='artist', suffixes=('_artist', '_song'))


def get_skips_analysis( df, time_threshold_ms=3000 , min_plays = 10):
    df_tmp = df.copy()

    df_tmp['if_skip'] = np.where(
        (df_tmp['reason_end'] == 'fwdbtn') & (df_tmp['ms_played'] < time_threshold_ms),
        1,
        0
    )
    skip_analysis = df_tmp.groupby(['artist', 'song']).agg(
        skip_count=('if_skip', 'sum'),
        total_plays=('ms_played', 'count')
    ).reset_index()

    skip_analysis['skips%rate'] = (skip_analysis['skip_count'] / skip_analysis['total_plays'] * 100)
    return skip_analysis[skip_analysis['total_plays'] >= min_plays].\
        sort_values('skips%rate', ascending=False).reset_index()


def add_time_features(df):
    df['hour'] = df['timestamp'].dt.hour
    df['day_of_week'] = df['timestamp'].dt.day_name()
    df['month'] = df['timestamp'].dt.month

    days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    df['day_of_week'] = pd.Categorical(df['day_of_week'], categories=days_order, ordered=True)
    return df


def get_discovery_types(df_final):
    conditions = [
        (df_final['reason_start'] == 'clickrow') & (df_final['global_hit'] == False),
        (df_final['reason_start'] == 'trackdone') & (df_final['global_hit'] == False),
        (df_final['reason_start'] == 'trackdone') & (df_final['global_hit'] == True)
    ]
    choices = ['Niszowe odkrycie (Moje)', 'Niszowy test algorytmu', 'Bezpieczny Mainstream (Automat)']
    df_final['discovery_type'] = np.select(conditions, choices, default='Inne')
    return df_final


def get_top_albums(df, n=15):
    top_album = (df.groupby(['artist', 'album'])['ms_played']
                 .sum()
                 .sort_values(ascending=False)
                 .reset_index())
    top_album['hours'] = (top_album['ms_played'] / 3600000).round(1)
    return top_album.head(n)


def get_top_played_by_reason(df,reason= 'clickrow', n=15):
    played = df[df['reason_start'] == reason]
    most_played = (played.groupby(['artist', 'song'])
                    .size()
                    .reset_index(name='ilosc')
                    .sort_values(by='ilosc', ascending=False))
    # etykieta do wykresu
    most_played['label'] = most_played['artist'] + ' - ' + most_played['song']
    return most_played.head(n)

def prepare_pie_data(series, top_n=4):
    """Grupuje najrzadsze powody w kategorię 'Inne' dla wykresów kołowych"""
    counts = series.value_counts()
    top = counts.head(top_n)
    inne = pd.Series({'Inne': counts.iloc[top_n:].sum()})
    return pd.concat([top, inne])
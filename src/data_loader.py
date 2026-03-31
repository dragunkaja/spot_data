import pandas as pd
from pathlib import Path

def load_and_clean_data(path_to_data):

    path = Path(path_to_data)
    jsons= list(path.glob('*.json'))

    if not jsons:
        raise FileNotFoundError("No .json files found in {}".format(path))

    dfs=[]
    for json in jsons:
        temp_df= pd.read_json(json)
        dfs.append(temp_df)


    df = pd.concat(dfs, ignore_index= True).copy()

    df = df.drop_duplicates()
    df = df.drop(columns=['ip_addr', 'episode_show_name', 'spotify_episode_uri', 'audiobook_title',
                          'audiobook_uri', 'audiobook_chapter_uri', 'audiobook_chapter_title', ])
    df = df.rename(columns={
        'ts': 'timestamp',
        'platform': 'device',
        'conn_country': 'country',
        'master_metadata_track_name': 'song',
        'master_metadata_album_artist_name': 'artist',
        'master_metadata_album_album_name': 'album',
        'spotify_track_uri': 'track_id',
        'episode_name': 'episode'
    })

    df['duration'] = pd.to_datetime(df['ms_played'], unit='ms').dt.strftime('%M:%S')
    df['timestamp'] = pd.to_datetime(df['timestamp']).dt.tz_localize(None)

    final_cols = [
        'timestamp', 'duration', 'song', 'artist', 'album', 'country',
        'device', 'ms_played', 'track_id', 'reason_start', 'reason_end',
        'shuffle', 'skipped', 'offline', 'episode', 'offline_timestamp', 'incognito_mode'
    ]


    existing_cols = [c for c in final_cols if c in df.columns]
    df = df[existing_cols]

    df['join_artist'] = df['artist'].astype(str).str.lower().str.strip()
    df['join_song'] = df['song'].astype(str).str.lower().str.strip()

    return df


# 2017 - 2021
def load_top_200(path):
    df = pd.read_csv(path)
    df['Date'] = pd.to_datetime(df['Date']).dt.tz_localize(None)
    df['join_artist'] = df['Artist'].astype(str).str.lower().str.strip()
    df['join_song'] = df['Track Name'].astype(str).str.lower().str.strip()
    return df.sort_values('Date')

def merge_with_top_200(df_user, df_top_200):
    min_date = df_top_200['Date'].min()
    max_date = df_top_200['Date'].max()

    # Filtrowanie czasu
    df_filtered = df_user[(df_user['timestamp'] >= min_date) & (df_user['timestamp'] <= max_date)].copy()

    # Merge asof
    df_final = pd.merge_asof(
        df_filtered.sort_values('timestamp'),
        df_top_200[['Date', 'join_song', 'join_artist', 'Position', 'Streams']],
        left_on='timestamp',
        right_on='Date',
        left_by=['join_song', 'join_artist'],
        right_by=['join_song', 'join_artist'],
        direction='backward'
    )
    df_final['global_hit'] = df_final['Position'].notna()
    return df_final
def get_top_ranking(df, groupby_col, n):
    ranking = (df.groupby(str(groupby_col)).agg(
        ms_played=('ms_played', 'sum'),
        streams=('ms_played', 'count'),
    ).sort_values('ms_played', ascending=False).head(n).reset_index())
    ranking['hours']= (ranking['ms_played']/3600000).round(1)
    ranking.index = ranking.index +1
    return ranking


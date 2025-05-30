import pandas as pd

def expand_levels(df : pd.DataFrame, df_maps : pd.DataFrame) -> pd.DataFrame:
    
    """
    Expand the interval between levels because the log doesn't show every levelup and match the leveling map

    Parâmetros
    ----------
    df : pd.DataFrame
        master dataframe
    df_maps : tipo
        dataframe with maps information

    Returns
    -------
    pd.DataFrame
        expanded dataframe
    """
    
    expanded_rows = []

    for ci, group in df.groupby('CI'):
        group = group.sort_values('CL').reset_index(drop=True)

        for i in range(len(group) - 1):
            cl_start = group.loc[i, 'CL']
            cl_end = group.loc[i + 1, 'CL']
            time_start = group.loc[i, 'TimeInterval']
            time_end = group.loc[i + 1, 'TimeInterval']
            date_start = group.loc[i, 'date']

            for cl in range(cl_start, cl_end + 1):
                map_row = df_maps[(df_maps['lvl_min_map'] <= cl) & (cl <= df_maps['lvl_max_map'])]
                if not map_row.empty:
                    map_name = map_row.iloc[0]['Map']
                else:
                    map_name = None

                if cl <= df_maps[(df_maps['Map'] == group.loc[i, 'Map'])]['lvl_max_map'].max():
                    interval = time_start
                    date = date_start
                else:
                    interval = time_end
                    date = group.loc[i + 1, 'date']

                expanded_rows.append({
                    'CI': ci,
                    'CL': cl,
                    'TimeInterval': interval,
                    'Map': map_name,
                    'date': date
                })

        last_row = group.iloc[-1]
        expanded_rows.append({
            'CI': ci,
            'CL': last_row['CL'],
            'TimeInterval': last_row['TimeInterval'],
            'Map': last_row['Map'],
            'date': last_row['date']
        })

    expanded_df = pd.DataFrame(expanded_rows).drop_duplicates().sort_values(by=['CI', 'CL'])
    
    return expanded_df
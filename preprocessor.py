import pandas as pd
def preprocess(df, region_df):
    #filtering for summer olympics
    df = df[df['Season'] == 'Summer']
    #merge dataframes
    df = df.merge(region_df, on='NOC', how='left')
    #dropping duplicates
    df.drop_duplicates(inplace=True)
    #one hot encoding medal column
    df = pd.concat([df, pd.get_dummies(df['Medal'])], axis=1)
    return df

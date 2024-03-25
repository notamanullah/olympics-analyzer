def country_year_list(df):
    years = df['Year'].dropna().unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    country = df['region'].dropna().unique().tolist()
    country.sort()
    country.insert(0, 'Overall')

    return years, country

def filter_medals(df, year, country):
    medals_df = df.drop_duplicates(subset = ['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])

    flag = 0

    if year == 'Overall' and country == 'Overall':
        medals_to_filter = medals_df
    elif year == 'Overall' and country != 'Overall':
        flag = 1
        medals_to_filter = medals_df[medals_df['region'] == country]
    elif year != 'Overall' and country == 'Overall':
        medals_to_filter = medals_df[medals_df['Year'] == year]
    else:
        medals_to_filter = medals_df[(medals_df['Year'] == year) & (medals_df['region'] == country)]
    
    if flag == 1:
        medals_to_filter = medals_to_filter.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()
    else:
        medals_to_filter = medals_to_filter.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index()

    medals_to_filter['Total'] = medals_to_filter['Gold'] + medals_to_filter['Silver'] + medals_to_filter['Bronze']   

    return medals_to_filter
 
def data_over_time(df, col):
    nations_over_time = df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index().sort_values('Year')
    nations_over_time.rename(columns={'count':col},inplace=True)
    return nations_over_time

def top_athletes(df, sport):
    temp_df = df.dropna(subset=['Medal'])

    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]
    
    temp_df = temp_df['Name'].value_counts().reset_index().merge(df)[['Name', 'count', 'Sport', 'region']].drop_duplicates('Name').head(50)
    
    temp_df.rename(columns={'count':'Medals'},inplace=True)

    temp_df.reset_index(drop='index', inplace=True)

    return temp_df

def year_wise_medals(df, country):
    temp_df = df.dropna(subset=['Medal'])

    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    temp_df = temp_df[temp_df['region'] == country]

    temp_df = temp_df.groupby('Year').count()[['Medal']].reset_index()

    return temp_df

def top_countries_sports(df, country):
    temp_df = df.dropna(subset=['Medal'])

    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    temp_df = temp_df[temp_df['region'] == country]

    temp_df = temp_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)

    return temp_df

def top_athletes_country_wise(df, country):
    temp_df = df.dropna(subset=['Medal'])

    temp_df = temp_df[temp_df['region'] == country]

    temp_df = temp_df['Name'].value_counts().reset_index().head(20).merge(df)[['Name', 'count', 'Sport']].drop_duplicates('Name')

    temp_df.rename(columns={'count':'Medals'}, inplace=True)

    return temp_df

def weight_vs_height(df, sport):
    temp_df = df.drop_duplicates(subset=['Name', 'region'])

    temp_df['Medal'].fillna('No Medal', inplace=True)

    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]
        return temp_df
    else:
        return temp_df

def men_vs_women(df):
    athletes_df = df.drop_duplicates(subset=['Name', 'region'])

    men = athletes_df[athletes_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athletes_df[athletes_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    both = men.merge(women, on='Year')

    both.rename(columns={'Name_x':'Men', 'Name_y':'Women'}, inplace=True)

    both.fillna(0, inplace=True)

    return both
    
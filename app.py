import streamlit as st
import pandas as pd
import preprocessor, helper
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.figure_factory as ff

df = pd.read_csv('olympics data/athlete_events.csv')
regions_df = pd.read_csv('olympics data/noc_regions.csv')

df = preprocessor.preprocess(df = df, region_df = regions_df)   

st.sidebar.title('Olympics Analysis')
st.sidebar.image('https://e7.pngegg.com/pngimages/1020/402/png-clipart-2024-summer-olympics-brand-circle-area-olympic-rings-olympics-logo-text-sport.png')
user_menu = st.sidebar.radio('Select an option',
                 ('Medal Tally','Overall Analysis','Country-wise Analysis','Athlete wise Analysis')
                 )

if user_menu == 'Medal Tally':

    st.sidebar.header('Medal Tally')

    years, country = helper.country_year_list(df=df)

    selected_year = st.sidebar.selectbox('Select Year', years)
    selected_country = st.sidebar.selectbox('Select Country', country)

    medal_tally = helper.filter_medals(df=df, year=selected_year, country=selected_country)

    if (selected_year == 'Overall') and (selected_country == 'Overall'):
        st.title('Overall Tally')

    if (selected_year != 'Overall') and (selected_country == 'Overall'):
        st.title('Medal Tally in ' + str(selected_year))

    if (selected_year == 'Overall') and (selected_country != 'Overall'):
        st.title(selected_country + ' Overall Performance')

    if (selected_year != 'Overall') and (selected_country != 'Overall'):
        st.title(selected_country + ' Performance in ' + str(selected_year))

    st.table(medal_tally)

if user_menu  == 'Overall Analysis':
    editions = df['Year'].unique().shape[0]
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    event = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title('Top Stats')

    col1,col2,col3 = st.columns(3)

    with col1:
        st.header('Editions')
        st.title(editions)
    with col2:
        st.header('Cities')
        st.title(cities)
    with col3:
        st.header('Sports')
        st.title(sports)

    col4,col5,col6 = st.columns(3)

    with col4:
        st.header('Events')
        st.title(event)
    with col5:
        st.header('Athletes')
        st.title(athletes)
    with col6:
        st.header('Nations')
        st.title(nations)

    nations_over_time = helper.data_over_time(df=df, col='region')
    fig = px.line(nations_over_time, x='Year', y='region')
    st.title('Participating Nations Over The Years')
    st.plotly_chart(fig)

    event_over_time = helper.data_over_time(df=df, col='Event')
    fig = px.line(event_over_time, x='Year', y='Event')
    st.title('Events Over The Time')
    st.plotly_chart(fig)

    athletes_over_time = helper.data_over_time(df=df, col='Name')
    fig = px.line(athletes_over_time, x='Year', y='Name')
    st.title('Athletes Over The Time')
    st.plotly_chart(fig)

    st.title('No Of Events Over Time(Every Sport)')
    no_of_event_over_time = df.drop_duplicates(['Year','Sport','Event'])
    fig,ax = plt.subplots(figsize=(14,13))
    ax = sns.heatmap(no_of_event_over_time.pivot_table(index='Sport', columns='Year',values='Event',aggfunc='count').fillna(0).astype(int),annot=True)
    st.pyplot(fig)

    st.title('Top Athletes')
    sports_list = df['Sport'].unique().tolist()
    sports_list.sort()
    sports_list.insert(0, 'Overall')
    selected_sport = st.selectbox('Select a Sport', sports_list)
    top_athletes = helper.top_athletes(df=df, sport=selected_sport) 
    st.table(top_athletes)

if user_menu == 'Country-wise Analysis':
    
    st.sidebar.title('Country-wise Analysis')
    countries_list = df['region'].dropna().unique().tolist()
    countries_list.sort()
    selected_region = st.sidebar.selectbox('Select a Country', countries_list)
    countries_df = helper.year_wise_medals(df=df, country=selected_region)
    fig = px.line(countries_df, x='Year', y='Medal')
    st.title(selected_region + ' Medals Over The Years')
    st.plotly_chart(fig)

    st.title(selected_region, ' Excels IN Following Sports')
    top_countries = helper.top_countries_sports(df=df, country=selected_region)
    fig, ax = plt.subplots(figsize=(11, 10))
    ax = sns.heatmap(top_countries, annot=True)
    st.pyplot(fig)

    st.title('Top Athletes Of ' + selected_region)
    top_athletes_country_wise = helper.top_athletes_country_wise(df=df, country=selected_region)
    st.table(top_athletes_country_wise)

if user_menu == 'Athlete wise Analysis':

    st.title('Distribution Of Age')

    athletes_df = df.drop_duplicates(subset=['Name', 'region'])

    athletes_age = athletes_df['Age'].dropna()
    gold_athletes = athletes_df[athletes_df['Medal'] == 'Gold']['Age'].dropna()
    silver_athletes = athletes_df[athletes_df['Medal'] == 'Silver']['Age'].dropna()
    bronze_athletes = athletes_df[athletes_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([athletes_age, gold_athletes, silver_athletes, bronze_athletes], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'], show_rug=False)
    fig.update_layout(autosize=False, width=950, height=600)
    st.plotly_chart(fig)

    x = []
    name = []
    famous_sports = df['Sport'].unique().tolist()
    for sport in famous_sports:
        temp_df = athletes_df[athletes_df['Sport'] == sport]
        x.append(gold_athletes)
        name.append(sport)

    fig = ff.create_distplot(x, name, show_rug=False)
    fig.update_layout(autosize=False, width=950, height=600)
    st.title('Distribution Of Age By Sports(Gold Medalist)')
    st.plotly_chart(fig)

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')
    selected_sport = st.selectbox('Select A Sport ', sport_list)
    st.title('Height VS Weight')
    height_vs_weight = helper.weight_vs_height(df=df, sport=selected_sport)
    fig,ax = plt.subplots()
    ax = sns.scatterplot(x=height_vs_weight['Weight'], y=height_vs_weight['Height'], hue=height_vs_weight['Medal'], style=height_vs_weight['Sex'], s=60)
    st.pyplot(fig)

    st.title('Men VS Women Participations Over The Years')
    both = helper.men_vs_women(df=df)
    fig = px.line(both, x='Year', y=['Men', 'Women'])
    fig.update_layout(autosize=False, width=950, height=600)
    st.plotly_chart(fig)
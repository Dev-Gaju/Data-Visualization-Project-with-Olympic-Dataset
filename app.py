import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import seaborn as sns
import scipy

import preprocessor, helper

df = pd.read_csv('Dataset/athlete_events.csv')
region_df = pd.read_csv('Dataset/noc_regions.csv')

df = preprocessor.Preprocessor(df, region_df)

st.sidebar.title("Olympic Analysis")
st.sidebar.image("https://stillmed.olympics.com/media/Images/OlympicOrg/IOC/The_Organisation/The-Olympic-Rings/Olympic_rings_TM_c_IOC_All_rights_reserved_1.jpg")

user_menu = st.sidebar.radio(
    'Select an Option',
    ("Medal Tally", "Overall Analysis", "Country-Wise Analysis", "Athlete-Wise Analysis")
)
# st.dataframe(df)

if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years, country = helper.country_year_list(df)
    selected_years = st.sidebar.selectbox("Select Year", years)
    selected_country = st.sidebar.selectbox("Select Country", country)
    medal_tally = helper.fetcch_medal_tally(df, selected_country, selected_years)
    if selected_country == 'Overall' and selected_years == 'Overall':
        st.title("Overall Tally")
    if selected_country != 'Overall' and selected_years == 'Overall':
        st.title(str(selected_country) + " Over all Performance")
    if selected_country == 'Overall' and selected_years != 'Overall':
        st.title("Medal Tally in " + str(selected_years) + " Olympics")
    if selected_country != 'Overall' and selected_years != 'Overall':
        st.title(str(selected_country) + ' Performance in ' + str(selected_years))
    st.table(medal_tally)

if user_menu == 'Overall Analysis':
    edition = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title("All About Olympic")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(edition)
    with col2:
        st.header("Hosts")
        st.title(cities)

    with col3:
        st.header("Sports")
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Nations")
        st.title(nations)

    with col3:
        st.header("Athletes")
        st.title(athletes)

    nations_over_time = helper.data_over_time(df, 'region')
    # st.dataframe(df)
    st.title("Participation Country over the Year")
    fig = px.line(nations_over_time, x='Editions', y="region")
    st.plotly_chart(fig)

    event_over_time = helper.data_over_time(df, 'Event')
    # st.dataframe(df)
    st.title("No of  Events  over the Year")
    fig = px.line(event_over_time, x='Editions', y="Event")
    st.plotly_chart(fig)

    athletes_over_time = helper.data_over_time(df, 'Name')
    # st.dataframe(df)
    st.title("No of  Athletes  over the Year")
    fig = px.line(athletes_over_time, x='Editions', y="Name")
    st.plotly_chart(fig)

    st.title("Number of Events Over time")
    fig, ax = plt.subplots(figsize=(20, 20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(
        x.pivot_table(index="Sport", columns="Year", values="Event", aggfunc="count").fillna(0).astype("int"),
        annot=True)
    st.pyplot(fig)

    st.title("Most Successful Athelets")
    sports_list = df["Sport"].unique().tolist()
    sports_list.sort()
    sports_list.insert(0, "Overall")
    selected_sports = st.selectbox("Select A Sports", sports_list)
    x = helper.most_succes(df, selected_sports)
    st.table(x)

if user_menu == 'Country-Wise Analysis':
    country = df['region'].dropna().unique().tolist()
    country.sort()
    selected_countries = st.sidebar.selectbox("Select a Country", country)
    st.title(str(selected_countries) + " Medal Tally over the Year")
    x = helper.year_wiseMedal(df, selected_countries)
    a = px.line(x, x='Year', y="Medal")
    st.plotly_chart(a)

    st.title("Events Participate By the Country")
    pt = helper.overall_event_by_heatmap(df, selected_countries)
    fig, ax = plt.subplots(figsize=(20, 20))
    ax = sns.heatmap(pt, annot=True)
    st.pyplot(fig)

    st.title(" Top 10 Athletes in " + selected_countries)
    top_country_athletes = helper.most_succes_country_wise(df, selected_countries)
    st.table(top_country_athletes)

if user_menu == 'Athlete-Wise Analysis':
    athletes_df = df.drop_duplicates(subset=["Name", "region"])
    x = athletes_df['Age'].dropna()
    x1 = athletes_df[athletes_df['Medal'] == "Gold"]['Age'].dropna()
    x3 = athletes_df[athletes_df['Medal'] == "Silver"]['Age'].dropna()
    x2 = athletes_df[athletes_df['Medal'] == "Bronze"]['Age'].dropna()
    fig = ff.create_distplot([x, x1, x2, x3], ['Overall Age', "Gold Age", "Silver Age", "Bronze Age"], show_hist=False,
                             show_rug=False)
    st.title("Distribution of Age")
    fig.update_layout(autosize=False, width=800, height=600)
    st.plotly_chart(fig)

    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']

    x = []
    name = []
    for sport in famous_sports:
        temp_df = athletes_df[athletes_df['Sport'] == sport]
        x.append(temp_df[temp_df["Medal"] == "Gold"]["Age"].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    st.title("Distribution of Age wrt  Sports")
    fig.update_layout(autosize=False, width=750, height=600)
    st.plotly_chart(fig)

    st.title("Weight vs Height Distribution")
    sports_list = df["Sport"].unique().tolist()
    sports_list.sort()
    sports_list.insert(0, "Overall")
    selected_sports = st.selectbox("Select A Sports", sports_list)
    temp_df=helper.weight_vs_heights(df, selected_sports)
    fig, ax = plt.subplots(figsize=(15, 16))
    ax = sns.scatterplot(temp_df,x=temp_df['Height'], y=temp_df['Weight'], hue=temp_df["Medal"], style=temp_df['Sex'])
    st.pyplot(fig)

    st.title("Male & Female Performance Over the Year")
    athletes_df = df.drop_duplicates(subset=["Name", "region"])
    male = athletes_df[athletes_df['Sex'] == "M"].groupby("Year").count()["Name"].reset_index()
    female = athletes_df[athletes_df['Sex'] == "F"].groupby("Year").count()["Name"].reset_index()
    final_df = male.merge(female, on="Year")
    final_df.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)
    a=px.line(final_df, x="Year", y=['Male', 'Female'])
    a.update_layout(autosize=False,height=600, width=800)
    st.plotly_chart(a)
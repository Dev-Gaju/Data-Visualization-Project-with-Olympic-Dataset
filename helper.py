import numpy as np


def fetcch_medal_tally(df, country, years):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0
    if country == 'Overall' and years == 'Overall':
        temp_df = medal_df
    if country == 'Overall' and years != 'Overall':
        temp_df = medal_df[medal_df['Year'] == years]
    if country != 'Overall' and years == 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    if country != 'Overall' and years != 'Overall':
        temp_df = medal_df[(medal_df['region'] == country) & (medal_df['Year'] == years)]

    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values("Gold").reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values("Gold",
                                                                                      ascending=False).reset_index()
    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']

    x['Gold'] = x["Gold"].astype('int')
    x['Silver'] = x["Silver"].astype('int')
    x['Bronze'] = x["Bronze"].astype('int')
    x['total'] = x["total"].astype('int')

    return x


def MedalTally(df):
    medal_tally = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    medal_tally = medal_tally.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values("Gold",
                                                                                                ascending=False).reset_index()
    medal_tally['total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']

    medal_tally['Gold'] = medal_tally["Gold"].astype('int')
    medal_tally['Silver'] = medal_tally["Silver"].astype('int')
    medal_tally['Bronze'] = medal_tally["Bronze"].astype('int')
    medal_tally['total'] = medal_tally["total"].astype('int')
    return medal_tally


def country_year_list(df):
    years = df["Year"].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, "Overall")

    return years, country


def data_over_time(df, col):
    country_overtime = df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index().sort_values('index')
    country_overtime.rename(columns={"index": "Editions", "Year": col}, inplace=True)
    return country_overtime


def most_succes(df, sports):
    temp_df = df.dropna(subset=['Medal'])

    if sports != "Overall":
        temp_df = temp_df[temp_df["Sport"] == sports]
    x = temp_df["Name"].value_counts().reset_index().head(15).merge(df, left_on="index",
                                                                    right_on="Name",
                                                                    how="left")[
        ["index", 'Name_x', "Sport", "region"]].drop_duplicates("index")
    x = x.rename(columns={'index': 'Name', "Name_x": "Medals"})
    return x


def year_wiseMedal(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=["Team", "NOC", "Games", "Year", "City", "Sport", "Event", "Medal"], inplace=True)
    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby("Year").count()['Medal'].reset_index()

    return final_df


def overall_event_by_heatmap(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=["Team", "NOC", "Games", "Year", "City", "Sport", "Event", "Medal"], inplace=True)
    new_df = temp_df[temp_df['region'] == country]
    p_table = new_df.pivot_table(index="Sport", columns="Year", values="Medal", aggfunc='count').fillna(0)
    return p_table


def most_succes_country_wise(df, country):
    temp_df = df.dropna(subset=['Medal'])

    temp_df = temp_df[temp_df["region"] == country]
    x = temp_df["Name"].value_counts().reset_index().head(10).merge(df, left_on="index",
                                                                    right_on="Name",
                                                                    how="left")[
        ["index", 'Name_x', "Sport"]].drop_duplicates("index")
    x = x.rename(columns={'index': 'Name', "Name_x": "Medals"})
    return x


def weight_vs_heights(df, sports):
    athletes_df = df.drop_duplicates(subset=["Name", "region"])
    athletes_df["Medal"].fillna("No Medal", inplace=True)
    if sports != "Overall":
        temp_df = athletes_df[athletes_df['Sport'] == sports]
        return temp_df
    else:
        return athletes_df



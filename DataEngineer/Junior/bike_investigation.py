#!/usr/bin/env python
# coding: utf-8

"""
#==================================#
| Bike Sharing - Fulll hiring test |
#==================================#
> Thomas Rigole
---------------
"""

import time

# import numpy as np
import pandas as pd

CITY_DATA = {
    "chicago": "chicago.csv",
    "new york city": "new_york_city.csv",
    "washington": "washington.csv",
}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print("Hello! Let's explore some bikeshare data!")

    # Get user input for city (chicago, new york city, washington)
    city = ''
    while city not in CITY_DATA:
        city = input("Choose a city (chicago, new york city, washington): ").lower().strip()
        if city not in CITY_DATA:
            print("Invalid city name, please choose one of the displayed names.")

    # Get user input for month (all, january, february, ... , june)
    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    # datetime/calendar library converters can be used in case of scalability needs
    month = ''
    while month not in months:
        month = input("Choose a month (all, january, february, ... , june): ").lower().strip()
        if month not in months:
            print("Invalid month, please try again (between january and june).")

    # Get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    # datetime/calendar library converters can be used in case of scalability needs
    day = ''
    while day not in days:
        day = input("Choose a weekday (all, monday, tuesday, ... , sunday): ").lower().strip()
        if day not in days:
            print("Invalid day, please try again.")

    print("-" * 40)
    return city, month, day


def clean_data(df):
    """
    Cleans data of the current df by handling missing values, duplicates, and coherence issues.

    Args:
        df - "Uncleaned" Pandas DataFrame
    Returns:
        df - Cleaned Pandas DataFrame
    """
    # ===============
    # Duplicates & NA
    # ---------------
    # Drop duplicates
    df = df.drop_duplicates()

    # Identify Missing values (% of missing values / total rows)
    # print("Missing values :\n", df.isna().sum() * 100 / df.shape[0], "-" * 12, sep='')

    # Drop na rows in relevant columns
    df = df.dropna(subset=['Start Time', 'End Time', 'Trip Duration'])

    # ======================
    # Replace missing values
    # ----------------------
    df['User Type'] = df['User Type'].fillna('Unknown')
    if 'Gender' in df.columns:
        df['Gender'] = df['Gender'].fillna('Unknown')
    # Replace with the most common year if needed
    # if 'Birth Year' in df.columns:
    #     df['Birth Year'] = df['Birth Year'].fillna(df['Birth Year'].mode()[0])

    # ====================================
    # Identify outliers in relevant column
    # ------------------------------------
    # Limits to detect outliers (3 std)
    lower_bound = df['Trip Duration'].mean() - df['Trip Duration'].std() * 3
    upper_bound = df['Trip Duration'].mean() + df['Trip Duration'].std() * 3
    # Identify outliers
    duration_outliers = df[(df['Trip Duration'] < lower_bound) | (df['Trip Duration'] > upper_bound)]
    print(f"Trip Duration outliers rows removed : {len(duration_outliers)}")
    # Drop outliers rows
    df = df.drop(duration_outliers.index)

    # ====================
    # Consistency problems
    # --------------------
    # Check year (supposed 2017)
    # print(df.groupby(df['Start Time'].dt.year).size())

    # Drop negative duration rows
    df = df[df['Trip Duration'] > 0]

    # Check Start/End Time with Trip Duration
    df['Calculated Trip Duration'] = (df['End Time'] - df['Start Time']).dt.total_seconds()
    # Drop negative calculated duration rows
    print(f"Negative Trip Duration rows removed : {len(df[df['Calculated Trip Duration'] < 0])}")
    df = df[df['Calculated Trip Duration'] > 0]

    # Identify inconsistent duration rows
    inconsistent_duration = df[
        (abs(df['Trip Duration'] - df['Calculated Trip Duration']) >
         df[['Trip Duration', 'Calculated Trip Duration']].min(axis=1) * 0.01) &  # 1% tolerence
        (abs(df['Trip Duration'] - df['Calculated Trip Duration']) > 300)  # 300 secs min threshold
    ]
    print(f"Anomalies/inconsistencies in trip durations removed : {len(inconsistent_duration)}")
    # Drop rows with inconsistent duration
    df = df.drop(inconsistent_duration.index)

    # -----------------
    # Cleaned DataFrame
    return df


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # Data reading from selected csv
    df = pd.read_csv(CITY_DATA[city], parse_dates=['Start Time', 'End Time'])
    df = df.rename(columns={df.columns[0]: 'Id'})

    # New columns for month and weekday (filters)
    df['Month'] = df['Start Time'].dt.month_name().str.lower()
    df['Weekday'] = df['Start Time'].dt.day_name().str.lower()
    df['Hour'] = df['Start Time'].dt.hour

    # Data cleaning
    df = clean_data(df)

    # Filtering (month & weekday)
    if month != 'all':
        df = df[df['Month'] == month]
    if day != "all":
        df = df[df['Weekday'] == day]

    # Filtered DataFrame
    print(f"> {df.shape[0]} rows left after cleaning/filtering.")
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print("\nCalculating The Most Frequent Times of Travel...\n")
    start_time = time.time()

    # Check if DataFrame is empty
    if df.empty:
        print("/!\\ No data available to display time statistics.")
        return

    # Display the most common month
    if df['Month'].nunique() == 1:
        print(f"Filter set to {df['Month'].iloc[0].capitalize()}")
    else:
        month_counts = df['Month'].value_counts().sort_index()
        print(f"The most common month is {month_counts.idxmax().capitalize()}, with {month_counts.max()} occurrences.")

    # Display the most common day of week
    if df['Weekday'].nunique() == 1:
        print(f"Filter set to {df['Weekday'].iloc[0].capitalize()}")
    else:
        day_counts = df['Weekday'].value_counts().sort_index()
        print(f"The most common weekday is {day_counts.idxmax().capitalize()}, with {day_counts.max()} occurrences.")

    # Display the most common start hour
    hour_counts = df['Hour'].value_counts().sort_index()
    print(f"The most common start hour is {int(hour_counts.idxmax())}h, with {hour_counts.max()} occurrences.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print("\nCalculating The Most Popular Stations and Trip...\n")
    start_time = time.time()

    # Check if DataFrame is empty
    if df.empty:
        print("/!\\ No data available to display station statistics.")
        return

    # Display the most commonly used start station
    start_st_counts = df['Start Station'].value_counts().sort_index()
    print(f"The most commonly used start station is {start_st_counts.idxmax()}, with {start_st_counts.max()} occurrences.")

    # Display the most commonly used end station
    end_st_counts = df['End Station'].value_counts().sort_index()
    print(f"The most commonly used end station is {end_st_counts.idxmax()}, with {end_st_counts.max()} occurrences.")

    # Display the most frequent combination of start station and end station trip
    st_trip_counts = (df['Start Station'] + " --> " + df['End Station']).value_counts().sort_index()
    print(f"The most common trip is: {st_trip_counts.idxmax()}, with {st_trip_counts.max()} occurrences.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print("\nCalculating Trip Duration...\n")
    start_time = time.time()

    # Check if DataFrame is empty
    if df.empty:
        print("/!\\ No data available to display duration statistics.")
        return

    # Display the total travel time
    total_tt = df['Trip Duration'].sum()
    print(f"Total travel time : {total_tt:,.2f}sec = {total_tt/60:,.2f}min = {total_tt/3600:,.2f}h = {total_tt/86400:,.2f} days")

    # Display the mean travel time
    mean_tt = df['Trip Duration'].mean()
    print(f"Mean travel time : {mean_tt:,.2f}sec = {mean_tt/60:,.2f}min = {mean_tt/3600:,.2f}h")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print("\nCalculating User Stats...\n")
    start_time = time.time()

    # Check if DataFrame is empty
    if df.empty:
        print("/!\\ No data available to display user statistics.")
        return

    # Display the counts of user types
    print(f"{df['User Type'].value_counts().sort_index().to_string()}\n")
    # print(f"{df['User Type'].value_counts().drop('Unknown').to_string()}\n")

    # Display the counts of gender
    if 'Gender' in df.columns:
        print(f"{df['Gender'].value_counts().sort_index().to_string()}\n")
        # print(f"{df['Gender'].value_counts().drop('Unknown').to_string()}")
    else:
        print('No gender data available for this city.')

    # Display the earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print(f"Earliest year of birth: {df['Birth Year'].sort_index().min():.0f}")
        print(f"Most recent year of birth: {df['Birth Year'].sort_index().max():.0f}")
        print(f"Most common year of birth: {df['Birth Year'].mode()[0]:.0f}")
    else:
        print('No data on dates of birth available for this city.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)


def main():
    while True:
        # city, month, day = get_filters()
        city, month, day = 'chicago', 'july', 'all'
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input("\nWould you like to restart? Enter yes or no.\n")
        if restart.lower() != "yes":
            break


if __name__ == "__main__":
    main()

import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}
cities = ("chicago", "new york city", "washington")
months = (
    "all", "january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november",
    "december")
days = ("all", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday")


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    city = get_filter("Select a city to analyze {}:", cities)

    # TO DO: get user input for month (all, january, february, ... , june)
    month = get_filter("Select a month to filter {}:", months)

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = get_filter("Select a day to filter {}:", days)

    print('-' * 40)
    return city, month, day


def get_filter(message, info_tuple):
    """
    Meanwhile the user doesn't input the correct data, the message will appear in order to give another
    chance to the user in order to input the data correctly. Once the user inputs the correct data, the input will be return.

    Method steps:

    1. Create the appropiate message formatting with the especific info tuple (cities, months, days)
    2. Obtain the input from user
    3. Check the input exist in the info_tuple

    :param message: Select city/month/day message
    :param info_tuple: city/month/day global tuple
    :return: The correct input
    """
    while True:
        info = input(message.format(info_tuple))
        if info.lower() in info_tuple:
            return info.lower()


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
    df = pd.read_csv(CITY_DATA.get(city))
    df.dropna(axis=0, inplace=True)
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month
    df['Day of week'] = df['Start Time'].dt.dayofweek
    # If month is different  to all, filter the month column value with the index of the month (1 to 12)
    if month != 'all':
        df = df[df['Month'] == months.index(month)]
    # If day is different  to all, filter the day column value with the index of the day (0 to 6)
    if day != 'all':
        df = df[df['Day of week'] == (days.index(day)-1)]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    try:
        print("The most common month: {}".format(months[df['Month'].mode()[0]]))
    except KeyError:
        print("There is no information for that specific month")
    # TO DO: display the most common day of week
    try:
        print("The most common day of week: {}".format(days[df['Day of week'].mode()[0]+1]))
    except KeyError:
        print("There is no information for that specific day of week")

    # TO DO: display the most common start hour
    try:
        df['hour'] = df['Start Time'].dt.hour
        print("The most common start hour: {}".format(df['hour'].mode()[0]))
    except KeyError:
        print("There is no information for that specific start hour")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print ('Most commonly used start station:{}'.format(df['Start Station'].mode()[0]))
    # TO DO: display most commonly used end station
    print('Most commonly used end station:{}'.format(df['End Station'].mode()[0]))
    # TO DO: display most frequent combination of start station and end station trip
    gk = df.groupby(['Start Station', 'End Station'])
    print('Most frequent combination of start station and end station trip:{}'.format(gk.first()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    print("Total travel time: {}".format(df['Trip Duration'].sum()))
    # TO DO: display mean travel time
    print ("Mean travel time: {}".format(df['Trip Duration'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    try:

        # TO DO: Display counts of user types
        print("Counts of user types:{}".format(df['User Type'].count()))
        # TO DO: Display counts of gender
        print("Counts of gender:{}".format(df['Gender'].count()))
        # TO DO: Display earliest, most recent, and most common year of birth
        df['Birth Year DT'] = pd.to_datetime(df['Birth Year'])

        print("Most earliest birth year: {}".format(df['Birth Year DT'].min()))
        print("Most recent birth year: {}".format(df['Birth Year DT'].max()))
        print("Most common year of birth: {}".format(df['Birth Year DT'].dt.year.mode()[0]))
    except KeyError:
        print("There is no information for user (Gender and Birth year)")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def display_data(df):
    """
    This method asks the user, if the user wants to see the next 5 rows of data, depending on the
    answer of the user, it will proceed in different ways. If the user answer yes, the method would
    print the next 5 rows of data, meanwhile the data frame is not empty. In the other hand, if the
    user answers no, or hte the method will finish.
    :param df:dataframe
    """
    start_loc_start, start_loc_end = 0, 0

    while True:
        answer = input("Do you want to see the next 5 rows of data? (yes/no): ")
        if answer.lower() == 'yes':
            start_loc_end += 5
            dfn = df.iloc[start_loc_start:start_loc_end, :]
            if dfn.empty:
                print("There is no more raw data to display")
                break
            else:
                print(dfn)
            start_loc_start = start_loc_end
        else:
            break


def main():
     """Bikeshare data analysis main"""
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        bikeshare_stats(df)

        if input('\nWould you like to restart? Enter yes or no.\n').lower() != 'yes':
            break

def bikeshare_stats(df):
    time_stats(df)
    station_stats(df)
    trip_duration_stats(df)
    user_stats(df)
    display_data(df)


if __name__ == "__main__":
    main()

#Program belongs to Y. Chang#
import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    #get user input for city (chicago, new york city, washington). 
    city=input ("\n Which city would you like to analyze? ").lower()

    #Error check
    while city !="new york city" and city != "chicago" and city !="all" and city !="washington":
        city=input ("\n Input error, you must enter all, new york city, chicago or washingon.  Try again").lower()
        
    #get user input for month (all, january, february, ... , june), need error input
    month=input("\n Which month would you like to analyze? ").lower()

    #error check
    while month not in  ['all','january', 'february', 'march', 'april', 'may', 'june']:
          if month.isdigit():
                print("\n If you were trying to enter a numerical month, please use the word instead")
          month=input ("\n Input error, you must enter a valid month").lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day=input("\n Which day of the week would you like to analyze? ").lower()

    #error check
    while day not in  ['all','monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday','sunday']:
          if day.isdigit():
                print("\n If you were trying to enter a numerical day, please use the word instead")
          day=input ("\n Input error, you must enter a valid day").lower()
    print('-'*40)
    return city, month, day


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
    if city=='all': 
        df_chicago=pd.read_csv(CITY_DATA['chicago'])
        df_chicago['city'] = 'chicago' 

        df_nyc=pd.read_csv(CITY_DATA['new york city'])
        df_nyc['city'] = 'new york city' 

        df_washington=pd.read_csv(CITY_DATA['washington'])
        df_washington['city'] = 'washington'
        df=df_chicago.append(df_nyc, sort=False).append(df_washington, sort=False)

    else:
        df = pd.read_csv(CITY_DATA[city])
        df['city'] = city
    df.rename(columns={'Unnamed: 0':'unknown_no'}, inplace=True)

    # convert the Start and End Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['Start Time'])


    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    #Show Data
    print('\n This is the first 5 rows of the dataset \n')
    disp_data='yes'
    idx=0
    while disp_data=='yes':
        print(idx)
        if idx+5>=len(df):
            last_idx=len(df)
            disp_data='no'
            print(df.iloc[idx:len(df)])
            print('\n This is the end of the dataset')
        else:
            print(df.iloc[idx:idx+5])
            disp_data=input("\n Would you like to view another 5 rows of the data? (yes/no) \n").lower()
            idx+=5
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    
    # display the most common month
    popular_month = df['month'].mode()[0]
    print('\n Most Popular Start Month:', popular_month)


    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('\n Most Popular Day:', popular_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('\n Most Popular Start Hour:', popular_hour)


    #print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start = df['Start Station'].mode()[0]
    print('\n Most Popular Start Station:', popular_start)

    # display most commonly used end station
    popular_end = df['End Station'].mode()[0]
    print('\n Most Popular End Station:', popular_end)

    # display most frequent combination of start station and end station trip
    df['start_end']=df['Start Station']+ ' and ' +df['End Station']
    popular_combination = df['start_end'].mode()[0]
    print('\n Most Popular Start-End Station Combination:', popular_combination)

    #print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('\n The total travel time is', df['Trip Duration'].sum()/60/60/60, 'days.')

    # display mean travel time
    print('\n The mean travel time is', df['Trip Duration'].mean()/60,'minutes.')

    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare user but no info available for washington users."""

    print('\nCalculating User Stats...\n')

    # Display counts of user types (counting by the number of rows, there is an unique unkown no for every row)
    print("\n Here is a breakdown of bike user type \n",df.groupby(['User Type'])['unknown_no'].count())
    if df['city'].iloc[0] !='washington':
    #Display counts of gender
        print("\n Here is a breakdown of bike user by gender \n",df.groupby(['Gender'])['unknown_no'].count())

    #Display earliest, most recent, and most common year of birth
        print("\n The most recent year of birth is ", int(df['Birth Year'].max()))
        print("\n The earliest year of birth is ", int(df['Birth Year'].min()))
        print("\n The most common year of birth is ", int(df['Birth Year'].mode()[0]))
    else:
        print("\n No user data available for Washington")

    print('-'*40)


def main():

	#Provide the user with an option to run the query multiple times
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
main()

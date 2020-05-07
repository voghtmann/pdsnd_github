import time
import datetime
#calendar module needed to convert int to month name
import calendar
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
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
 
    city = input('\nPlease select a city from chicago, new york city or washington\n').lower()  
    while city not in ['chicago','new york city','washington']:
      city = input('\nSelection invalid. Please choose city again from chicago, new york city or washington\n').lower()
    
    print('\nYou can now filter the data for {} by month and day of week. Selecting \'all\' will remove the filter.'.format(city))
    # TO DO: get user input for month (all, january, february, ... , june)
    month = input('\nPlease select month: (all, january, february, ... ,june)\n').lower()
    while month not in  ['all','january','february','march','april','may','june']:
        month = input('\nInvalid month. Please a month in the range: (all, january, february, ... , june)\n').lower()
        
    # use the index of the months list to get the corresponding int
       
      
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('\nPlease select day of week: (all, monday, tuesday, ... , sunday)\n').lower()
    while day not in ['all','monday','tuesday','wednesday','thursday','friday','saturday','sunday']:
      day = input('\nInvalid day. Please select a weekday: (all, monday, tuesday, ... , friday)\n').lower()
 
      
    print('-'*40)
    
    # Message to let user know data is being processed
    print('Your data is being processed.....\n')
    
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
    df = pd.read_csv(CITY_DATA[city])
    
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['month'] = df['Start Time'].dt.month
    
    if month != 'all': 
        months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
        month = months.index(month) + 1
        df = df[df['month'] == month]
    
    
    #change month int to month name with lambda function
    df['month'] = df['month'].apply(lambda x: calendar.month_abbr[x])
    
    df['day_of_week'] = df['Start Time'].dt.weekday_name
  
   
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]
    
    #confirm data is loaded
    #print(df.head(10))
    
    #check the column and row size: Chicago 300k x 11 New York city 300k x 11, Washington 300k x 9
    #print(df.shape)
    
    #check for missing or inconsistent data
    #Chicago missing Gender and Birth Year info
    #New York City missing Gender,Birth Year and user info
    
    #print(df.isnull().sum())
    
    #Washington has no columns for Gender to create and fill with default if city selected
    if city == 'washington':
        df['Gender'] = 'Gender not recorded'
       
    #Fill missing values with a default category that can then be shown later in stats function
    df['Gender'].fillna("Gender not recorded", inplace = True) 
    df['User Type'].fillna("User not recorded", inplace = True) 
    
    #check columns added and missing info updated
    #print(df.shape)
    #print(df.isnull().sum())
    
    display = 5
    see_data = ' '
    #see_data = input('\nSee the first 5 rows of data - yes or no?\n').lower()
    
    #Give user the option to display data
    while see_data != 'no': 
      print('\nSee the first {} rows of data?'.format(display))
      see_data = input('....Enter yes or no to continue?\n').lower() 
      print(df.head(display))
      display += 5
 
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    
    common_month = df['month'].mode()[0]

    print('Most common month:', common_month)
    
    # TO DO: display the most common day of week
    
    common_day = df['day_of_week'].mode()[0]

    print('Most common day of the week:', common_day)


    # TO DO: display the most common start hour
    
    df['hour'] = df['Start Time'].dt.hour
    
    common_hour = df['hour'].mode()[0]

    print('Most common starting hour (in the 24 hour clock):', common_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    
    common_start_station = df['Start Station'].mode()[0]

    print('Station(s) most frequently started from:', common_start_station)


    # TO DO: display most commonly used end station
    
    common_end_station = df['End Station'].mode()[0]

    print('Station(s) most frequently ended at:', common_end_station)


    # TO DO: display most frequent combination of start station and end station trip
    
    df['routes'] = df['Start Station'] + ' and ' +  df['End Station']
    
    common_route_stations = df['routes'].mode()[0]
    print('The route between stations {} is most common.'.format(common_route_stations))
    
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    

    # TO DO: display total travel time
    df['trip_length'] = df['End Time'] - df['Start Time'] 
    
    total_trip_length = df['trip_length'].sum()
    
    print('\nTotal travel time for the selected period: ', total_trip_length)


    # TO DO: display mean travel time
    
    mean_trip = df['trip_length'].mean()

    
    print('\nMean travel time for the selected period: ', mean_trip)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    # sort by ascending
    user_types = df['User Type'].value_counts(sort=True, ascending=False)

    print('\n', user_types)


    # TO DO: Display counts of gender
    
    gender_types = df['Gender'].value_counts()
    
    print('\n', gender_types)


    # TO DO: Display earliest, most recent, and most common year of birth
    # washington has no Birth Year information
    if 'Birth Year' in df.columns:
        earliest = str(int(df['Birth Year'].min()))
        latest = str(int(df['Birth Year'].max()))
        common = str(int(df['Birth Year'].mode()))
        print('\nThe earliest birth year is {}, the most recent is {} and the year {} is the most common. '.format(earliest, latest, common))
    else:
        # user message
        print('Birth Year information has not been recorded for this city')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
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


if __name__ == "__main__":
	main()

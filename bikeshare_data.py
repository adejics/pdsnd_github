import time
import pandas as pd

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
    print('Hi Viewer! It\'s time to explore some US bikeshare data!\nEnter a city name to begin!!!\n')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("Please select any of the following cities:\n 'Chicago', 'New York City' or 'Washington': \n").lower().strip()
    city_select = ['chicago', 'new york city', 'washington']
    while city not in city_select:
        print('You entered a wrong information, reselect any of the following city: chicago, new york city, washington')
        city = input("\nKindly choose any of the following cities: Chicago, New York or Washington: \n").lower().strip()
    # get user input for month (all, january, february, ... , june)
    month = input("Thank you! now select a month from january to june,\n" 
                        "or enter 'all' to select all the months  : ").lower().strip()
    month_select = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    while month not in month_select:
        print('You did not select a valid month\n')
        month = input("We only have data ofjanuary to june, Kindly select any of the six months\n" 
                        "or choose 'all' to read the data for all the months: ").lower().strip()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("\nConsider choosing a day of the week from 'sunday' to 'saturday'or enter 'all' to avoid filter: ").lower().strip()
    day_select = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all']
    while day not in day_select:
        print('You did not select a valid day\n')
        day = input("Kindly select any of the day of the week from sunday' to 'saturday' or enter 'all': ").lower().strip()

    print('-'*40, "let's go!")
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

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

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

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    
    # extract Month from the Start Time column to create a column
    df['month'] = df['Start Time'].dt.month
    # find the most popular month
    popular_month = (df['month'].mode()[0]) -1
    month_select = ['january', 'february', 'march', 'april', 'may', 'june']
    print('The month with the most travels for the selected filter is: ', (month_select[popular_month]).title())


    # display the most common day of week
    # extract hour from the Start Time column to create an hour column
    df['day'] = df['Start Time'].dt.day
    popular_day = df['day'].mode()[0]

    # display the most common start hour   
    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print("\nThis is the popular day: ", popular_day, "\nThis is the popular hour: ", popular_hour)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print("The most commonly used start station is: ", popular_start_station)

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print("It is interesting to know that the most commonly used end station is: ", popular_end_station)

    # display most frequent combination of start station and end station trip
    df['combine'] = df['Start Station'] + ' and ' + df['End Station'] # this adds the start and end stations
    most_combine = df['combine'].mode()[0] # this selects the most occured combination of both stations 
    print("The most frequent combined stations trip is: ", most_combine)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_duration = df['Trip Duration'].sum()
    print("This is the total travel time in seconds:  ", total_duration)

    # display mean travel time
    mean_duration = df['Trip Duration'].mean()
    print("This is the avaerage travel time in seconds:  ", mean_duration)
    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = dict(df.groupby(["User Type"])["User Type"].count())
    print("The user type statistics are stated below: \n")
    for user_type in user_types.keys():
        print("{} occured {} times. \n".format(user_type, user_types[user_type]))
    # Display counts of gender
    try:    #this will prevent exceptions error where some city has no gender data
        gender = dict(df.groupby(["Gender"])["Gender"].count())
        print("The gender statistics are stated below: \n")
        print("The data below shows the available gender and the number of times they occur\n")
        for user_gender in gender.keys():
            print("{} occured {} times. \n".format(user_gender, gender[user_gender]))
    except: # this will ensure the code doesnt break if no gender column exists
        print("We are sorry, there is no information on gender for the selected city")

    # Display earliest, most recent, and most common year of birth
    print("...The user type statistics are stated below: \n")
    try:
        earliest_year = list(df["Birth Year"].dropna().sort_values(ascending=True).head(1))
        print("The oldest bike rider for the selected city was born in {}".format(int(earliest_year[0])))

        latest_year = list(df["Birth Year"].dropna().sort_values(ascending=False).head(1))
        print("The youngest bike rider for the selected city was born in {}".format(int(latest_year[0])))

        most_common_year = int(df["Birth Year"].mode()[0])
        print("The most common year of birth for the selected filter is {}".format(most_common_year))
    except:# this prevents the code from breaking in the absence of data on year of birth
        print("We are sorry, there is no information on birth year for the city you selected \n")
        print("Other available information wil be displayed below.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def see_raw_data(df):
    """
        Display the data set used for the analysis in steps of 5 rows based on user interest.
        Args:
            (dataframe) df - dataframe used for the analysis
        """

    #remove some of the columns earlier created to make it cleaner
    df = df.drop(columns=['combine', 'day', 'month', 'day_of_week'], axis=1)
    #confirm if user wants to see more raw data
    see_more = input("Do you want the first 10 rows of the raw data set displayed? Select 'proceed' or 'stop': ").lower().strip()

    #index position for the extent of data to be shown
    index_begin = 0
    index_end = 10

    # this while loop request from viewer to see more raw data
    while see_more == "proceed" and index_end <= df.size:
        print(df[index_begin: index_end])
        index_begin = index_end
        index_end += 10
        see_more = input("You want to continue to see the next 10 rows of the raw data? Select 'proceed' or 'stop' : ").lower().strip()

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        see_raw_data(df)

        restart = input("\nThat is all!. Do you want to start again? Enter 'proceed' or 'stop'.\n")
        if restart.lower() != 'proceed':
            break

if __name__ == "__main__":
	main()

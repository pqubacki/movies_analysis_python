#Author:  Piotr Kubacki
#Student: R00222345

import pandas as pd 
import matplotlib.pyplot as plt

############################################### ACCESSORY FUNCTIONS #############################################################
def readData():

    """Reads dataframe from csv file dropping rows with null values. Returns clean dataframe."""

    df = pd.read_csv("C:\\Users\\Piotr Kubacki\\Documents\\CollegeDataScience\\Python programming\\movie_metadata.csv")

    df = df.dropna()

    return df

def validateInput(min, max):

    """Validates user integer input acording to type and valid options range"""

    #sets boolean flag to be used in while loop
    flag = True

    while flag:

        try:

            userInput = int(input("Enter number: "))

        except ValueError:

            print("Input must be integer. Try again: ")

        else:
            
            #sets flag to false when input is valid integer and breaks the while loop
            flag = False
    
    #checks additionally if input is logically valid
    if min <= userInput <= max:

        return userInput

    else:

        #if input is logically not correct returns recursive call back to function itself with the same arguments
        print("Wrong input! ")

        return validateInput(min, max)

############################################### QUESTION ONE ####################################################################
def topDirectors(data):

    """Displays bar plot of top directors by gross movie earnings based on user input count"""

    #gets number of entries to return from the user
    print("Enter the number of top Directors you want to display? ")
    
    directorCount = validateInput(1,1000)

    #sorts dataframe by gross column descending
    grossSortedData = data.sort_values(by='gross', ascending=False)

    #gets directors and gross columns, remove duplicates
    allDirectors = grossSortedData[['director_name','gross']].drop_duplicates('director_name').head(directorCount)

    #sets arguments for plot
    x = allDirectors.director_name
    y = allDirectors.gross

    #creates plot container
    fig = plt.figure()

    #adjusts subplot positions from bottom and left of the container
    fig.subplots_adjust(bottom=0.15, left=0.25)

    #adds one subplot 
    ax = fig.add_subplot()

    #adds bars
    ax.barh(x, y)

    #formaty y so its not scientific notation
    ax.ticklabel_format(style="plain",axis="x")

    #rotates x ticks so they do not overlap
    plt.xticks(rotation=45)

    #adds main title
    plt.title("Gross Earning vs Top Directors")

    #shows plot
    plt.show()

    return

def topActors(data):

    """Displays bar plot of top directors by gross movie earnings based on user input count"""

    print("Enter the number of top Actors you want to display: ")

    #gets number of entries to return from the user
    actorsCount = validateInput(1,1000)

    #sorts dataframe by gross column descending
    grossSortedData = data.sort_values(by='gross', ascending=False)
    
    #gets actrors and gross columns, removes duplicates
    #decided to use primary starring actors hence actor_1_name
    allActors = grossSortedData[['actor_1_name','gross']].drop_duplicates('actor_1_name').head(actorsCount)

    #sets arguments for plot
    x = allActors.actor_1_name
    y = allActors.gross

    #creates plot container
    fig = plt.figure()

    #adjusts subplot positions from bottom and left of the container
    fig.subplots_adjust(bottom=0.15, left=0.25)

    #adds one subplot 
    ax = fig.add_subplot()

    #adds bars
    ax.barh(x, y)

    #formaty y so its not scientific notation
    ax.ticklabel_format(style="plain",axis="x")

    #rotates x ticks so they do not overlap
    plt.xticks(rotation=45)

    #adds main title
    plt.title("Gross Earning vs Top Actors")

    #shows plot
    plt.show()

    return

############################################### QUESTION TWO ####################################################################
def plotComparison(x, y, title, label):

    """Plots comparison between two movies."""

    #prints plot arguments information
    print(x,'\n',y)

    #creates plot container
    fig = plt.figure()

    #adjusts subplot positions from bottom and left of the container
    fig.subplots_adjust(bottom=0.25, left=0.20)

    #adds one subplot 
    ax = fig.add_subplot()

    #adds bars
    ax.bar(x, y)

    #formaty y so its not scientific notation
    ax.ticklabel_format(style="plain",axis="y")

    #rotates x ticks so they do not overlap
    plt.xticks(rotation=45)

    #adds y label from caller function
    plt.ylabel(label)

    #adds main title
    plt.title(title)

    #shows plot
    plt.show()

    return

def compareMovies(data):

    """Compares two titles entered by the user"""

    #gets movie title column as array
    movieTitleSearch = pd.array(data['movie_title'])

    #replaces non breaking line from the and of the title using list comprehensions
    movieTitleSearch = [title.replace('\xa0','') for title in movieTitleSearch]

    #gets first title
    movieOne = input("\nEnter first movie title: ")
    
    #prompts again if title not found
    while movieOne not in movieTitleSearch:
        movieOne = input("\nMovie title not found; Enter first movie title again: ")

    #gets second title
    movieTwo = input("\nEnter second movie title: ")

    #prompts again if title not found
    while movieTwo not in movieTitleSearch:
        movieTwo = input("\nMovie title not found; Enter second movie title again: ")

    #selects rows containing either first or second title entered by user
    movieRows = data[data["movie_title"].str.contains(movieOne) | data["movie_title"].str.contains(movieTwo) ]
    
    #provides submenu for further options when movies found
    subMenu=True
    while subMenu:
        
        print("""
        -------------------------------Film comparison-------------------------------------
        1. IMDB Scores
        2. Gross Earning
        3. Movie Facebook Like
        4. Main Menu
        -----------------------------------------------------------------------------------
        """)

        print("What would you like to do? ")

        #gets user valid option input
        subMenu = validateInput(1,4)

        #calls previous accessory plotComparison function with apropriate arguments
        if subMenu==1:

            plotComparison(movieRows["movie_title"],movieRows['imdb_score'], "IMDB Scores Comparison", "IMDB Score")

        elif subMenu==2:

            plotComparison(movieRows["movie_title"],movieRows['gross'], "Gross Earning Comparison", "Gross Earning")

        elif subMenu==3:

            plotComparison(movieRows["movie_title"],movieRows['movie_facebook_likes'],"Movie Facebook Likes Comparison", "Facebook Likes")

        elif subMenu==4:

            #sets flag false and "break the loop"
            subMenu = False

############################################### QUESTION THREE ##################################################################
def grossEarningDistribution(data):
    """Plots line graph of minimum, average and maximum gross earning distribution from start to end year"""

    #althoug history of the movie recordings stretches to 1895 lets call valid year range for this task 1900-2021
    print("Enter start year: ")

    startYear = validateInput(1900,2021)

    print("Enter end year: ")

    endYear = validateInput(1900,2021)

    #selects rows where year greater or equal start year
    movieRows = data[data["title_year"] >= startYear]

    #selects rows where year less or equal end year
    movieRows = movieRows[movieRows["title_year"] <= endYear]

    #groups dataframe by the year
    movieGroup = movieRows.groupby(["title_year"])

    #gets descriptive statistics for gross column for each year
    movieGroup = movieGroup.describe()['gross']

    #we are interested in columns min, mean and max 
    movieGroup = pd.DataFrame(movieGroup[['min','mean','max']])

    #extract each column to list including index (year)
    year = movieGroup.index.tolist()
    min  = movieGroup['min'].tolist()
    mean  = movieGroup['mean'].tolist()
    max  = movieGroup['max'].tolist()

    #add each line to plot, format y to standard notation add labels, legend and title
    plt.plot(year, min, label='min')
    plt.plot(year, mean, label='mean')
    plt.plot(year, max, label='max')
    plt.ticklabel_format(style="plain",axis="y")
    plt.ylabel("Gross Earning")
    plt.legend()
    plt.title("Gross Earning Distribution Statistics Over Years")

    #shows plot
    plt.show()

    return

############################################### QUESTION FOUR  ##################################################################
def selfDirecting(data):

    """Return list of directors who performed in the movies they produced"""

    #selects only columns important for analysis
    allDirectors = data.loc[:,['director_name','actor_1_name','actor_2_name','actor_3_name']]

    #adds 'self_directed' column 
    #uses apply function on each row
    #lambda creates list from row and counts number of ocurrences of 'director_name' in list - if its greater I assume director also performed
    allDirectors['self_directed'] = allDirectors.apply(lambda row: True if list(row).count(row['director_name']) > 1 else False, axis=1)

    #selects rows where 'self_directed' value was set to True
    #grouping will "remove duplicates", count will be used after sorting to determine most selfdirecting directors
    selfDirectedDirectors = allDirectors[['director_name', 'self_directed']][allDirectors.self_directed == True]\
        .groupby('director_name')\
        .count()\
        .sort_values('self_directed', ascending=False)

    #returns list of directors
    selfDirectedDirectorsList = selfDirectedDirectors.index.tolist()

    print("----------------------------------------List of self directed directors---------------------------------------------------")

    for director in selfDirectedDirectorsList:
        print(director)

    print("----------------------------------------Top 5 most self directed directors-------------------------------------------------")

    #returns 5 most often selfdirected directors
    print(selfDirectedDirectors.head(5))

    return

############################################### QUESTION FIVE  ##################################################################      
def featureComparison(data):
    """IMDB Score column vs particular numerical column in dataframe"""

    df=data

    #scatterplots ......
    plt.title("num_critic_for_reviews vs imdb_score")
    plt.xlabel("num_critic_for_reviews")
    plt.ylabel("imdb_score")
    plt.scatter(df.num_critic_for_reviews, df.imdb_score)
    plt.show()

    plt.title("duration vs imdb_score")
    plt.xlabel("duration")
    plt.ylabel("imdb_score")
    plt.scatter(df.duration, df.imdb_score)
    plt.show()

    plt.title("actor_1_facebook_likes vs imdb_score")
    plt.xlabel("actor_1_facebook_likes")
    plt.ylabel("imdb_score")
    plt.scatter(df.actor_1_facebook_likes, df.imdb_score)
    plt.show()

    plt.title("actor_2_facebook_likes vs imdb_score")
    plt.xlabel("actor_2_facebook_likes")
    plt.ylabel("imdb_score")
    plt.scatter(df.actor_2_facebook_likes, df.imdb_score)
    plt.show()

    plt.title("actor_3_facebook_likes vs imdb_score")
    plt.xlabel("actor_3_facebook_likes")
    plt.ylabel("imdb_score")
    plt.scatter(df.actor_3_facebook_likes, df.imdb_score)
    plt.show()

    plt.title("gross vs imdb_score")
    plt.xlabel("gross")
    plt.ylabel("imdb_score")
    plt.scatter(df.gross,df.imdb_score)
    plt.show()

    plt.title("aspect_ratio vs imdb_score")
    plt.xlabel("aspect_ratio")
    plt.ylabel("imdb_score")
    plt.scatter(df.aspect_ratio,df.imdb_score)
    plt.show()


    plt.title("num_voted_users vs imdb_score")
    plt.xlabel("num_voted_users")
    plt.ylabel("imdb_score")
    plt.scatter(df.num_voted_users,df.imdb_score)
    plt.show()


    plt.title("director_facebook_likes vs imdb_score")
    plt.xlabel("director_facebook_likes")
    plt.ylabel("imdb_score")
    plt.scatter(df.director_facebook_likes, df.imdb_score)
    plt.show()

    plt.title("facenumber_in_poster vs imdb_score")
    plt.xlabel("facenumber_in_poster")
    plt.ylabel("imdb_score")
    plt.scatter(df.facenumber_in_poster, df.imdb_score)
    plt.show()

    plt.title("num_user_for_reviews vs imdb_score")
    plt.xlabel("num_user_for_reviews")
    plt.ylabel("imdb_score")
    plt.scatter(df.num_user_for_reviews, df.imdb_score)
    plt.show()

    plt.title("budget vs imdb_score")
    plt.xlabel("budget")
    plt.ylabel("imdb_score")
    plt.scatter(df.budget, df.imdb_score)
    plt.show()

############################################### MAIN MENU FUNCTION ##############################################################
def displayMainMenu(data):

    #sets flag for main menu
    mainMenu=True

    while mainMenu:
        print("""
        ----------------------------------Main Menu----------------------------------------
        1. Most successful directors or actors
        2. Film comparison
        3. Analyse the distribution of gross earnings
        4. Self-Directing
        5. Earnings and IMDB scores
        6. Exit
        -----------------------------------------------------------------------------------
        """)

        print("What would you like to do? ")

        mainMenu=validateInput(1,6)

        if mainMenu==1:

            #sets flag for sub menu
            subMenu=True

            while subMenu:

                print("""
                ----------------------Most successful directors or actors--------------------------
                1. Top Directors
                2. Top Actors
                3. Main Menu
                -----------------------------------------------------------------------------------
                """)

                print("What would you like to do? ")

                subMenu = validateInput(1,3)

                if subMenu == 1:

                    topDirectors(data)

                elif subMenu == 2:

                    topActors(data)

                elif subMenu == 3:
                    #exit submenu loop
                     subMenu = False

        elif mainMenu == 2:

            compareMovies(data)

        elif mainMenu == 3:

            grossEarningDistribution(data)

        elif mainMenu == 4:

            selfDirecting(data)

        elif mainMenu == 5:

            featureComparison(data)

        elif mainMenu == 6:

            print("\n Goodbye")
            #set main flag to false exits main menu loop
            mainMenu = False
            
#main definition
def main():
    data = readData()
    displayMainMenu(data)

main()

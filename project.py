# -*- coding: utf-8 -*-
"""
Created on Tue Dec  7 10:10:48 2021

@author: Piotr Kubacki
"""
import pandas as pd



#definition of function displaying initial menu for the user
def menu():
    """Displays main menu with 6 options to choose from."""
    print(
    """
    Please select one of the following options:
    1. Most successful directors or actors 
    2. Film comparison 
    3. Analyse the distribution of gross earnings 
    4. Self-Directing
    5. Earnings and IMDB scores 
    6. Exit
    """
    )
        
    try:
        
        #defines integer variable carrying user's choice    
        option = int(input("Enter numeric option to process dataset: "))
        
        if option == 1:
            print( "1. Most successful directors or actors")
            successfulDirectorsActors()
        elif option == 2:
            print("2. Film comparison")
            filmComparison()
        elif option == 3:
            print("3. Analyse the distribution of gross earnings")
            grossEarnDistibution()
        elif option == 4:
            print("4. Self-Directing")
            selfDirect()
        elif option == 5:
            print("5. Earnings and IMDB scores")
            earningsAndScores()
        elif option == 6:
            print("Exiting...")
        else:
            print("Make sure you enterd number of valid option from 1 to 6.")
        
    except ValueError:
        print("Option must be valid integer.")
        
def successfulDirectorsActors():
    pass

def filmComparison():
    pass

def grossEarnDistibution():
    pass
def selfDirect():
    pass

def earningsAndScores():
    pass

def meniu(**options):
    print(options)
    


def main():
    #df = pd.read_csv("movie_metadata.csv")
    #print(df)
    menu()

main()

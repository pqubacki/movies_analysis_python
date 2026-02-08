"""
Movie Analysis Application
Author: Piotr Kubacki

Analyzes movie metadata from IMDB, providing insights on directors,
actors, earnings, and various film comparisons.
"""

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from typing import Optional


def read_data(path: str, dropna: bool = True) -> pd.DataFrame:
    """
    Read movie metadata from CSV file.

    Args:
        path: Path to the CSV file.
        dropna: If True, remove rows with missing values.

    Returns:
        DataFrame containing movie data.

    Raises:
        FileNotFoundError: If the CSV file does not exist.
        pd.errors.EmptyDataError: If the CSV file is empty.
    """
    csv_path = Path(path)
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    df = pd.read_csv(csv_path)
    if dropna:
        df = df.dropna()

    return df


def validate_input(minimum: int, maximum: int, prompt: str = "Enter number: ") -> int:
    """
    Prompt user for integer input within specified range.

    Uses a loop (not recursion) to avoid stack overflow for repeated invalid input.

    Args:
        minimum: Minimum acceptable value (inclusive).
        maximum: Maximum acceptable value (inclusive).
        prompt: Custom prompt message.

    Returns:
        Valid integer within [minimum, maximum].
    """
    while True:
        try:
            user_input = int(input(prompt))
        except ValueError:
            print("Input must be an integer. Try again.")
            continue

        if minimum <= user_input <= maximum:
            return user_input
        else:
            print(f"Value must be between {minimum} and {maximum}. Try again.")


# ==================== QUESTION ONE: Top Directors & Actors ====================

def _plot_horizontal_bar(names: pd.Series, values: pd.Series, title: str) -> None:
    """
    Create and display a horizontal bar chart.

    Args:
        names: Series of entity names (x-axis).
        values: Series of numeric values (y-axis).
        title: Chart title.
    """
    fig = plt.figure()
    fig.subplots_adjust(bottom=0.15, left=0.25)
    ax = fig.add_subplot()

    ax.barh(names, values)
    ax.ticklabel_format(style="plain", axis="x")
    plt.xticks(rotation=45)
    plt.title(title)
    plt.tight_layout()
    plt.show()
    plt.close(fig)


def top_directors(data: pd.DataFrame) -> None:
    """
    Display bar plot of top directors by gross movie earnings.

    Prompts user for the number of top directors to display.
    """
    print("Enter the number of top Directors you want to display: ")
    director_count = validate_input(1, 1000)

    # Sort by gross and get unique directors
    gross_sorted = data.sort_values(by='gross', ascending=False)
    top_dirs = gross_sorted[['director_name', 'gross']].drop_duplicates(
        'director_name'
    ).head(director_count)

    _plot_horizontal_bar(
        top_dirs['director_name'],
        top_dirs['gross'],
        "Gross Earning vs Top Directors"
    )


def top_actors(data: pd.DataFrame) -> None:
    """
    Display bar plot of top actors by gross movie earnings.

    Uses primary actor (actor_1_name) to avoid duplicates across roles.
    """
    print("Enter the number of top Actors you want to display: ")
    actors_count = validate_input(1, 1000)

    # Sort by gross and get unique actors
    gross_sorted = data.sort_values(by='gross', ascending=False)
    top_acts = gross_sorted[['actor_1_name', 'gross']].drop_duplicates(
        'actor_1_name'
    ).head(actors_count)

    _plot_horizontal_bar(
        top_acts['actor_1_name'],
        top_acts['gross'],
        "Gross Earning vs Top Actors"
    )


# ==================== QUESTION TWO: Film Comparison ====================

def _plot_comparison(names: pd.Series, values: pd.Series, title: str, label: str) -> None:
    """
    Plot comparison between entities using a vertical bar chart.

    Args:
        names: Series of entity names.
        values: Series of numeric values.
        title: Chart title.
        label: Y-axis label.
    """
    fig = plt.figure()
    fig.subplots_adjust(bottom=0.25, left=0.20)
    ax = fig.add_subplot()

    ax.bar(names, values)
    ax.ticklabel_format(style="plain", axis="y")
    plt.xticks(rotation=45)
    plt.ylabel(label)
    plt.title(title)
    plt.tight_layout()
    plt.show()
    plt.close(fig)


def compare_movies(data: pd.DataFrame) -> None:
    """
    Compare two movies selected by the user across multiple metrics.

    Allows user to compare IMDB scores, gross earnings, and Facebook likes.
    """
    # Normalize titles: remove non-breaking spaces and strip whitespace
    data_copy = data.copy()
    data_copy['movie_title_clean'] = (
        data_copy['movie_title']
        .str.replace('\xa0', '', regex=False)
        .str.strip()
    )
    available_titles = set(data_copy['movie_title_clean'].values)

    # Get first movie title
    movie_one = input("\nEnter first movie title: ").strip()
    while movie_one not in available_titles:
        movie_one = input("Movie title not found. Enter first movie title again: ").strip()

    # Get second movie title
    movie_two = input("\nEnter second movie title: ").strip()
    while movie_two not in available_titles:
        movie_two = input("Movie title not found. Enter second movie title again: ").strip()

    # Filter rows for selected movies
    movie_rows = data_copy[
        data_copy['movie_title_clean'].isin([movie_one, movie_two])
    ]

    # Submenu for comparison options
    sub_menu = True
    while sub_menu:
        print("""
        ----------------------- Film Comparison Menu -----------------------
        1. IMDB Scores
        2. Gross Earning
        3. Movie Facebook Likes
        4. Back to Main Menu
        -------------------------------------------------------------------
        """)

        choice = validate_input(1, 4, "What would you like to compare? ")

        if choice == 1:
            _plot_comparison(
                movie_rows['movie_title_clean'],
                movie_rows['imdb_score'],
                "IMDB Scores Comparison",
                "IMDB Score"
            )
        elif choice == 2:
            _plot_comparison(
                movie_rows['movie_title_clean'],
                movie_rows['gross'],
                "Gross Earning Comparison",
                "Gross Earning ($)"
            )
        elif choice == 3:
            _plot_comparison(
                movie_rows['movie_title_clean'],
                movie_rows['movie_facebook_likes'],
                "Movie Facebook Likes Comparison",
                "Facebook Likes"
            )
        elif choice == 4:
            sub_menu = False


# ==================== QUESTION THREE: Gross Earning Distribution ====================

def gross_earning_distribution(data: pd.DataFrame) -> None:
    """
    Plot line graph of minimum, average and maximum gross earnings over years.

    Prompts user for start and end years, then visualizes distribution statistics.
    """
    print("Enter start year: ")
    start_year = validate_input(1900, 2021)

    print("Enter end year: ")
    end_year = validate_input(1900, 2021)

    # Filter movies by year range
    movie_rows = data[(data["title_year"] >= start_year) & (data["title_year"] <= end_year)]

    # Group by year and get descriptive statistics for gross column
    grouped = movie_rows.groupby("title_year")['gross'].describe()
    stats = pd.DataFrame(grouped[['min', 'mean', 'max']])

    # Extract data for plotting
    years = stats.index.tolist()
    min_values = stats['min'].tolist()
    mean_values = stats['mean'].tolist()
    max_values = stats['max'].tolist()

    # Create plot
    fig = plt.figure()
    plt.plot(years, min_values, label='Min', marker='o')
    plt.plot(years, mean_values, label='Mean', marker='s')
    plt.plot(years, max_values, label='Max', marker='^')
    plt.ticklabel_format(style="plain", axis="y")
    plt.xlabel("Year")
    plt.ylabel("Gross Earning ($)")
    plt.legend()
    plt.title("Gross Earning Distribution Statistics Over Years")
    plt.tight_layout()
    plt.show()
    plt.close(fig)


# ==================== QUESTION FOUR: Self-Directing ====================

def self_directing(data: pd.DataFrame) -> None:
    """
    Display directors who performed in the movies they directed.

    Shows all self-directing directors and top 5 most frequent ones.
    """
    # Select relevant columns
    all_directors = data.loc[:, ['director_name', 'actor_1_name', 'actor_2_name', 'actor_3_name']].copy()

    # Check if director appears in actor columns (director also acted in their movie)
    all_directors['self_directed'] = all_directors.apply(
        lambda row: row['director_name'] in row.values[1:],
        axis=1
    )

    # Filter self-directing directors and count occurrences
    self_directed_directors = (
        all_directors[all_directors['self_directed']]
        [['director_name']]
        .groupby('director_name')
        .size()
        .sort_values(ascending=False)
    )

    # Display results
    print("\n" + "="*80)
    print("List of Self-Directing Directors")
    print("="*80)
    for director in self_directed_directors.index:
        print(f"  {director}")

    print("\n" + "="*80)
    print("Top 5 Most Self-Directing Directors")
    print("="*80)
    print(self_directed_directors.head(5))


# ==================== QUESTION FIVE: Feature Comparison ====================

def feature_comparison(data: pd.DataFrame) -> None:
    """
    Create scatter plots comparing IMDB score with various numerical features.

    Visualizes relationships between movie features and IMDB ratings.
    """
    features = [
        ('num_critic_for_reviews', 'Number of Critic Reviews'),
        ('duration', 'Duration (minutes)'),
        ('actor_1_facebook_likes', 'Actor 1 Facebook Likes'),
        ('actor_2_facebook_likes', 'Actor 2 Facebook Likes'),
        ('actor_3_facebook_likes', 'Actor 3 Facebook Likes'),
        ('gross', 'Gross Earnings ($)'),
        ('aspect_ratio', 'Aspect Ratio'),
        ('num_voted_users', 'Number of Voted Users'),
        ('director_facebook_likes', 'Director Facebook Likes'),
        ('facenumber_in_poster', 'Face Count in Poster'),
        ('num_user_for_reviews', 'Number of User Reviews'),
        ('budget', 'Budget ($)'),
    ]

    for feature_col, feature_label in features:
        fig = plt.figure()
        plt.scatter(data[feature_col], data['imdb_score'])
        plt.xlabel(feature_label)
        plt.ylabel("IMDB Score")
        plt.title(f"{feature_label} vs IMDB Score")
        plt.tight_layout()
        plt.show()
        plt.close(fig)


# ==================== MAIN MENU ====================

def _display_top_menu(data: pd.DataFrame) -> None:
    """Display submenu for top directors/actors."""
    sub_menu = True

    while sub_menu:
        print("""
        ----------------------Most successful directors or actors--------------------------
        1. Top Directors
        2. Top Actors
        3. Main Menu
        -----------------------------------------------------------------------------------
        """)

        choice = validate_input(1, 3, "What would you like to do? ")

        if choice == 1:
            top_directors(data)
        elif choice == 2:
            top_actors(data)
        elif choice == 3:
            sub_menu = False


def display_main_menu(data: pd.DataFrame) -> None:
    """
    Display main menu and handle user navigation.

    Args:
        data: DataFrame containing movie metadata.
    """
    main_menu = True

    while main_menu:
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

        choice = validate_input(1, 6, "What would you like to do? ")

        if choice == 1:
            _display_top_menu(data)
        elif choice == 2:
            compare_movies(data)
        elif choice == 3:
            gross_earning_distribution(data)
        elif choice == 4:
            self_directing(data)
        elif choice == 5:
            feature_comparison(data)
        elif choice == 6:
            print("\nGoodbye!")
            main_menu = False


def main() -> None:
    """
    Entry point for the movie analysis application.

    Loads data and launches the main menu.
    """
    try:
        path = "movie_metadata.csv"
        data = read_data(path)
        display_main_menu(data)
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()

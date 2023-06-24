# Movie Data Analysis

This repository contains a program that allows you to manipulate and analyze up-to-date movie data using the top-rated movies list from [The Movie Database](https://www.themoviedb.org/). With this program, you can compare directors, genres, and more!

## Getting Started

To use this program, follow the instructions below:

1. Clone the repository to your local machine or download the source code files.

2. Make sure you have Python installed on your system (version 3.6 or higher).

3. Install the required dependencies by running the following command:

   ```
   pip install -r requirements.txt
   ```

4. Run the `main.py` file in your preferred Python environment.

   ```
   python main.py
   ```

## Program Usage

1. Upon running the program, you will be prompted to enter a sample size of movies to check on the webpage. Enter a multiple of 20 within the range of 0 to 8700.

2. The program will fetch and create a CSV file with the top movies and their data based on your input.

3. Once the CSV file is created, you will be welcomed to the genre and director data analysis tool.

4. You will be presented with a menu of analysis methods to choose from. Enter the name of the desired method to perform the analysis.

5. The program will display the results of the analysis based on your chosen method.

6. After each analysis, you will be prompted to continue with further analysis or exit the program.

## Available Analysis Methods

The following analysis methods are available to use:

- `print_directors`: Prints the list of directors in the sample set.

- `print_genres`: Prints the list of genres in the sample set.

- `highest_rated_movie_by_director`: Displays the highest-rated movie directed by a specified director.

- `highest_rated_movie_by_genre`: Displays the highest-rated movie in a specified genre.

- `highest_rated_director`: Displays the highest-rated director based on a minimum number of movies they have in the sample set.

- `highest_rated_genre`: Displays the highest-rated genre based on a minimum number of movies in the sample set.

- `highest_rated_director_by_genre`: Displays the highest-rated director in a specified genre based on a minimum number of movies.

- `highest_rated_genre_by_director`: Displays the highest-rated genre directed by a specified director based on a minimum number of movies.

## Example Usage

Here's an example of how you can use the program:

1. Enter a sample size of movies to check on the webpage, e.g., `40` (which corresponds to 2 pages of 20 movies each).

2. The program will create a CSV file with the top 40 movies and their data.

3. Choose to continue with the analysis.

4. Enter `print_directors` to see the list of directors in the sample set.

5. Enter `highest_rated_movie_by_director` and provide a director's name to find their highest-rated movie.

6. Continue exploring other analysis methods or choose to exit the program.

## Note

Please ensure that the CSV file is created properly before performing the analysis. If an error occurs during the creation of the CSV file, the program will notify you.

Thank you for using the Movie Data Analysis program! If you have any questions or issues, feel free to contact us.

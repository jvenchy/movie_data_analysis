# Movie Data Analysis

This repository contains a Python program that allows you to analyze up-to-date movie data using the top-rated movies list from [themoviedb.org](https://www.themoviedb.org/). The program provides various analysis methods to compare directors, genres, and more.

## Usage

To use the program, follow these steps:

1. Clone the repository to your local machine.
2. Make sure you have Python installed.
3. Run the `main.py` file in your preferred Python environment.

## Program Flow

1. Upon running the program, you will be prompted to enter the sample size of movies to check on the webpage. The sample size must be entered in multiples of 20 and should be between 0 and 8700.
2. The program will fetch the movie information from the top-rated movies list and create a `.csv` file with the specified number of movies.
3. Once the file is created, you will see a message confirming the completion and welcoming you to the analysis tool.
4. You will then be prompted to choose an analysis method from the following options:
   - `print_directors`: Prints a list of directors in the dataset.
   - `print_genres`: Prints a list of genres in the dataset.
   - `highest_rated_movie_by_director`: Finds the movie with the highest rating made by a given director.
   - `highest_rated_movie_by_genre`: Finds the movie with the highest rating in a given genre.
   - `highest_rated_director`: Finds the director with the highest average ratings, considering a minimum number of movies.
   - `highest_rated_genre`: Finds the genre with the highest average ratings, considering a minimum number of movies.
   - `highest_rated_director_by_genre`: Finds the director with the highest average ratings in a given genre, considering a minimum number of movies.
   - `highest_rated_genre_by_director`: Finds the genre with the highest average ratings by a given director, considering a minimum number of movies.
5. After selecting a method, the program will display the results of the analysis.
6. You will then be prompted to continue with the analysis or exit the program.
7. If you choose to continue, you can select another analysis method.
8. Once you are done with the analysis, you can choose to exit the program.

## Dependencies

The program depends on the following libraries:

- `csv`: Used for reading and writing CSV files.
- `matplotlib`: Used for plotting and visualizing the data.

Make sure you have these libraries installed before running the program. You can install them using the following command:

```
pip install matplotlib
```

## File Structure

The repository consists of the following files:

- `main.py`: The main runner file that interacts with the user and calls the analysis methods.
- `pull_information.py`: Contains the code for fetching movie information from the top-rated movies list and creating the `.csv` file.
- `analysis.py`: Contains the code for reading the created `.csv` file and performing various analysis methods.
- `movies.csv`: The generated CSV file containing movie data.
- `README.md`: The README file that provides information about the program and usage instructions.

## Acknowledgments

The program utilizes the top-rated movies list from [themoviedb.org](https://www.themoviedb.org/) to gather movie information for analysis.

Please note that the program relies on the availability and accuracy of the top-rated movies list. Any changes to the webpage structure or data format may affect the program's functionality.

Feel free to explore the code and customize it according to your needs. Enjoy analyzing movie data with this program!


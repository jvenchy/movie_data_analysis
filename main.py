"""
Main runner file for a user to interact with and input parameters in the console. A program user interface coming soon.
"""

import pull_information
import analysis

print("Hey there! Let's get started.")
print("Using the top rated movies list on https://www.themoviedb.org/.org, "
      "this program lets you manipulate up-to-date movie data to compare directors, genres, and much more!")
input_sample_size = input("Enter your sample size of movies to check on the page, in multiples of 20:")

while int(input_sample_size) > 8700 or int(input_sample_size) < 0:
    input_sample_size = input("Error! Input must be between 0 and 8700, try again. "
                              "Enter your sample size of movies to check on the page, in multiples of 20:")

pull_information.pull_and_create(int(input_sample_size))
print('The program is creating a .csv file with your top ' + input_sample_size + ' movies and their data...')

analysis.read()
if not analysis.data:
    print('Error, the csv file must not have been created properly. Something went wrong. Oops!')
else:
    print('Welcome to your very own genre and director data analysis tool on ' + input_sample_size + ' movies!')

    continue_prompt = input('Do you wish to continue to the analysis? Enter Y for yes or N for no.')

    while continue_prompt == 'Y':
        print('Choose one of the following methods to analyse movie rankings with:')
        print('print_directors')
        print('print_genres')
        print('highest_rated_movie_by_director')
        print('highest_rated_movie_by_genre')
        print('highest_rated_director')
        print('highest_rated_genre')
        print('highest_rated_director_by_genre')
        print('highest_rated_genre_by_director')
        input_method = input("Type one of the above methods here!")

        if input_method == 'print_directors':
            print(analysis.print_directors())

        elif input_method == 'print_genres':
            print(analysis.print_genres())

        elif input_method == 'highest_rated_movie_by_director':
            director = input("Type a director's name into here!")
            print(analysis.highest_rated_movie_by_director(director))

        elif input_method == 'highest_rated_movie_by_genre':
            genre = input("Type a genre into here!")
            print(analysis.highest_rated_movie_by_genre(genre))

        elif input_method == 'highest_rated_director':
            minimum_num = int(input("Considering how many or more movies a director must have in the sample set?"))
            print(analysis.highest_rated_director(minimum_num))

        elif input_method == 'highest_rated_genre':
            minimum_num = int(input("Considering how many or more movies a director must have in the sample set?"))
            print(analysis.highest_rated_genre(minimum_num))

        elif input_method == 'highest_rated_director_by_genre':
            minimum_num = int(input("Considering how many or more movies a director must have in the sample set?"))
            genre = input("Also, type a genre into here!")
            print(analysis.highest_rated_director_by_genre(minimum_num, genre))

        elif input_method == 'highest_rated_genre_by_director':
            minimum_num = int(input("Considering how many or more movies a director must have in the sample set?"))
            director = input("Also, type a director into here!")
            print(analysis.highest_rated_genre_by_director(minimum_num, director))

        else:
            print('You did not input a correct method named as mentioned above. Try again or quit the program!')

        continue_prompt = input('Do you wish to continue with the analysis? Enter Y for yes or N for no.')

    print('You are exiting the program. Thank you!')

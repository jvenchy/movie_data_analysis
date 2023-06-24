"""
Python code for reading the created .csv file and analysing the parameters
"""

import csv
import matplotlib.pyplot as plt


def read() -> []:
    """
    Read the CSV file
    """

    csv_file = 'movies.csv'
    data = []
    with open(csv_file, 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)

    return data


data = read()


def print_directors() -> []:
    """
    Print a list of directors in the data set (csv file)
    """
    director_list = []
    for datapoint in data:
        directors = datapoint['Director(s)'].split(', ')
        for director in directors:
            if director not in director_list:
                director_list.append(director)

    return director_list


def print_genres() -> []:
    """
    Print a list of directors in the data set (csv file)
    """
    genre_list = []
    for datapoint in data:
        genres = datapoint['Genre(s)'].split(', ')
        for genre in genres:
            if genre not in genre_list:
                genre_list.append(genre)

    return genre_list


def highest_rated_movie_by_director(director: str) -> tuple | str:
    """
    Find the movie in the sample set with the highest rating considering only movies made by the given director.
    Return 'Not Found' if input director isn't in sample set.
    """
    movie = 'Not Found'

    for datapoint in data:
        if director in datapoint['Director(s)'] and movie == 'Not Found':
            movie = (datapoint['Title'], datapoint['Rating'])

        elif len(movie) == 2 and director in datapoint['Director(s)']:

            # check if any ratings are higher than current highest rated movie
            if movie[1] < datapoint['Rating']:
                movie = (datapoint['Title'], datapoint['Rating'])

    return movie


def highest_rated_movie_by_genre(genre: str) -> tuple | str:
    """
    Find the movie in the sample set with the highest rating considering only movies of the given genre.
    Return 'Not Found' if input genre isn't in the sample set.
    """
    movie = 'Not Found'

    for datapoint in data:
        if genre in datapoint['Genre(s)'] and movie == 'Not Found':
            movie = (datapoint['Title'], datapoint['Rating'])

        elif len(movie) == 2 and genre in datapoint['Genre(s)']:

            # check if any ratings are higher than current highest rated movie
            if movie[1] < datapoint['Rating']:
                movie = (datapoint['Title'], datapoint['Rating'])

    return movie


def highest_rated_director(minimum_num: int) -> tuple:
    """
    Find the director with the highest average ratings, considering only those with minimum_num or more movies in the
    sample set

    Return 'Try a lower minimum num!' if no director has minimum_num or more movies.
    """
    # map every director to a tuple with their average rating and num movies in average
    director_dict = {}
    for datapoint in data:
        directors = datapoint['Director(s)'].split(', ')
        for director in directors:
            if director not in director_dict:
                director_dict[director] = (int(datapoint['Rating']), 1)
            else:
                avg_so_far = director_dict[director][0]
                movies_so_far = director_dict[director][1]
                new_avg = ((avg_so_far * movies_so_far) + int(datapoint['Rating']))/(movies_so_far + 1)
                director_dict[director] = (new_avg, movies_so_far + 1)

    print(director_dict)

    # find the highest rated director with minimum_num movies
    best_director_so_far = 'Try a lower minimum num!'
    highest_rating_so_far = 0

    for director in director_dict:
        if director_dict[director][0] > highest_rating_so_far and director_dict[director][1] >= minimum_num:
            best_director_so_far = director
            highest_rating_so_far = director_dict[director][0]

    return (best_director_so_far, highest_rating_so_far)


def highest_rated_genre(minimum_num: int) -> tuple:
    """
    Find the genre with the highest average ratings, considering only those with minimum_num or more movies in the
    sample set

    Return 'Try a lower minimum num!' if no genre has minimum_num or more movies.
    """
    # map every genre to a tuple with its average rating and num movies in average
    genre_dict = {}
    for datapoint in data:
        genres = datapoint['Genre(s)'].split(', ')
        for genre in genres:
            if genre not in genre_dict:
                genre_dict[genre] = (int(datapoint['Rating']), 1)
            else:
                avg_so_far = genre_dict[genre][0]
                movies_so_far = genre_dict[genre][1]
                new_avg = ((avg_so_far * movies_so_far) + int(datapoint['Rating'])) / (movies_so_far + 1)
                genre_dict[genre] = (new_avg, movies_so_far + 1)

    print(genre_dict)

    # find the highest rated genre with minimum_num movies
    best_genre_so_far = 'Try a lower minimum num!'
    highest_rating_so_far = 0

    for genre in genre_dict:
        if genre_dict[genre][0] > highest_rating_so_far and genre_dict[genre][1] >= minimum_num:
            best_genre_so_far = genre
            highest_rating_so_far = genre_dict[genre][0]

    num_top_movies = genre_dict[best_genre_so_far][1]

    return (best_genre_so_far, highest_rating_so_far, 'Had ' + str(num_top_movies) + ' top movies')


def highest_rated_director_by_genre(minimum_num: int, genre: str) -> tuple:
    """
    Find the director with the highest average ratings, considering only those with minimum_num or more movies in the
    sample set, as well as only movies of a given genre.

    Return 'Not Found' if input genre isn't in sample set.
    Return 'Try a lower minimum num!' if no director has minimum_num or more movies.
    """
    # if movie matches given genre, map every director to a tuple with their average rating and num movies in average
    director_dict = {}
    for datapoint in data:
        genres = datapoint['Genre(s)'].split(', ')
        if genre in genres:
            directors = datapoint['Director(s)'].split(', ')
            for director in directors:
                if director not in director_dict:
                    director_dict[director] = (int(datapoint['Rating']), 1)
                else:
                    avg_so_far = director_dict[director][0]
                    movies_so_far = director_dict[director][1]
                    new_avg = ((avg_so_far * movies_so_far) + int(datapoint['Rating'])) / (movies_so_far + 1)
                    director_dict[director] = (new_avg, movies_so_far + 1)

    print(director_dict)

    # find the highest rated director with minimum_num movies
    best_director_so_far = 'Try a lower minimum num!'
    highest_rating_so_far = 0

    for director in director_dict:
        if director_dict[director][0] > highest_rating_so_far and director_dict[director][1] >= minimum_num:
            best_director_so_far = director
            highest_rating_so_far = director_dict[director][0]

    return (best_director_so_far, genre, highest_rating_so_far)


def highest_rated_genre_by_director(minimum_num: int, director: str) -> tuple:
    """
    Find the genre with the highest average ratings, considering only those with minimum_num or more movies in the
    sample set, as well as only movies by a given director.

    Return 'Not Found' if input director isn't in sample set.
    Return 'Try a lower minimum num!' if no genre has minimum_num or more movies.
    """
    # if movie matches given director, map every genre to a tuple with its average rating and num movies in average
    genre_dict = {}
    for datapoint in data:
        directors = datapoint['Director(s)'].split(', ')
        if director in directors:
            genres = datapoint['Genre(s)'].split(', ')
            for genre in genres:
                if genre not in genre_dict:
                    genre_dict[genre] = (int(datapoint['Rating']), 1)
                else:
                    avg_so_far = genre_dict[genre][0]
                    movies_so_far = genre_dict[genre][1]
                    new_avg = ((avg_so_far * movies_so_far) + int(datapoint['Rating'])) / (movies_so_far + 1)
                    genre_dict[genre] = (new_avg, movies_so_far + 1)

    print(genre_dict)

    # find the highest rated genre with minimum_num movies
    best_genre_so_far = 'Try a lower minimum num!'
    highest_rating_so_far = 0

    for genre in genre_dict:
        if genre_dict[genre][0] > highest_rating_so_far and genre_dict[genre][1] >= minimum_num:
            best_genre_so_far = genre
            highest_rating_so_far = genre_dict[genre][0]

    num_top_movies = genre_dict[best_genre_so_far][1]

    return (best_genre_so_far, director, highest_rating_so_far, 'Had ' + str(num_top_movies) + ' top movies')

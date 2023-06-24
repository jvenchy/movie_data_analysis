"""
Python code for pulling information from TMDb HTML code into a .csv file
"""
import requests
from bs4 import BeautifulSoup as bs
import csv


def pull_and_create(num_pulled: int):
    """
    Scrapes the top-rated age, and each individual movie card on a page to obtain necessary information such as title,
    genre(s), director(s), and rating of the movie.
    """
    # number of movies to scrape (multiples of 20, can go up to 8700!)
    top_x_movies = num_pulled

    # number of pages to scrape, automatically calculated
    pages = top_x_movies // 20

    # create the csv file
    csv_file = 'movies.csv'
    headers = ['Title', 'Genre(s)', 'Director(s)', 'Rating']

    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(headers)

        for page in range(pages + 1):
            # request the top-rated movies page
            url = 'https://www.themoviedb.org/movie/top-rated?page=' + str(page) + '&language=en-US'
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
            r = requests.get(url, headers=headers)
            soup = bs(r.text, 'html.parser')

            # identify movie cards in the html code
            movie_cards = soup.find_all('div', class_='card', limit=23)

            # iterate over the movie cards and scrape required information
            for movie_card in movie_cards:
                if movie_card.find('h2') is not None and movie_card.find('h2').find('a') is not None:
                    movie_url = movie_card.find('h2').find('a')['href']

                    # scrape the movie's TMDb page as long as it exists
                    if movie_url != []:
                        full_request_url = 'https://www.themoviedb.org' + movie_url
                        mr = requests.get(full_request_url, headers=headers)
                        soup_2 = bs(mr.text, 'html.parser')

                        # find movie title
                        title = soup_2.find('h2').find('a').text

                        # find genres and store in list
                        genres = soup_2.find('span', class_='genres').find_all('a')
                        genre_list = [genre.text for genre in genres]

                        # find directors of the movie
                        director_list = []
                        for profile in soup_2.find_all('li', class_='profile'):
                            # check if the profile credited is to a director
                            if 'Director' in profile.find('p', class_='character').text:
                                director_list.append(profile.find('p').text)

                        # find rating of movie
                        rating_element = soup_2.find('div', class_='percent').find('span')
                        rating = rating_element['class'][-1][-2:]

                        # Write the movie's information to the CSV file
                        print(title, genre_list, director_list, rating)
                        writer.writerow([title, ', '.join(genre_list), ', '.join(director_list), rating])

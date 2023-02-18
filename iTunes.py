
# modules

import json
import requests
import webbrowser


# classes

class Media:
    def __init__(self, title='No Title', author='No Author', \
        release_year='No Release Year', url='No URL', json=None):

        self.json = json

        if json is not None:
            try:
                try:
                    self.title = self.json['trackName']
                except:
                    self.title = self.json['collectionName']
            except:
                self.title = 'No Title'
            self.author = self.json['artistName']
            self.release_year = self.json['releaseDate'][:4]
            try:
                try:
                    self.url = self.json['trackViewUrl']
                except:
                    self.url = self.json['collectionViewUrl']
            except:
                self.url = 'No URL'

        else:
            self.title = title
            self.author = author
            self.release_year = release_year
            self.url = url

    def info(self):
        return f"{self.title} by {self.author} ({self.release_year})"

    def length(self):
        return 0

class Song(Media):
    def __init__(self, title='No Title', author='No Author', \
        release_year='No Release Year', url='No URL', json=None, \
        album='No Album', genre='No Genre', track_length=0):
        super().__init__(title, author, release_year, url, json)

        if self.json is not None:
            self.album = self.json['collectionName']
            self.genre = self.json['primaryGenreName']
            self.track_length = self.json['trackTimeMillis']

        else:
            self.album = album
            self.genre = genre
            self.track_length = track_length

    def info(self):
        return super().info() + f'[{self.genre}]'

    def length(self):
        return self.track_length/1000%60

class Movie(Media):
    def __init__(self, title='No Title', author='No Author', \
        release_year='No Release Year', url='No URL', json=None, \
        rating='No Rating', movie_length=0):
        super().__init__(title, author, release_year, url, json)

        if self.json is not None:
            self.rating = self.json['contentAdvisoryRating']
            self.movie_length = self.json['trackTimeMillis']

        else:
            self.rating = rating
            self.movie_length = movie_length

    def info(self):
        return super().info() + f'[{self.rating}]'

    def length(self):
        return self.length/1000/60%60


# functions

def make_object(j):
    try:
        if j['kind']=='feature-movie':
            return Movie(json=j)
        elif j['kind']=='song':
            return Song(json=j)
        else:
            return Media(json=j)
    except:
        return Media(json=j)

def get_list_of_dicts_from_api(search_term):
    search_term = search_term.lower().replace(' ', '+')
    object = requests.get(f'https://itunes.apple.com/search?term={search_term}')
    dictionary = object.json()

    return dictionary['results']

def create_lists(list_of_dicts):
    songs = []
    movies = []
    other = []

    for result in list_of_dicts:
        obj = make_object(result)
        if type(obj)==Song:
            songs.append(obj)
        elif type(obj)==Movie:
            movies.append(obj)
        else:
            other.append(obj)

    final = songs + movies + other

    return songs, movies, other, final

def print_results(lists):
    i = 1
    print('\n---SONGS----------------------------------')
    if len(lists[0]) > 0:
        for song in lists[0]:
            print(i, song.info())
            i +=1
    else:
        print('(No songs returned.)')
    print('\n---MOVIES---------------------------------')
    if len(lists[1]) > 0:
        for movie in lists[1]:
            print(i, movie.info())
            i +=1
    else:
        print('(No movies returned.)')
    print('\n---OTHER MEDIA----------------------------')
    if len(lists[2]) > 0:
        for o in lists[2]:
            print(i, o.info())
            i +=1
    else:
        print('(No other media returned.)')

    return None

def search_function(user_input):
    if user_input=='exit':
        print('Bye!')
        quit()

    else:
        results = get_list_of_dicts_from_api(user_input)
        lists = create_lists(results)
        print_results(lists)

    while True:

        user_input = input('Please enter a number for more information, or a new search term, or "exit" to quit: ')

        if user_input.isnumeric():
            if int(user_input) < len(lists[-1]):
                search_this = lists[-1][int(user_input)-1].url
                webbrowser.open(search_this)
                continue
            else:
                search_function(user_input)

        else:
            search_function(user_input)

def main():
    user_input = input('Please enter a search term, or "exit" to quit: ')
    search_function(user_input)


# main

if __name__=="__main__":
    main()
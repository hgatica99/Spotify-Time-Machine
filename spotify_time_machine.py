import calendar

from calendar import monthrange
import requests
from bs4 import BeautifulSoup


class SpotifyTimeMachine:
    def __init__(self, url, todays_date):

        self.formatted_artists_names = []
        self.y_m_d_list = None
        self.user_input = None
        self.user_day_int = None
        self.user_month_int = None
        self.user_year_int = None

        self.rankings_list = None
        self.song_names_list = None

        self.todays_date = todays_date
        self.todays_year = todays_date.year
        self.todays_month = todays_date.month
        self.todays_day = todays_date.day

        self.url = url
        self.url_ending = None

        self.response = None

    def get_input(self):
        self.user_input = input("Which year do you wish to travel to? Type the date in this format YYYY-MM-DD:\n")

        while not self.check_input(user_input=self.user_input):
            self.user_input = input("Please try again: \n")

    def check_input(self, user_input):
        print("Checking input")
        self.y_m_d_list = user_input.split("-")

        # Try converting strings to int to check if the formatted input contains numbers
        try:
            self.user_year_int = int(self.y_m_d_list[0])
            self.user_month_int = int(self.y_m_d_list[1])
            self.user_day_int = int(self.y_m_d_list[2])

        except ValueError:
            print(" Invalid format. Make sure you follow the format YYYY-MM-DD. A")
            return False
        except IndexError:
            print(" Invalid format. Make sure you follow the format YYYY-MM-DD. A")
            return False

        else:
            # If the strings are numbers, then make sure the numbers are the correct length to follow the format
            if not len(self.y_m_d_list[0]) == 4 or not len(self.y_m_d_list[1]) == 2 or not len(self.y_m_d_list[2]) == 2:
                print("Invalid format. Make sure it follows the format YYYY-MM-DD. B")
                return False

            # Checking if the year given is greater than current year
            elif self.user_year_int > self.todays_year:
                print("Invalid format. Unfortunately we can't see into the future (Year). C")
                return False

            # Checking if month given is greater than current month and less than 13
            elif self.user_month_int <= 12 and self.user_year_int == int(self.user_input[0]):
                if self.todays_month < self.user_month_int:
                    print("Invalid format. Unfortunately we can't see into the future (Month). D")
                    return False

            # Checking if day given is greater than current day
            elif self.todays_day < self.user_day_int and self.user_year_int == int(self.user_input[0]):
                print("Invalid format. Unfortunately we can't see into the future (Day). E")
                return False

            try:
                months_total_days = monthrange(self.user_year_int, self.user_month_int)[1]
                if self.user_day_int > months_total_days:
                    print(f"Invalid format. There are less than {self.user_day_int} days in "
                          f"{self.y_m_d_list[1]}/{self.user_year_int}. D")

            except calendar.IllegalMonthError:
                print("Invalid format. There are only 12 months in a year.")
                return False
            else:
                print("Valid Input")
                self.url_ending = f"{self.y_m_d_list[0]}-{self.y_m_d_list[1]}-{self.y_m_d_list[2]}/"
                return True

    def get_rankings_info(self):
        self.response = requests.get(f"{self.url}{self.url_ending}")
        spotify_web_page = self.response.text
        soup = BeautifulSoup(spotify_web_page, "html.parser")

        ranking_containers = soup.find_all('li', attrs={'class': 'o-chart-results-list__item // '
                                                                 'lrv-u-background-color-black lrv-u-color-white '
                                                                 'u-width-100 u-width-55@mobile-max '
                                                                 'u-width-55@tablet-only lrv-u-height-100p lrv-u-flex '
                                                                 'lrv-u-flex-direction-column@mobile-max '
                                                                 'lrv-u-flex-shrink-0 lrv-u-align-items-center '
                                                                 'lrv-u-justify-content-center lrv-u-border-b-1 '
                                                                 'u-border-b-0@mobile-max lrv-u-border-color-grey'})
        song_names_containers = soup.select("li ul li h3")
        artists_containers = soup.select("ul li ul li span")

        self.song_names_list = [item.text.split("\n")[1] for item in song_names_containers]
        self.rankings_list = [item.text.split("\n")[2] for item in ranking_containers]
        artists_names = [item.text.split('\n') for item in artists_containers]

        for x in artists_names:
            for y in x:
                if y == "" or y == "-":
                    pass
                else:
                    try:
                        int_y = int(y)
                    except ValueError:
                        self.formatted_artists_names.append(y)
                    else:
                        pass

    def get_artists_list(self):
        return self.formatted_artists_names

    def get_rankings_list(self):
        return self.rankings_list

    def get_songs_list(self):
        return self.song_names_list

    def find_rank(self, rank_number):
        print(f'Number {self.get_rankings_list()[rank_number - 1]} was "{self.get_songs_list()[rank_number - 1]}" by {self.get_artists_list()[rank_number - 1]}')

    def get_new_playlist_name(self):
        name = f"Top 100: {self.y_m_d_list[1]}/{self.y_m_d_list[2]}/{self.y_m_d_list[0]}"
        return name


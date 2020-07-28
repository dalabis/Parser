import time
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup

from bookmaker_parsers.Bookmaker import Bookmaker


class Fonbet(Bookmaker):

    def __init__(self):
        driver = webdriver.Chrome("C:\Program Files (x86)\chromedriver.exe")
        driver.get("https://www.fonbet.ru/live/")
        self.driver = driver
        self.container_css_selector = "div.line-filter-layout__content--q-JdM"
        self.container = None
        time.sleep(5)

    def set_container(self):
        self.container = self.driver.find_element_by_css_selector(self.container_css_selector).get_attribute("innerHTML")

    def track_matches(self):
        container = self.container
        soup = BeautifulSoup(container, "html.parser")
        content = soup.select(".table__body")

        df = pd.DataFrame(columns=['Sport', 'Team_1', 'Team_2', 'time', 'Score_1', 'Score_2', 'Total',  # match data
                                   'Bet_win_1', 'Bet_win_2', 'Bet_draw',  # 1 X 2
                                   'Bet_not_win_1', 'Bet_not_win_2', 'Bet_not_draw',  # X1 12 X2
                                   'Handicap_value_1', 'Bet_handicap_1', 'Handicap_value_2', 'Bet_handicap_2',  # Ф1 Ф2
                                   'Bet_total_value', 'Bet_total_more', 'Bet_total_less'])  # Т Б М
        for matches_in_content in content:
            sport = matches_in_content.select_one(".table__title-text")
            matches = matches_in_content.select('tr[class$="table__row"]')
            try:
                sport = sport.text
            except AttributeError:
                continue
            sport = sport.split('.')[0].strip()
            for match in matches:
                try:
                    team_1, team_2 = self.get_teams(match)
                    time = self.get_time(match)
                    score_1, score_2 = self.get_score(match)
                    total = score_1 + score_2
                except AttributeError:
                    continue
                if sport == 'Футбол':
                    bets, handicaps = self.get_bets_football(match)
                else:
                    break
                if len(bets) == 10 and len(handicaps) == 3 and not all([i == 'nan' for i in bets]):
                    df = df.append({
                        'Sport': sport, 'Team_1': team_1, 'Team_2': team_2, 'time': time,
                        'Score_1': score_1, 'Score_2': score_2, 'Total': total,
                        'Bet_win_1': bets[0], 'Bet_draw': bets[1], 'Bet_win_2': bets[2],  # 1 X 2
                        'Bet_not_win_1': bets[3], 'Bet_not_draw': bets[4], 'Bet_not_win_2': bets[5],  # X1 12 X2
                        'Handicap_value_1': handicaps[0], 'Bet_handicap_1': bets[6],  # Ф1
                        'Handicap_value_2': handicaps[1], 'Bet_handicap_2': bets[7],  # Ф2
                        'Bet_total_value': handicaps[2], 'Bet_total_more': bets[8], 'Bet_total_less': bets[9]},  # T
                        ignore_index=True)
        return df

    def get_teams(self, match):
        teams = match.select_one('h3[class$="table__match-title-text"]', href=True)
        teams = teams.text
        [team_1, team_2] = teams.split('—')  # длинное тире: U+2014 or &#8212
        return team_1.strip(), team_2.strip()

    def get_time(self, match):
        time = match.select_one(".table__time-text")
        time = time.text
        return int(time.split(':')[0])  # mm:ss -> mm

    def get_score(self, match):
        score = match.select_one(".table__score-normal")
        score = score.text
        [score_1, score_2] = score.split(':')
        return int(score_1), int(score_2)

    def get_bets_football(self, match):
        bets_btn = match.select(".table__col._type_btn")
        handicaps_fora = match.select(".table__col._type_fora")
        bets = []
        for bet in bets_btn:
            if bet.get_text() == '':
                bets.append('nan')
                continue
            try:
                bets.append(bet.get_text())
                bets[-1] = float(bets[-1])
            except:
                bets.append('nan')
        handicaps = []
        for handicap in handicaps_fora:
            if handicap.get_text() == '':
                handicaps.append('nan')
                continue
            try:
                handicaps.append(handicap.get_text())
                handicaps[-1] = float(handicaps[-1])
            except:
                handicaps.append('nan')
        return bets, handicaps
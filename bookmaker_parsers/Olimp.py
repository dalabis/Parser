import time
import re
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup

from bookmaker_parsers.Bookmaker import Bookmaker


class Olimp(Bookmaker):

    def __init__(self):
        driver = webdriver.Chrome("C:\Program Files (x86)\chromedriver.exe")
        driver.get("https://www.olimp.bet/live/")
        self.driver = driver
        self.container_css_selector = "div.matches__Wrapper-sc-1tpetmk-1.fTijZo"
        self.container = None
        time.sleep(5)

    def set_container(self):
        self.container = self.driver.find_element_by_css_selector(self.container_css_selector).get_attribute("innerHTML")

    def track_matches(self):
        container = self.container
        soup = BeautifulSoup(container, "html.parser")
        sports = soup.select(".head__StyledWrap-h49frn-0.hEqtLH.many-matches__SportHead-sc-1ag51a6-0.axKuN")
        content = soup.select(".styled__Matches-sc-14faxw8-2.gtEFhx")

        df = pd.DataFrame(columns=['Sport', 'Team_1', 'Team_2', 'time', 'Score_1', 'Score_2', 'Total',  # match data
                                   'Bet_win_1', 'Bet_win_2', 'Bet_draw',  # 1 X 2
                                   'Bet_not_win_1', 'Bet_not_win_2', 'Bet_not_draw',  # X1 12 X2
                                   'Handicap_value_1', 'Bet_handicap_1', 'Handicap_value_2', 'Bet_handicap_2',  # Ф1 Ф2
                                   'Bet_total_value', 'Bet_total_more', 'Bet_total_less'])  # Т Б М
        if len(sports) == len(content):
            for sport, matches_in_sport in zip(sports, content):
                try:
                    sport = sport.text
                except AttributeError:
                    continue
                matches = soup.select(".common__Item-sc-1p0w8dw-0.matches-item__MatchesListItem-gievcx-0.bqzwgE")
                for match in matches:
                    try:
                        team_1, team_2 = self.get_teams(match)
                        time = self.get_time(match)
                        score_1, score_2 = self.get_score(match)
                        total = score_1 + score_2
                    except AttributeError:
                        continue
                    if sport == 'Футбол':
                        bets = self.get_bets_football(match)
                    else:
                        break
                    if len(bets) == 13 and not all([i == 'nan' for i in bets]):
                        df = df.append({
                            'Sport': sport, 'Team_1': team_1, 'Team_2': team_2, 'time': time,
                            'Score_1': score_1, 'Score_2': score_2, 'Total': total,
                            'Bet_win_1': bets[0], 'Bet_draw': bets[1], 'Bet_win_2': bets[2],  # 1 X 2
                            'Bet_not_win_1': bets[3], 'Bet_not_draw': bets[4], 'Bet_not_win_2': bets[5],  # X1 12 X2
                            'Handicap_value_1': bets[6], 'Bet_handicap_1': bets[7],  # Ф1
                            'Handicap_value_2': bets[8], 'Bet_handicap_2': bets[9],  # Ф2
                            'Bet_total_value': bets[10], 'Bet_total_more': bets[11], 'Bet_total_less': bets[12]},  # T
                            ignore_index=True)
        return df

    def get_teams(self, match):
        teams = match.select_one(".default__Link-sc-14zuwl2-0.jyPsAe.title")
        teams = teams.text
        [team_1, team_2] = re.split(r'\s-\s', teams)
        return team_1.strip(), team_2.strip()

    def get_time(self, match):
        time = match.select_one(".short-match__TextSmall-sc-1l87zpe-0.ldGhIe")
        time = time.text
        m = re.search(r'\d+\"', time)
        time = int(time[m.start():m.end() - 1])  # 66"
        return time

    def get_score(self, match):
        score = match.select_one(".styled__MatchScore-vrkr7n-3.coVZux")
        score = score.get('title')
        [score_1, score_2] = score.split(':')
        return int(score_1), int(score_2)

    def get_bets_football(self, match):
        bets_btn = match.find_all('button')
        bets = []
        for bet in bets_btn:
            try:
                bets.append(bet.get_text())
            except AttributeError:
                continue
            try:
                bets[-1] = float(bets[-1])
            except:
                bets[-1] = 'nan'
        return bets[:-1]  # last element pop-up menu, for example: +100
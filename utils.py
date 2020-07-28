import re
import pandas as pd

def find_fork_2(df_1, df_2):
    forks = pd.DataFrame(columns=['Sport', 'Team_11', 'Team_12', 'Team_21', 'Team_22', 'time',
                                  'Score_1', 'Score_2', 'Total',  # match data
                                  'type', 'percent', 'Bet_1', 'Bet_2'])

    for i in range(len(df_1)):
        sport = df_1.loc[i, 'Sport']
        score_1 = df_1.loc[i, 'Score_1']
        score_2 = df_1.loc[i, 'Score_2']
        total = df_1.loc[i, 'Total']
        time = df_1.loc[i, 'time']
        team_11, team_12 = df_1.loc[i, 'Team_1'], df_1.loc[i, 'Team_2']
        for j in range(len(df_2)):
            team_21, team_22 = df_2.loc[j, 'Team_1'], df_2.loc[j, 'Team_2']
            if team_equality(team_11, team_21) and team_equality(team_12, team_22):
                """ вилка на фору"""
                Handicap_value_11, Handicap_value_12 = df_1.loc[i, 'Handicap_value_1'], df_1.loc[i, 'Handicap_value_2']
                Handicap_value_21, Handicap_value_22 = df_2.loc[j, 'Handicap_value_1'], df_2.loc[j, 'Handicap_value_2']
                if Handicap_value_11 == Handicap_value_21 and Handicap_value_12 == Handicap_value_22 and not Handicap_value_11 == 'nan' and not Handicap_value_21 == 'nan':
                    Bet_handicap_11, Bet_handicap_12 = df_1.loc[i, 'Bet_handicap_1'], df_1.loc[i, 'Bet_handicap_2']
                    Bet_handicap_21, Bet_handicap_22 = df_2.loc[j, 'Bet_handicap_1'], df_2.loc[j, 'Bet_handicap_2']
                    if not Bet_handicap_11 == 'nan' and not Bet_handicap_12 == 'nan' and not Bet_handicap_21 == 'nan' and not Bet_handicap_22 == 'nan':
                        Bet_1, Bet_2, percent = fork_check(Bet_handicap_11, Bet_handicap_12, Bet_handicap_21, Bet_handicap_22)
                        type = "handicap " + str(Handicap_value_11)
                        forks = forks.append({'Sport': sport, 'Team_11': team_11, 'Team_12': team_12,
                                              'Team_21': team_21, 'Team_22': team_22, 'time': time,
                                              'Score_1': score_1, 'Score_2': score_2, 'Total': total,  # match data
                                              'type': type, 'percent': percent, 'Bet_1': Bet_1, 'Bet_2': Bet_2}, ignore_index=True)
                """ вилка на тотал"""
                Bet_total_value_1 = df_1.loc[i, 'Bet_total_value']
                Bet_total_value_2 = df_2.loc[j, 'Bet_total_value']
                if Bet_total_value_1 == Bet_total_value_2 and not Bet_total_value_1 == 'nan':
                    Bet_total_more_1, Bet_total_less_1 = df_1.loc[i, 'Bet_total_more'], df_1.loc[i, 'Bet_total_less']
                    Bet_total_more_2, Bet_total_less_2 = df_2.loc[j, 'Bet_total_more'], df_2.loc[j, 'Bet_total_less']
                    if not Bet_total_more_1 == 'nan' and not Bet_total_less_1 == 'nan' and not Bet_total_more_1 == 'nan' and not Bet_total_less_1 == 'nan':
                        Bet_1, Bet_2, percent = fork_check(Bet_total_more_1, Bet_total_less_1, Bet_total_more_2, Bet_total_less_2)
                        type = "total " + str(Bet_total_value_1)
                        forks = forks.append({'Sport': sport, 'Team_11': team_11, 'Team_12': team_12,
                                              'Team_21': team_21, 'Team_22': team_22, 'time': time,
                                              'Score_1': score_1, 'Score_2': score_2, 'Total': total,  # match data
                                              'type': type, 'percent': percent, 'Bet_1': Bet_1, 'Bet_2': Bet_2},
                                             ignore_index=True)
    return forks


def fork_check(Bet_11, Bet_12, Bet_21, Bet_22):
    try:
        percent_1 = 1 / (1 / Bet_11 + 1 / Bet_22)
        percent_2 = 1 / (1 / Bet_12 + 1 / Bet_21)
    except TypeError:
        print(f'One or more of the operands {Bet_11}, {Bet_12}, {Bet_21}, {Bet_22} has not an int type')
        raise
    if percent_1 > percent_2:
        return Bet_11, Bet_22, int(percent_1 * 100)
    else:
        return Bet_12, Bet_21, int(percent_2 * 100)


def team_equality(team_1, team_2):
    team_1 = team_1.lower()
    team_2 = team_2.lower()
    team_1 = team_1.replace('ё', 'е')
    team_2 = team_2.replace('ё', 'е')
    team_1 = re.sub(r'[\(\)]', '', team_1)
    team_2 = re.sub(r'[\(\)]', '', team_2)
    words_1 = team_1.split()
    words_2 = team_2.split()
    for word_1 in words_1:
        for word_2 in words_2:
            if word_1 == word_2 and ((len(words_1)==2 and len(words_2)==1) or (len(words_1)==1 and len(words_2)==2)):
                return True
    return team_1 == team_2
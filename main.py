import os
import time
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

from bookmaker_parsers.Olimp import Olimp
from bookmaker_parsers.Fonbet import Fonbet
from utils import find_fork_2


if __name__ == "__main__":
    olimp = Olimp()
    fonbet = Fonbet()

    olimp.set_container()
    df_olimp = olimp.track_matches()
    temp_hash_olimp = hash(olimp.container)

    fonbet.set_container()
    df_fonbet = fonbet.track_matches()
    temp_hash_fonbet = hash(fonbet.container)

    while True:
        olimp.set_container()
        fonbet.set_container()

        if temp_hash_olimp != hash(olimp.container):
            df_olimp = olimp.track_matches()
            temp_hash_olimp = hash(olimp.container)
        if temp_hash_fonbet != hash(fonbet.container):
            df_fonbet = fonbet.track_matches()
            temp_hash_fonbet = hash(fonbet.container)

        forks = find_fork_2(df_olimp, df_fonbet)
        os.system("cls")
        print(forks)

        time.sleep(1)
import unittest
from utils import team_equality


class PythonTeamEquality(unittest.TestCase):

    def test_1(self):
        team_1 = 'Рубин'
        team_2 = 'Рубин Казань'

        expected = True
        actual = team_equality(team_1, team_2)

        assert expected == actual

    def test_2(self):
        team_1 = 'ИФК Норрчёпинг'
        team_2 = 'Норрчепинг'

        expected = True
        actual = team_equality(team_1, team_2)

        assert expected == actual

    def test_3(self):
        team_1 = 'Варбергс'
        team_2 = 'Варберг'

        expected = True
        actual = team_equality(team_1, team_2)

        assert expected == actual

    def test_4(self):
        team_1 = 'СК Мариа Ланзендорф'
        team_2 = 'Мария Ланцендорф'

        expected = True
        actual = team_equality(team_1, team_2)

        assert expected == actual

    def test_5(self):
        team_1 = 'Брейдаблик/Аугнаблик (до 19)'
        team_2 = 'Брейдаблик-2 U19'

        expected = True
        actual = team_equality(team_1, team_2)

        assert expected == actual

    def test_6(self):
        team_1 = 'Челси (Костин)'
        team_2 = 'Костин (NFC) Челси'

        expected = True
        actual = team_equality(team_1, team_2)

        assert expected == actual

    def test_7(self):
        team_1 = 'Лацио (Jenko)'
        team_2 = 'Лацио (Jenko)'

        expected = True
        actual = team_equality(team_1, team_2)

        assert expected == actual

    def test_8(self):
        team_1 = 'Наполи (Supernova)'
        team_2 = 'Наполи (Kiser)'

        expected = False
        actual = team_equality(team_1, team_2)

        assert expected == actual

    def test_9(self):
        team_1 = 'Лион (WALKER)'
        team_2 = 'Лион (walker)'

        expected = True
        actual = team_equality(team_1, team_2)

        assert expected == actual

    def test_10(self):
        team_1 = 'Неман Гродно (жен)'
        team_2 = 'Неман (ж)'

        expected = True
        actual = team_equality(team_1, team_2)

        assert expected == actual

if __name__ == "__main__":
    unittest.main()

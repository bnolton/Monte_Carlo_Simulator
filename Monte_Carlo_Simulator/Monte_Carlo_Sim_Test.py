import unittest
import pandas as pd
import numpy as np
from Monte_Carlo_Sim import Die, Game, Analyzer


class TestDie(unittest.TestCase):

    def test_Die_init(self):
        coin = np.array(['H', 'T'])
        self.die = Die(coin)
        self.assertTrue(isinstance(coin, np.ndarray))
        self.assertEqual(len(self.die.die), 2)
        self.assertEqual(list(self.die.die.index), ['H', 'T'])

    def test_change_face_weight(self):
        coin = np.array(['H', 'T'])
        self.die = Die(coin)
        self.die.change_face_weight('H', 2)
        self.assertEqual(self.die.die.loc[1, 'Weights'], 2)

    def test_roll_die(self):
        coin = np.array(['H', 'T'])
        self.die = Die(coin)
        rolls = self.die.roll_die(10)
        self.assertEqual(len(rolls), 10)
        self.assertTrue(all(face in ['H', 'T'] for face in rolls))


class TestGame(unittest.TestCase):

    def test_Game_init(self):
        coin = np.array(['H', 'T'])
        die1 = Die(coin)
        die2 = Die(coin)
        self.game = Game([die1, die2])
        self.assertIsNone(self.game.results)
        self.assertEqual(len(self.game.dice), 2)

    def test_play(self):
        coin = np.array(['H', 'T'])
        die1 = Die(coin)
        die2 = Die(coin)
        self.game = Game([die1, die2])
        self.game.play(10)
        self.assertIsInstance(self.game.results, pd.DataFrame)
        self.assertEqual(len(self.game.results), 10)
        self.assertEqual(len(self.game.results.columns), 2)

    def test_show_wide(self):
        coin = np.array(['H', 'T'])
        die1 = Die(coin)
        die2 = Die(coin)
        self.game = Game([die1, die2])
        self.game.play(10)
        result = self.game.show('wide')
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(result.shape, (10, 2))

    def test_show_narrow(self):
        coin = np.array(['H', 'T'])
        die1 = Die(coin)
        die2 = Die(coin)
        self.game = Game([die1, die2])
        self.game.play(10)
        result = self.game.show('narrow')
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), 20)  # 10 rolls * 2 dice


class TestAnalyzer(unittest.TestCase):

    def test_init(self):
        coin = np.array(['H', 'T'])
        die1 = Die(coin)
        die2 = Die(coin)
        game = Game([die1, die2])
        game.play(10)
        self.analyzer = Analyzer(game)
        with self.assertRaises(ValueError):
            Analyzer("not a game")

    def test_jackpot(self):
        coin = np.array(['H', 'T'])
        die1 = Die(coin)
        die2 = Die(coin)
        game = Game([die1, die2])
        game.play(10)
        self.analyzer = Analyzer(game)
        result = self.analyzer.jackpot()
        self.assertIsInstance(result, int)
        self.assertTrue(result >= 0)

    def test_face_counts(self):
        coin = np.array(['H', 'T'])
        die1 = Die(coin)
        die2 = Die(coin)
        game = Game([die1, die2])
        game.play(10)
        self.analyzer = Analyzer(game)
        result = self.analyzer.face_counts()
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result.columns), 2)  # H and T

    def test_combo_count(self):
        coin = np.array(['H', 'T'])
        die1 = Die(coin)
        die2 = Die(coin)
        game = Game([die1, die2])
        game.play(10)
        self.analyzer = Analyzer(game)
        result = self.analyzer.combo_count()
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result.columns), 1)
        self.assertTrue('count' in result.columns)

    def test_permu_count(self):
        coin = np.array(['H', 'T'])
        die1 = Die(coin)
        die2 = Die(coin)
        game = Game([die1, die2])
        game.play(10)
        self.analyzer = Analyzer(game)
        result = self.analyzer.permu_count()
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result.columns), 1)
        self.assertTrue('count' in result.columns)


if __name__ == '__main__':
    unittest.main()
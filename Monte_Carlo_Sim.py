import numpy as np
import pandas as pd


class Die():
    """
    A class representing a die with customizable faces and weights.

    This class creates a die object that can have arbitrary face values and weights.
    The faces must be unique and are stored in a numpy array. Each face has an
    associated weight that affects the probability of rolling that face.

    Attributes:
        sides (numpy.ndarray): Array of unique face values for the die
        die (pandas.DataFrame): DataFrame storing faces as index and their weights

    Methods:
        change_face_weight(face, new_weight): Changes the weight of a specific face
        roll_die(r=1): Rolls the die r times and returns results
        die_state(): Prints current state of die faces and weights
    """

    def __init__(self, sides):
        """
        Initialize a Die object with given sides.

        Parameters:
        -----------
        sides : numpy.ndarray
            Array of unique values representing the faces of the die

        Raises:
        -------
        TypeError
            If sides is not a numpy array
        ValueError
            If the array has repeated sides
        """

        self.sides = sides
        # if it is a numpy array#
        if isinstance(sides, np.ndarray):
            # test for uniqueness#
            if len(self.sides) == len(set(self.sides)):
                # set up weights variable#
                weights = np.array([1])
                # make weights same length as sides#
                while len(weights) < len(self.sides):
                    weights = np.append(weights, 1)
                # set up dataframe#
                self.die = pd.DataFrame({'Faces': self.sides, 'Weights': weights})
                self.die.set_index('Faces', inplace=True)
            else:
                raise ValueError('The array has repeated sides')
        else:
            raise TypeError('Sides is not a numpy array')

    def change_face_weight(self, face, new_weight):
        """
        Change the weight of a specified face of the die.

        Parameters:
        -----------
        face : any
            The face value to modify (must exist in die faces)
        new_weight : float
            The new weight to assign to the face

        Raises:
        -------
        IndexError
            If the specified face is not on the die
        TypeError
            If the new weight is not numeric
        """

        if face in self.sides:
            if new_weight == float(new_weight):
                try:
                    # Check to see if new_weight is the right value type.#
                    new_weight = float(new_weight)
                except(ValueError, TypeError):
                    raise TypeError('The weight of the face must be numeric')
                self.die.loc[face, 'Weights'] = new_weight
        else:
            raise IndexError('This face is not on the die')

    def roll_die(self, r=1):
        """
        Roll the die one or more times.

        Parameters:
        -----------
        r : int, optional
            Number of times to roll the die (default is 1)

        Returns:
        --------
        list
            Results of the die rolls based on face weights
        """

        probs = self.die['Weights'] / self.die['Weights'].sum()
        die_roll = list(np.random.choice(self.die.index, size=r, p=probs))
        return die_roll

    def die_state(self):
        """
        Show the current state of the die.

        Returns:
        --------
        None
            Prints the DataFrame showing faces and their weights
        """

        print(self.die)


class Game():
    """
    A class to simulate rolling multiple dice and store the results.

    Attributes:
        dice (list): A list of Die objects to be used in the game
        results (DataFrame): A DataFrame containing the results of the dice rolls, where each column represents a die and each row represents a roll

    Methods:
        play(n_rolls): Rolls all dice n_rolls times and stores results
        show(form): Returns the results in either 'wide' or 'narrow' format
    """

    def __init__(self, dice):
        """Initialize a new dice game.

        Parameters:
        -----------
        dice : list
             A list of Die objects to be used in the game

        Returns:
        --------
        None
        """

        self.dice = dice
        self.results = None

    def play(self, n_rolls):
        """Play the dice game by rolling all dice n_rolls times.

        Parameters:
        -----------
        n_rolls : int
            The number of times to roll all the dice

        Returns:
        --------
        None
            Results are stored in self.results DataFrame
        """

        # Store the results#
        results = {f'die_{i}': Die.roll_die(n_rolls)
                   for i, Die in enumerate(self.dice, 1)}
        # Create DataFrame with roll numbers as index#
        self.results = pd.DataFrame(results, index=[f'roll_{i + 1}' for i in range(n_rolls)])

    def show(self, form='wide'):
        """Display the results of the dice game.

        Parameters:
        -----------
        form : str, optional
            Format of the results, either 'wide' or 'narrow' (default is 'wide')
            - 'wide': Each die roll is a column
            - 'narrow': Results are melted into a long format with die number and outcome columns

        Returns:
        --------
        pandas.DataFrame
            DataFrame containing the results in the specified format

        Raises:
        -------
        ValueError
            If no games have been played or if form is not 'wide' or 'narrow'
        """

        if self.results is None:
            raise ValueError("No games have been played yet")

        if form.lower() not in ['wide', 'narrow']:
            raise ValueError("Form must be 'wide' or 'narrow'")

        if form.lower() == 'wide':
            return self.results
        else:
            return self.results.melt(ignore_index=False, var_name='die', value_name='outcome').set_index('die', append=True)


class Analyzer:
    """
    A class to analyze the results of a dice game.

    This class provides methods to analyze various aspects of dice game results, including counting jackpots (all dice showing same face), counting face occurrences, and analyzing combinations and permutations of dice outcomes.

    Methods:
        jackpot(): Returns the number of rolls that resulted in all dice showing the same face
        face_counts(): Returns a DataFrame showing the count of each face value per roll
        combo_count(): Returns counts of unique combinations of faces (order doesn't matter)
        permu_count(): Returns counts of unique permutations of faces (order matters)
    """
    def __init__(self, game):
        if not isinstance(game, Game):
            raise ValueError("Input must be a Game object.")
        self.game = game

    def jackpot(self):
        """
        Counts the number of rolls where all dice show the same face.

        Returns:
        --------
            int: Number of jackpots (rolls with all matching faces)
        """
        outcome = self.game.show()
        return sum(outcome.nunique(axis=1) == 1)

    def face_counts(self):
        """
        Computes how many times each face appears in each roll.

        Returns:
        --------
            DataFrame: Index shows roll numbers, columns show possible faces, values show count of each face in that roll
        """
        outcome = self.game.show()
        faces = pd.unique(outcome.values.ravel())
        counts = pd.DataFrame(index=outcome.index, columns=faces)
        for face in faces:
            counts[face] = (outcome == face).sum(axis=1)
        return counts

    def combo_count(self):
        """
        Computes distinct combinations of faces rolled and their frequencies.
        Combinations are order-independent (sorted).

        Returns:
        --------
            DataFrame: Index shows distinct combinations, column shows count of occurrences
        """
        outcome = self.game.show()
        combos = outcome.apply(lambda x: tuple(sorted(x.values)), axis=1)
        return pd.DataFrame(combos.value_counts(), columns=['count'])

    def permu_count(self):
        """
        Computes distinct permutations of faces rolled and their frequencies.
        Permutations are order-dependent (unsorted).

        Returns:
        --------
            DataFrame: Index shows distinct permutations, column shows count of occurrences
        """
        outcome = self.game.show()
        permus = outcome.apply(lambda x: tuple(x.values), axis=1)
        return pd.DataFrame(permus.value_counts(), columns=['count'])
# Monte_Carlo_Simulator
DS5100 Final Project
Brian Nolton

This module is a Monte Carlo Simulator I created for my DS5100 class at UVA. In it, you can create dice of any size and weights, roll them, and analyze the results. Here is an example of how that works:

###Die CLass###

#Create dice#
d6 = np.array([1,2,3,4,5,6])
d1 = Die(d6)
d2 = Die(d6)
d3 = Die(d6)

#Change the weight#
d2.change_face_weight(6,5)
d3.change_face_weight(1,5)

#Roll a die 4 times
d1.roll(4)

#Check the die weight status
d1.die_state()

###Game Class###

#Play a game 1000 times rolling all 3 dice
dg = Game([d1,d2,d3])
dg.play(1000)

#Show the results
dg.show()

###Analyzer Class###

#Show how many jackpots are won (all dice showing the same face)
dga = Analyzer(dg)
dg1a.jackpot()

#Count how many times each face was rolled for each roll
dga.face_counts()

#Show how many combinations were rolled and how many times they were rolled
dga.combo_count()

#Show how many permutations were rolled and how many times they were rolled
dga.permu_count()


Here are the docstrings for Monte_Carlo_Sim:

class Die(builtins.object)
 |  Die(sides)
 |  
 |  A class representing a die with customizable faces and weights.
 |  
 |  This class creates a die object that can have arbitrary face values and weights.
 |  The faces must be unique and are stored in a numpy array. Each face has an
 |  associated weight that affects the probability of rolling that face.
 |  
 |  Attributes:
 |      sides (numpy.ndarray): Array of unique face values for the die
 |      die (pandas.DataFrame): DataFrame storing faces as index and their weights
 |  
 |  Methods:
 |      change_face_weight(face, new_weight): Changes the weight of a specific face
 |      roll_die(r=1): Rolls the die r times and returns results
 |      die_state(): Prints current state of die faces and weights
 |  
 |  Methods defined here:
 |  
 |  __init__(self, sides)
 |      Initialize a Die object with given sides.
 |      
 |      Parameters:
 |      -----------
 |      sides : numpy.ndarray
 |          Array of unique values representing the faces of the die
 |      
 |      Raises:
 |      -------
 |      TypeError
 |          If sides is not a numpy array
 |      ValueError
 |          If the array has repeated sides
 |  
 |  change_face_weight(self, face, new_weight)
 |      Change the weight of a specified face of the die.
 |      
 |      Parameters:
 |      -----------
 |      face : any
 |          The face value to modify (must exist in die faces)
 |      new_weight : float
 |          The new weight to assign to the face
 |      
 |      Raises:
 |      -------
 |      IndexError
 |          If the specified face is not on the die
 |      TypeError
 |          If the new weight is not numeric
 |  
 |  die_state(self)
 |      Show the current state of the die.
 |      
 |      Returns:
 |      --------
 |      None
 |          Prints the DataFrame showing faces and their weights
 |  
 |  roll_die(self, r=1)
 |      Roll the die one or more times.
 |      
 |      Parameters:
 |      -----------
 |      r : int, optional
 |          Number of times to roll the die (default is 1)
 |      
 |      Returns:
 |      --------
 |      list
 |          Results of the die rolls based on face weights
 |  
 |  ----------------------------------------------------------------------
 |  Data descriptors defined here:
 |  
 |  __dict__
 |      dictionary for instance variables (if defined)
 |  
 |  __weakref__
 |      list of weak references to the object (if defined)


class Game(builtins.object)
 |  Game(dice)
 |  
 |  A class to simulate rolling multiple dice and store the results.
 |  
 |  Attributes:
 |      dice (list): A list of Die objects to be used in the game
 |      results (DataFrame): A DataFrame containing the results of the dice rolls, where each column represents a die and each row represents a roll
 |  
 |  Methods:
 |      play(n_rolls): Rolls all dice n_rolls times and stores results
 |      show(form): Returns the results in either 'wide' or 'narrow' format
 |  
 |  Methods defined here:
 |  
 |  __init__(self, dice)
 |      Initialize a new dice game.
 |      
 |      Parameters:
 |      -----------
 |      dice : list
 |           A list of Die objects to be used in the game
 |      
 |      Returns:
 |      --------
 |      None
 |  
 |  play(self, n_rolls)
 |      Play the dice game by rolling all dice n_rolls times.
 |      
 |      Parameters:
 |      -----------
 |      n_rolls : int
 |          The number of times to roll all the dice
 |      
 |      Returns:
 |      --------
 |      None
 |          Results are stored in self.results DataFrame
 |  
 |  show(self, form='wide')
 |      Display the results of the dice game.
 |      
 |      Parameters:
 |      -----------
 |      form : str, optional
 |          Format of the results, either 'wide' or 'narrow' (default is 'wide')
 |          - 'wide': Each die roll is a column
 |          - 'narrow': Results are melted into a long format with die number and outcome columns
 |      
 |      Returns:
 |      --------
 |      pandas.DataFrame
 |          DataFrame containing the results in the specified format
 |      
 |      Raises:
 |      -------
 |      ValueError
 |          If no games have been played or if form is not 'wide' or 'narrow'
 |  
 |  ----------------------------------------------------------------------
 |  Data descriptors defined here:
 |  
 |  __dict__
 |      dictionary for instance variables (if defined)
 |  
 |  __weakref__
 |      list of weak references to the object (if defined)


class Analyzer(builtins.object)
 |  Analyzer(game)
 |  
 |  A class to analyze the results of a dice game.
 |  
 |  This class provides methods to analyze various aspects of dice game results, including counting jackpots (all dice showing same face), counting face occurrences, and analyzing combinations and permutations of dice outcomes.
 |  
 |  Methods:
 |      jackpot(): Returns the number of rolls that resulted in all dice showing the same face
 |      face_counts(): Returns a DataFrame showing the count of each face value per roll
 |      combo_count(): Returns counts of unique combinations of faces (order doesn't matter)
 |      permu_count(): Returns counts of unique permutations of faces (order matters)
 |  
 |  Methods defined here:
 |  
 |  __init__(self, game)
 |      Initialize self.  See help(type(self)) for accurate signature.
 |  
 |  combo_count(self)
 |      Computes distinct combinations of faces rolled and their frequencies.
 |      Combinations are order-independent (sorted).
 |      
 |      Returns:
 |      --------
 |          DataFrame: Index shows distinct combinations, column shows count of occurrences
 |  
 |  face_counts(self)
 |      Computes how many times each face appears in each roll.
 |      
 |      Returns:
 |      --------
 |          DataFrame: Index shows roll numbers, columns show possible faces, values show count of each face in that roll
 |  
 |  jackpot(self)
 |      Counts the number of rolls where all dice show the same face.
 |      
 |      Returns:
 |      --------
 |          int: Number of jackpots (rolls with all matching faces)
 |  
 |  permu_count(self)
 |      Computes distinct permutations of faces rolled and their frequencies.
 |      Permutations are order-dependent (unsorted).
 |      
 |      Returns:
 |      --------
 |          DataFrame: Index shows distinct permutations, column shows count of occurrences
 |  
 |  ----------------------------------------------------------------------
 |  Data descriptors defined here:
 |  
 |  __dict__
 |      dictionary for instance variables (if defined)
 |  
 |  __weakref__
 |      list of weak references to the object (if defined)

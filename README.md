# 8_puzzle
Some thing I did in my spare time after a lecture in my A.I course.

# Details
To play use the play function with a 3x3 list of lists. If the puzzle is solveable the way to the goal state will appear. Play also takes a depth arg, which limits the depth of each tree search. By eliminating the exponential branching affect, the program runs fairly quickly. 

# Example
play([[5,2,0],[1,6,4],[3,7,8]])

 [5, 2, 0] 
 [1, 6, 4] 
 [3, 7, 8] 

 [5, 0, 2] 
 [1, 6, 4] 
 [3, 7, 8] 

 [0, 5, 2] 
 [1, 6, 4] 
 [3, 7, 8] 

 [1, 5, 2] 
 [0, 6, 4] 
 [3, 7, 8] 

 continues...

 [1, 0, 2] 
 [4, 5, 3] 
 [7, 8, 6] 

 [1, 2, 0] 
 [4, 5, 3] 
 [7, 8, 6] 

 [1, 2, 3] 
 [4, 5, 0] 
 [7, 8, 6] 

 [1, 2, 3] 
 [4, 5, 6] 
 [7, 8, 0] 
 
# Currently Testing Peformance 
I am comparing my programs results with the optimal result for all possible solvable boards. I am hoping for less than 3% error on average.
# Possible continuation
May build off this program and apply it too 15-puzzle.


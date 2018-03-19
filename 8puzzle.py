from TreeNode import Node, Tree, GOAL_STATE

class Game:
    def __init__(self, initial=None):
        if not initial:
            self.sequence = []
        else:
            self.sequence=[initial]
    
    @property
    def countMoves(self):
        if self.sequence:
            return len(self.sequence)
        else:
            return 0
      
    def addMove(self, board):
        self.sequence.append(board)
    
    def getCurrentBoard(self):
        if self.sequence:
            return self.sequence[-1]
        else:
            print("haven't started")
            return None
    
    def isGoal(self):
        data = self.getCurrentBoard()
        for row in range(len(data)):
            for col in range(len(data[row])):
                if data[row][col]!= GOAL_STATE[row][col]:
                    return False
        return True
        
    def isSolvable(self):
        data = self.getCurrentBoard()
        inverse = 0
        for row in range(len(data)):
            for col in range(row+1,len(data)):
                if data[col]!=0 and data[row]!=0 and data[row]>data[col]:
                    inverse +=1
        return(inverse%2==0)
    
    
    def __str__(self):
        out = []
        for board in self.sequence:
            out.append(
                     " {0} \n {1} \n {2} \n".format(
                             board[0],
                             board[1],
                             board[2],
                             )
                     )
        return("\n".join(out))
            
        
def play(data, treedepth=10):
    game = Game(initial=data)
    if not game.isSolvable():
        print("not solvable")
        return
    tree = Tree(data=game.getCurrentBoard())
    depth = treedepth
    iterdepth = treedepth
    while not game.isGoal():
        createChildren(tree.root, depth)
        move = findNextMove(tree)
        while move is tree.root:
            #---------------------------
            #if a smaller hueristic value is not found we look deeper
            #---------------------------
            iterdepth += 5
            tree = Tree(data=move.data)
            createChildren(tree.root, iterdepth)
            move = findNextMove(tree)
            if isGoal(move.data):
                stack = [move.data]
                while move.getParent():
                    move = move.getParent()
                    stack.append(move.data)
                while stack:
                    game.addMove(stack.pop())
                #---------------------------
                #this returns the path to the solution found. 
                #the stack is the best solution given the initial state for
                #the last move found outside the current while loop
                #---------------------------
                print(game)
                return
        if isGoal(move.data):
                stack = [move.data]
                while move.getParent():
                    move = move.getParent()
                    stack.append(move.data)
                while stack:
                    game.addMove(stack.pop())
                break
        game.addMove(move.data)
        tree = Tree(data=game.getCurrentBoard())

    #---------------------------
    #This print statement is if the game has no local mins
    #---------------------------
    print(game)
    

    
def isGoal(data):
    for row in range(len(data)):
        for col in range(len(data[row])):
            if data[row][col]!= GOAL_STATE[row][col]:
                return False
    return True
	 
    
def findNextMove(tree):
    #------------------------------------------------
    #suseptible to local min in hill climbing problem
    #------------------------------------------------
    boardsize = len(tree.root.data)
    minval = boardsize**boardsize
    minnode = None
    que, gen = [tree.root], []
    while que:
        currentgen = []
        for node in que:
            for kid in node.children:
                currentgen.append(kid)
            if node.val == 0:
                minval = node.val
                minnode = node
                return minnode
            # this returns minnode but need 
            elif node.val <= minval and not minnode:
                minval=node.val
                minnode = node
            elif node.val<minval and node is not tree.root:
                minval=node.val
                minnode = node
        gen.append(currentgen)
        que=currentgen
    if minnode is tree.root:
        return minnode
    while minnode.getParent() is not tree.root:
        minnode = minnode.getParent()
    return minnode
                
    
def createState(data, r0, c0, r1, c1):
    num = data[r1][c1]
    state = []
    for row in range(len(data)):
        group = []
        for col in range(len(data[row])):
            if row==r0 and col==c0:
                group.append(num)
            elif row==r1 and col==c1:
                group.append(0)
            else:
                same = data[row][col]
                group.append(same)
        state.append(group)
    return state


def find0(data):
    for r in range(len(data)):
        for c in range(len(data[r])):
            if data[r][c]==0:
                 return r , c 
    return -1, -1 

def createChildren(root, maxdepth):
        que, mem = [root], []
        while que:
            gen = []
            cost = 0 if not mem else cost+1
            #------------------------------
            #need to edit for cost of each move
            #------------------------------
            for parent in que:
                current_state = parent.data
                r0, c0 = find0(current_state)
                kidState = []
                if r0-1>=0:
                    #------------------------------------------------
                    #can move left
                    #------------------------------------------------
                    r1 = r0-1
                    kidState.append(createState(current_state, r0, c0, r1, c0))
                if r0+1<=2:
                    #------------------------------------------------
                    #can move right
                    #------------------------------------------------
                    r2 = r0+1
                    kidState.append(createState(current_state, r0, c0, r2, c0))
                if c0-1>=0:
                    #------------------------------------------------
                    #can move down
                    #------------------------------------------------
                    c1 = c0-1
                    kidState.append(createState(current_state, r0, c0, r0, c1))
                if c0+1<=2:
                    #------------------------------------------------
                    #can move up
                    #------------------------------------------------
                    c2 = c0+1
                    kidState.append(createState(current_state, r0, c0, r0, c2))
                
                for state in kidState:
                    #------------------------------------------------
                    #can move left
                    #------------------------------------------------
                    if state == GOAL_STATE:
                        #------------------------------------------------
                        #no need to go any further
                        #------------------------------------------------
                        kid = Node(data=state)
                        parent.addChild(kid)
                        return
                    
                    elif parent.parent is None:
                        #------------------------------------------------
                        #first generation from root
                        #------------------------------------------------
                        kid = Node(data=state)
                        parent.addChild(kid)
                        gen.append(kid)
                        
                    elif state != parent.parent.data:
                        #------------------------------------------------
                        #removing kids that are same move as grandparent
                        #reducing copies deduces branching affect 
                        #helps optimize searches
                        #------------------------------------------------
                        kid = Node(data=state)
                        parent.addChild(kid)
                        gen.append(kid)
            mem.append(gen)
            que = gen
            if len(mem) >= maxdepth:
                que=[]
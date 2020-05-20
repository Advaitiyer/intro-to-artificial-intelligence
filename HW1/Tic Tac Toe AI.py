import numpy as np

NETID = "aiyer01" # Replace with your NetID!
BLANK = "_"

def state_str(state, prefix=""):
    return "\n".join("%s%s" % (prefix, "".join(row)) for row in state)

def move(state, symbol, row, col):
    if state[row,col] != BLANK: return False
    new_state = state.copy()
    new_state[row,col] = symbol
    return new_state

def score(state):
    
    for symbol, point in zip("ox", [[-2,-2,-3,-2],[2,2,3,2]]):
        if (state == symbol).all(axis=1).any(): return point[0]
        if (state == symbol).all(axis=0).any(): return point[1]
        if (np.diagonal(state) == symbol).all(): return point[2]   
        if (np.diagonal(np.rot90(state)) == symbol).all(): return point[3]
    
    return 0

def dfs(state, symbol):
    a=score(state)
    if a in [-2,-2,-3,-2,2,2,3,2]: return [1,a]

    has_child = False
    leaf_count = 0
    v=0
    for row in range(3):
        for col in range(3):
            child = move(state, symbol, row, col)
            if child is False: continue
            has_child = True
            ls1 = dfs(child, "x" if symbol is "o" else "o")
            leaf_count += ls1[0]
            v=v+ls1[1]
    
    if has_child: return [leaf_count,v]
    else: return [1,v]

if __name__ == "__main__":

    state0 = np.array([[BLANK]*3]*3)
    
    state1 = move(state0, "x", 0, 0)
    state2 = move(state1, "x", 0, 0)
    print(state_str(state0))
    print(state_str(state1))
    print(state2)
    
    ls = dfs(state0, "x")
    #v =0 # fix value for v 
    print("DFS: leaf count = %d, expected value = %f" % (ls[0],ls[1]))

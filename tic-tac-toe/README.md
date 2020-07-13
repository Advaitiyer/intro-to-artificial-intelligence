## Tic Tac Toe with Minimax search

**Description:** Implementation of the game of Tic Tac Toe.

### 1. Define moves

```javascript
define(move):
  if state is not empty return False
  or input into state
```

### 2. Define scores

Symbols and points are defined such that one among "O" receives negative and "X" receives positive scores.

```javascript
for symbol, point in ("OX", [[-2,-2,-3,-2],[2,2,3,2]]):
  provide [-2,2] if state == symbol in "Y" axis
  provide [-2,2] if state == symbol in "X" axis
  provide [-3,3] if state == symbol in diagonal axis
  provide [-2,2] if state == symbol 90 degrees rotated
```

### 3. Depth first search algorithm

```javascript
define DFS(state, symbol):
  initial_score = score(state of the system)
  if initial score is in [-2,-2,-3,-2,2,2,3,2]: return [1, initial_score]
  Initial has_child = False
  Initial leaf_count = 0
  Initial expected_value = 0
  for row in range(3):
    for column in range(3):
      child = move(state, symbol, row, column)
      if child is False: continue
      has_child = True
      children_list = DFS(child, "X" if symbol is "O", else "O")
      leaf_count += children_list[0]
      expected_value = expected_value + children_list[1]
```

### 4. Leaf counts and expected values

Depending on how much the depth the algorithm has to traverse, the leaf count value changes. 

The expected value is the score that is received at that state.

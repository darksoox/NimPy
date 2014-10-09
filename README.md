NimPy
=====

Python implementation of the mathematical strategy game Nim.

I wanted to check if it was possible to implement the game such that the
computer you play against always puts you into a kernel position if it is
possible, that is, a losing position.

Who wins this game will mainly depend on who starts, and what board is set. If
you set a board such that you start in a kernel position, then you will lose (if
this is correct). Otherwise you will have to make a series of only correct moves 
in order to win the game, if you at any time make an incorrect move, the
computer will put you into a kernel position, and the game is lost.

Explanation of Nim: http://en.wikipedia.org/wiki/Nim

If interested in kernels, please see:
- http://www.youtube.com/watch?v=oDniZCmNmNw&t=8m10s (Explains how this works in
  Nim)
- http://www.sciencedirect.com/science/article/pii/S0012365X06003268

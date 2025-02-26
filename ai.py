"""
  Wumpus World

  Class Attribute:
    SIZE = 4

  Public Attributes:
    observation -> the player's current perception as a list
      Order: [Stench, Breeze, Glitter, Bump, Scream]

    moves -> a list of the moves taken so far. First move is at index 0

    facing -> the players facing as an (x, y) tuple
    Facing (0, 1) -> up
      1, 0 === "right"
      0, 1 === "up"
      -1, 0 === "left"
      0, -1 === "down"

    player_loc  -> the players location as an (x, y) tuple

    start_loc   -> player starting location (1, 1)

    has_gold    -> True/False

    ammo        -> 1 or 0

    You should only need these attributes.

    Possible Actions: "forward", "left", "right", "grab", "climb", "shoot"
"""

from wumpus import WumpusWorld

def pick_move(wordl: WumpusWorld):
    pass
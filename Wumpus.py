# Author: Gentry Atkinson
# Organization: St. Edwards University

import os
import pygame
from random import randint

IMG = "imgs"


# A class representing the Wumpus World game environment.
class WumpusWorld:
  SIZE = 4
  LEGAL_MOVES = ['forward', 'right', 'left', 'shoot', 'grab', 'climb']

  # Initialize the game environment with random locations for hazards.
  def __init__(self):
    self.player_loc = (1, 1)
    self.__wumpus_loc = (randint(1, self.SIZE), randint(2, self.SIZE))
    self.start_loc = (1, 1)
    self.__gold_loc = (randint(1, self.SIZE), randint(2, self.SIZE))
    self.__pits = self.__generate_pits()
    self.moves = []
    self.observation = ["None"] * 5
    self.facing = (0, 1)  # Initially facing up.
    self.has_gold = False
    self.escape = False
    self.ammo = 1
    self.died = False
    self.__load_images()
    self.perceive()

  def __load_images(self):
    self.imgs = {
      'world' : pygame.image.load(os.path.join(IMG, 'world.png')),
      'wumpus' : pygame.image.load(os.path.join(IMG, 'wumpus.png')),
      'breeze' : pygame.image.load(os.path.join(IMG, 'breeze.png')),
      'stink' : pygame.image.load(os.path.join(IMG, 'stink.png')),
      'gold' : pygame.image.load(os.path.join(IMG, 'gold.png')),
      'pit' : pygame.image.load(os.path.join(IMG, 'pit.png')),
    }    

  # Randomly generate pit locations, avoiding start and hazard locations.
  def __generate_pits(self):
    pits = []
    for _ in range(randint(1, 4)):
      x, y = randint(1, self.SIZE), randint(1, self.SIZE)
      if (x, y) in [self.start_loc, self.__wumpus_loc, self.__gold_loc]:
        continue
      pits.append((x, y))
    return pits

  # Visualize the current state of the Wumpus World environment.
  def draw(self):
    #plt.figure(figsize=(4, 4))
    #ax = plt.gca()
    #ax.get_xaxis().set_visible(False)
    #ax.get_yaxis().set_visible(False)
    #ax.set_xlim((0, self.SIZE))
    #ax.set_ylim((0, self.SIZE))

    # Draw grid lines.
    for i in range(self.SIZE + 1):
      #plt.axvline(x=i, color="black", linewidth=3.0)
      #plt.axhline(y=i, color="black", linewidth=3.0)
      pass

    # Draw entities in the environment.
    self.__draw_entity(IMG + "/player.png", self.player_loc, 0.8, 0.9)
    self.__draw_entity(IMG + "/wumpus.png", self.__wumpus_loc, 1, 1)
    self.__draw_entity(IMG + "/gold.png", self.__gold_loc, 1, 0.5)
    self.__draw_entity(IMG + "/start.png", self.start_loc, 1, 0.3)
    for pit in self.__pits:
      self.__draw_entity(IMG + "/pit.png", pit, 1, 1)

    #plt.tight_layout()
    # plt.savefig("world.png")
    #plt.show()

  # Helper function to draw an entity at a specified location.
  def __draw_entity(self, img_path, location, width, height):
    if location:
      icon_x, icon_y = float(location[0] - 1), float(location[1] - 1)
      #plt.imshow(mpimg.imread(img_path), extent=(icon_x, icon_x + width, icon_y, icon_y + height))

  # Update the player's observations based on the current state.
  def perceive(self):
    self.observation = [
        "None", "None", "None", self.observation[3], self.observation[4]
    ]
    if self.player_loc == self.__gold_loc:
      self.observation[2] = "Glitter"
    self.__update_observation_for_hazards()

  def __update_observation_for_hazards(self):
    """Check proximity to Wumpus and pits to update observations."""
    # Check for Wumpus proximity.
    if self.__is_adjacent(self.player_loc, self.__wumpus_loc):
      self.observation[0] = "Stench"
    # Check for pit proximity.
    for pit in self.__pits:
      if self.__is_adjacent(self.player_loc, pit):
        self.observation[1] = "Breeze"

  # Determine if two locations are adjacent (excluding diagonal).
  @staticmethod
  def __is_adjacent(loc1, loc2):
    return abs(loc1[0] - loc2[0]) + abs(loc1[1] - loc2[1]) == 1

  # Check if the player has died from falling into a pit or encountering the Wumpus.
  def player_dead(self):
    if self.player_loc in self.__pits:
      print("Our hero falls screaming into a bottomless pit.")
      self.died = True
      return True
    if self.player_loc == self.__wumpus_loc:
      print("Our hero is torn to bloody shreds by a ravenous Wumpus.")
      self.died = True
      return True
    return False

  # Perform an action from the set of legal moves and update the game state.
  def act(self, action):
    assert action in self.LEGAL_MOVES, "Illegal Action"
    self.observation[3:] = ["None", "None"]
    self.moves.append(action)
    self.__execute_action(action)
    self.perceive()

  # Internal method to handle the execution of player actions.
  def __execute_action(self, action):
    match action:
      case "forward":
        self.__move_forward()
      case "left":
        self.facing = self.__rotate_left(self.facing)
      case "right":
        self.facing = self.__rotate_right(self.facing)
      case "grab":
        self.__grab_gold()
      case "climb":
        self.__attempt_climb()
      case "shoot":
        self.__shoot_arrow()

  # Attempt to move the player forward based on the current facing direction.
  def __move_forward(self):
    new_x, new_y = (self.player_loc[0] + self.facing[0], self.player_loc[1] + self.facing[1])
    if not (1 <= new_x <= self.SIZE) or not (1 <= new_y <= self.SIZE):
      self.observation[3] = "Bump"
    else:
      self.player_loc = (new_x, new_y)

  # Rotate the player's facing direction to the left.
  @staticmethod
  def __rotate_left(facing):
    return (-facing[1], facing[0])

  # Rotate the player's facing direction to the right.
  @staticmethod
  def __rotate_right(facing):
    return (facing[1], -facing[0])

  # Allow the player to grab gold if it is in the same location.
  def __grab_gold(self):
    if self.player_loc == self.__gold_loc:
      print("Our hero retrieves the glittering gold.")
      self.__gold_loc = None
      self.has_gold = True

  # Check if the player can climb out of the dungeon.
  def __attempt_climb(self):
    if self.player_loc == self.start_loc:
      print("Our hero climbs panting from the wretched dungeon.")
      self.escape = True

  # Handle the shooting of an arrow and its consequences.
  def __shoot_arrow(self):
    if self.ammo > 0:
      self.ammo -= 1
      arrow_loc = (self.player_loc[0] + self.facing[0], self.player_loc[1] + self.facing[1])
      while 1 <= arrow_loc[0] <= self.SIZE and 1 <= arrow_loc[1] <= self.SIZE:
        if arrow_loc == self.__wumpus_loc:
          print("The arrow sinks deeply into the torso of the wailing Wumpus.")
          self.observation[4] = "Scream"
          self.__wumpus_loc = None
          break
        arrow_loc = (arrow_loc[0] + self.facing[0], arrow_loc[1] + self.facing[1])

  # Calculate and return the player's score based on game outcomes.
  def score(self):
    score = -len(self.moves)
    if self.died:
      score -= 1000
    if self.has_gold and self.escape:
      score += 1000
    if self.ammo < 1:
      score -= 10
    return score
import sys
from character import Character
from monster import Dragon
from monster import Goblin
from monster import Troll


class Game:
  def setup(self):
    self.player = Character()
    self.monsters = [
      Goblin(),
      Troll(),
      Dragon()
    ]
    self.monster = self.get_next_monster()

    
  def get_next_monster(self):
    try:
      return self.monsters.pop(0)
    except IndexError:
      return None

    
  def monster_turn(self):
    #Monster attacks
    if self.monster.attack():
      print ("{} is attacking!".format(self.monster))
      
      #Player dodge decision and results of dodge attempt
      if input ("Dodge? Y/N").lower() == "y":
        if self.player.dodge():
          print("You dodged the attack!")
        else:
          print("You got hit anyway!")
          self.player.hit_points -= 1
      else:
        print("{} hit you for 1 point.".format(self.monster))
        self.player.hit_points -= 1
    
    #Monster does not attack
    else:
      print("{} isn't attacking this turn.".format(self.monster))

      
  def player_turn(self):
    #let the player attack, rest, or quit
    player_choice = input("[A]ttack, [R]est, [Q]uit").lower()
    #if they attack:
    if player_choice == "a":
      print("You're attacking {}!".format(self.monster))
      
      #see if the attack is successful
      if self.player.attack():
        #See if the monster dodges
        if self.monster.dodge():
          # if dodged, print that
          print ("{} dodged your attack!".format(self.monster))
        #if not dodged, subtract the right num hit points from the monster
        else:
          if self.player.leveled_up():
            self.monster.hit_points -= 2
          else:
            self.monster.hit_points -= 1
          #Print statement that player hit monster
          print ("You hit {} with your {}!".format(
              self.monster, self.player.weapon))
      #if not a good attack, tell the player
      else:
        print ("You missed!")
    
    #if they rest:
    elif player_choice == "r":
      self.player.rest()
    
    #if they quit, exit the game
    elif player_choice == "q":
      sys.exit()
    
    #if they pick anything else, re-run this method
    else:
      self.player_turn()

        
  def cleanup(self):
    #if the monster has no more hit points:
    if self.monster.hit_points <= 0:
      #Up the player's experience
      self.player.experience += self.monster.experience
      #Print a message
      print("You killed {}!".format(self.monster))
      #Get a new monster
      self.monster = self.get_next_monster()

  
  #Running of the game loop itself
  def __init__(self):
    self.setup()
    
    while self.player.hit_points and (self.monster or self.monsters):
      print('\n'+'='*20)
      
      #Display player status
      print(self.player)
      
      #Monster's turn
      self.monster_turn()
      print('-'*20)
      
      #Player's turn
      self.player_turn()
      
      #Cleanup
      self.cleanup()
      print('\n'+'='*20)
    
    #Endings
    if self.player.hit_points:
      print("You win!")
    elif self.monsters or self.monster:
      print("You lose!")
    sys.exit()
    
Game()
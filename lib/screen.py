
import pygame
from pygame import display
from player import Player
from pygame.locals import *
from main_menu import MainMenu

class Screen (object):
    """This Class represents the screen on which movement occurs. It handles
    collisions and movement."""
    
    ##TODO: We need to layer the game-objects with an z coord, because otherwise
    ##      we will have our objects colliding with the background, etc.
    ##      Possible fix: gameobject.collides_with(obj) method

    def __init__(self, dimensions=(640,480), player=None):
        """Takes a coordinate pair (x,y) as dimensions, and constructs
        a screen on which all objects are displayed."""
        self.dimensions = dimensions
        pygame.init()
        display.init()
        display.set_caption("Dungeon-RPG")
        self.surface = display.set_mode(dimensions)
        self.surface.fill((0,255,0))
        self.background = self.surface.copy()
        self.gameobjects = []
        self.rect = pygame.Rect((0,0), self.dimensions)
        self.player = player
        #we only will update the dirty_objs to boost our speeds
        self.dirty_objs = []
        self.dirty_rects = []
        #refresh the background the first time through:
        self.add_to_dirty_rects(self.rect)
        
    def update(self):
        """Renders all elements and refreshes the display"""
        #clear the screen:
        #self.surface.blit(self.background, (0,0))
        #erase where we've been to avoid streaky trails.
        for rect in self.dirty_rects:
            subsurface = self.background.subsurface(rect).copy()
            self.surface.blit(subsurface, (rect.left, rect.top) )
        for obj in self.dirty_objs:
            self.surface.blit(obj.render(), obj.position)   
        pygame.display.update(self.dirty_rects)
        #clear our rects, we've updated these now.
        self.dirty_objs = []
        self.dirty_rects = []
    
    def add_to_dirty_objs(self, obj):
        self.dirty_objs.append(obj)    
        
    def add_to_dirty_rects(self, obj):
        self.dirty_rects.append(obj)
        
    def dirtied(self, obj):
        """Takes a gameobject and appends it to dirty_objs and dirty_rects
        to make sure we update it on the screen."""
        self.dirty_objs.append(obj)
        self.dirty_rects.append(obj.rect)
    
    def run(self):
        """Our main loop while the screen is running."""
        #allow keys to be held down
        pygame.key.set_repeat(1,0) #milis delay, repeat
        while True:
            self.update()
            for event in pygame.event.get():
                if event.type == QUIT:
                    return
                if event.type == KEYDOWN:
                    if event.key == K_UP:
                        self.player.move_up()
                    if event.key == K_DOWN:
                        self.player.move_down()
                    if event.key == K_LEFT:
                        self.player.move_left()
                    if event.key == K_RIGHT:
                        self.player.move_right()
                    if event.key == K_SPACE:
                        self.main_menu()
                  
                        
        
    def add_object(self, gameobject):
        """Does exactly what it sounds like: adds a gameobject to this
        gamescreen"""
        self.gameobjects.append(gameobject)
        self.dirtied(gameobject)
        
    def remove_object(self, gameobject):
        """Removes object from gameobjects. If it does not exist, no action
        is taken."""
        if gameobject in self.gameobjects:
            self.gameobjects.remove(gameobject)
            #TODO: remove the surface from the display
    
    
    def add_player(self, player):
        """Adds a player character to the screen. also adds the player to
        gameobjects. It will check to make sure that the player is not already
        added."""
        player.screen = self
        self.player = player
        if player not in self.gameobjects:
            self.gameobjects.append(player)
        self.dirtied(player)
             
    
    def kill(self):
        """Close the screen."""
        display.quit()

    def check_collisions(self, gameobject):
        """Checks collisions on this screen.
        returns obj that gameobject has collided with. None if no collision."""
        for obj in self.gameobjects:
            if obj is not gameobject:
                #have obj to the checking because obj may be non-collidable 
                if obj.collides_with(gameobject):
                    return obj
        return None
            
            
    def in_bounds(self, obj):
        """Checks if the given gameobject is in bounds."""
        print "Checking if "+ str(obj) +" is in bounds... ",
        a =  bool( self.rect.contains(obj.rect) )
        print a
        #print self.rect
        #print obj.rect
        return a

    def main_menu(self):
        menu = MainMenu(self)
        menu.run()


    ## ==============================================
    ## The following functions deal with battle mode.
    ## ==============================================
    
    def battle(self, enemy):
        """Starts a battle between the enemy and the player"""
        print "Initiate battle!"
        #TODO: make attribute for battle-screen which is background for battle scene
        bak_background = self.background.copy()
        bak_gobs = self.gameobjects
        self.dirty_objs = []
        self.dirty_rects = []
        
        ## do stuff here
        ## ==============
        
        #make ourselves a new background
        self.background.fill( (255,0,0) )
        self.add_to_dirty_rects(self.rect)
        
        
        
        
        
        ## restore our regular settings.
        ## =============================
        
        self.background = bak_background    
        self.gameobjects = bak_gobs
        self.dirty_objs = []
        self.dirty_rects = []
        
    

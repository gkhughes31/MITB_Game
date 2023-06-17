import pygame
import random
import math
import button

# Define global variables
male_wrestlers = ("Ricochet","Shinsuke Nakamura","LA Knight","Santos Escobar","Butch","Damien Priest")
female_wrestlers = ("Becky Lynch","Zelina Vega", "Zoey Stark", "Bayley", "Iyo Sky", "Mystery Woman")


# Set default image size
default_image_size = (100,50)

# Initialize Pygame
pygame.init()


class Wrestler:   
    def __init__(self, wname, wgender, wnumber):
        self.wname = wname.replace("_"," ")
        self.wgender = wgender
        self.wnumber = wnumber
        self.wrestler_x = self.wnumber%3+1
        self.wrestler_y = math.ceil(self.wnumber/3)
        self.image = pygame.image.load(self.wname + ".png")
        self.rect = self.image.get_rect()
        self.winner = False
        self.bettors = []    
    
    def __str__(self):
        return self.wname + " is " + self.wgender

class Player:    
    def __init__(self, pname, initials, color):
        self.pname = pname
        self.initials = initials
        self.color = color
        self.wrestler = ""
        self.points = 0
        self.moves = 0
        self.position_x= 0
        self.position_y= 0
        self.choice = False
    
    def __str__(self):
        return self.pname + " has " + str(self.points) + " points"


# Set up the window dimensions

window = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
w, h = pygame.display.get_surface().get_size()
pygame.display.set_caption("Money in the Bank Game")
pygame_icon = pygame.image.load("wwe belt.png")
pygame.display.set_icon(pygame_icon)

#   Global variables for timer
clock = pygame.time.Clock()


class MITB:
    def __init__(self):
        self.wrestlers = {}
        self.players_list = []
        self.players = {}
        self.gender = "male"
        self.game_on = True
        self.full_game_on = True
        self.game_state = "title"
        self.timer = ""
        self.current_time = 0
        self.button_press_time = 0
        self.screen_color = (192,192,192)
        self.number_of_players =""
        
    def make_game(self):   
        for count, wrestler in enumerate(male_wrestlers, start = 1):
            name = wrestler
            self.wrestlers[name] = self.wrestlers.get(name, Wrestler(wname = name, wgender ="male", wnumber = count))
        for count, wrestler in enumerate(female_wrestlers, start = 1):
            name = wrestler
            self.wrestlers[name] = self.wrestlers.get(name, Wrestler(wname = name, wgender ="female", wnumber = count))        
    
    def countdown(self, t):
        pass
    
    def player_info_entry(self):   
        for i,val in enumerate(self.players_list):
            name = self.players_list[i]
            initials = self.players_list[i][0] + str(i+1)
            color = "red"
            mitb.players[name] = mitb.players.get(name, Player(pname = name, initials = initials, color =  color))
            
            
    def assign_initial_wrestler(self): 
        initialbank = []
        for wrestler in self.wrestlers:
            if self.wrestlers[wrestler].wgender == self.gender:
                initialbank.append(self.wrestlers[wrestler].wname)
        for player in self.players:
            self.players[player].wrestler = random.choice(initialbank)
            selection = self.players[player].wrestler
            self.wrestlers[selection].bettors.append(self.players[player].initials)

def draw_centered_text(screen1, x, y, text, fontstyle):
    words = fontstyle.render(text, True, black)
    rectangle = words.get_rect(center=(x,y))
    screen1.blit(words, rectangle)

def draw_circle(screen, x, y, text, color, fontstyle):
    pygame.draw.circle(screen, color, (x,y), 25)
    words = fontstyle.render(text, True, black)
    rectangle = words.get_rect(center=(x,y))
    screen.blit(words, rectangle)

# Create MITB instance        
mitb = MITB()

#load button images
start_button_img = pygame.image.load("wwe belt.png")

# Create button instances
start_game_button = button.Button(w/2, .86*h, start_button_img, .5)

# Set up the font for labels
font = pygame.font.SysFont('Georgia', 30, bold=True)
font_num = pygame.font.SysFont('Helvetica',50,bold =True)
font_title = pygame.font.SysFont('Georgia', 75 ,bold=True)

# Set up colors
black = (0, 0, 0)
white = (255, 255, 255)
blue =  (  0,   0, 255)
green = (  0, 255,   0)
red =   (255,   0,   0)

# Define FPS
FPS = 30

# Check game state and then draw cooresponding items
def draw_window():
    # title screen
    if mitb.game_state == "title":
        window.fill(mitb.screen_color)
        draw_centered_text(window, w/2, h*.1, "Money in the Bank", font_title)
        if start_game_button.draw(window):
            mitb.make_game()
            mitb.game_state = "player_entry"
    
    # player info entry screen
    elif mitb.game_state == "player_entry":
        window.fill(mitb.screen_color)
        draw_centered_text(window, w/2, h*.1, "Player Info", font_title)
        text_surface = font_num.render(mitb.number_of_players, True, (0,0,0))
        window.blit(text_surface, (w/2,h*.3))
        # put name on screen after entry
        for i, val in enumerate(mitb.players_list):
            player = font.render(mitb.players_list[i], True, black)
            window.blit(player, (0, h*.5 + 12*i))
        if start_game_button.draw(window):
            mitb.player_info_entry()
            mitb.assign_initial_wrestler()
            mitb.game_state = "main_game"
    
    
    elif mitb.game_state == "main_game":
        # Clear the screen
        window.fill(mitb.screen_color)
        # Draw the wrestler icons and labels
        for wrestler in mitb.wrestlers:
            if mitb.wrestlers[wrestler].wgender == mitb.gender:
                wrestler_icon = mitb.wrestlers[wrestler].image.convert_alpha()
                wrestler_icon = pygame.transform.smoothscale(wrestler_icon, (.25*w,.25*h))
                wrestler_rect = wrestler_icon.get_rect()
                wrestler_rect.center = (mitb.wrestlers[wrestler].wrestler_x*1/4*w+(mitb.wrestlers[wrestler].wrestler_x*40-80), 
                                        mitb.wrestlers[wrestler].wrestler_y*1/3*h+(mitb.wrestlers[wrestler].wrestler_y-1)*40)
                window.blit(wrestler_icon, wrestler_rect)
                wrestler_title = font.render(mitb.wrestlers[wrestler].wname, True, black)
                wrestler_rectangle = wrestler_title.get_rect(center=(mitb.wrestlers[wrestler].wrestler_x*1/4*w+mitb.wrestlers[wrestler].wrestler_x*40-80,
                                                                     (mitb.wrestlers[wrestler].wrestler_y*1/3*h+(mitb.wrestlers[wrestler].wrestler_y-1)*40)-100))
                window.blit(wrestler_title, wrestler_rectangle)
        # put player chips on cooresponding wrestlers
        for wrestler in mitb.wrestlers:
            for i, val in enumerate(mitb.wrestlers[wrestler].bettors):
                draw_circle(window, mitb.wrestlers[wrestler].wrestler_x*1/4*w+(mitb.wrestlers[wrestler].wrestler_x*40-80), mitb.wrestlers[wrestler].wrestler_y*1/3*h+(mitb.wrestlers[wrestler].wrestler_y-1)*40, mitb.wrestlers[wrestler].bettors[i], red, font)
                
        if mitb.button_press_time != 0:
            display_timer = font_num.render(str(240-(mitb.current_time-mitb.button_press_time)), True, black)
            display_timer_rect = display_timer.get_rect()
            display_timer_rect.center = (w/2, .07*h)
            window.blit(display_timer, display_timer_rect)

                
# Game loop
def main():
    run = True
    while run:
        # Sets clocked framerate
        clock.tick(FPS)
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                if mitb.game_state == "player_entry" and event.key == pygame.K_BACKSPACE:
                    mitb.number_of_players = mitb.number_of_players[:-1]
                if mitb.game_state == "player_entry" and event.key == pygame.K_RETURN:
                    mitb.players_list.append(mitb.number_of_players)
                    mitb.number_of_players = ""
                if mitb.game_state == "player_entry" and event.key != pygame.K_BACKSPACE and event.key != pygame.K_RETURN:
                    mitb.number_of_players += event.unicode
                if mitb.game_state == "main_game" and event.key == pygame.K_SPACE:
                    mitb.button_press_time = int(math.floor(pygame.time.get_ticks()/1000))
                    mitb.screen_color = (255,0,0)
                
        draw_window()
        # Update the display
        pygame.display.flip()

        mitb.current_time = int(math.floor(pygame.time.get_ticks()/1000))
    
    # Quit the game
    pygame.quit()

if __name__ == "__main__":
    main()

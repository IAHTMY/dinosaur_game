import pygame # klíčová knihovna umožňující vytvářet jednoduše nejen hry
import random
pygame.init() # nutný příkaz hned na začátku pro správnou inicializaci knihovny

class Player(pygame.sprite.Sprite):
    def __init__(self): #konstruktor
        super().__init__() #povolává z mrtvých konstruktor při vytvoření
        self.image = pygame.image.load("pixil-frame-1.png")
        self.image = pygame.transform.scale(self.image, (50,150))
        self.rect = self.image.get_rect(midbottom = (100, 0.75*window_height))
        self.gravity = 0

    def player_input(self): 
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300: # výskok po zmáčknutí mezerníku
            self.gravity = -20

    def apply_gravity(self): # F = (G*m1*m2)/(r*r)
        self.gravity +=1
        self.rect.y += self.gravity
        if self.rect.bottom >= 0.75*window_height:
            self.rect.bottom = 0.75*window_height

    def update(self):
        self.player_input()
        self.apply_gravity()

class Obstacle(pygame.sprite.Sprite):
     def __init__(self):
        super().__init__()
        self.image = pygame.image.load("kaktus.png").convert_alpha()
        size = random.randint(30,80)
        self.image = pygame.transform.scale(self.image,(size, size))
        self.rect = self.image.get_rect(bottomleft = (600, 0.75*window_height))
        self.speed  = 10
        
     def update(self):
        self.rect.x -= 6
        self.destroy()
        
     def destroy(self):
          if self.rect.x <= -100: 
              self.kill()

def is_collision():
    if pygame.sprite.spritecollide(player.sprite, obstacles_group, False):
        obstacles_group.empty() #vymazání kaktusů, hra skončí touto kolizí
        return False #hra končí
    return True #hra jede dál
# herní okno
window_width = 800
window_height = 400
screen = pygame.display.set_mode((window_width, window_height))
    # dvojice (w,h) v parametru se nazývá *tuple*
pygame.display.set_caption("Dino offline hra") # nastavíme do hlavičky okna název hry

clock = pygame.time.Clock() # díky hodinám nastavíme frekvenci obnovování herního okna

# přidání objektů (tzv. surface) do scény
sky_surface = pygame.Surface((window_width,0.75*window_height))
sky_surface.fill("darkslategray1")
ground_surface = pygame.Surface((window_width,0.25*window_height))
ground_surface.fill("lightsalmon4")

player = pygame.sprite.GroupSingle()
player.add(Player()) #přidává se nový hráč podle předlohy groupsingle player

count = 0

text_font = pygame.font.Font("PixelifySans.ttf",100) # 100 je velikost písma
text_surface = text_font.render("GAME OVER!", True, "Black") # text, anti-aliasing, černá barva písma
text_rect = text_surface.get_rect(center=(window_width/2, window_height/2)) # kam se to má vykreslit

n = 0
score_font = pygame.font.Font("PixelifySans.ttf",100) # 100 je velikost písma
score_surface = text_font.render(f"Skore: {n}", True, "Black") # text, anti-aliasing, černá barva písma
score_rect = text_surface.get_rect(center=(window_width/2, window_height/2)) # kam se to má vykreslit
counter = 0
game_active = True
# herní smyčka

obstacles_group = pygame.sprite.Group()
while True:
    # zjistíme co dělá hráč za akci
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit() # zavřeme herní okno
            exit() # úplně opustíme herní smyčku, celý program se ukončí
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_active == False: #Game over stav
                    game_active = True
                else:
                    game_active = True
                    
    if game_active:            
        # pozadí
        screen.blit(sky_surface,(0,0)) # položíme sky_surface na souřadnice [0,0]
        screen.blit(ground_surface,(0,0.75*window_height)) # položíme ground_surface na souřadnice [0,300] (pod oblohu)
        screen.blit(score_surface, score_rect)

        
        if counter > 120:
            counter = 0
            obstacles_group.add(Obstacle())
            
        else:
            counter += 1
        # nepřítel
        obstacles_group.draw(screen)
        obstacles_group.update()

        #hráč
        player.draw(screen)
        player.update()

        count += 1
        score_surface = text_font.render(f"Skore: {count // 60}", True, "Black") # text, anti-aliasing, černá barva písma
        score_rect = text_surface.get_rect(center=(window_width/2, window_height/2)) # kam se to má vykreslit

        game_active = is_collision() #byla kolize?
        
    else:
        screen.blit(sky_surface,(0,0))
        screen.blit(text_surface, text_rect)
        count = 0
    pygame.display.update() # updatujeme vykreslené okno
    clock.tick(60) # herní smyčka proběhne maximálně 60x za sekundu
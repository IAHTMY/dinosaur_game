import pygame # klíčová knihovna umožňující vytvářet jednoduše nejen hry
pygame.init() # nutný příkaz hned na začátku pro správnou inicializaci knihovny

# herní okno
window_width = 800
window_height = 400
screen = pygame.display.set_mode((window_width, window_height))
    # dvojice (w,h) v parametru se nazývá *tuple*
pygame.display.set_caption("Název hry") # nastavíme do hlavičky okna název hry

clock = pygame.time.Clock() # díky hodinám nastavíme frekvenci obnovování herního okna

# přidání objektů (tzv. surface) do scény
sky_surface = pygame.Surface((window_width,0.75*window_height))
sky_surface.fill("darkslategray1")
ground_surface = pygame.Surface((window_width,0.25*window_height))
ground_surface.fill("lightsalmon4")

enemy_surface = pygame.image.load("kaktus.png")
enemy_surface = pygame.transform.scale(enemy_surface, (50,50))
enemy_rect = enemy_surface.get_rect(midbottom = (600, 0.75*window_height))
enemy_speed  = 4

text_font = pygame.font.Font("PixelifySans.ttf",100) # 100 je velikost písma
text_surface = text_font.render("GAME OVER!", True, "Black") # text, anti-aliasing, černá barva písma
text_rect = text_surface.get_rect(center=(window_width/2, window_height/2)) # kam se to má vykreslit

n = 0
score_font = pygame.font.Font("PixelifySans.ttf",100) # 100 je velikost písma
score_surface = text_font.render(f"Skore: {n}", True, "Black") # text, anti-aliasing, černá barva písma
score_rect = text_surface.get_rect(center=(window_width/2, window_height/2)) # kam se to má vykreslit


player_surface = pygame.image.load("pixil-frame-1.png")
player_surface = pygame.transform.scale(player_surface, (50,150))
enemy_x_position = 600
player_rect = player_surface.get_rect(midbottom = (600, 0.75*window_height))
player_gravity = 0

game_active = True
# herní smyčka
count = 0
while True:
    # zjistíme co dělá hráč za akci
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit() # zavřeme herní okno
            exit() # úplně opustíme herní smyčku, celý program se ukončí
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and player_rect.bottom == 0.75*window_height:
                player_gravity = -20
        else:
            game_active = True
            enemy_rect.left = 200 # posunutí nepřítele doháje
    if game_active:            
        # pozadí
        screen.blit(sky_surface,(0,0)) # položíme sky_surface na souřadnice [0,0]
        screen.blit(ground_surface,(0,0.75*window_height)) # položíme ground_surface na souřadnice [0,300] (pod oblohu)
        screen.blit(score_surface, score_rect)
        # nepřítel
        enemy_rect.left -= enemy_speed
        if enemy_rect.right < 0:
            enemy_rect.left = window_width
        screen.blit(enemy_surface, enemy_rect)

        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 0.75*window_height:
            player_rect.bottom = 0.75*window_height
        screen.blit(player_surface, player_rect)
        count += 1
        score_surface = text_font.render(f"Skore: {count // 60}", True, "Black") # text, anti-aliasing, černá barva písma
        score_rect = text_surface.get_rect(center=(window_width/2, window_height/2)) # kam se to má vykreslit
        if player_rect.colliderect(enemy_rect):
            print("kolize a krize a katastrofa")
            game_active = False
        
    else:
        screen.blit(sky_surface,(0,0))
        screen.blit(text_surface, text_rect)
    pygame.display.update() # updatujeme vykreslené okno
    clock.tick(60) # herní smyčka proběhne maximálně 60x za sekundu
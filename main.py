
# Sprawdzanie czy pagame jest w ogole dostepny
import time
import os
import random
import save
from characters import character, enemy

try:
    from pygame import *
    print("Pygame installer")
except ImportError as e:
    print(f'{e} Install pygame package',e)
else:
    if init()[1]!=0:
        raise Exception("Some imported pygame modules coud't be uploaded")
    game_saves=save.saves()
    game_saves.load()
    print(game_saves.saved)
    arena_level = 500
    window_width = 1000
    window_height = 800
    surface = display.set_mode([window_width,window_height],flags=0,depth=3,display=0,vsync=0)
    clock=time.Clock()
    bg_image = transform.scale(
        image.load('images/background.jpg').convert_alpha(), (window_width, window_height))
    victory=mixer.Sound('sounds/victory.mp3')
    click=mixer.Sound('sounds/click.mp3')
    jump=mixer.Sound('sounds/jump.mp3')
    level_up=mixer.Sound('sounds/level_up.mp3')

    punch=mixer.Sound('sounds/punch.mp3')
    shout=mixer.Sound('sounds/shout.mp3')
    sounf_trunk=mixer.music.load('sounds/sound_truck.mp3')
    mixer.music.play(-1, 0.0)



    from pygame import transform
    import pygame


    class button(pygame.sprite.Sprite):
        def __init__(self, image,x, y,scale=1):
            super().__init__()
            width = image.get_width()
            height = image.get_height()
            self.image = transform.scale(image, (int(width * scale), (int)(height * scale)))
            self.scale = scale
            self.rect = self.image.get_rect()
            self.rect.topleft = (x, y)
            self.clicked = False
            self.on=True



        def draw(self):
            if self.on==True:
                action = False
                # get mouse position
                pos = mouse.get_pos()
                # check mouseover and click condiction
                if self.rect.collidepoint(pos):
                    if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                        self.clicked = True
                        action = True
                        click.play()

                    if pygame.mouse.get_pressed()[0] == 0:
                        self.clicked = False
                surface.blit(self.image, (self.rect.x, self.rect.y))
                return action
        def update(self,x,y,visible_boolean):
            self.rect.move_ip(x,y)
            self.on = visible_boolean


    class hud_bars(sprite.Sprite):
        def __init__(self, max_value, color_bg, color_bar, pos_x, pos_y, height, width, side):

            self.max_value = max_value
            self.value = max_value
            self.pos_x = pos_x
            self.pos_y = pos_y
            self.height = height
            self.width = width
            self.color_bar = color_bar
            self.side = side
            self.color_bg = color_bg

        def draw(self, surface):

            if self.side == -1 and self.value >= 0:
                ratio = int(self.value) / self.max_value
                draw.rect(surface, self.color_bg, Rect(self.pos_x, self.pos_y, self.width, self.height))
                draw.rect(surface, self.color_bar, Rect(self.pos_x, self.pos_y, self.width * ratio, self.height))
            if self.side == 1 and self.value >= 0:
                ratio = (self.max_value - int(self.value)) / self.max_value
                draw.rect(surface, self.color_bar, Rect(self.pos_x, self.pos_y, self.width, self.height))
                draw.rect(surface, self.color_bg, Rect(self.pos_x, self.pos_y, self.width * ratio, self.height))
        def refull(self):
            self.value=self.max_value


    hp_bar_player = hud_bars(100, (255, 0, 0), (0, 255, 0), 800, 20, 20, 100, -1)
    hp_bar_enemy = hud_bars(100, (255, 0, 0), (0, 255, 0), 200, 20, 20, 100, 1)
    #stamine_bar_player=hud_bars(100, (125, 125, 125),(255, 255, 0), 800, 40, 20, 80, -1)
    defence_bra_player=hud_bars(100,  (255, 255, 255),(125, 125, 125), 800, 40, 20, 80, -1)
    defence_bra_enemy=hud_bars(100,  (255, 255, 255),(125, 125, 125), 220, 40, 20, 80, 1)
    charsma_bra=hud_bars(100,(0,255,0),(210,105,30),450,20,20,200,1)



    path_walk = os.path.join(os.getcwd(), 'images/player1/Nowy/walk4/left')

    path_jump = os.path.join(os.getcwd(), 'images/player1/Nowy/jump/left')

    path_shout = os.path.join(os.getcwd(), 'images/player1/Nowy/shout/left')

    path_attack = os.path.join(os.getcwd(), 'images/player1/Nowy/attack')
    path_charm = os.path.join(os.getcwd(), 'images/player1/Nowy/charm')

    file_names = os.listdir(path_walk)
    images_walk=[]
    for file_name in file_names:
        tmp=pygame.image.load(os.path.join(path_walk, file_name)).convert()
        tmp.set_colorkey((37,37,37))
        images_walk.append(tmp)


    file_names = os.listdir(path_jump)
    images_jump = []
    for file_name in file_names:
        tmp = pygame.image.load(os.path.join(path_jump, file_name)).convert()
        tmp.set_colorkey((37, 37, 37))
        images_jump.append(tmp)
    file_names = os.listdir(path_shout)
    images_shout = []
    for file_name in file_names:
        tmp = pygame.image.load(os.path.join(path_shout, file_name)).convert()
        tmp.set_colorkey((37, 37, 37))
        images_shout.append(tmp)

    file_names = os.listdir(path_attack)
    images_attack = []
    for file_name in file_names:
        tmp = pygame.image.load(os.path.join(path_attack, file_name)).convert()
        tmp.set_colorkey((37, 37, 37))
        images_attack.append(tmp)
    file_names = os.listdir(path_charm)
    images_charm = []
    for file_name in file_names:
        tmp = pygame.image.load(os.path.join(path_charm, file_name)).convert()
        tmp.set_colorkey((37, 37, 37))
        images_charm.append(tmp)
    button_scale=0.1



    player = character(images_walk,images_jump,images_shout,images_attack,images_charm, 750, arena_level, -1,0.12,)
    enemy=enemy(images_walk,images_jump,images_shout,images_attack,images_charm,20,arena_level,1,0.12)
    button_jump_left = button(image.load('images/player1/icon_jump_left.png'),player.rect.left-30,player.rect.y-0,button_scale)
    button_walk_left = button(image.load('images/player1/icon_walk_left.png'),player.rect.left-30,player.rect.y+40,button_scale)
    button_attack = button(image.load('images/player1/icon_attack.png'),player.rect.left-10,player.rect.y+80,button_scale)

    button_jump_right = button(image.load('images/player1/icon_jump_right.png'), player.rect.right + 10, player.rect.y - 0, button_scale)
    button_walk_right = button(image.load('images/player1/icon_walk_right.png'), player.rect.right + 30, player.rect.y + 40, button_scale)
    button_shaut = button(image.load('images/player1/icon_shaut.png'), player.rect.right + 10, player.rect.y + 80, button_scale)
    button_charm = button(image.load('images/player1/icon_charm.png'), player.rect.right -10, player.rect.y + 120, button_scale)


    moving_sprites=pygame.sprite.Group()
    action_buttons=pygame.sprite.Group(button_jump_left,button_walk_left,button_attack,button_jump_right,button_walk_right,button_shaut,button_charm)
    moving_sprites.add(player,enemy)

    fight=False
    exit=False
    tour = True
    #pętla gry
    button_scale = 0.1

    text_font = font.SysFont('Arial', 30)


    def draw_text(text, text_color, font, x, y, surface):
        img = font.render(text, True, text_color)
        surface.blit(img, (x, y))
        return img.get_rect()



    play_button_image = os.path.join(os.getcwd(), 'images/play_button_image.png')
    load_button_image = os.path.join(os.getcwd(), 'images/load_button_image.png')
    quit_button_image = os.path.join(os.getcwd(), 'images/quit_button_image.png')
    finish_button_image = os.path.join(os.getcwd(), 'images/triangle_image_finish.png')
    save_button_image = os.path.join(os.getcwd(), 'images/save_image_button.png')
    fight_button_image = os.path.join(os.getcwd(), 'images/fight_button_image.png')
    upgrade_button_image = os.path.join(os.getcwd(), 'images/upgrade_button_image.png')
    mainmenu_button_image = os.path.join(os.getcwd(), 'images/main_menu_button_image.png')
    mainmenu_button_image_from_loads = os.path.join(os.getcwd(), 'images/main_menu_button_image.png')


    triangle_button = os.path.join(os.getcwd(), 'images/triangle_image.png')
    stats_button_scale = 0.1
    triangle_strenght_left = button(image.load(triangle_button), 140, 5, stats_button_scale)
    triangle_strenght_right = button(transform.flip(image.load(triangle_button), True, False), 180, 5,
                                     stats_button_scale)

    triangle_perception_left = button(image.load(triangle_button), 140, 45, stats_button_scale)
    triangle_perception_right = button(transform.flip(image.load(triangle_button), True, False), 180, 45,
                                       stats_button_scale)

    triangle_endurance_left = button(image.load(triangle_button), 140, 85, stats_button_scale)
    triangle_endurance_right = button(transform.flip(image.load(triangle_button), True, False), 180, 85,
                                      stats_button_scale)

    triangle_charisma_left = button(image.load(triangle_button), 140, 125, stats_button_scale)
    triangle_charisma_right = button(transform.flip(image.load(triangle_button), True, False), 180, 125,
                                     stats_button_scale)

    triangle_inteligence_left = button(image.load(triangle_button), 140, 165, stats_button_scale)
    triangle_inteligence_right = button(transform.flip(image.load(triangle_button), True, False), 180, 165,
                                        stats_button_scale)

    triangle_agility_left = button(image.load(triangle_button), 140, 205, stats_button_scale)
    triangle_agility_right = button(transform.flip(image.load(triangle_button), True, False), 180, 205,
                                    stats_button_scale)

    triangle_defence_left = button(image.load(triangle_button), 140, 285, stats_button_scale)
    triangle_defence_right = button(transform.flip(image.load(triangle_button), True, False), 180, 285,
                                    stats_button_scale)

    play_button = button(image.load(play_button_image), 325, 200, 0.5)
    load_button = button(image.load(load_button_image), 325, 325, 0.5)
    quit_button = button(image.load(quit_button_image), 325, 450, 0.5)
    finish_button = button(image.load(finish_button_image), 200, 600, 0.2)

    fight_button = button(image.load(fight_button_image), 325, 200, 0.5)
    upgrade_button = button(image.load(upgrade_button_image), 325, 325, 0.5)
    save_button = button(image.load(save_button_image), 325, 450, 0.5)
    main_menu_button = button(image.load(mainmenu_button_image), 0,0, 0.5)
    main_menu_button_from_loads = button(image.load(mainmenu_button_image_from_loads), 325, 700, 0.5)

    loads=False
    create_character = False
    menu = True
    exit = False
    game_menu = False
    display_stats = [0, 0]
    while exit!=True:


        for eve in event.get():
            if eve.type ==QUIT:
                exit=True
        surface.fill((255,255,255))
        if fight:
            surface.blit(bg_image,(0,0))


            if button_walk_left.draw() :
                player.get_event("go_left",0.1)
                player.oponent_move=True
            if button_walk_right.draw() :
                player.get_event("go_right",0.2)
                player.oponent_move = True
            if button_jump_left.draw() :
                player.get_event("jump_left",0.1)
                player.oponent_move = True
            if button_jump_right.draw() :
                player.get_event("jump_right", 0.1)
                player.oponent_move = True
            if button_attack.draw():
                player.get_event("attack",0.1)
                player.oponent_move = True
            if button_shaut.draw():
                player.get_event("shout",0.1)
                player.oponent_move = True
            if button_charm.draw():
                player.get_event("charm",0.1)
                player.oponent_move = True
                charsma_bra.value-=player.stats["charisma"]

            if (not player.animatig) and enemy.animatig==False:
                action_buttons.update(0,0,True)
            else:
                action_buttons.update(0, 0, False)

            if player.walking:
                    action_buttons.update(player.walking_side, 0, False)
            if player.jumping == False and player.rect.y != arena_level:
                action_buttons.update(player.walking_side,0,False)

            if button_walk_right.rect.right >= window_width:
                player.rect.right-=1
                action_buttons.update(-1, 0, False)
            if button_walk_left.rect.left<=0:
                player.rect.left +=2
                action_buttons.update(2, 0, False)
            # attack module
            hp_bar_player.max_value=player.stats["hp"]
            hp_bar_enemy.max_value=enemy.stats["hp"]
            if player.rect.colliderect(enemy) and (player.attack or enemy.attack):
                if enemy.attack:
                    if(enemy.hit_test(player.stats["agility"])):
                        if(not player.block_test(enemy.stats["strength"])):
                            if defence_bra_player.value>0:
                                defence_bra_player.value-=(enemy.stats["strength"]+30)
                            else:
                                hp_bar_player.value-=(enemy.stats["strength"]+20)

                if player.attack:

                    if (player.hit_test(enemy.stats["agility"])):
                        if (not enemy.block_test(player.stats["strength"])):
                            if defence_bra_enemy.value > 0:
                                defence_bra_enemy.value -= (player.stats["strength"] + 30)
                            else:
                                hp_bar_enemy.value -= (player.stats["strength"] + 20)



                player.attack=False
                enemy.attack=False




            if player.oponent_move and player.animatig==False:
                action_buttons.update(0, 0, False)
                if  not enemy.walking and not enemy.animatig:
                    enemy.inteligence(player.rect.center)
                    enemy.update(0.1)
                else:
                    player.oponent_move=False

            player.inteligence(enemy.rect.center)
            moving_sprites.draw(surface)
            moving_sprites.update(0.1)
            hp_bar_player.draw(surface)
            hp_bar_enemy.draw(surface)
            defence_bra_player.draw(surface)
            defence_bra_enemy.draw(surface)
            charsma_bra.draw(surface)
            if(hp_bar_enemy.value<=0):
                fight=False
                game_menu=True
                victory.play()
                enemy.randomize_stat(1)
                print(charsma_bra.value)
                player.stats["gold"]+=(charsma_bra.max_value-charsma_bra.value)*20+100
                print(charsma_bra.value)
                player.stats["exp"]+=enemy.stats["strength"]+enemy.stats["perception"]*10*player.stats["inteligence"]
                hp_bar_player.max_value = player.stats["hp"]
                hp_bar_enemy.max_value = enemy.stats["hp"]
                defence_bra_player.max_value = player.stats["df"]
                defence_bra_enemy.max_value = enemy.stats["df"]
                hp_bar_enemy.refull()
                hp_bar_player.refull()
                defence_bra_enemy.refull()
                defence_bra_player.refull()
                player.rect=player.start_position
                enemy.rect=enemy.start_position

            if(hp_bar_player.value<=0):
                fight=False
                menu=True
                enemy.reset()
                player.reset()




        if menu:
            if play_button.draw():
                create_character = True
                menu = False
            if load_button.draw():
                menu=False
                loads=True



            if quit_button.draw():
                exit = True
        if create_character:
            r = Rect(player.display.get_rect()).topleft = (400, 10)
            surface.blit(player.display, r)
            for i in player.stats:
                text = f'{i}:{player.stats[i]}'
                draw_text(text, (0, 0, 0), text_font, display_stats[0], display_stats[1], surface)
                display_stats[1] += 40
            display_stats[1] = 0

            if (triangle_strenght_left.draw()):
                if (player.stats['exp']) >= 100:
                    player.stats["strength"] += 1
                    player.stats['exp'] -= 100
            if (triangle_strenght_right.draw()):
                if (player.stats["strength"] > 1):
                    player.stats["strength"] -= 1
                    player.stats['exp'] += 100
            if (triangle_perception_left.draw()):
                if (player.stats['exp']) >= 100:
                    player.stats["perception"] += 1
                    player.stats['exp'] -= 100
            if (triangle_perception_right.draw()):
                if (player.stats["perception"] > 1):
                    player.stats["perception"] -= 1
                    player.stats['exp'] += 100
            if (triangle_endurance_left.draw()):
                if (player.stats['exp']) >= 100:
                    player.stats["endurance"] += 1
                    player.stats['exp'] -= 100
            if (triangle_endurance_right.draw()):
                if (player.stats["endurance"] > 1):
                    player.stats["endurance"] -= 1
                    player.stats['exp'] += 100
            if (triangle_charisma_left.draw()):
                if (player.stats['exp']) >= 100:
                    player.stats["charisma"] += 1
                    player.stats['exp'] -= 100
            if (triangle_charisma_right.draw()):
                if (player.stats["charisma"] > 1):
                    player.stats["charisma"] -= 1
                    player.stats['exp'] += 100
            if (triangle_inteligence_left.draw()):
                if (player.stats['exp']) >= 100:
                    player.stats["inteligence"] += 1
                    player.stats['exp'] -= 100
            if (triangle_inteligence_right.draw()):
                if (player.stats["inteligence"] > 1):
                    player.stats["inteligence"] -= 1
                    player.stats['exp'] += 100
            if (triangle_agility_left.draw()):
                if (player.stats['exp']) >= 100:
                    player.stats["agility"] += 1
                    player.stats['exp'] -= 100
            if (triangle_agility_right.draw()):
                if (player.stats["agility"] > 1):
                    player.stats["agility"] -= 1
                    player.stats['exp'] += 100
            if (triangle_defence_left.draw()):
                if player.stats["gold"] >= 100:
                    player.stats["df"] += 1
                    player.stats["gold"] -= 100
            if (triangle_defence_right.draw()):
                if (player.stats["df"] > 1):
                    player.stats["df"] -= 1
                    player.stats["gold"] += 100
            if finish_button.draw():
                create_character = False
                game_menu = True
                level_up.play()

                hp_bar_player.max_value = player.stats["hp"]
                hp_bar_enemy.max_value = enemy.stats["hp"]
                defence_bra_player.max_value = player.stats["df"]
                defence_bra_enemy.max_value = enemy.stats["df"]
                hp_bar_enemy.refull()
                hp_bar_player.refull()
                defence_bra_enemy.refull()
                defence_bra_player.refull()
            player.level_up(0)
            enemy.level_up(0)
        if loads:
            y = 80
            for i in game_saves.saved:
                game_saves.load()
                y += 40
                text = f'Load from :{i[1]}'
                s=draw_text(text, (0,0,0), text_font, 20, y, surface)
                s.left+20
                s.top=y
                clicked = False
                pos=mouse.get_pos()
                if s.collidepoint(pos):
                    if pygame.mouse.get_pressed()[0] == 1 and clicked == False:
                        clicked = True

                        player.stats=i[0]["player"]
                        enemy.stats=i[0]["enemy"]
                        game_menu = True
                        loads = False

                    if pygame.mouse.get_pressed()[0] == 0:
                        clicked = False
            if main_menu_button_from_loads.draw():
                menu = True
                loads = False
        if game_menu:
            if fight_button.draw():
                fight=True
                game_menu=False
                hp_bar_player.refull()
                hp_bar_enemy.refull()
            if upgrade_button.draw():
                game_menu=False
                create_character=True
            if save_button.draw():
                game_saves.add({"player":player.stats,"enemy":enemy.stats})
                game_saves.save()
            if main_menu_button.draw():
                menu=True
                game_menu=False
                player.reset()
                enemy.reset()



        display.update()
        clock.tick(60)





import pygame
from pygame import *
from random import *
pygame.init()


jump=mixer.Sound('sounds/jump.mp3')

miss=mixer.Sound('sounds/miss.mp3')
punch=mixer.Sound('sounds/punch.mp3')
shout=mixer.Sound('sounds/shout.mp3')

arena_level = 500
class character(sprite.Sprite):
    def __init__(self, images_walk, images_jump, images_shout, images_attack, images_charm, x, y, walking_side,
                 scale=1):
        super().__init__()

        self.sprites = []
        self.sprite_walk_left = []
        self.sprite_walk_right = []

        width = images_walk[0].get_width()
        height = images_walk[0].get_height()
        self.display = transform.scale(images_walk[0], (int(width * 0.5), (int)(height * 0.5)))
        for i in images_walk:
            width = i.get_width()
            height = i.get_height()
            i = transform.scale(i, (int(width * scale), (int)(height * scale)))
            j = transform.flip(i, True, False)
            self.sprite_walk_left.append(i)
            self.sprite_walk_right.append(j)

        self.sprite_jump_left = []
        self.sprite_jump_right = []
        for i in images_jump:
            width = i.get_width()
            height = i.get_height()
            i = transform.scale(i, (int(width * scale), (int)(height * scale)))
            j = transform.flip(i, True, False)
            self.sprite_jump_left.append(i)
            self.sprite_jump_right.append(j)

        self.sprite_shout_left = []
        self.sprite_shout_right = []
        for i in images_shout:
            width = i.get_width()
            height = i.get_height()
            i = transform.scale(i, (int(width * scale), (int)(height * scale)))
            j = transform.flip(i, True, False)
            self.sprite_shout_left.append(i)
            self.sprite_shout_right.append(j)

        self.sprite_attack_left = []
        self.sprite_attack_right = []
        for i in images_attack:
            width = i.get_width()
            height = i.get_height()
            i = transform.scale(i, (int(width * scale), (int)(height * scale)))
            j = transform.flip(i, True, False)
            self.sprite_attack_left.append(i)
            self.sprite_attack_right.append(j)
        self.sprite_charm_left = []
        self.sprite_charm_right = []
        for i in images_charm:
            width = i.get_width()
            height = i.get_height()
            i = transform.scale(i, (int(width * scale), (int)(height * scale)))
            j = transform.flip(i, True, False)
            self.sprite_charm_left.append(i)
            self.sprite_charm_right.append(j)

        self.walking_side = walking_side
        self.walking = False
        if self.walking_side <= 0:
            self.sprites = self.sprite_walk_left
        else:
            self.sprites = self.sprite_walk_right
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.animatig = False

        self.jumping = False
        self.max_height = arena_level - 150

        self.stats = {"strength": 1, "perception": 1, "endurance": 1, "charisma": 1, "inteligence": 1, "agility": 1,
                      "hp": 0, "df": 1, "exp": 1000, "gold": 100}
        self.oponent_move = False
        self.attack = False
        self.start_position = self.rect

    def level_up(self, defence):

        self.stats["hp"] = 20 * self.stats['strength'] + 100

        self.max_height = arena_level - self.stats["agility"]

    def animate(self):
        self.animatig = True

    def update(self, speed):
        if self.animatig == True:
            if (len(self.sprites) > int(self.current_sprite + speed)):
                self.current_sprite += speed

            else:
                self.current_sprite = speed
                self.animatig = False
                self.walking = False
            self.image = self.sprites[int(self.current_sprite)]
        if self.jumping == True:
            self.rect.move_ip([self.walking_side, -1])
            #action_buttons.update(self.walking_side, 0, False)
            if self.rect.y == self.max_height:
                self.jumping = False
        if self.jumping == False and self.rect.y != arena_level:
            self.rect.move_ip([self.walking_side, 1])

        if self.walking and self.animatig:
            self.rect.move_ip([self.walking_side, 0])

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def get_event(self, order, speed):
        destination = 10

        if order == "go_left":
            self.sprites = self.sprite_walk_left
            self.walking_side = -1
            self.animate()
            self.walking = True

        if order == "go_right":
            self.sprites = self.sprite_walk_right
            self.walking_side = 1
            self.walking = True

            self.animate()

        if order == "jump_right":
            self.sprites = self.sprite_jump_right
            self.walking_side = 1
            self.jumping = True
            self.animate()
            jump.play()
        if order == "jump_left":
            self.sprites = self.sprite_jump_left
            self.walking_side = -1
            self.jumping = True
            self.animate()
            jump.play()
        if order == "shout":
            if (self.walking_side == -1):
                self.sprites = self.sprite_shout_left
                self.animate()
            if (self.walking_side == 1):
                self.sprites = self.sprite_shout_right
                self.animate()
            shout.play()
        if order == "attack":
            if (self.walking_side == -1):
                self.sprites = self.sprite_attack_left
                self.animate()
            if (self.walking_side == 1):
                self.sprites = self.sprite_attack_right
                self.animate()
            self.attack = True
            punch.play()
        if order == "charm":
            if (self.walking_side == -1):
                self.sprites = self.sprite_charm_left
                self.animate()
            if (self.walking_side == 1):
                self.sprites = self.sprite_charm_right
                self.animate()

    def hit_test(self, agillity_enemy):
        if (agillity_enemy - self.stats["perception"] <= 0):
            boundary = 1
        else:
            boundary = randint(1, agillity_enemy - self.stats["agility"])

        if randint(1, self.stats["perception"]) >= boundary:
            print("hit")
            return True
        else:
            print("unhit")
            miss.play()
            return False

    def block_test(self, enemy_strength):
        if (enemy_strength - self.stats["perception"] <= 0):
            boundary = 0
        else:
            boundary = randint(1, enemy_strength - self.stats["strength"])
            print(f'boundary:{boundary}')
        s = randint(1, self.stats["perception"])
        print(f'los:{s}')
        if s >= boundary:

            miss.play()
            return True
        else:

            return False

    def inteligence(self, enemy_position):
        distance = enemy_position[0] - self.rect.center[0]
        if self.animatig == False and self.rect.y == arena_level:
            if distance > 0:
                self.walking_side = 1
            else:
                self.walking_side = -1

    def reset(self):
        self.stats = {"strength": 1, "perception": 1, "endurance": 1, "charisma": 1, "inteligence": 1, "agility": 1,
                      "hp": 0, "df": 0, "exp": 1000, "gold": 100}
        self.rect = self.start_position
class enemy(character):

    def inteligence(self,enemy_position):
        distance=enemy_position[0]-self.rect.center[0]

        if distance>0:
            self.walking_side=1
        else:
             self.walking_side=-1


        if abs(distance)>140:
            if distance>0:

                self.get_event("go_right",0.1)
            else:
                self.get_event("go_left",0.1)
        else:
            self.get_event("attack",0.1)
        return self.animatig
    def randomize_stat(self,dificult_level):
        for i in self.stats:
            if i not in ("hp","gold","exp",):
                self.stats[i]+=randint(0,dificult_level)
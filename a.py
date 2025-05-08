from pygame import *
from random import randint
import time
import math

mixer.init()
mixer.music.load("nachalo.mp3")
mixer.music.play()

natusk_sound = mixer.Sound("natusk.mp3")

win_width = 700
win_height = 500

font.init()
font2 = font.Font('pixel_font.ttf', 30)
font3 = font.Font('pixel_font.ttf', 20)  # smaller font for text inside frame

init()

loading_screen = transform.scale(image.load("nachalo.png"), (win_width, win_height))
background_screen2 = transform.scale(image.load("background.jpg"), (win_width, win_height)) 

window = display.set_mode((win_width, win_height))
display.set_caption("Моя Гра")

text_color = (255, 255, 255)

button_play_text = font2.render("Іграть", True, text_color)
button_play_rect = button_play_text.get_rect(center=(win_width // 2, win_height // 2 - 35))

button_exit_game_text = font2.render("Вийти з гри", True, text_color)
button_exit_game_rect = button_exit_game_text.get_rect(center=(win_width // 2, win_height // 2 + 45))

star_left_img_original = image.load("star.png").convert_alpha()
star_right_img_original = image.load("star2.png").convert_alpha()
logo_img_original = image.load("logo.png").convert_alpha()
star3_img_original = image.load("Star3.png").convert_alpha()
star4_img_original = image.load("Star4.png").convert_alpha()

star_scale = 0.5
logo_scale = 2
star3_scale = 2
star4_scale = 2

star_left_img = transform.scale(star_left_img_original, (int(star_left_img_original.get_width() * star_scale), int(star_left_img_original.get_height() * star_scale)))
star_right_img = transform.scale(star_right_img_original, (int(star_right_img_original.get_width() * star_scale), int(star_right_img_original.get_height() * star_scale)))
logo_img = transform.scale(logo_img_original, (int(logo_img_original.get_width() * logo_scale), int(logo_img_original.get_height() * logo_scale)))
star3_img = transform.scale(star3_img_original, (int(star3_img_original.get_width() * star3_scale), int(star3_img_original.get_height() * star3_scale)))
star4_img = transform.scale(star4_img_original, (int(star4_img_original.get_width() * star4_scale), int(star4_img_original.get_height() * star4_scale)))

star_left_rect = star_left_img.get_rect()
star_right_rect = star_right_img.get_rect()
logo_rect = logo_img.get_rect(centerx=win_width // 2 + 17, y=0)
star3_left_rect = star3_img.get_rect(topleft=(-90, -50))
star3_right_rect = star3_img.get_rect(topright=(win_width + 85, -50))
star4_left_rect = star4_img.get_rect(topleft=(-90, 200))
star4_right_rect = star4_img.get_rect(topright=(win_width + 85, 200))
star4_down_rect = star4_img.get_rect(topright=(win_width - 50, 300))

class AnimatedSprite:
    def __init__(self, image, rect, fade_duration=1000, start_time=None):
        self.original_image = image
        self.rect = rect
        self.fade_duration = fade_duration
        if start_time is None:
            self.start_time = time.time() * 1000
        else:
            self.start_time = start_time
        self.fading_in = True

    def update(self):
        current_time = time.time() * 1000
        elapsed_time = current_time - self.start_time
        alpha = 0
        if self.fading_in:
            alpha = int((elapsed_time / self.fade_duration) * 255)
            if alpha > 255:
                alpha = 255
                self.fading_in = False
                self.start_time = current_time
        else:
            alpha = 255 - int((elapsed_time / self.fade_duration) * 255)
            if alpha < 125:
                alpha = 50
                self.fading_in = True
                self.start_time = current_time

        self.image = self.original_image.copy()
        self.image.set_alpha(alpha)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

animated_star_left_missions = AnimatedSprite(star_left_img, star_left_rect.copy(), fade_duration=randint(500, 1500))
animated_star_right_missions = AnimatedSprite(star_right_img, star_right_rect.copy(), fade_duration=randint(800, 2000), start_time=(time.time() * 1000) + randint(0, 500))
animated_star_left_modes = AnimatedSprite(star_left_img, star_left_rect.copy(), fade_duration=randint(700, 1800), start_time=(time.time() * 1000) + randint(200, 800))
animated_star_right_modes = AnimatedSprite(star_right_img, star_right_rect.copy(), fade_duration=randint(600, 1600))
animated_logo = AnimatedSprite(logo_img, logo_rect.copy(), fade_duration=2000)
animated_star3_left = AnimatedSprite(star3_img, star3_left_rect.copy(), fade_duration=randint(1000, 2500), start_time=(time.time() * 1000) + randint(0, 1000))
animated_star3_right = AnimatedSprite(star3_img, star3_right_rect.copy(), fade_duration=randint(900, 2200))
animated_star4_left = AnimatedSprite(star4_img, star4_left_rect.copy(), fade_duration=randint(1200, 2800), start_time=(time.time() * 1000) + randint(300, 900))
animated_star4_right = AnimatedSprite(star4_img, star4_right_rect.copy(), fade_duration=randint(1100, 2600))
animated_star4_down = AnimatedSprite(star4_img, star4_down_rect.copy(), fade_duration=randint(1300, 3000), start_time=(time.time() * 1000) + randint(100, 600))

class MenuRocket(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed, target_rect=None):
        sprite.Sprite.__init__(self)
        self.original_image = image.load(player_image).convert_alpha()
        self.image = transform.scale(self.original_image, (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.start_time = time.time()
        self.animation_interval = 7
        self.target_rect = target_rect
        self.active = False
        self.spawn_time = 0
        self.base_speed = player_speed
        self.speed_multiplier = 0.7
        self.dx = 0
        self.dy = 0

    def update(self):
        current_time = time.time()
        if not self.active and current_time - self.spawn_time >= self.animation_interval:
            self.rect.x = -self.rect.width
            self.rect.y = randint(50, win_height - 150)
            self.active = True
            self.speed = self.base_speed * self.speed_multiplier
            if self.target_rect:
                angle = math.atan2(self.target_rect.centery - self.rect.centery, self.target_rect.centerx - self.rect.centerx)
                self.dx = self.speed * math.cos(angle)
                self.dy = self.speed * math.sin(angle)
            else:
                self.dx = self.speed
                self.dy = 0
            self.spawn_time = current_time

        if self.active:
            self.rect.x += self.dx
            self.rect.y += self.dy
            if self.rect.left > win_width or self.rect.top < -self.rect.height or self.rect.bottom > win_height:
                self.kill()

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

menu_rockets = sprite.Group()
last_rocket_spawn_time = time.time()
rocket_spawn_interval = 8
rocket_speed = 0.1

def spawn_menu_rocket(target_rect=None):
    global last_rocket_spawn_time, rocket_speed
    current_time = time.time()
    if current_time - last_rocket_spawn_time >= rocket_spawn_interval:
        rocket = MenuRocket("raketa2.png", -100, win_height // 2, 80, 100, rocket_speed, target_rect)
        menu_rockets.add(rocket)
        last_rocket_spawn_time = current_time

def draw_main_menu():
    window.blit(loading_screen, (0, 0))
    animated_logo.update()
    animated_logo.draw(window)
    animated_star3_left.update()
    animated_star3_left.draw(window)
    animated_star3_right.update()
    animated_star3_right.draw(window)
    animated_star4_left.update()
    animated_star4_left.draw(window)
    animated_star4_right.update()
    animated_star4_right.draw(window)
    animated_star4_down.update()
    animated_star4_down.draw(window)

    animated_star_left_missions.rect.right = button_play_rect.left - 10
    animated_star_left_missions.rect.centery = button_play_rect.centery
    animated_star_left_missions.update()
    animated_star_left_missions.draw(window)

    animated_star_right_missions.rect.left = button_play_rect.right + 10
    animated_star_right_missions.rect.centery = button_play_rect.centery
    animated_star_right_missions.update()
    animated_star_right_missions.draw(window)

    if button_play_rect.collidepoint(mouse.get_pos()):
        scaled_play_text = transform.scale(button_play_text, (int(button_play_text.get_width() * 1.25), int(button_play_text.get_height() * 1.25)))
        scaled_play_rect = scaled_play_text.get_rect(center=button_play_rect.center)
        window.blit(scaled_play_text, scaled_play_rect)
    else:
        window.blit(button_play_text, button_play_rect)

    if button_exit_game_rect.collidepoint(mouse.get_pos()):
        scaled_exit_game_text = transform.scale(button_exit_game_text, (int(button_exit_game_text.get_width() * 1.25), int(button_exit_game_text.get_height() * 1.25)))
        scaled_exit_game_rect = scaled_exit_game_text.get_rect(center=button_exit_game_rect.center)
        window.blit(scaled_exit_game_text, scaled_exit_game_rect)
    else:
        window.blit(button_exit_game_text, button_exit_game_rect)

    menu_rockets.update()
    menu_rockets.draw(window)

    display.update()

def draw_screen2():
    window.blit(background_screen2, (0, 0))
    player.draw(window)
    player.draw_health(window)
    for meteor in meteors:
        meteor.draw(window)
    for enemy in enemies:
        enemy.draw(window)
    enemy_bullets.draw(window)
    bullets.draw(window)
    hit_effects.update()
    hit_effects.draw(window)
    if show_fuel:
        elapsed = time.time() - fuel_blink_start_time
        alpha = 128 + int(127 * math.sin(elapsed * 5))  # Blink speed multiplier 5
        if alpha < 0:
            alpha = 0
        elif alpha > 255:
            alpha = 255
        fuel_image = fuel_image_original.copy()
        fuel_image.set_alpha(alpha)
        fuel_rect = fuel_image.get_rect(midtop=(win_width // 2, 10))
        window.blit(fuel_image, fuel_rect)

        padding = 30
        vertical_offset2 = 50
        horizontal_offset = 55

        # Text to display, default
        if not hasattr(draw_screen2, "current_text"):
            draw_screen2.current_text = "Ой-ой, у тебе закінчилося пальне."

        # Ensure current_text is a string before rendering
        if isinstance(draw_screen2.current_text, list):
            text_to_render = "\n".join(draw_screen2.current_text)
        else:
            text_to_render = draw_screen2.current_text

        text2 = font3.render(text_to_render, True, (255, 255, 255))
        # Calculate frame size based on text size and padding
        frame2_width = text2.get_width() + padding * 2 + 100
        frame2_height = text2.get_height() + padding * 2 + 80
        # Position frame below fuel image with vertical offset
        frame2_rect = Rect(0, 0, frame2_width, frame2_height)
        frame2_rect.centerx = win_width // 2 + horizontal_offset
        frame2_rect.top = fuel_rect.bottom + vertical_offset2
        # Position text centered inside frame but slightly higher
        text2_rect = text2.get_rect(center=(frame2_rect.centerx, frame2_rect.centery - 30))
        frame2_surface = Surface((frame2_rect.width, frame2_rect.height), SRCALPHA)
        transparent_gray = (200, 200, 200, 100)
        frame2_surface.fill(transparent_gray)
        window.blit(frame2_surface, frame2_rect.topleft)
        window.blit(text2, text2_rect)
    display.update()

class Player(sprite.Sprite):
    def __init__(self, image_path, x, y, width, height):
        super().__init__()
        self.original_image = image.load(image_path).convert_alpha()
        self.image = transform.scale(self.original_image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 1
        self.move_up = False
        self.move_down = False
        self.health = 3
        self.invulnerable = False
        self.invulnerable_start_time = 0
        self.image_changed_time = 0
        self.original_image_scaled = self.image
        self.damaged_image = transform.scale(image.load("raketa_gg.png").convert_alpha(), (width, height))
        self.can_move = True

    def update(self):
        current_time = time.time()
        if self.invulnerable:
            if current_time - self.invulnerable_start_time >= 3:
                self.invulnerable = False
                self.image.set_alpha(255) 
            else:
                elapsed = current_time - self.invulnerable_start_time
                alpha = 50 + int((math.sin(elapsed * 10) + 1) / 2 * (255 - 50))
                self.image.set_alpha(alpha)
        if self.image == self.damaged_image and current_time - self.image_changed_time >= 1:
            self.image = self.original_image_scaled
            self.can_move = True

        if self.can_move:
            if self.move_up:
                self.rect.y -= self.speed
                if self.rect.y < 0:
                    self.rect.y = 0
            if self.move_down:
                self.rect.y += self.speed
                if self.rect.y > win_height - self.rect.height:
                    self.rect.y = win_height - self.rect.height

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))

    def draw_health(self, surface):
        health_text = font2.render(f"Здоров'я: {self.health}", True, (255, 0, 0))
        surface.blit(health_text, (10, 10))

current_menu = "loading"
loading_start_time = time.time()
loading_duration = 6
game = True

screen2_start_time = None
fuel_image_original = transform.scale(image.load("fuel.png").convert_alpha(), (420, 320))
fuel_image = fuel_image_original.copy()
fuel_blink_start_time = time.time()
show_fuel = False

class Meteor(sprite.Sprite):
    def __init__(self, image_path, x, y, width, height, speed):
        super().__init__()
        self.original_image = image.load(image_path).convert_alpha()
        self.image = transform.scale(self.original_image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.rect.x = win_width + randint(20, 100)
            self.rect.y = randint(0, win_height - self.rect.height)

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))

meteors = sprite.Group()
meteor_speed = 1.5
meteor_count = randint(3, 5)

for _ in range(meteor_count):
    meteor_x = win_width + randint(20, 300)
    meteor_y = randint(0, win_height - 60)
    meteor = Meteor("meteor.png", meteor_x, meteor_y, 70, 40, meteor_speed)
    meteors.add(meteor)

last_meteor_spawn_time = time.time()
meteor_spawn_interval = randint(3, 5)
max_meteors = 5

enemy_image_path = "monster.png"
enemy_width = 60
enemy_height = 60
enemy_speed = 1.0
enemy_count = 3
enemy_fire_rate = 0.5 

monster_gg_image = transform.scale(image.load("monster_gg.png").convert_alpha(), (enemy_width, enemy_height))

class HitEffect(sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = monster_gg_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.start_time = time.time()

    def update(self):
        if time.time() - self.start_time > 0.5:
            self.kill()

class Enemy(sprite.Sprite):
    def __init__(self, image_path, x, y, width, height, speed):
        super().__init__()
        self.original_image = image.load(image_path).convert_alpha()
        self.image = transform.scale(self.original_image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.last_shot_time = time.time()  

    def update(self):
        if not hasattr(self, 'dx'):
            self.dx = -self.speed
            self.dy = 0
            self.change_dir_time = time.time() + 2

        current_time = time.time()
        if current_time > self.change_dir_time:
            directions = [
                (-self.speed, 0),  
                (self.speed, 0),   
                (0, -self.speed),  
                (0, self.speed)    
            ]
            self.dx, self.dy = directions[randint(0, 3)]
            self.change_dir_time = current_time + randint(1, 3)

        new_x = self.rect.x + self.dx
        new_y = self.rect.y + self.dy

        if new_x < win_width // 2:
            new_x = win_width // 2
            self.dx = -self.dx 

        if new_x > win_width - self.rect.width:
            new_x = win_width - self.rect.width
            self.dx = -self.dx

        if new_y < 0:
            new_y = 0
            self.dy = -self.dy

        if new_y > win_height - self.rect.height:
            new_y = win_height - self.rect.height
            self.dy = -self.dy

        self.rect.x = new_x
        self.rect.y = new_y
        self.shoot()

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))

    def shoot(self):
        current_time = time.time()
        if current_time - self.last_shot_time >= 1 / enemy_fire_rate:
            bullet_x = self.rect.left
            bullet_y = self.rect.centery - 5
            bullet = EnemyBullet(bullet_x, bullet_y)
            enemy_bullets.add(bullet)
            self.last_shot_time = current_time

class EnemyBullet(sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = transform.scale(image.load("pyli2.png").convert_alpha(), (60, 35))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = -3  

    def update(self):
        self.rect.x += self.speed
        if self.rect.right < 0:
            self.kill()

enemies = sprite.Group()
enemy_bullets = sprite.Group() 

enemy_x = win_width + randint(20, 300)
enemy_y = randint(0, win_height - enemy_height)
enemy = Enemy(enemy_image_path, enemy_x, enemy_y, enemy_width, enemy_height, enemy_speed)
enemies.add(enemy)

last_enemy_spawn_time = time.time()
enemy_spawn_interval = randint(2, 5) 
max_enemies = 3

player = Player("raketa2.png", 10, win_height // 2 - 50, 80, 100)  

class Bullet(sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = transform.scale(image.load("pyli.png").convert_alpha(), (20, 10))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 3

    def update(self):
        self.rect.x += self.speed
        if self.rect.left > win_width:
            self.kill()

bullets = sprite.Group()

hit_effects = sprite.Group()

draw_main_menu()

while game:
    current_time = time.time()
    if current_menu == "loading":
        window.fill((0, 0, 0))
        loading_img = transform.scale(image.load("loading.png"), (win_width, win_height))
        window.blit(loading_img, (0, 0))
        large_font = font.Font('pixel_font.ttf', 60)
        loading_text = large_font.render("Загрузка...", True, (255, 255, 255))
        loading_text_rect = loading_text.get_rect(center=(win_width // 2, win_height // 2 - 50))
        window.blit(loading_text, loading_text_rect)

        # Load and display player2.png image centered above the loading text
        player2_img = transform.scale(image.load("player2.png").convert_alpha(), (300, 300))
        player2_rect = player2_img.get_rect(center=(win_width // 2 - 130, win_height // 2 + 70))
        window.blit(player2_img, player2_rect)
        display.update()
        if current_time - loading_start_time >= loading_duration:
            current_menu = "main"
    else:
        spawn_menu_rocket()
        for e in event.get():
            if e.type == QUIT:
                game = False
            elif e.type == KEYDOWN:
                if e.key == K_UP or e.key == K_w:
                    player.move_up = True
                elif e.key == K_DOWN or e.key == K_s:
                    player.move_down = True
                elif e.key == K_SPACE and current_menu == "screen2":
                    bullet_x = player.rect.right
                    bullet_y = player.rect.centery - 5  
                    bullet = Bullet(bullet_x, bullet_y)
                    bullets.add(bullet)
                elif e.key == K_e and current_menu == "screen2":
                    # Cycle through texts on pressing E
                    if not hasattr(draw_screen2, "text_index"):
                        draw_screen2.text_index = 0
                    draw_screen2.text_index = (draw_screen2.text_index + 1) % 3
                    if draw_screen2.text_index == 0:
                        draw_screen2.current_text = ["Ой-ой, у тебе закінчилося пальне."]
                    elif draw_screen2.text_index == 1:
                        draw_screen2.current_text = ["Дивися, он планета С-333", "сядь на неї й спробуй знайти пальне."]
                    elif draw_screen2.text_index == 2:
                        draw_screen2.current_text = ["Там є військова база, якщо не помиляюся."]
                elif e.key == K_q and current_menu == "screen2":
                    # Reset to first text on pressing Q
                    draw_screen2.text_index = 0
                    draw_screen2.current_text = "Ой-ой, у тебе закінчилося пальне."
            elif e.type == KEYUP:
                if e.key == K_UP or e.key == K_w:
                    player.move_up = False
                elif e.key == K_DOWN or e.key == K_s:
                    player.move_down = False
            elif e.type == MOUSEBUTTONDOWN:
                if e.button == 1:
                    mouse_pos = e.pos
                    if current_menu == "main":
                        if button_play_rect.collidepoint(mouse_pos):
                            natusk_sound.play()
                            current_menu = "screen2"  
                        elif button_exit_game_rect.collidepoint(mouse_pos):
                            natusk_sound.play()
                            game = False

        if current_menu == "main":
            draw_main_menu()
        if current_menu == "screen2":
            if screen2_start_time is None:
                screen2_start_time = time.time()

            player.update()
            meteors.update()
            bullets.update()
            enemy_bullets.update() 

            current_time = time.time()
            if current_time - screen2_start_time >= 15:
                meteors.empty()
                enemies.empty()
                show_fuel = True

            if current_time - last_meteor_spawn_time >= meteor_spawn_interval:
                if len(meteors) < max_meteors:
                    meteor_x = win_width + randint(20, 100)
                    meteor_y = randint(0, win_height - 60)
                    new_meteor = Meteor("meteor.png", meteor_x, meteor_y, 70, 40, meteor_speed)
                    meteors.add(new_meteor)
                last_meteor_spawn_time = current_time
                meteor_spawn_interval = randint(3, 5)

            for meteor in meteors:
                if player.rect.colliderect(meteor.rect):
                    if not player.invulnerable:
                        player.health -= 1
                        player.invulnerable = True
                        player.invulnerable_start_time = time.time()
                        player.image = player.damaged_image
                        player.image_changed_time = time.time()
                        player.can_move = False
                    meteor.rect.x = win_width + randint(20, 100)
                    meteor.rect.y = randint(0, win_height - meteor.rect.height)
                    if player.health < 0:
                        player.health = 0

            for bullet in enemy_bullets:
                if player.rect.colliderect(bullet.rect):
                    if not player.invulnerable:
                        player.health -= 1
                        player.invulnerable = True
                        player.invulnerable_start_time = time.time()
                        player.image = player.damaged_image
                        player.image_changed_time = time.time()
                        player.can_move = False
                    bullet.kill()
                    if player.health < 0:
                        player.health = 0

            collisions = sprite.groupcollide(bullets, enemies, True, True)
            for bullet, hit_enemies in collisions.items():
                for enemy in hit_enemies:
                    hit_x = enemy.rect.centerx - monster_gg_image.get_width() // 2
                    hit_y = enemy.rect.centery - monster_gg_image.get_height() // 2
                    hit_effect = HitEffect(hit_x, hit_y)
                    hit_effects.add(hit_effect)

            current_time = time.time()
            if len(enemies) < max_enemies and current_time - last_enemy_spawn_time >= enemy_spawn_interval:
                enemy_x = win_width + randint(20, 300)
                enemy_y = randint(0, win_height - enemy_height)
                new_enemy = Enemy(enemy_image_path, enemy_x, enemy_y, enemy_width, enemy_height, enemy_speed)
                enemies.add(new_enemy)
                last_enemy_spawn_time = current_time
                enemy_spawn_interval = randint(2, 5) 

            draw_screen2() 
            for meteor in meteors:
                meteor.draw(window)

            enemies.update()
            for enemy in enemies:
                enemy.draw(window)

            bullets.draw(window)

            hit_effects.update()
            hit_effects.draw(window)

quit()

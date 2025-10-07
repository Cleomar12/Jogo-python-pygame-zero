import pgzrun
from pygame import Rect
import random

WIDTH = 1200
HEIGHT = 600
sound_enabled = True
game_state = "menu"

# Botões do jogo
buttons = {
    "start": Rect(WIDTH // 2 - 150, 200, 300, 50), #Começar Jogo
    "toggle_sound": Rect(WIDTH // 2 - 150, 280, 300, 50),# Ativa/desativar sons
    "exit": Rect(WIDTH // 2 - 150, 360, 300, 50),# Sair
    "back_button": Rect(5, 5, 100, 20), # Voltar ao Menu
    "try_agan": Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 40) # Jogar Novamente
}

# Classe
class Hero:
    def __init__(self):
        self.images_up = ['hero_swim1', 'hero_swim2']
        self.images_down = ['herodown_swim1', 'herodown_swim2']
        self.images_left = ['heroleft_swim1', 'heroleft_swim2']
        self.images_right = ['heroright_swim1', 'heroright_swim2']

        self.current_images = self.images_up
        self.actor = Actor(self.current_images[0], (WIDTH // 2, HEIGHT // 2))
        self.frame = 0
        clock.schedule_interval(self.animate, 0.3)

    def animate(self):
        self.frame = (self.frame + 1) % len(self.current_images)
        self.actor.image = self.current_images[self.frame]

    def update(self):
        moving = False
        if keyboard.left:
            self.actor.x -= 4
            self.current_images = self.images_left
            moving = True
        if keyboard.right:
            self.actor.x += 4
            self.current_images = self.images_right
            moving = True
        if keyboard.up:
            self.actor.y -= 4
            self.current_images = self.images_up
            moving = True
        if keyboard.down:
            self.actor.y += 4
            self.current_images = self.images_down
            moving = True
        if not moving:
            self.current_images = self.images_up

        self.actor.x = max(self.actor.width // 2, min(WIDTH - self.actor.width // 2, self.actor.x))
        self.actor.y = max(self.actor.height // 2, min(HEIGHT - self.actor.height // 2, self.actor.y))

    def draw(self):
        self.actor.draw()


class Enemy:
    def __init__(self, side):
        self.images = []
        self.actor = Actor("enemy1_down1")
        self.frame = 0
        self.vx, self.vy = 0, 0
        self.reset(side)
        clock.schedule_interval(self.animate, 0.3)

    def reset(self, side):
        self.side = side
        self.enemy_type = random.choice(['enemy1', 'enemy2'])

        if side == "top":
            self.images = [f"{self.enemy_type}_down1", f"{self.enemy_type}_down2"]
            self.actor.pos = (random.randint(50, WIDTH - 50), -50)
            self.vx, self.vy = 0, random.randint(2, 4)
        elif side == "bottom":
            self.images = [f"{self.enemy_type}_up1", f"{self.enemy_type}_up2"]
            self.actor.pos = (random.randint(50, WIDTH - 50), HEIGHT + 50)
            self.vx, self.vy = 0, -random.randint(2, 4)
        elif side == "left":
            self.images = [f"{self.enemy_type}_right1", f"{self.enemy_type}_right2"]
            self.actor.pos = (-50, random.randint(50, HEIGHT - 50))
            self.vx, self.vy = random.randint(2, 4), 0
        elif side == "right":
            self.images = [f"{self.enemy_type}_left1", f"{self.enemy_type}_left2"]
            self.actor.pos = (WIDTH + 50, random.randint(50, HEIGHT - 50))
            self.vx, self.vy = -random.randint(2, 4), 0

        self.actor.image = self.images[0]

    def animate(self):
        self.frame = (self.frame + 1) % len(self.images)
        self.actor.image = self.images[self.frame]

    def update(self):
        self.actor.x += self.vx
        self.actor.y += self.vy

        if (self.actor.x < -100 or self.actor.x > WIDTH + 100 or
            self.actor.y < -100 or self.actor.y > HEIGHT + 100):
            new_side = random.choice(["top", "bottom", "left", "right"])
            self.reset(new_side)

    def draw(self):
        self.actor.draw()


# objetos Globais
hero = None
enemies = []

# Inicia e reinicia o jogo
def start_game():
    global hero, enemies, game_state
    hero = Hero()
    enemies = [Enemy(random.choice(["top", "bottom", "left", "right"])) for _ in range(6)]
    game_state = "game"
    if sound_enabled:
        music.play("menu_music")

# Funções principais
def update():
    global game_state
    if game_state == "game":
        hero.update()
        for enemy in enemies:
            enemy.update()
            if hero.actor.colliderect(enemy.actor):
                if sound_enabled:
                    sounds.hit.play()
                game_state = "game_over"
                music.stop()


def draw():
    screen.clear()
    screen.blit('background', (0, 0))

    if game_state == "menu":
        screen.draw.text("MENU", center=(WIDTH//2, 100), fontsize=60, color="white")

        screen.draw.filled_rect(buttons["start"], "green")
        screen.draw.text("Start Game", center=buttons["start"].center, fontsize=40, color="white")

        screen.draw.filled_rect(buttons["toggle_sound"], "blue")
        sound_text = "Sounds: On" if sound_enabled else "Sounds: Off"
        screen.draw.text(sound_text, center=buttons["toggle_sound"].center, fontsize=40, color="white")

        screen.draw.filled_rect(buttons["exit"], "red")
        screen.draw.text("Exit", center=buttons["exit"].center, fontsize=40, color="white")

    elif game_state == "game":
        hero.draw()
        for enemy in enemies:
            enemy.draw()

        screen.draw.filled_rect(buttons["back_button"], "blue")
        screen.draw.text("Menu", center=buttons["back_button"].center, fontsize=20, color="white")

    elif game_state == "game_over":
        screen.draw.text("GAME OVER", center=(WIDTH//2, HEIGHT//2 - 50), fontsize=80, color="red")
        screen.draw.text("You collided with an enemy!", center=(WIDTH//2, HEIGHT//2 + 20), fontsize=40, color="white")

        screen.draw.filled_rect(buttons["back_button"], "blue")
        screen.draw.text("Menu", center=buttons["back_button"].center, fontsize=30, color="white")

        screen.draw.filled_rect(buttons["try_agan"], "green")
        screen.draw.text("TENTAR DE NOVO", center=buttons["try_agan"].center, fontsize=30, color="white")

def on_mouse_down(pos):
    global game_state, sound_enabled

    if game_state == "menu":
        if buttons["start"].collidepoint(pos):
            start_game()
        elif buttons["toggle_sound"].collidepoint(pos):
            sound_enabled = not sound_enabled
            if not sound_enabled:
                music.stop()
            else:
                if game_state == "game":
                    music.play("menu_music")
        elif buttons["exit"].collidepoint(pos):
            exit()

    elif game_state == "game_over":
        if buttons["back_button"].collidepoint(pos):
            game_state = "menu"
            music.stop()
        elif buttons["try_agan"].collidepoint(pos):
            start_game()

    elif game_state == "game":
        if buttons["back_button"].collidepoint(pos):
            game_state = "menu"
            music.stop()

pgzrun.go()
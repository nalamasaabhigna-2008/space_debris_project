import pygame
import random
import math

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("NASA Space Debris Monitoring System")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 16)

# Load images
earth_img = pygame.image.load("earth.png")
earth_img = pygame.transform.scale(earth_img, (120, 120))

iss_img = pygame.image.load("iss.png")
iss_img = pygame.transform.scale(iss_img, (60, 40))

# Load sounds
beep_sound = pygame.mixer.Sound("beep.wav")
pop_sound = pygame.mixer.Sound("pop.wav")

# Colors
WHITE = (255, 255, 255)
RED = (255, 80, 80)
GREEN = (0, 255, 150)
BLACK = (0, 0, 0)

# Stars
stars = [(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(150)]

# Debris
class Debris:
    def __init__(self):
        self.radius = random.randint(140, 300)
        self.angle = random.uniform(0, 2*math.pi)
        self.speed = random.uniform(0.005, 0.02)

    def update(self):
        self.angle += self.speed

    def get_pos(self):
        x = WIDTH//2 + self.radius * math.cos(self.angle)
        y = HEIGHT//2 + self.radius * math.sin(self.angle)
        return x, y

    def draw(self):
        x, y = self.get_pos()
        pygame.draw.circle(screen, RED, (int(x), int(y)), 4)
        label = font.render("Debris", True, WHITE)
        screen.blit(label, (int(x)+5, int(y)))

# ISS
class ISS:
    def __init__(self):
        self.radius = 180
        self.angle = 0
        self.speed = 0.01

    def update(self):
        self.angle += self.speed

    def draw(self):
        x = WIDTH//2 + self.radius * math.cos(self.angle)
        y = HEIGHT//2 + self.radius * math.sin(self.angle)
        screen.blit(iss_img, (int(x), int(y)))
        label = font.render("ISS", True, WHITE)
        screen.blit(label, (int(x), int(y)-15))
        return x, y

# Robot
class Robot:
    def __init__(self):
        self.x = WIDTH//2
        self.y = HEIGHT//2 - 150
        self.speed = 2
        self.target = None

    def move(self, target):
        self.target = target
        beep_sound.play()

        dx = target[0] - self.x
        dy = target[1] - self.y
        dist = math.hypot(dx, dy)

        if dist > 0:
            self.x += (dx/dist) * self.speed
            self.y += (dy/dist) * self.speed

    def draw(self):
        pygame.draw.circle(screen, GREEN, (int(self.x), int(self.y)), 8)
        label = font.render("Robot", True, WHITE)
        screen.blit(label, (int(self.x)+5, int(self.y)))

        if self.target:
            pygame.draw.line(screen, GREEN, (int(self.x), int(self.y)), (int(self.target[0]), int(self.target[1])), 1)

# Create objects
robot = Robot()
iss = ISS()
debris_list = [Debris() for _ in range(8)]
removed_count = 0

running = True
while running:
    screen.fill(BLACK)

    for star in stars:
        pygame.draw.circle(screen, WHITE, star, 1)

    screen.blit(earth_img, (WIDTH//2 - 60, HEIGHT//2 - 60))
    earth_label = font.render("Earth", True, WHITE)
    screen.blit(earth_label, (WIDTH//2 - 20, HEIGHT//2 + 60))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    iss.draw()
    iss.update()

    positions = []

    for d in debris_list:
        d.update()
        d.draw()
        positions.append((d, d.get_pos()))

    if positions:
        nearest = min(positions, key=lambda p: math.hypot(robot.x-p[1][0], robot.y-p[1][1]))
        robot.move(nearest[1])

        if math.hypot(robot.x-nearest[1][0], robot.y-nearest[1][1]) < 10:
            debris_list.remove(nearest[0])
            removed_count += 1
            pop_sound.play()

    robot.draw()

    pygame.draw.rect(screen, (20, 20, 20), (0, 0, WIDTH, 40))
    text1 = font.render(f"Debris Remaining: {len(debris_list)}", True, WHITE)
    text2 = font.render(f"Debris Removed: {removed_count}", True, WHITE)
    text3 = font.render("System: ACTIVE", True, GREEN)

    screen.blit(text1, (10, 10))
    screen.blit(text2, (200, 10))
    screen.blit(text3, (400, 10))

    pygame.display.update()
    clock.tick(60)

pygame.quit()

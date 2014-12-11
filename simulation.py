__author__ = 'conrad'
import pygame, random

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400

SMALL = 1
MEDIUM = 2
LARGE = 3

class Animal(pygame.sprite.Sprite):

    def __init__(self, animalType, x, y, spriteGroupSelf, spriteGroupPrey, spriteGroupAll):

        pygame.sprite.Sprite.__init__(self)

        self.animalType = animalType
        self.spriteGroupSelf = spriteGroupSelf
        self.spriteGroupPrey = spriteGroupPrey
        self.spriteGroupAll = spriteGroupAll

        self.width = animalType*SCREEN_WIDTH/100
        self.height = animalType*SCREEN_WIDTH/100

        self.image = pygame.Surface((self.width, self.height))
        if animalType == SMALL:
            self.image.fill(BLUE)
        if animalType == MEDIUM:
            self.image.fill(GREEN)
        if animalType == LARGE:
            self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        '''
        self.image.set_colorkey(BLACK)
        if animalType == SMALL:
            pygame.draw.circle(self.image, BLUE, (x, y), animalType*5)
        if animalType == MEDIUM:
            pygame.draw.circle(self.image, GREEN, (x, y), animalType*5)
        if animalType == LARGE:
            pygame.draw.circle(self.image, RED, (x, y), animalType*5)
        '''

        self.hspeed = random.randint((-1 * (animalType-2) + 2) * -(SCREEN_WIDTH/100), (-1 * (animalType-2) + 2) * (SCREEN_WIDTH/100))
        self.vspeed = random.randint((-1 * (animalType-2) + 2) * -(SCREEN_WIDTH/100), (-1 * (animalType-2) + 2) * (SCREEN_WIDTH/100))

        self.hunger = 100

    def update(self):

        extinctionSafe = False
        population = 0
        for animal in self.spriteGroupSelf.sprites():
            population += 1
        if not population > 1:
            extinctionSafe = True

        if self.hunger > 300 and not extinctionSafe:
            self.kill()
        elif self.hunger < 0:
            offspring = Animal(self.animalType, self.rect.x, self.rect.y, self.spriteGroupSelf, self.spriteGroupPrey, self.spriteGroupAll)
            self.spriteGroupSelf.add(offspring)
            self.spriteGroupAll.add(offspring)
            self.hunger = 150
            #print("offspring born")
        else:
            self.hunger += 1

        extinctionSafePrey = False
        populationPrey = 0
        for animal in self.spriteGroupPrey.sprites():
            populationPrey += 1
        if not populationPrey > 1:
            extinctionSafePrey = True
        if not extinctionSafePrey:
            eatenList = pygame.sprite.spritecollide(self, self.spriteGroupPrey, False)
            eat = False
            for prey in eatenList:
                if not eat:
                    self.hunger -= 100
                    prey.kill()
                    eat = True

        if random.randint(1, 90) == 90:
            self.hspeed = random.randint((-1 * (self.animalType-2) + 2) * -3, (-1 * (self.animalType-2) + 2) * 3)
            self.vspeed = random.randint((-1 * (self.animalType-2) + 2) * -3, (-1 * (self.animalType-2) + 2) * 3)
        if SCREEN_WIDTH - self.width > self.rect.x + self.hspeed > 0:
            self.rect.x += self.hspeed
        else:
            self.hspeed *= -1
            self.rect.x += self.hspeed
        if SCREEN_HEIGHT - self.height > self.rect.y + self.vspeed > 0:
            self.rect.y += self.vspeed
        else:
            self.vspeed *= -1
            self.rect.y += self.vspeed

        #print(self.hunger)

class Food(pygame.sprite.Sprite):

    def __init__(self, x, y):

        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((SCREEN_WIDTH/150, SCREEN_WIDTH/150))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Simulation():

    def __init__(self):

        self.spriteGroupFood = pygame.sprite.Group()
        self.spriteGroupSmall = pygame.sprite.Group()
        self.spriteGroupMedium = pygame.sprite.Group()
        self.spriteGroupLarge = pygame.sprite.Group()
        self.spriteGroupAll = pygame.sprite.Group()
        self.foodTotal = 2000
        for i in range(300):
            food = Food(random.randint(1, SCREEN_WIDTH - SCREEN_WIDTH/150), random.randint(1, SCREEN_HEIGHT - SCREEN_WIDTH/150))
            self.spriteGroupFood.add(food)
            self.spriteGroupAll.add(food)
        for i in range(50):
            animal = Animal(SMALL, random.randint(1, SCREEN_WIDTH - SCREEN_WIDTH/100), random.randint(1, SCREEN_HEIGHT), self.spriteGroupSmall, self.spriteGroupFood, self.spriteGroupAll)
            self.spriteGroupSmall.add(animal)
            self.spriteGroupAll.add(animal)
        for i in range(10):
            animal = Animal(MEDIUM, random.randint(1, SCREEN_WIDTH - 2 * SCREEN_WIDTH/100), random.randint(1, SCREEN_HEIGHT), self.spriteGroupMedium, self.spriteGroupSmall, self.spriteGroupAll)
            self.spriteGroupMedium.add(animal)
            self.spriteGroupAll.add(animal)
        for i in range(3):
            animal = Animal(LARGE, random.randint(1, SCREEN_WIDTH - 3 * SCREEN_WIDTH/100), random.randint(1, SCREEN_HEIGHT), self.spriteGroupLarge, self.spriteGroupMedium, self.spriteGroupAll)
            self.spriteGroupLarge.add(animal)
            self.spriteGroupAll.add(animal)

        self.screen = pygame.display.set_mode((SCREEN_WIDTH + 800, SCREEN_HEIGHT))
        pygame.display.set_caption("simulation")
        self.graph = Graph(self.spriteGroupFood, self.spriteGroupSmall, self.spriteGroupMedium, self.spriteGroupLarge, self.screen)
        self.graphUpdateCount = 0
        self.clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            self.foodTotal = 0
            for food in self.spriteGroupFood:
                self.foodTotal += 1
            for i in range(int(.01*self.foodTotal) + 1):
                food = Food(random.randint(1, SCREEN_WIDTH - SCREEN_WIDTH/150), random.randint(1, SCREEN_HEIGHT - SCREEN_WIDTH/150))
                self.spriteGroupFood.add(food)
                self.spriteGroupAll.add(food)

            self.spriteGroupAll.update()
            self.screen.fill(BLACK)
            self.spriteGroupAll.draw(self.screen)
            self.graph.update()
            pygame.display.flip()
            self.clock.tick(30)

class Graph():

    def __init__(self, foodGroup, smallGroup, mediumGroup, largeGroup, screen):

        self.foodGroup = foodGroup
        self.smallGroup = smallGroup
        self.mediumGroup = mediumGroup
        self.largeGroup = largeGroup
        self.screen = screen

        self.food = [0] * 801
        self.small = [0] * 801
        self.medium = [0] * 801
        self.large = [0] * 801

    def update(self):

        countList = self.foodGroup.sprites()
        count = 0
        for i in countList:
            count += 1
        self.food.insert(0, count)
        var = self.food.pop()
        countList = self.smallGroup.sprites()
        count = 0
        for i in countList:
            count += 1
        self.small.insert(0, count * 1.5)
        var = self.small.pop()
        countList = self.mediumGroup.sprites()
        count = 0
        for i in countList:
            count += 1
        self.medium.insert(0, count * 5)
        var = self.medium.pop()
        countList = self.largeGroup.sprites()
        count = 0
        for i in countList:
            count += 1
        self.large.insert(0, count * 5)
        var = self.large.pop()

        pygame.draw.rect(self.screen, BLACK, (SCREEN_WIDTH, 0, SCREEN_WIDTH+800, SCREEN_HEIGHT))
        for i in range(800):
            pygame.draw.line(self.screen, WHITE, (SCREEN_WIDTH + i, SCREEN_HEIGHT - self.food[i]), (SCREEN_WIDTH + i + 1, SCREEN_HEIGHT - self.food[i+1]))
        for i in range(800):
            pygame.draw.line(self.screen, BLUE, (SCREEN_WIDTH + i, SCREEN_HEIGHT - self.small[i]), (SCREEN_WIDTH + i + 1, SCREEN_HEIGHT - self.small[i+1]))
        for i in range(800):
            pygame.draw.line(self.screen, GREEN, (SCREEN_WIDTH + i, SCREEN_HEIGHT - self.medium[i]), (SCREEN_WIDTH + i + 1, SCREEN_HEIGHT - self.medium[i+1]))
        for i in range(800):
            pygame.draw.line(self.screen, RED, (SCREEN_WIDTH + i, SCREEN_HEIGHT - self.large[i]), (SCREEN_WIDTH + i + 1, SCREEN_HEIGHT - self.large[i+1]))

simulation = Simulation()
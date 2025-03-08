import pygame
from misc import Vector
import misc
import random
import sys


pygame.font.init()

FONT1 = "Arial"

GEN_FONT = pygame.font.SysFont(FONT1, 70, bold=True)
MISC_FONT = pygame.font.SysFont(FONT1, 20, bold=True)

WIDTH = 600
HEIGHT = 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))


DOT_W = 10
DOT_H = 10

TARGET_W = 50
TARGET_H = TARGET_W / (170/216)

INCENTIVE_W = 30
INCENTIVE_H = INCENTIVE_W / (938/853)

DOT_PNG = pygame.image.load("Assets/dot.png")
TARGET_PNG = pygame.image.load("Assets/target.png")
INCENTIVE_PNG = pygame.image.load("Assets/incentive.png")
CHOSEN_DOT_PNG = pygame.image.load("Assets/chosen_dot.png")

DOT = pygame.transform.scale(DOT_PNG, (DOT_W, DOT_H))
TARGET = pygame.transform.scale(TARGET_PNG, (TARGET_W, TARGET_H))
INCENTIVE = pygame.transform.scale(
    INCENTIVE_PNG, (INCENTIVE_W, INCENTIVE_H))

CHOSEN_DOT = pygame.transform.scale(CHOSEN_DOT_PNG, (DOT_W, DOT_H))

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (200, 200, 200)
RED = (255, 0, 0)
BEIGE = ("#000000")


class Target:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)

    def draw(self, target: bool):
        if target:
            WIN.blit(TARGET, (self.rect.x, self.rect.y))
        else:
            WIN.blit(INCENTIVE, (self.rect.x, self.rect.y))
            pass


class Dot:
    def __init__(self, max_step, incent: list):

        self.goals_done = 0
        self.goal_lis = [Target(elem[0], elem[1],
                                INCENTIVE_W, INCENTIVE_H) for elem in incent]

        self.goal_lis[-1] = Target(incent[-1][0],
                                   incent[-1][1], TARGET_W, TARGET_H)

        # if max_step is None:
        #     steps = 400
        # else:
        #     steps = max_step

        self.rect = pygame.Rect(WIDTH / 2, HEIGHT - 50, DOT_W, DOT_H)
        self.acc = Vector(0, 0)
        self.vel = Vector(0, 0)

        self.chosen = False
        self.dead = False
        self.goal = False

        self.direct = misc.directions(max_step)
        self.step = 0

    def draw_goal(self):

        self.goal_lis[-1].draw(target=True)

        for i in range(len(self.goal_lis)-1):
            self.goal_lis[i].draw(target=False)

    def check_collide(self):

        if self.rect.colliderect(self.goal_lis[0].rect):
            if len(self.goal_lis) == 1:
                self.dead = True
                self.goal = True
            else:
                self.goal_lis.pop(0)
                self.goals_done += 1

    def draw(self, best):

        if self.chosen:
            WIN.blit(CHOSEN_DOT, (self.rect.x, self.rect.y))

        elif not best:
            WIN.blit(DOT, (self.rect.x, self.rect.y))

    def move(self):
        if not (0 < self.rect.x < WIDTH-10) or not (0 < self.rect.y < HEIGHT - 10):
            self.dead = True

        if not self.dead:
            try:
                self.acc = self.direct[self.step]
            except IndexError:
                self.dead = 1

            else:
                self.step += 1

                self.vel += self.acc
                if self.vel.mag > 7:
                    self.vel.mag = 7
                self.rect.x += self.vel._xcomp()
                self.rect.y += self.vel._ycomp()


class Generation:
    def __init__(self):
        self.val = 1

    def draw(self):
        self.surf = GEN_FONT.render(f"Gen: {self.val}", True, WHITE)
        self.surf.set_alpha(100)
        WIN.blit(self.surf, (WIDTH/2 - 100, HEIGHT - 300))

    def add_gen(self):
        self.val += 1


class NumMoves:
    def __init__(self, start):
        self.val = start

    def add_moves(self, val):
        if self.val < 600:
            self.val += val

    def draw(self):
        surf = MISC_FONT.render(f"Moves: {self.val}", True, WHITE)
        surf.set_alpha(100)
        WIN.blit(surf, (0, 0))


class Speed:
    def __init__(self):
        self.val = 1

    def double(self):
        self.val *= 2

    def half(self):
        self.val /= 2

    def draw(self):
        if self.val >= 1:
            self.val = int(self.val)

        surf = MISC_FONT.render(f"Speed: {self.val}x", True, WHITE)
        surf.set_alpha(100)
        WIN.blit(surf, (WIDTH - 120, 0))


class MiscText:
    def __init__(self, text, x, y):
        self.text = text
        self.x = x
        self.y = y

    def draw(self):
        surf = MISC_FONT.render(f"{self.text}", True, WHITE)
        surf.set_alpha(100)
        WIN.blit(surf, (self.x, self.y))


class Obstacles:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)
        self.surf = pygame.Surface((w, h))
        self.surf.fill(BEIGE)
        self.surf.set_alpha(100)

    def draw(self):
        WIN.blit(self.surf, (self.rect.x, self.rect.y))


def main(population: int,
         obs: list,
         mr: int,
         moves_init: dict,
         parent_selector: str,
         incentives: list):

    def new_dots(max_steps=None):
        return [Dot(max_steps, incent=incentives) for i in range(population)]

    def fitness_func():
        res = []
        for elem in dots:
            if elem.goal:
                calc = (1.0/16.0) + 10_000.0/(elem.step**2)

            else:
                dist = misc.dist(elem.rect, elem.goal_lis[0].rect)
                calc = 100/(dist) + elem.goals_done*1000

            res.append(calc)
        return res

        # --------------for not maze------------------
        # calc = 1/(dist**2) + (1/((20+elem.rect.y)**2)) * 2000

        # if elem.rect.y > HEIGHT - 20:
        #     calc = 0

        # --------------for maze------------------
        # | mutation rate -> 1%
        # dist = misc.dist(elem.rect, elem.goal_lis[0].rect)
        # calc = 1/(dist**2) + elem.goals_done*1000

    def best_dot():
        canditates = []
        for elem in dots:
            if elem.goal:
                canditates.append(elem)

        if len(canditates) == 0:
            lis = fitness_func()

            maxi_val = lis[0]
            maxi_i = 0
            for index in range(len(lis)):
                if maxi_val < lis[index]:
                    maxi_val = lis[index]
                    maxi_i = index

            # print(maxi_val)

            return {"dot": dots[maxi_i],
                    "steps": moves.val}

        chosen = canditates[0]
        least_steps = chosen.step
        for elem in canditates:
            if elem.step < least_steps:
                chosen = elem
                least_steps = chosen.step

        return {"dot": chosen,
                "steps": least_steps}

    def parent_selection():
        fitness_lis = fitness_func()
        # print(max(fitness_func))

        total_fitness = sum(fitness_lis)

        running_sum = 0

        r = random.uniform(0, total_fitness)

        for index in range(len(dots)):
            if running_sum <= r <= running_sum + fitness_lis[index]:
                return dots[index]

            running_sum += fitness_lis[index]

    def baby_maker(daddy):
        new_dot = Dot(moves.val, incentives)
        new_dot.direct = daddy.direct
        return new_dot

    def mutate(patient, best, max_steps):
        next_gen_dots = new_dots(max_steps)

        mutation_rate = mr

        for index in range(len(next_gen_dots)):

            for i in range(len(next_gen_dots[index].direct)):

                r = random.randint(1, 100)
                if r <= mutation_rate:

                    pass
                else:
                    try:
                        next_gen_dots[index].direct[i] = patient.direct[i]
                    except IndexError:
                        pass

        next_gen_dots[0].direct = best.direct
        next_gen_dots[0].chosen = True

        return next_gen_dots

    def evolve():
        nonlocal gen, moves

        gen.add_gen()

        if gen.val % moves_init["gen_to_incr"] == 0:
            moves.add_moves(moves_init["added_moves"])

        # find best dot
        best_dict = best_dot()
        best_one = best_dict["dot"]
        best_steps = best_dict["steps"]

        if best_steps < moves.val:
            moves.val = best_steps

        # select parent
        parent = parent_selection()
        # make baby from parent
        # baby = baby_maker(parent)
        if parent_selector == "Rank-based":
            baby = baby_maker(best_one)
        elif parent_selector == "Roulette Wheel":
            baby = baby_maker(parent)

        # mutate babies
        return mutate(baby, best_one, best_steps)

    fps = 60
    speed = Speed()
    gen = Generation()
    clock = pygame.time.Clock()

    show_best = False
    moves = NumMoves(moves_init["starting_moves"])
    show_obs = True

    instr = MiscText("[Space]: only show best",
                     x=WIDTH / 2 - 100, y=HEIGHT - 100)
    dots = new_dots(moves.val)

    while True:

        drawer = dots[0]
        num_dead = 0

        WIN.fill(GREY)

        instr.draw()
        speed.draw()
        moves.draw()
        gen.draw()

        if show_obs:
            for elem in obs:
                elem.draw()

        for elem in dots:

            elem.move()
            elem.draw(show_best)
            elem.check_collide()

            if drawer.goals_done < elem.goals_done:
                drawer = elem

            if show_obs:
                for elem_obs in obs:
                    if elem.rect.colliderect(elem_obs.rect):
                        elem.dead = True

            if elem.dead:
                num_dead += 1

        drawer.draw_goal()

        if num_dead == population:
            dots = evolve()

        clock.tick(fps)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    show_best = not show_best
                if event.key == pygame.K_UP:
                    speed.double()
                    fps *= 2

                if event.key == pygame.K_DOWN:
                    speed.half()
                    fps /= 2

                if event.key == pygame.K_f:
                    show_obs = not show_obs

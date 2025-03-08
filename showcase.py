from brain import *

# Change things here
COURSE_NUM = 2
POPULATION = 600
MUTATION_RATE = 10

STARTING_MOVES = 50
MOVE_INCR = 10
GEN_INCR = 5

RANK_BASED = True
ROULETTE_WHEEL = not RANK_BASED


def create_courses():
    res = []
    # ----------------------- course 0 -------------------------- #
    obs = []
    res.append(obs)

    # ----------------------- course 1 -------------------------- #
    obs = []
    obs.append(Obstacles(x=WIDTH/2 - 150, y=HEIGHT/2, w=300, h=10))
    obs.append(Obstacles(x=WIDTH/2+100, y=HEIGHT/2 - 100, w=300, h=10))
    obs.append(Obstacles(0, y=HEIGHT/2 - 100, w=300, h=10))
    obs.append(Obstacles(WIDTH/2, y=HEIGHT/2 - 200, w=100, h=10))
    res.append(obs)

    # ----------------------- course 2 -------------------------- #
    obs = []
    obs.append(Obstacles(x=50, y=HEIGHT/2 + 10, w=10, h=190))
    obs.append(Obstacles(x=50, y=HEIGHT/2 + 200, w=WIDTH, h=10))
    obs.append(Obstacles(x=0, y=HEIGHT/2 - 50, w=WIDTH/2 - 30, h=10))
    obs.append(Obstacles(x=50, y=HEIGHT/2, w=WIDTH, h=10))
    obs.append(Obstacles(x=WIDTH/2 + 30, y=HEIGHT/2 - 50, w=WIDTH/2, h=10))
    obs.append(Obstacles(x=WIDTH/2 + 30, y=HEIGHT/2 - 250, w=10, h=200))
    obs.append(Obstacles(x=WIDTH/2 - 40, y=HEIGHT/2 - 250, w=10, h=200))
    res.append(obs)

    # ----------------------- course 3 -------------------------- #
    obs = []

    obs.append(Obstacles(x=0, y=HEIGHT - 100, w=WIDTH - 30, h=10))
    obs.append(Obstacles(x=20, y=HEIGHT - 130, w=WIDTH, h=10))
    obs.append(Obstacles(x=20, y=HEIGHT - 300, w=10, h=170))
    obs.append(Obstacles(x=20, y=HEIGHT - 310, w=50, h=10))
    obs.append(Obstacles(x=0, y=HEIGHT - 340, w=110, h=10))
    obs.append(Obstacles(x=70, y=HEIGHT - 310, w=10, h=180))
    obs.append(Obstacles(x=100, y=HEIGHT - 330, w=10, h=170))
    obs.append(Obstacles(x=100, y=HEIGHT - 160, w=WIDTH - 130, h=10))
    obs.append(Obstacles(x=140, y=HEIGHT - 190, w=WIDTH - 130, h=10))
    obs.append(Obstacles(x=140, y=HEIGHT - 310, w=10, h=120))

    res.append(obs)
    return res


def incentives_creator():

    res = []
    # --------------- course 0 -------------------#
    incent = [(WIDTH/2 - TARGET_W/2, 5)]
    res.append(incent)
    # --------------- course 1 -------------------#
    incent = [(WIDTH/2 - TARGET_W/2, 5)]
    res.append(incent)

    # --------------- course 2 -------------------#
    incent = [(5, HEIGHT - 190),
              (5, HEIGHT - 385),
              (WIDTH/2 - TARGET_W/2 + 5, HEIGHT - 420),
              (WIDTH/2 - TARGET_W/2, 5)]
    res.append(incent)

    # --------------- course 3 -------------------#
    incent = [(WIDTH - 30, HEIGHT-123),
              (-5, HEIGHT-123),
              (-5, HEIGHT-335),
              (73, HEIGHT-333),
              (77, HEIGHT-157),
              (WIDTH - 27, HEIGHT-183),
              (108, 510),
              (WIDTH/2 - TARGET_W/2, 5)]
    res.append(incent)

    return res


def parent_select():
    if RANK_BASED:
        return "Rank-based"
    else:
        return "Roulette Wheel"


def not_main():

    str_select = parent_select()
    course_obstacles = create_courses()[COURSE_NUM]
    incentives = incentives_creator()[COURSE_NUM]

    moves_dict = {
        "starting_moves": STARTING_MOVES,
        "added_moves": MOVE_INCR,
        "gen_to_incr": GEN_INCR
    }
    main(population=POPULATION,
         obs=course_obstacles,
         incentives=incentives,
         mr=MUTATION_RATE,
         moves_init=moves_dict,
         parent_selector=str_select)


if __name__ == "__main__":
    not_main()

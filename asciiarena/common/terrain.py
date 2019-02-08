class Terrain:
    EMPTY = 0
    WALL = 1
    BORDER_WALL = 2

    WALL_SEED = 100

    @staticmethod
    def is_blocked(terrain):
        return (terrain == Terrain.WALL
             or terrain == Terrain.BORDER_WALL)


    @staticmethod
    def is_any(terrain, filter_terrain_list):
        for filter_terrain in filter_terrain_list:
            if filter_terrain == terrain:
                return True

        return False


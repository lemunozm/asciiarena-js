from common.util.vec2 import Vec2

class Direction:
    NONE = 0
    UP = 1 << 0
    DOWN = 1 << 1
    RIGHT = 1 << 2
    LEFT = 1 << 3
    LEFT_UP = 1 << 4
    LEFT_DOWN  = 1 << 5
    RIGHT_UP  = 1 << 6
    RIGHT_DOWN = 1 << 7

    ANY_ORTHOGONAL = UP | DOWN | RIGHT | LEFT
    ANY_DIAGONAL = LEFT_UP | LEFT_DOWN | RIGHT_UP | RIGHT_DOWN
    ANY = ANY_ORTHOGONAL | ANY_DIAGONAL

    _TO_VEC2 = {
        NONE:       Vec2(0, 0),
        UP:         Vec2(0, -1),
        DOWN:       Vec2(0, 1),
        LEFT:       Vec2(-1, 0),
        RIGHT:      Vec2(1, 0),
        LEFT_UP:    Vec2(-1, -1),
        LEFT_DOWN:  Vec2(-1, 1),
        RIGHT_UP:   Vec2(1, -1),
        RIGHT_DOWN: Vec2(1, 1),
    }


    @staticmethod
    def is_orthogonal(direction):
        return ANY_ORTHOGONAL | direction == ANY_ORTHOGONAL


    @staticmethod
    def is_diagonal(direction):
        return ANY_DIAGONAL | direction == ANY_DIAGONAL


    @staticmethod
    def as_vector(direction):
        Direction._DIRECTION_VECTOR_DICT.get(direction, Direction.NONE)

    ORTHOGONAL_VECTOR_LIST = [_TO_VEC2.get(UP), _TO_VEC2.get(DOWN), _TO_VEC2.get(LEFT), _TO_VEC2.get(RIGHT)]
    DIAGONAL_VECTOR_LIST = [_TO_VEC2.get(LEFT_UP), _TO_VEC2.get(LEFT_DOWN), _TO_VEC2.get(RIGHT_UP), _TO_VEC2.get(RIGHT_DOWN)]
    ALL_VECTOR_LIST = ORTHOGONAL_VECTOR_LIST + DIAGONAL_VECTOR_LIST

    @staticmethod
    def as_vector_list(directions):
        if Direction.ANY == directions:
            return Direction.ALL_VECTOR_LIST
        elif Direction.ANY_ORTHOGONAL == directions:
            return Direction.ORTHOGONAL_VECTOR_LIST
        elif Direction.ANY_DIAGONAL == directions:
            return Direction.DIAGONAL_VECTOR_LIST
        else:
            vector_list = []
            while directions > 0:
                current_bit = 0
                if directions & 1:
                    vector_list.append(as_vector(1 << current_bit))

                directions >>= 1
                current_bit += 1

            return vector_list


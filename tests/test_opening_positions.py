from model.opening import Opening
from utils.constants import OPENING_BASE_POSITION, OPENING_INCREMENT

def test_opening_positions():
    pos1 = OPENING_BASE_POSITION
    pos2 = OPENING_BASE_POSITION + OPENING_INCREMENT

    o1 = Opening(1, 1, pos1)
    o2 = Opening(2, 1, pos2)

    assert o2.absolutePosition - o1.absolutePosition == OPENING_INCREMENT
from levels.data import xp_list


def current_level(xp):
    for min_xp, level in xp_list:
        if min_xp > xp:
            return level

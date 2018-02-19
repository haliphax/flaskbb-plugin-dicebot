'Entry point for flaskbb-plugin-dicebot'

# stdlib
from os.path import dirname, join
from random import seed, randint
import re
# 3rd party
from flask_babelplus import gettext as _
from flask_login import current_user
from flaskbb.user.models import User
from flaskbb.utils.helpers import real
from flaskbb.utils.markup import markdown
from sqlalchemy import text

MODE_SIDES = 0
MODE_NUM = 1
MODE_MOD = 2

def flaskbb_load_migrations():
    return join(dirname(__file__), 'migrations')


def flaskbb_evt_after_post(post, is_new):
    'After-post hook'

    if not is_new:
        return

    if not post.content.lstrip().startswith('/roll '):
        return

    seed()
    rollstr = post.content.replace('/roll', '').replace(' ', '')
    total = 0
    pos = 0
    die_num = '0'
    die_sides = '0'
    die_mod = '0'
    mode = MODE_NUM
    neg = False

    for pos in range(len(rollstr)):
        char = rollstr[pos]

        if char.isdigit():
            if mode == MODE_SIDES:
                die_sides += char
            elif mode == MODE_NUM:
                die_num += char
            elif mode == MODE_MOD:
                die_mod += char
        elif char.lower() == 'd':
            mode = MODE_SIDES
        elif char in '+-':

            if pos > 0 and mode != MODE_NUM:
                if mode == MODE_NUM:
                    mode = MODE_SIDES
                elif mode == MODE_SIDES:
                    mode = MODE_MOD

                num = int(die_num)
                sides = int(die_sides)
                roll = 0

                if sides > 0:
                    if num == 0:
                        num = 1

                    roll = _roll_dice(num, sides)
                else:
                    roll = int(die_mod)

                roll *= (-1 if neg else 1)
                total += roll
                die_num = '0'
                die_sides = '0'
                die_mod = '0'
            if char == '+':
                neg = False
            else:
                neg = True


    num = int(die_num)
    sides = int(die_sides)
    roll = 0

    if sides > 0:
        if num == 0:
            num = 1

        roll = _roll_dice(num, sides)
    else:
        roll = int(die_mod)

    roll *= (-1 if neg else 1)
    total += roll
    post.content = (':game_die: {username}\n{rollstr} = **{total}**'
        .format(username=post.user.username, rollstr=rollstr, total=total))
    post.user = User.query.filter_by(username='Bot').one()
    post.save()


def _roll_dice(num, sides):
    roll = 0

    for i in range(num):
        roll += randint(1, sides)

    return roll

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


def flaskbb_event_post_save_after(post, is_new):
    'After-post hook'

    if not is_new:
        return

    if not post.content.lstrip().startswith('/roll '):
        return

    seed()
    rollobj = re.match(r'^\s*/roll ([-+d0-9]+) ?(.*)', post.content)
    total = 0
    pos = 0
    die_num = u'0'
    die_sides = u'0'
    die_mod = u'0'
    mode = MODE_NUM
    neg = False
    rollstr = rollobj.group(1)
    rolldesc = rollobj.group(2)

    for pos in range(len(rollstr)):
        char = rollstr[pos]

        if char.isdigit():
            if mode == MODE_SIDES:
                die_sides += char
            elif mode == MODE_NUM:
                die_num += char
            elif mode == MODE_MOD:
                die_mod += char
        elif char.lower() == u'd':
            mode = MODE_SIDES
        elif char in u'+-':

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
                die_num = u'0'
                die_sides = u'0'
                die_mod = u'0'
            if char == u'+':
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
    rolldesc = ' _{rolldesc}_' if len(rolldesc) > 0 else ''
    post.content = (
        u'`{username}`\n\U0001f3b2 {rollstr}{rolldesc} = **{total}**'
        .format(username=post.user.username, rollstr=rollstr,
                rolldesc=rolldesc, total=total)
    post.user = User.query.filter_by(username=u'Bot').one()
    post.save()


def _roll_dice(num, sides):
    roll = 0

    for i in range(num):
        roll += randint(1, sides)

    return roll

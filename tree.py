#
# tree.py
# author: Michael Curley
#

from os import listdir, path

# ----- globals (constants) ----------------------------------------------------

INDENT = 1
BAR_CORNER = '\\'
BAR_VERTICAL = '|'
BAR_HORIZONTAL = '_'

FULL_SPACE = ' ' * (INDENT + 2)
FULL_BAR = BAR_HORIZONTAL * INDENT + ' '
BAR_SPACE = BAR_VERTICAL + FULL_SPACE[1:]

DIR_TOKEN = '/'
DIR_COLOR = '\033[94m'
ERR_COLOR = '\033[91m'
RESET_COLOR = '\033[0m'


# ----- tree -------------------------------------------------------------------

def tree(cur_dir: str, spacers: list) -> None:
    global BAR_CORNER, BAR_VERTICAL, FULL_SPACE, BAR_SPACE, FULL_BAR,\
            DIR_TOKEN, DIR_COLOR, ERR_COLOR, RESET_COLOR
    if cur_dir == '.':
        print(cur_dir)
    space = ''.join(spacers)
    try:
        nodes = sorted(listdir(cur_dir), key = lambda x: (path.isdir(x), x))
    except PermissionError as e:
        print(f'{space}{ERR_COLOR}{cur_dir} permission denied:{e}{RESET_COLOR}')
        return
    count = len(nodes)
    for i in range(count):
        node = nodes[i]
        full = f'{cur_dir}/{node}'
        last = i == count - 1
        cvbar = BAR_CORNER if last else BAR_VERTICAL
        isdir = path.isdir(full)
        color = DIR_COLOR if isdir else RESET_COLOR
        token = DIR_TOKEN if isdir else ''
        print(f'{space}{cvbar}{FULL_BAR}{color}{node}{RESET_COLOR}{token}')
        if isdir:
            tree(full, spacers + [FULL_SPACE if last else BAR_SPACE])



# ----- exe entry --------------------------------------------------------------

if __name__ == '__main__':
    tree('.', list())


# ----- end of file ------------------------------------------------------------






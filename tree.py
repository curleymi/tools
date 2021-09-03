#
# tree.py
# author: Michael Curley
#

from os import access, listdir, path, X_OK

# ----- globals (constants) ----------------------------------------------------

BAR_CORNER = '└' # '\\'
BAR_VERTICAL = '│' # '|'
BAR_EDGE = '├' # BAR_VERTICAL
BAR_HORIZONTAL = '─' # '_'
DIR_TOKEN = '/'

RESET_COLOR = '\033[0m'
BAR_COLOR = RESET_COLOR 
DIR_COLOR = '\033[94m'
EXE_COLOR = '\033[92m'
ZIP_COLOR = '\033[91m'
PIC_COLOR = '\033[95m'
ERR_COLOR = '\033[91m'

# ----- text -------------------------------------------------------------------

def full_space(indent: int) -> str:
    return ' ' * (indent + 2)

def full_bar(indent: int) -> str:
    global BAR_HORIZONTAL
    return BAR_HORIZONTAL * indent + ' '

def bar_space(indent: int) -> str:
    global BAR_VERTICAL
    return BAR_VERTICAL + full_space(indent)[1:]

# ----- colored text -----------------------------------------------------------

def colored(color: str, string: str) -> str:
    global RESET_COLOR
    return f'{color}{string}{RESET_COLOR}'

def bar_str(bar: str) -> str:
    global BAR_COLOR
    return colored(BAR_COLOR, bar)

def dir_str(name: str) -> str:
    global DIR_COLOR
    return colored(DIR_COLOR, name)

def err_str(error: str) -> str:
    global ERR_COLOR
    return colored(ERR_COLOR, error)

# ----- tree -------------------------------------------------------------------

def tree(cur_dir: str = '.', space: str = '',
         dirs: int = 0, files: int = 0,
         indent: int = None) -> (int, int):
    global BAR_CORNER, BAR_VERTICAL, BAR_EDGE, DIR_TOKEN, RESET_COLOR,\
            DIR_COLOR, EXE_COLOR, ZIP_COLOR, PIC_COLOR, ERR_COLOR
    indent = indent or 0
    base = cur_dir == '.'
    if base:
        print(dir_str(cur_dir))
    try:
        nodes = sorted([x for x in listdir(cur_dir) if x[0] != '.'],
                key = lambda x: (x.lower(), path.isdir(x)))
    except PermissionError as e:
        print(err_str(f'{space}{cur_dir} permission denied:{e}'))
        return
    count = len(nodes)
    for i in range(count):
        node = nodes[i]
        if node[0] == '.':
            continue
        full = f'{cur_dir}/{node}'
        last = i == count - 1
        cvbar = BAR_CORNER if last else BAR_EDGE
        isdir = path.isdir(full)
        if isdir:
            color = DIR_COLOR
        elif access(full, X_OK):
            color = EXE_COLOR
        elif any(full.endswith(x)  for x in ['.zip', '.tar', '.tar.gz']):
            color = ZIP_COLOR
        elif any(full.endswith(x)  for x in ['.bmp', '.png', '.jpeg']):
            color = PIC_COLOR
        else:
            color = RESET_COLOR
        token = DIR_TOKEN if isdir else ''
        bar = bar_str(cvbar + full_bar(indent))
        print(f'{space}{bar}{colored(color, node)}{token}')
        if isdir:
            dirs, files = tree(full, space + (full_space(indent) if last\
                    else bar_space(indent)), dirs + 1, files, indent)
        else:
            files += 1
    if base:
        print(f'\n{dirs} {"directory" if dirs == 1 else "directories"}, '\
                f'{files} {"file" if files == 1 else "files"}')
    return dirs, files

# ----- exe entry --------------------------------------------------------------

if __name__ == '__main__':
    from sys import argv
    try:
        tree(indent = int(argv[1]))
    except:
        tree()

# ----- end of file ------------------------------------------------------------



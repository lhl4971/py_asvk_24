import argparse
import random
import re
from dataclasses import dataclass
from os import PathLike
from pathlib import Path, PurePath
from textwrap import wrap
from typing import TextIO, Union, Dict, List
from unicodedata import east_asian_width

HEREDOC_PATTERN = re.compile(
    r'\$.* = <<["\']?(.*)["\']?;?(?P<the_cow>[\w\W]*)\1'
)


@dataclass
class Option:
    eyes: str = 'oo'
    tongue: str = '  '


COW_PEN = (Path(__file__) / '..' / 'cows').resolve()

COW_OPTIONS = {
    'b': Option(eyes='=='),
    'd': Option(eyes='XX', tongue='U '),
    'g': Option(eyes='$$'),
    'p': Option(eyes='@@'),
    's': Option(eyes='**', tongue='U '),
    't': Option(eyes='--'),
    'w': Option(eyes='OO'),
    'y': Option(eyes='..'),
}


@dataclass
class Bubble:
    stem: str = '\\'
    l: str = '<'
    r: str = '>'
    tl: str = '/'
    tr: str = '\\'
    ml: str = '|'
    mr: str = '|'
    bl: str = '\\'
    br: str = '/'


THOUGHT_OPTIONS = {
    'cowsay': Bubble('\\', '<', '>', '/', '\\', '|', '|', '\\', '/'),
    'cowthink': Bubble('o', '(', ')', '(', ')', '(', ')', '(', ')'),
}

ESCAPES = {
    r'\@': '@',
    r'\$': '$',
    r'\\': '\\',
}


def read_dot_cow(f: TextIO, escapes: Dict[str, str] = None) -> str:
    """
    Reads and parses a .cow file to a string. Unescapes characters in doing
    so. This function will search for a heredoc in the .cow file. If found,
    it will extract the cow in the heredoc, otherwise the whole file is used.

    :param f: The File to read from
    :param escapes: A dictionary mapping escape codes to their respective
        characters
    :return: The cow
    """
    if escapes is None:
        escapes = ESCAPES
    the_cow = f.read()
    match = HEREDOC_PATTERN.search(the_cow)
    if match is not None:
        the_cow = match.group('the_cow')
    for escape, replacement in escapes.items():
        the_cow = the_cow.replace(escape, replacement)
    return the_cow.strip('\r\n')


def list_cows(cow_path: Union[str, PathLike] = COW_PEN):
    """Lists all cow file names in the given directory"""
    cows = Path(cow_path).glob('*.cow')
    return [cow.stem for cow in cows]


def get_random_cow(path: Union[str, PathLike] = COW_PEN) -> str:
    """
    Searches the given dir for all .cow files and returns the name of a
    random one
    """
    cows = list_cows(path)
    return random.choice(cows)


def get_cow(cow, cow_path=COW_PEN):
    """
    Retrieves the cowfile text from the cowfile with the corresponding cow name
    """
    file = PurePath(cow_path) / f'{cow}.cow'
    with open(file) as f:
        the_cow = read_dot_cow(f)
    return the_cow


def build_cow(message: str,
              the_cow: str,
              cow_config: Option,
              thought_config: Bubble,
              width: int,
              wrap_text: bool) -> str:
    """
    Takes a string representing a cow and adds the message bubble, thoughts,
    eyes, and tongue. $thoughts, $eyes, $tongue if present will be replaced
    with their corresponding strings.

    :param the_cow: A string representing a cow. Characters are not escaped
    :param cow_config: An Option object defining the eyes, thoughts, and tongue
    :param thought_config: A thought option defining the text bubble chars
    :return: The formatted cow
    """
    the_cow = the_cow.replace('$eyes', cow_config.eyes)
    the_cow = the_cow.replace('$thoughts', thought_config.stem)
    the_cow = the_cow.replace('$tongue', cow_config.tongue)
    message = make_bubble(
        message,
        brackets=thought_config,
        width=width,
        wrap_text=wrap_text,
    )
    return '\n'.join((message, the_cow))


def fit_text(text: str,
             width: int,
             wrap_text: bool = True) -> List[str]:
    """
    Wraps each paragraph in the given text to the specified width and pads
    each line such that they are all the same length with at least one space
    of padding. If wrap_text is False, paragraphs are not wrapped but are
    still padded with spaces.
    """
    text = text.replace('\t', ' ' * 4)
    if not wrap_text:
        lines = text.splitlines()
    else:
        lines = []
        paragraphs = re.split(r'(?:\r\n?|\n)\s+', text)
        for i in range(len(paragraphs)):
            lines += wrap(paragraphs[i], width=width) or ' '
            lines.append('')
        lines.pop()
    return pad_lines(lines)


def pad_lines(lines):
    max_width = max(len(line) for line in lines)
    return [f' {line:<{max_width}} ' for line in lines]


def wrap_bubble(lines: List[str], ops: Bubble) -> str:
    """
    Puts text into a text bubble. This is done by just inserting the given
    bracket characters onto the ends of each line.
    """
    res = [*f' {"_" * len(lines[0])} \n']
    if len(lines) == 1:
        res += f'{ops.l}{lines[0]}{ops.r}\n'
    else:
        res += f'{ops.tl}{lines[0]}{ops.tr}\n'
        for line in lines[1:-1]:
            res += f'{ops.ml}{line}{ops.mr}\n'
        res += f'{ops.bl}{lines[-1]}{ops.br}\n'
    res += f' {"-" * len(lines[0])} '
    return ''.join(res)


def make_bubble(text,
                brackets=THOUGHT_OPTIONS['cowsay'],
                width=40,
                wrap_text=True):
    """
    Wraps text is wrap_text is true, then pads text and sets inside a bubble.
    This is the text that appears above the cows
    """
    lines = fit_text(text, width, wrap_text)
    return normalise_width(wrap_bubble(lines, brackets))


def to_full_width(string):
    """Converts non-full-width characters to full-width"""
    # From: https://stackoverflow.com/a/4632373/18307756
    neutral_width = "".join(chr(i) for i in range(ord(" "), ord("~")))
    full_width = (
            "\u3000"  # Full-Width Space
            + "".join(chr(i) for i in range(ord("！"), ord("～")))
    )
    full = str.maketrans(neutral_width, full_width)
    return string.translate(full)


def normalise_width(cow):
    """
    If any full-width characters are found, convert all characters to full width
    """
    if any(east_asian_width(c) in ("W", "F", "A") for c in cow):
        return to_full_width(cow)
    return cow


def cowsay(message: str,
           cow: str = 'default',
           preset: str = None,
           eyes: str = Option.eyes,
           tongue: str = Option.tongue,
           width: int = 40,
           wrap_text: bool = True,
           cowfile: str = None) -> str:
    """
    Similar to the cowsay command. Parameters are listed with their
    corresponding options in the cowsay command. Returns the resulting cowsay
    string

    :param message: The message to be displayed
    :param cow: -f – the available cows can be found by calling list_cows
    :param preset: -[bdgpstwy]
    :param eyes: -e or eye_string
    :param tongue: -T or tongue_string
    :param width: -W
    :param wrap_text: -n
    :param cowfile: a string containing the cow file text (chars are not
    decoded as they are in read_dot_cow) if this parameter is provided the
    cow parameter is ignored
    """
    the_cow = get_cow(cow) if cowfile is None else cowfile
    cow_ops = COW_OPTIONS.get(preset, Option(eyes=eyes, tongue=tongue))
    thought_ops = THOUGHT_OPTIONS['cowsay']
    return build_cow(message, the_cow, cow_ops, thought_ops, width, wrap_text)


parser = argparse.ArgumentParser(
    prog = 'cow_say',
    description = 'This program works similarly python-cowsay',
    epilog = 'Similar to the cowsay command. Parameters are listed. Prints the resulting cowsay string'
)

parser.add_argument('message', help='The message to be displayed')
parser.add_argument('-f', metavar='cow', help='The available cows can be found by paramater -l', default='default')
parser.add_argument('-m', metavar='preset', choices=[None, 'b', 'd', 'g', 'p', 's', 't', 'w', 'y'], default=None, help='Presets of eyes and tongue')
parser.add_argument('-e', metavar='eyes', default=Option.eyes, help='Custom eyes string')
parser.add_argument('-T', metavar='tongue', default=Option.tongue, help='Custom tougue string')
parser.add_argument('-W', type=int, metavar='width', default=40)
parser.add_argument('-n', type=bool, metavar='wrap_text', default=True)
parser.add_argument('-l', metavar='list_cows', action="extend", help='Lists all cow file names in the given directory')
parser.add_argument('-cf', metavar='cowfile', default=None, help='Custom cowfile path')

args = parser.parse_args()

if(args.l):
    print(list_cows(''.join(args.l)))
else:
    print(cowsay(args.message,args.f,args.m,args.e,args.T,args.W,args.n,args.cf))









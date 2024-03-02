import cowsay as cs
import random

def ask(prompt: str, valid: list[str] = None) -> str:
    cowname = random.choices(cs.list_cows())[0]
    word = input(cs.cowsay(prompt, cow=cowname))
    return word

def inform(format_string: str, bulls: int, cows: int) -> None:
    cowname = random.choices(cs.list_cows())[0]
    print(cs.cowsay(format_string.format(bulls, cows), cow=cowname))
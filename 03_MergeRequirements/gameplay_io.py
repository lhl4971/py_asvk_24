def ask(prompt: str, valid: list[str] = None) -> str:
    word = input(prompt)
    return word

def inform(format_string: str, bulls: int, cows: int) -> None:
    print(format_string.format(bulls, cows))
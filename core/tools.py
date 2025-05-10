import requests


def calculate_expression(expression: str) -> str:

    try:
        result = eval(expression)

        return f"The result is: {result}"
    
    except Exception as e: 
        
        return f"Couldn't calculate!!. Error {e}"


def define_word(word: str) -> str:

    try:
        url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
        res = requests.get(url=url)
        res.raise_for_status()
        data = res.json()

        definition = data[0]['meanings'][0]['definitions'][0]['definitions']

        return f"{word.capitalize()}: {definition}"
    
    except Exception:

        return f"Couldn't find the meaning for the word '{word}'."
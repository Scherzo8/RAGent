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

        res = requests.get(url, timeout=5)
        res.raise_for_status()
        data = res.json()

        if isinstance(data, list) and data[0].get("meanings"):
            defs = data[0]["meanings"][0]["definitions"]
            definition = defs[0]["definition"] if defs else "No definition found."
            return f"{word.capitalize()}: {definition}"

        return f"No structured definition found for '{word}'."
    
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Dictionary API request failed: {e}")
        return f"Couldn't reach the dictionary service right now."

    except Exception as e:
        print(f"Unexpected dictionary error: {e}")
        return f"Something went wrong while defining '{word}'."
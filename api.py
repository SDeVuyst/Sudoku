import requests


def get_puzzle():
    url = "https://sudoku-generator1.p.rapidapi.com/sudoku/generate"

    querystring = {}

    headers = {
        'x-rapidapi-host': "sudoku-generator1.p.rapidapi.com",
        'x-rapidapi-key': "9488e43fecmsh355fccfff10f9cep1208f7jsn69bbc54b6c3c"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    data = response.json()
    return(data)
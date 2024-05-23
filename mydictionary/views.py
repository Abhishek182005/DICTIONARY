from django.shortcuts import render
from PyDictionary import PyDictionary
from bs4 import BeautifulSoup
import requests

def homeView(request):
    return render(request, 'mydictionary/index.html')

def fetch_thesaurus_data(word, data_type):
    url = f"https://www.thesaurus.com/browse/{word}"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        if data_type == 'synonyms':
            synonyms_list = soup.find_all('a', {'class': 'css-1gyuw4i eh475bn0'})  # Updated selector
            return [synonym.text for synonym in synonyms_list]
        elif data_type == 'antonyms':
            antonyms_list = soup.find_all('a', {'class': 'css-15bafsg eh475bn1'})  # Updated selector
            return [antonym.text for antonym in antonyms_list]
    return []

def searchView(request):
    word = request.GET.get('search')
    if word:
        dictionary = PyDictionary()
        meanings = dictionary.meaning(word)
        synonyms = dictionary.synonym(word) or []
        antonyms = dictionary.antonym(word) or []

        thesaurus_synonyms = fetch_thesaurus_data(word, 'synonyms')
        thesaurus_antonyms = fetch_thesaurus_data(word, 'antonyms')

        # Debugging: Print fetched data
        print(f"Word: {word}")
        print(f"Meanings: {meanings}")
        print(f"Synonyms from PyDictionary: {synonyms}")
        print(f"Antonyms from PyDictionary: {antonyms}")
        print(f"Synonyms from Thesaurus.com: {thesaurus_synonyms}")
        print(f"Antonyms from Thesaurus.com: {thesaurus_antonyms}")

        context = {
            'word': word,
            'meanings': meanings,
            'synonyms': synonyms + thesaurus_synonyms,
            'antonyms': antonyms + thesaurus_antonyms
        }
    else:
        context = {
            'word': None,
            'meanings': None,
            'synonyms': None,
            'antonyms': None
        }

    return render(request, 'mydictionary/search.html', context)
import os, sys
import json
import requests
from bs4 import BeautifulSoup


def get_languages():
    # Read the JSON file
    with open('language-codes_json.json', 'r') as json_file:
        data = json.load(json_file)

    result = dict()
    for d in data:
        result[d['English']] = d['alpha2']

    common_lang = [
        'ar',
        'de',
        'es',
        'fr',
        'en',
        'it',
        'nl',
        'ja',
        'pl',
        'pt',
        'ko',
        'ru',
        'sv',
        'uk',
        'vi',
        'zh'
    ]

    result = {k: v for k, v in result.items() if v in common_lang}

    return result


def open_directory(path):
    if sys.platform.startswith('darwin'):  # macOS
        os.system('open "{}"'.format(path))
    elif sys.platform.startswith('win'):  # Windows
        os.system('start "" "{}"'.format(path))
    elif sys.platform.startswith('linux'):  # Linux
        os.system('xdg-open "{}"'.format(path))
    else:
        print("Unsupported operating system.")

def make_wiki_doc_url(wiki_lang, doc_name):
    wikipedia_doc_prefix = f'https://{wiki_lang}.wikipedia.org/wiki/'
    wikipedia_url = f'{wikipedia_doc_prefix}{doc_name}'
    return wikipedia_url


def wikidoc_to_txt(wiki_lang, doc_name, save_dir=None):
    try:
        if save_dir:
            pass
        else:
            save_dir = doc_name
            os.makedirs(save_dir, exist_ok=True)
        url = make_wiki_doc_url(wiki_lang=wiki_lang, doc_name=doc_name)
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            paragraphs = soup.find_all('p')
            content = "\n".join([paragraph.get_text() for paragraph in paragraphs])
            filename = f'{save_dir}/{doc_name}.txt'
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
        else:
            print("Failed to retrieve content from the website.")
            return None
    except Exception:
        raise Exception


def get_python_documentation_list(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        documentation_in_categories = []

        # Find the section with the documentation list
        sections = soup.find_all('div', {'id': 'mw-pages'})
        for section in sections:
            for li in section.find_all('li'):
                documentation_in_categories.append(li.get_text())
        return documentation_in_categories
    else:
        print("Failed to retrieve content from the website.")
        return None


class NoResultException(Exception):
    def __init__(self, message="No result found."):
        self.message = message
        super().__init__(self.message)


def wikicate_to_txt(wiki_lang, category, save_dir=None, max_len=None):
    try:
        save_dir = save_dir if save_dir else category
        wikipedia_doc_prefix = f'https://{wiki_lang}.wikipedia.org/wiki/'
        wikipedia_url = f'{wikipedia_doc_prefix}Category:{category}'

        documentation_list = get_python_documentation_list(wikipedia_url)

        if len(documentation_list) == 0:
            raise NoResultException

        max_len = max_len if max_len else len(documentation_list)

        os.makedirs(save_dir, exist_ok=True)

        for i in range(max_len):
            doc_name = documentation_list[i]
            wikidoc_to_txt(wiki_lang=wiki_lang, doc_name=doc_name, save_dir=save_dir)
    except Exception as e:
        print(e)

# IF YOU WANT TO USE THIS AS CUI, THEN YOU CAN USE LIKE BELOW:

# Get single document
# wikipedia_url = 'https://en.wikipedia.org/wiki/Python_(programming_language)'
# wikidoc_to_txt(wiki_lang='en', doc_name='Python_(programming_language)')


# wiki_lang = 'en'
# category = 'Python_(programming_language)'
# wikicate_to_txt(wiki_lang, category, save_dir='practice')

# pyqt-wikipedia-crawler
Crawling the Wikipedia with Python Desktop Application powered by BeautifulSoup4

This requires beautifulsoup4 and requests to use it as only CUI.

If you want to use this as GUI, you have to install PyQt5.

## Requirements
* requests
* beautifulsoup4
* PyQt5 >= 5.14

## How To Run
1. clone this repo
2. pip install -r requirements.txt
3. in the src folder, you can find the script.py which you can run it right away. You can find the sample code in the very bottom of the script.
4. 
5. If you want to use the GUI, run main.py as
```
python main.py
```

## Method Overview (CUI only)
```python
wikidoc_to_txt(wiki_lang, doc_name, save_dir=None) # download single document
wikicate_to_txt(wiki_lang, category, save_dir=None, max_len=None) # download every documents in certain category
```

Both methods are pretty self-explanatory.

You can download any document from the Wikipedia (no matter the language is) and you can get it in your local directory as text file.

There are two types of document you can download. One is single document and the other is category document.

The latter one, you can crawl every documents in that category. Each document will be saved as a separate text file.

## GUI Preview
![image](https://github.com/yjg30737/pyqt-wikipedia-crawler/assets/55078043/62481f73-8c4b-4b79-92ae-372e1c3305c5)


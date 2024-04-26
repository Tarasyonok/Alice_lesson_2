import requests
from flask import Flask, request, jsonify
import logging
import json
from googletrans import Translator, constants
translator = Translator()
app = Flask(__name__)

logging.basicConfig(level=logging.ERROR)

cities = {
    'москва': ['997614/39788b89f4000dfec536',
               '1030494/8c859295042551b8fb83'],
    'нью-йорк': ['1030494/64544a6824f53056736e',
                 '997614/55d064efd558f789e7f1'],
    'париж': ["1030494/bcdf373091d9728a5897",
              '213044/0bb800cc57553a488332']
}

sessionStorage = {}


@app.route('/post', methods=['POST'])
def main():
    logging.info('Request: %r', request.json)
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }
    handle_dialog(response, request.json)
    logging.info('Response: %r', response)
    return jsonify(response)


def handle_dialog(res, req):
    com = req["request"]["command"]
    print(com, 'переведите слово' in com.lower(), 'переведи слово' in com.lower())
    if 'переведите слово' in com.lower() or 'переведи слово' in com.lower():
        word = com.split()[-1]
        try:
            translation = translator.translate(word)
            print(translation)
            res['response']['text'] = translation.text
        except Exception as error:
            res['response']['text'] = str(error)
    else:
        res['response']['text'] = 'Я смогу перевести слово по этому запросу: Переведите (переведи) слово: *слово*'




if __name__ == '__main__':
    app.run()

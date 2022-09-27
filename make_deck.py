from translate import Translator
from google_images import ImageDownloader
from gtts import gTTS
import unidecode
import genanki
import os

LANG = 'fr'
RESUME = 133

my_model = genanki.Model(
    1607392329,
    'Simple Model',
    fields=[
        {'name': 'CardName'},
        {'name': 'Question'},
        {'name': 'Answer'},
        {'name': 'mp3'},
        {'name': 'image'}
    ],
    templates=[
        {
            'name': '{{CardName}}',
            'qfmt': '{{Question}}<br>{{image}}',
            'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}<br>{{mp3}}',
        },
    ])

# Go through the list of words.
with open('words.txt', 'r') as f:
    words = [w.strip() for w in f.readlines()]

# translate to chosen language
translator = Translator(to_lang=LANG, from_lang='en')
adj_helper = translator.translate('apple')

id = ImageDownloader()

my_notes = []

for i, word in enumerate(words):
    if i < RESUME:
        continue

    print(f'{i}/{len(words)} - {word}')

    original_word = word
    grammar_group = 'noun'

    try:
        if '(' in word:
            idx = word.find('(')

            if 'adjective' in word:
                grammar_group = 'adjective'
            elif 'verb' in word:
                grammar_group = 'verb'

            word = word[:idx]

        match grammar_group:
            case 'noun':
                translation = translator.translate(word)
            case 'adjective':
                translation = translator.translate(word + 'apple')
                t1, t2 = translation.split()
                if t1 != adj_helper:
                    translation = t1
                else:
                    translation = t2
            case 'verb':
                translation = translator.translate('to ' + word)

        # search for pictures using the given word and save it as {word}.png
        id.get_images(word)

        # mp3 file from word
        tts = gTTS(translation, lang=LANG)
        unaccented_word = unidecode.unidecode(word)
        tts.save(f'mp3s/{unaccented_word}.mp3')

        my_note = genanki.Note(
            model=my_model,
            fields=[unaccented_word, original_word, translation, f'[sound:{unaccented_word}.mp3]', f'<img src="{unaccented_word}.png">'])
        my_notes.append(my_note)
    except Exception as e:
        print(f'failed {original_word}', e)

# generate anki deck
my_deck = genanki.Deck(
    2059400110,
    f'{LANG} 625 words')

for note in my_notes:
    my_deck.add_note(note)
my_package = genanki.Package(my_deck)
media_files = ['images/' + img for img in os.listdir('images')] + ['mp3s/' + img for img in os.listdir('mp3s')]
my_package.media_files = media_files
my_package.write_to_file('output.apkg')
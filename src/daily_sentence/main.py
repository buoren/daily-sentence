from nicegui import ui
from daily_sentence.pages.index import main_page
import os

port = os.environ.get('PORT', 8080)

main_page()
ui.run(host='0.0.0.0', port=int(port), title='Daily Sentence')

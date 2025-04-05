from nicegui import ui, app, APIRouter
from daily_sentence.pages import index
import os

port = os.environ.get('PORT', 8080)

ui.run(host='0.0.0.0', port=int(port), title='Daily Sentence')

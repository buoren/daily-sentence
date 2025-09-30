from nicegui import ui
from daily_sentence.pages import create_app
import os

# Configure the page
@ui.page('/')
def main_page():
    ui.add_head_html('<link href="https://unpkg.com/eva-icons@1.1.3/style/eva-icons.css" rel="stylesheet" />')
    ui.query('body').classes('bg-sky-100 m-0 p-0')  # Light blue background for the whole page

    # Create and render the app
    app = create_app()
    app.render()

# Run the application
port = os.environ.get('PORT', 8080)
ui.run(host='0.0.0.0', port=int(port), title='Daily Sentence')

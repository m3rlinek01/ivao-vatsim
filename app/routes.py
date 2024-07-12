from app import app
from app.services.map_service import create_map
from flask import render_template_string

@app.route('/')
def map_page():
    m = create_map()
    return m.get_root().render()
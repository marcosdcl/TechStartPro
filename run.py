import csv
from app import create_app, init_db


app = create_app(config_filename='./settings.py')
init_db(app)
app.run(debug=True, use_reloader=True)

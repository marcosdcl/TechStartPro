from app import app
from views import init_db

init_db()
app.run(debug=True, use_reloader=True)

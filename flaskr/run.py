from app import create_app
from flask import render_template

config_name = os.getenv('APP_SETTINGS')
app = create_app(config_name)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")

if __name__ == '__main__':
    app.run()

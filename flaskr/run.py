from app import create_app, db, apply_views_and_security
from flask_security import login_required
from flask import render_template

config_name = 'development'
app = create_app(config_name)
apply_views_and_security(app)

with app.app_context():
    db.create_all()


@app.route('/', defaults={'path': ''})
#@app.route('/<path:path>')
@login_required
def catch_all(path):
    return render_template("index.html")

if __name__ == '__main__':
    app.run()

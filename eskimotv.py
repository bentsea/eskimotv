import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


import sys
if os.environ.get('FLASK_CONFIG') == "production":
    paths=["/home/eskimotv/public_html/"]
    for path in paths:
        if path not in sys.path:
            sys.path.append(path)
from app import create_app,db
from flask_login import current_user
from app.models import User,Role,Permission,CreativeWork,Article,ArticleType,Tags,Person
from flask_migrate import Migrate,upgrade
from datetime import datetime


app = create_app(os.environ.get('FLASK_CONFIG') or 'default')
migrate = Migrate(app,db,render_as_batch=True)

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role, Permission=Permission, CreativeWork=CreativeWork, Article=Article,ArticleType=ArticleType,Tags=Tags,Person=Person)

@app.context_processor
def inject_now():
    return {'now':datetime.utcnow()}

@app.cli.command()
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

@app.cli.command()
def deploy():
    """Run deployment tasks."""
    # migrate database to latest revision
    upgrade()

    # create or update user roles
    Role.insert_roles()

if __name__ == "__main__":
    app.run()

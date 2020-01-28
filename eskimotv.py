import os
from app import create_app,db
from app.models import User,Role,Permission,CreativeWork,Article
from flask_migrate import Migrate
from datetime import datetime

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app,db)

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role, Permission=Permission, CreativeWork=CreativeWork, Article=Article)

@app.context_processor
def inject_now():
    return {'now':datetime.utcnow()}

@app.cli.command()
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

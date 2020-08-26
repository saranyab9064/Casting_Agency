from app import APP
from models import db
from flask_migrate import Migrate
from flask_migrate import MigrateCommand
from flask_script import Manager




migrate = Migrate(APP, db)
manager = Manager(APP)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()

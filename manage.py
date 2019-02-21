from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flaskwebapp import create_app, db


app = create_app()
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flaskwebapp/site.db'

migrate = Migrate(app, db, render_as_batch=True)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()

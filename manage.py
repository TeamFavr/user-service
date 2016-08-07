from flask_script import Manager

from app import app

manager = Manager(app)

@manager.command
def run():
    app.run(host="0.0.0.0", port=5000)

if __name__ == "__main__":
    manager.run()
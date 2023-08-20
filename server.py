from flask_app import app
<<<<<<< Updated upstream
from flask_app.controllers import maps
from flask_app.controllers import map, user
=======
from flask_app.controllers import maps, user
>>>>>>> Stashed changes


if __name__ == '__main__':
    app.run(debug=True, host ="localhost", port="8000")
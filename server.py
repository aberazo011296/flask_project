from flask_app import app

from flask_app.controllers import users
from flask_app.controllers import eventos
from flask_app.controllers import banda
from flask_app.controllers import solicitudes
from flask_app.controllers import solicitudes_banda


if __name__=="__main__":
    app.run(debug=True)
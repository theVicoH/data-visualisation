from flask import Flask
from flasgger import Swagger
from src.routes import passengers, holidays, holidays_and_passengers

app = Flask(__name__)
swagger = Swagger(app)

app.register_blueprint(passengers.passengers_bp)
app.register_blueprint(holidays.holidays_bp)
app.register_blueprint(holidays_and_passengers.holidays_and_passengers_bp)

if __name__ == "__main__":
    app.run(debug=True)

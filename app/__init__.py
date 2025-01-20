from flask import Flask
from app.models import db

"""
     Initialises the application and sets the configuration
"""


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)

    from .routes import main
    app.register_blueprint(main)

    with app.app_context():
        from .models.country import Country
        from .models.weather_data import WeatherData

        db.create_all()
        initialize_countries()

    return app


"""
    Inicjalizacja skróconych nazw krajów na początku aplikacji jeżeli takowe nie występują w aplikacji
"""


def initialize_countries():
    from .models.country import Country
    from .data.country_data import countries

    if Country.query.count() == 0:
        for country in countries:
            new_country = Country(full_name=country['full_name'], short_name=country['short_name'])
            db.session.add(new_country)
        db.session.commit()

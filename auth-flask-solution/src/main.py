from api.v1.routes import api_v1
from core.app_factory import create_app
from db.db_factory import create_db

settings_filename = 'core.settings.DevSettings'
app = create_app(settings_filename)

create_db(app)

app.register_blueprint(api_v1)

if __name__ == '__main__':
    app.run()

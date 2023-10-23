import os 

from flask import Flask, render_template

#Se invoca a los módulos a usar

#FABRICA DE APLICACIONES (Despega todo)

def create_app(test_config = None):
    #Configuración de la app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY= 'dev',
        DATABASE= os.path.join(app.instance_path, 'biblioteca.sqlite'),
    )
    #Se importan las diferentes funciones como la database
    
    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    if test_config is None:
        #Si existe la función se debe de cargar aunque no se este probando
        app.config.from_pyfile("config.py", silent=True)
    else:
        #Si pasa, se carga la configuración
        app.config.from_mapping(test_config)
    
    #Comprobar que la carpeta exista
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    #Se regresa la vista
    @app.route('/')
    def index():
        return render_template('auth/index.html')
    
    @app.route('/auth/register')
    def register():
        return render_template('/auth/index.html')
    
    return app

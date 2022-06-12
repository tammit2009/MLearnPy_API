from flask import Flask, jsonify, redirect, render_template, request
import os
from flask_jwt_extended import JWTManager

from dotenv import load_dotenv
load_dotenv('.env')         # the path to your .env file
load_dotenv('.flaskenv')    # the path to your .flaskenv file

from src.libs.auth import auth
from src.libs.bookmarks import bookmarks
from src.libs.mlearn import mlearn
from src.libs.posts import posts_register
from src.libs.database import Bookmark, db, BlogPost
from src.constants.http_status_codes import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR

def create_app(test_config = None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_mapping( 
            SECRET_KEY=os.environ.get("SECRET_KEY"),
            SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCHEMY_DATABASE_URI"),
            SQLALCHEMY_TRACK_MODIFICATIONS = False, 
            JWT_SECRET_KEY=os.environ.get("JWT_SECRET_KEY"), 
        )
    else:
        app.config.from_mapping(test_config)

    # For sqlalchemy sqlite db initialization
    db.app=app
    db.init_app(app)

    # JWT
    JWTManager(app)

    # Route defs

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.get("/<string:short_url>")
    def redirect_to_url(short_url):
        bookmark = Bookmark.query.filter_by(short_url=short_url).first_or_404()
        if bookmark:
            bookmark.visits = bookmark.visits + 1
            db.session.commit()
        return redirect(bookmark.url) 

    # Define routes using Blueprints instead of here
    app.register_blueprint(auth)
    app.register_blueprint(bookmarks)
    app.register_blueprint(mlearn)
    posts_register(app)  # app.register_blueprint(posts)

    # Error Handlers (flask uses recognized http error codes)
    @app.errorhandler(HTTP_404_NOT_FOUND)  
    def handle_404(e):
        return jsonify({ "error": "Not found"}), HTTP_404_NOT_FOUND

    @app.errorhandler(HTTP_500_INTERNAL_SERVER_ERROR)
    def handle_500(e):
        return jsonify({ "error": "Something went wrong. Please try again..."}), HTTP_500_INTERNAL_SERVER_ERROR

    return app 

if __name__ == "__main__":
    app = create_app()
    app.run()

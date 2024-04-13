from flask import Flask, make_response, jsonify, session
from flask_migrate import Migrate
from math import ceil
from datetime import datetime

from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/clear')
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200

@app.route('/articles')
def index_articles():
    # This route can be implemented to return a list of articles if needed.
    pass

@app.route('/articles/<int:id>')
def show_article(id):
    # Get the current number of page views for the user
    page_views = session.get('page_views', 0)

    # Increment the page views for the user
    session['page_views'] = page_views + 1

    # Check if the user has exceeded the maximum page views
    if page_views >= 3:
        # Return a JSON response with an error message and status code 401
        return jsonify({'message': 'Maximum pageview limit reached'}), 401
    else:
        # Fetch the article directly from the database
        article = Article.query.get_or_404(id)
        # Create a preview of the content (truncate to 100 characters)
        preview = article.content[:100]
        # Calculate an estimate for the minutes to read the article
        # Assuming an average reading speed of 200 words per minute
        words_per_minute = 200
        words_count = len(article.content.split())
        minutes_to_read = ceil(words_count / words_per_minute)
        # Format the publication date
        publication_date = article.date.strftime('%Y-%m-%d')
        # Return a JSON response with the article data, preview, minutes to read, and publication date
        return jsonify({
            'id': article.id,
            'title': article.title,
            'author': article.author,
            'content': article.content,
            'preview': preview,
            'minutes_to_read': minutes_to_read,
            'date': publication_date
        }), 200
    
if __name__ == '__main__':
    app.run(port=5555)

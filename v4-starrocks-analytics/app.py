from flask import Flask
from app.api.ingest import bp as ingest_bp
from app.api.query import bp as query_bp

app = Flask(__name__)
app.register_blueprint(ingest_bp)
app.register_blueprint(query_bp)

if __name__ == "__main__":
    app.run(port=8003)

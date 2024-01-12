from flask import Flask, request , render_template_string
from flask_caching import Cache

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})









if __name__ == "__main__":
    cache.cache.set("s","123")

    print(cache.cache.get("s"))
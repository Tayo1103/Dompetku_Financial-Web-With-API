from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from config import Config
from models import db
from schemas import ma
from resources import ExpenseListResource, ExpenseResource, SummaryResource

app = Flask(__name__)
app.config.from_object(Config)

CORS(app, resources={r"/*": {"origins": "*"}})

db.init_app(app)
ma.init_app(app)
api = Api(app)

api.add_resource(ExpenseListResource, '/expenses')
api.add_resource(ExpenseResource, '/expenses/<int:expense_id>')
api.add_resource(SummaryResource, '/summary')

@app.before_request
def create_tables():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)

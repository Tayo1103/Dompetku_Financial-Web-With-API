from flask_marshmallow import Marshmallow
from models import Expense

ma = Marshmallow()

class ExpenseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Expense
        load_instance = True

    id = ma.auto_field(dump_only=True)
    title = ma.auto_field(required=True)
    amount = ma.auto_field(required=True)
    date = ma.auto_field(required=True)
    type = ma.auto_field(required=True)

expense_schema = ExpenseSchema()
expenses_schema = ExpenseSchema(many=True)

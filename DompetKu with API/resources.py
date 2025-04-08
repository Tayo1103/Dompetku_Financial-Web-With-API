from flask_restful import Resource, request
from models import Expense, db
from schemas import expense_schema, expenses_schema
from http import HTTPStatus
from marshmallow import ValidationError

class ExpenseListResource(Resource):
    def get(self):
        expenses = Expense.query.all()
        return expenses_schema.dump(expenses), HTTPStatus.OK

    def post(self):
        data = request.get_json()
        try:
            expense = expense_schema.load(data)
            db.session.add(expense)
            db.session.commit()
            return expense_schema.dump(expense), HTTPStatus.CREATED
        except ValidationError as err:
            return {'message': err.messages}, HTTPStatus.BAD_REQUEST
        except Exception as e:
            db.session.rollback()
            return {'message': str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR

class ExpenseResource(Resource):
    def get(self, expense_id):
        expense = Expense.query.get_or_404(expense_id)
        return expense_schema.dump(expense), HTTPStatus.OK

    def put(self, expense_id):
        data = request.get_json()
        try:
            expense = Expense.query.get_or_404(expense_id)
            expense = expense_schema.load(data, instance=expense, partial=True)
            db.session.commit()
            return expense_schema.dump(expense), HTTPStatus.OK
        except ValidationError as err:
            return {'message': err.messages}, HTTPStatus.BAD_REQUEST
        except Exception as e:
            db.session.rollback()
            return {'message': str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR

    def delete(self, expense_id):
        try:
            expense = Expense.query.get_or_404(expense_id)
            db.session.delete(expense)
            db.session.commit()
            return {'message': 'Catatan dihapus'}, HTTPStatus.OK
        except Exception as e:
            db.session.rollback()
            return {'message': str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR

class SummaryResource(Resource):
    def get(self):
        incomes = Expense.query.filter_by(type='income').all()
        expenses = Expense.query.filter_by(type='expense').all()
        total_income = sum(item.amount for item in incomes)
        total_expense = sum(item.amount for item in expenses)
        balance = total_income - total_expense

        return {
            'total_income': total_income,
            'total_expense': total_expense,
            'balance': balance
        }, 200

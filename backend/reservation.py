from flask_restx import Resource, Namespace, fields
from models import Reservation, Table
from flask import Flask, request, jsonify, make_response
from auth import login_model
from flask_jwt_extended import jwt_required, get_jwt_identity

res_ns = Namespace('res', description = "A namespace for Reservation")

reservation_model = res_ns.model(
    "Reserve",
    {
    "date": fields.String(),
    "time": fields.String(example="12:30"),
    "guests": fields.Integer(),
    "occasion": fields.String(),
    "table_id": fields.Integer(),
    "user_id": fields.Integer()
    }
)

table_model = res_ns.model(
    "Table",
    {
    "capacity": fields.Integer(),
    "availability": fields.Boolean()
    }
)

@res_ns.route('/available_tables')
class AvailableTables(Resource):
    @res_ns.expect(table_model)
    def get(self):
        # Get the date, time, and number of guests from the request arguments
        date = request.args.get('date')
        time = request.args.get('time')
        guests = request.args.get('guests')

        # Get all available tables that meet the criteria
        available_tables = Table.get_available_tables(date, time, guests)

        if not available_tables:
            return jsonify({"message": "No available tables found"})

        # Convert the available tables to a list of dictionaries
        result = []
        for table in available_tables:
            result.append({
                "id": table.id,
                "capacity": table.capacity,
                "availability": table.availability
            })

        # Return the list of available tables
        response = make_response(jsonify(result), 200)
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        return response


@res_ns.route('/reserve')
class Reserve(Resource):
    @res_ns.expect(reservation_model)
    def post(self):
        data=request.get_json()

        date = data.get('date')
        time = data.get('time')
        guests = data.get('guests')
        occasion = data.get('occasion')
        table_id = data.get('table_id')
        user_id = data.get('user_id')

        existing_res = Reservation.query.filter_by(date = date, time = time, table_id = table_id).first()
        if existing_res is not None:
            return jsonify({"message": "Reservation already exists"})

        new_res = Reservation(
            date = date,
            time = time,
            guests = guests,
            occasion = occasion,
            table_id = table_id,
            user_id = user_id,
        )

        new_res.save()

        response = make_response(jsonify({"message": "Reservation created successfully"}, 200))
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        return response

@res_ns.route('/reservations')
class Reservations(Resource):
    @res_ns.expect(reservation_model)
    def get(self):
        reservations = Reservation.get_all()
        return jsonify(reservations)

@res_ns.route('/reservations/<int:reservation_id>')
class ReservationById(Resource):
    @res_ns.doc(params={'reservation_id': 'The ID of the reservation to delete'})
    def delete(self, reservation_id):
        reservation = Reservation.query.get_or_404(reservation_id)
        reservation.delete()
        return {'message': 'Reservation has been deleted successfully.'}

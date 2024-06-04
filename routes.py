from collections import defaultdict
from flask import request
from models import db, Duck, Sale, sale_duck
from reports import *


def register_routes(app):
    @app.route('/ducks', methods=['POST'])
    def create_duck():
        data = request.json
        name = data.get('name', '')
        if not name:
            return jsonify({'error': "Name should not be empty"}), 400
        duck = Duck(name=data['name'], mother_id=data.get('mother_id'))
        db.session.add(duck)
        db.session.commit()
        return jsonify({"id": duck.id, "name": duck.name, "mother_id": duck.mother_id}), 201

    @app.route('/clients', methods=['POST'])
    def create_client():
        data = request.json
        name = data.get('name', '')
        if not name:
            return jsonify({'error': "Name should not be empty"}), 400

        client = Client(name=data['name'], eligible_for_discount=data.get('eligible_for_discount', False))
        db.session.add(client)
        db.session.commit()
        return jsonify({"id": client.id, "name": client.name, "Eligible for discount": client.eligible_for_discount}), 201

    @app.route('/sales', methods=['POST'])
    def create_sale():
        data = request.json
        client_name = data.get('client_name', '')
        if not client_name:
            return jsonify({'error': "Name should not be empty"}), 400

        client = Client.query.filter_by(name=data['client_name']).first()
        if not client:
            return jsonify({'message': 'Client not found'}), 404

        # Look for id
        ducks = Duck.query.filter(Duck.id.in_(data['duck_ids'])).all()

        if not ducks:
            return jsonify({'message': 'Duck not found'}), 404

        if not all(duck.is_sold == False for duck in ducks):
            return jsonify({"error": "Could not sale"}), 400

        total = 0

        if client.eligible_for_discount:
            for duck in ducks:
                if duck.mother is None:
                    total += duck.price[1] * 0.8
                else:
                    total += duck.price[0] * 0.8
        else:
            for duck in ducks:
                if duck.mother is None:
                    total += duck.price[1] * 0.8
                else:
                    total += duck.price[0] * 0.8

        sale = Sale(client=client)
        db.session.add(sale)
        db.session.commit()

        for duck in ducks:
            duck.is_sold = True
            sale_duck_entry = sale_duck.insert().values(sale_id=sale.id, duck_id=duck.id, duck_name=duck.name, client_name=client.name, value=total)
            db.session.execute(sale_duck_entry)

        db.session.commit()
        return jsonify({"id": sale.id, "total_price": total}), 201

    @app.route('/list-sales', methods=['GET'])
    def list_sales():
        sales = Sale.query.all()
        result = []
        for sale in sales:
            result.append({
                "date": sale.date,
                "client": sale.client.name,
                "duck_ids": [duck.id for duck in sale.ducks]
            })
        return jsonify(result), 200

    @app.route('/reset', methods=['POST'])
    def reset_database():
        db.drop_all()
        db.create_all()
        return jsonify({"message": "Database reset"}), 200

    @app.route('/reports', methods=['GET'])
    def generate_report():
        ducks = Duck.query.all()
        sales = Sale.query.all()

        duck_data = [{"id": duck.id, "name": duck.name, "mother_id": duck.mother_id, "is_sold": duck.is_sold} for duck in ducks]
        sale_data = [{"id": sale.id, "date": sale.date, "client": sale.client.name, "duck_ids": [duck.id for duck in sale.ducks]} for sale in sales]

        duck_dict = {duck['id']: duck for duck in duck_data}

        grouped_ducks = defaultdict(list)

        for duck in duck_data:
            if duck['mother_id']:
                grouped_ducks[duck['mother_id']].append(duck)
            else:
                grouped_ducks[duck['id']].append(duck)

        report_data = []
        for duck_id, ducks in grouped_ducks.items():
            duck_info = duck_dict[duck_id]
            if duck_id in grouped_ducks:
                duck_info['ducks'] = grouped_ducks[duck_id]
            report_data.append(duck_info)

        return report(report_data, sale_data)

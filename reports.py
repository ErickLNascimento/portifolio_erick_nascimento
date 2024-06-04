import pandas as pd
from flask import jsonify
from models import Client


def report(duck_data, sale_data):
    rows = []
    duck_sales = {}
    for sale in sale_data:
        print(sale)
        for duck_id in sale['duck_ids']:
            duck_sales[duck_id] = {
                "client": sale['client'],
                "date": sale['date'],
                "client_eligible_for_discount": "Yes" if Client.query.filter_by(name=sale['client']).first().eligible_for_discount else "No"
            }

    for duck_info in duck_data:
        if 'ducks' in duck_info:
            for duck in duck_info['ducks']:
                print(duck)
                sold_status = "Sold" if duck['is_sold'] else "Available"
                sale_info = duck_sales.get(duck['id'], {"client": "", "date": "", "client_eligible_for_discount": ""})
                rows.append({
                    "ID": duck['id'],
                    "Name": duck['name'],
                    "Mother ID": duck['mother_id'],
                    "Status": sold_status,
                    "Client": sale_info['client'],
                    "Date": sale_info['date'],
                    "Client Eligible for Discount": sale_info['client_eligible_for_discount']
                })
        else:
            sold_status = "Sold" if duck_info['is_sold'] else "Available"
            sale_info = duck_sales.get(duck_info['id'], {"client": "", "date": "", "client_eligible_for_discount": ""})
            rows.append({
                "ID": duck_info['id'],
                "Name": duck_info['name'],
                "Mother ID": duck_info['mother_id'],
                "Status": sold_status,
                "Client": sale_info['client'],
                "Date": sale_info['date'],
                "Client Eligible for Discount": sale_info['client_eligible_for_discount']
            })

    df = pd.DataFrame(rows)

    with pd.ExcelWriter('duck_report.xlsx') as writer:
        df.to_excel(writer, index=False)

    return jsonify({"message": "Report generated"}), 200

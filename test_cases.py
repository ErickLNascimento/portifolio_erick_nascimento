import unittest
import requests


class TestDuckSalesAPI(unittest.TestCase):
    BASE_URL = "http://localhost:5000/"

    def setUp(self):
        # Reset the database to a clean state
        requests.post(f"{self.BASE_URL}/reset")

    def test_duck_registration(self):
        # Test case for registering a new duck
        response = requests.post(f"{self.BASE_URL}/ducks", json={"name": "Duck1", "mother_id": '1'})
        self.assertEqual(response.status_code, 201)
        self.assertIn("name", response.json())

    def test_client_registration(self):
        # Test case for registering a new client
        response = requests.post(f"{self.BASE_URL}/clients", json={"name": "Client1", "eligible_for_discount": True})
        self.assertEqual(response.status_code, 201)
        self.assertIn("name", response.json())

    def test_sale_without_discount(self):
        # Register duck and client first
        duck_response = requests.post(f"{self.BASE_URL}/ducks", json={"name": "Duck1", "mother_id": '1'})
        duck_id = duck_response.json()["id"]
        print(duck_id)
        client_response = requests.post(f"{self.BASE_URL}/clients", json={"name": "Client1", "eligible_for_discount": False})
        client_name = client_response.json()["name"]
        print(client_name)

        # Test case for making a sale
        sale_response = requests.post(f"{self.BASE_URL}/sales", json={"client_name": client_name, "duck_ids": [duck_id]})
        self.assertEqual(sale_response.status_code, 201)
        self.assertIn("id", sale_response.json())

    def test_sale_with_discount(self):
        # Register duck and client first
        duck_response = requests.post(f"{self.BASE_URL}/ducks", json={"name": "Duck2", "mother_id": "10"})
        duck_id = duck_response.json()["id"]
        mother_id = duck_response.json()['mother_id']
        print(duck_id)
        print(mother_id)
        client_response = requests.post(f"{self.BASE_URL}/clients", json={"name": "Client2", "eligible_for_discount": True})
        client_name = client_response.json()["name"]
        print(client_name)

        # Test case for making a sale with discount
        sale_response = requests.post(f"{self.BASE_URL}/sales", json={"client_name": client_name, "duck_ids": [duck_id]})
        print(sale_response)
        self.assertEqual(sale_response.status_code, 201)
        self.assertIn("id", sale_response.json())

        # Verify that the discount was applied
        sale_data = sale_response.json()
        print(sale_data["total_price"])
        self.assertAlmostEqual(sale_data["total_price"], 0.8 * duck_response.json().get("price", 50))  # Adjust for actual price if available

    def test_listing_sold_ducks(self):
        # Register ducks and client, and make a sale
        duck_response1 = requests.post(f"{self.BASE_URL}/ducks", json={"name": "Duck3", "mother_id": "3"})
        duck_id1 = duck_response1.json()["id"]
        duck_response2 = requests.post(f"{self.BASE_URL}/ducks", json={"name": "Duck4", "mother_id": "5"})
        duck_id2 = duck_response2.json()["id"]
        client_response = requests.post(f"{self.BASE_URL}/clients", json={"name": "Client3", "eligible_for_discount": False})
        client_id = client_response.json()["id"]

        requests.post(f"{self.BASE_URL}/sales", json={"client_name": client_id, "duck_ids": [duck_id1]})
        requests.post(f"{self.BASE_URL}/sales", json={"client_name": client_id, "duck_ids": [duck_id2]})

        # Test case for listing sold ducks
        sold_ducks_response = requests.get(f"{self.BASE_URL}/list-sales")
        self.assertEqual(sold_ducks_response.status_code, 200)

    def test_report_generation(self):
        # Register ducks and client, and make a sale
        duck_response1 = requests.post(f"{self.BASE_URL}/ducks", json={"name": "Duck5", "mother_id": "2"})
        duck_id1 = duck_response1.json()["id"]
        client_response = requests.post(f"{self.BASE_URL}/clients", json={"name": "Client4", "eligible_for_discount": False})
        client_id = client_response.json()["id"]

        requests.post(f"{self.BASE_URL}/sales", json={"client_name": client_id, "duck_ids": [duck_id1]})

        # Test case for generating a report
        report_response = requests.get(f"{self.BASE_URL}/reports", params={})
        self.assertEqual(report_response.status_code, 200)
        self.assertIn("Report generated", report_response.json().get("message", ""))

    def test_duck_registration_special_characters(self):
        # Test case for registering a new duck with special characters in the name
        response = requests.post(f"{self.BASE_URL}/ducks", json={"name": "Duck@#!", "mother_id": None})
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.json())

    def test_duck_registration_empty_name(self):
        # Test case for registering a new duck with an empty name
        response = requests.post(f"{self.BASE_URL}/ducks", json={"name": "", "mother_id": "1"})
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())

    def test_client_registration_empty_name(self):
        # Test case for registering a new client with an empty name
        response = requests.post(f"{self.BASE_URL}/clients", json={"name": "", "eligible_for_discount": False})
        print(response.status_code)
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())

    def test_sale_with_empty_client(self):
        # Register duck first
        duck_response = requests.post(f"{self.BASE_URL}/ducks", json={"name": "Duck2", "mother_id": "3"})
        duck_id = duck_response.json()["id"]
        # Test case for making a sale with an empty client ID
        response = requests.post(f"{self.BASE_URL}/sales", json={"client_name": "", "duck_ids": [duck_id]})
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())


if __name__ == '__main__':
    unittest.main()

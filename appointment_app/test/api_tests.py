'''unit tests for api'''
import unittest
import requests as rq

# please run the sql before the tests
class ApiTests(unittest.TestCase):
    '''Unit tests for api'''
    URL = "http://localhost:5009/api"

    def __init__(self):
        super().__init__()
        print("Starting tests...")

    def get_all_appointments(self):
        ''' test for getting all the appointments'''
        resp = rq.get(self.URL + "/appointments")
        resp_obj = resp.json()
        self.assertEqual(resp.status_code, 200)
        self.assertIsNotNone(resp_obj)
        print("Test 'get_all_appointments' passed successful")

    def post_one_appointment(self):
        '''Test creating a new appointment'''
        data = {
            'status': 'ON GOING',
            'date_appointment': '2024-05-11',
            'slot': '10:00 - 11:00',
            'venue': 'Venue A',
            'client_id': 1,
            'professional_id': 1,
            'service_id': 1,
        }
        post_req = rq.post(self.URL + "/appointments", json=data)
        self.assertEqual(post_req.status_code, 200)
        print("Test 'post_one_appointment' passed successful")

    def get_one_appointment(self, appointment_id):
        '''Test getting a single appointment'''
        resp = rq.get(self.URL + f'/appointments/{appointment_id}')
        resp_obj = resp.json()
        self.assertEqual(resp_obj['appointment_id'], 1)
        self.assertEqual(resp_obj['status'], 'ON GOING')
        self.assertEqual(resp_obj['date'], '2024-05-15 00:00:00')
        self.assertEqual(resp_obj['slot'], '10:00 - 11:00')
        self.assertEqual(resp_obj['venue'], 'Venue A')
        self.assertEqual(resp_obj['client_id'], 1)
        self.assertEqual(resp_obj['professional_id'], 2)
        self.assertEqual(resp_obj['service_id'], 1)
        print("Test 'get_one_appointment' passed successful")

    def update_one_appointment(self, appointment_id):
        ''' test to update one appointment'''
        data = {
            'status': 'ENDED',
            'date_appointment': '2024-05-11',
            'slot': '11:00 - 12:00',
            'venue': 'Venue A',
            'service_id': 1,
            'number_of_services': 1
        }
        patch_req = rq.patch(self.URL + f"/appointments/{appointment_id}", json=data)
        self.assertEqual(patch_req.status_code, 200)
        print("Test 'update_one_appointment' passed successful")
        
    def delete_one_appointment(self, appointment_id):
        '''Test deleting a single appointment'''
        resp = rq.delete(self.URL + f"/appointments/{10}")
        self.assertEqual(resp.status_code, 200)
        self.assertIsNotNone(resp)
        print("Test passed 'delete_one_appointment' successful")


if __name__ == '__main__':
    test = ApiTests()
    print("Please run SQL script before running these tests")
    print("Else, it will cause some tests to fail")
    test.get_all_appointments()
    test.post_one_appointment()
    test.get_one_appointment(1)
    test.update_one_appointment(1)
    test.delete_one_appointment(10)
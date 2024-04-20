class Appointment:
    def __init__(self, appointment_id, status, date_appointment, slot, venue, client_id, prof_id, service_id):
        self.appointment_id = appointment_id
        self.status = status
        self.date_appointment = date_appointment
        self.slot = slot
        self.venue = venue
        self.client_id = client_id
        self.prof_id = prof_id
        self.service_id = service_id

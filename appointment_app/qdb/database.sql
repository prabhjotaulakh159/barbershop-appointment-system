DROP TABLE reports;
DROP TABLE appointments;
DROP TABLE services;
DROP TABLE logs;
DROP TABLE users;


CREATE TABLE users (
    user_id         NUMBER              GENERATED ALWAYS AS IDENTITY,
    is_enabled      NUMBER(1)           DEFAULT 1 NOT NULL,
    access_level    NUMBER(1)           DEFAULT 0 NOT NULL,
    user_type       VARCHAR2(255)       NOT NULL, 
    user_name       VARCHAR2(255)       NOT NULL,
    pass_word       VARCHAR2(255)       NOT NULL,
    email           VARCHAR2(255)       NOT NULL,
    avatar          VARCHAR2(255)       DEFAULT '/images/avatar.png',
    phone           VARCHAR2(255)       NOT NULL,
    address         VARCHAR2(255)       NOT NULL,
    age             NUMBER              NOT NULL,
    pay_rate        NUMBER              ,
    specialty       VARCHAR2(255)       ,
    warnings        NUMBER              DEFAULT 0,
    
    
    CONSTRAINT user_id_PK               PRIMARY KEY (user_id),
    CONSTRAINT user_name_Usr            UNIQUE (user_name)
);

CREATE TABLE services (
    service_id          NUMBER          GENERATED ALWAYS AS IDENTITY,
    service_name        VARCHAR2(255)   NOT NULL,
    service_duration    NUMBER          NOT NULL,
    service_price       NUMBER          NOT NULL,
    service_materials   VARCHAR2(255)   NOT NULL,
    
    CONSTRAINT service_id_PK            PRIMARY KEY (service_id),
    CONSTRAINT service_name_U           UNIQUE (service_name)
);

CREATE TABLE appointments (
    appointment_id      NUMBER              GENERATED ALWAYS AS IDENTITY,
    status              VARCHAR2(255)       DEFAULT 'Open' NOT NULL,
    date_appointment    DATE                NOT NULL,
    slot                VARCHAR2(255)       NOT NULL,
    venue               VARCHAR2(255)       NOT NULL,
    client_id           NUMBER              NOT NULL,
    professional_id     NUMBER              NOT NULL,
    service_id          NUMBER              NOT NULL,
    number_services     NUMBER              DEFAULT 1 NOT NULL,
    
    CONSTRAINT appointment_id_PK            PRIMARY KEY (appointment_id),
    CONSTRAINT client_id_FK                 FOREIGN KEY (client_id) REFERENCES users (user_id) ON DELETE CASCADE,
    CONSTRAINT professional_id              FOREIGN KEY (professional_id) REFERENCES users (user_id) ON DELETE CASCADE,
    CONSTRAINT service_id_FK                FOREIGN KEY (service_id) REFERENCES services (service_id) ON DELETE CASCADE
);

CREATE TABLE reports (
    report_id               NUMBER              GENERATED ALWAYS AS IDENTITY,
    feedback_client         VARCHAR2(255)       ,
    feedback_professional   VARCHAR2(255)       ,
    date_of_report          DATE                NOT NULL,
    appointment_id          NUMBER              NOT NULL,
    
    CONSTRAINT report_id_PK                     PRIMARY KEY (report_id),
    CONSTRAINT appointment_id_FK                FOREIGN KEY (appointment_id) REFERENCES appointments (appointment_id) ON DELETE CASCADE 
);

CREATE TABLE logs (
    log_id                  NUMBER              GENERATED ALWAYS AS IDENTITY,
    action                  VARCHAR2(255)       ,
    date_of_action          DATE                NOT NULL,
    table_name              VARCHAR2(50)        NOT NULL,
    user_name              VARCHAR2(50)        NOT NULL,
    user_id                NUMBER              NOT NULL,
    
    CONSTRAINT log_id_PK                        PRIMARY KEY (log_id),
    CONSTRAINT user_id_FK                      FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE 
);

-- Members 
INSERT INTO users (is_enabled, access_level, user_type, user_name, pass_word, email, phone, address, age)
VALUES (1, 0, 'Member', 'member1', '$2b$12$U4eQOXvNVz0K/hX3UtnBluuIkPf9KtQ12GnzVyGDnM37dJ7kKLvcK', 'member1@example.com', '123-456-7890', '123 Member St, City', 25);

INSERT INTO users (is_enabled, access_level, user_type, user_name, pass_word, email, phone, address, age)
VALUES (1, 0, 'Member', 'member2', '$2b$12$U4eQOXvNVz0K/hX3UtnBluuIkPf9KtQ12GnzVyGDnM37dJ7kKLvcK', 'member2@example.com', '987-654-0321', '456 Member Ave, Town', 30);

INSERT INTO users (is_enabled, access_level, user_type, user_name, pass_word, email, phone, address, age)
VALUES (1, 0, 'Member', 'member3', '$2b$12$U4eQOXvNVz0K/hX3UtnBluuIkPf9KtQ12GnzVyGDnM37dJ7kKLvcK', 'member3@example.com', '654-321-9987', '789 Member Rd, Village', 28);

INSERT INTO users (is_enabled, access_level, user_type, user_name, pass_word, email, phone, address, age)
VALUES (1, 0, 'Member', 'member4', '$2b$12$U4eQOXvNVz0K/hX3UtnBluuIkPf9KtQ12GnzVyGDnM37dJ7kKLvcK', 'member4@example.com', '321-987-9654', '101 Member Blvd, County', 35);

INSERT INTO users (is_enabled, access_level, user_type, user_name, pass_word, email, phone, address, age)
VALUES (1, 0, 'Member', 'member5', '$2b$12$U4eQOXvNVz0K/hX3UtnBluuIkPf9KtQ12GnzVyGDnM37dJ7kKLvcK', 'member5@example.com', '789-654-6123', '999 Member Lane, Hamlet', 22);

-- Professionals
INSERT INTO users (is_enabled, access_level, user_type, user_name, pass_word, email, phone, address, age, pay_rate, specialty)
VALUES (1, 0, 'Professional', 'barber1', '$2b$12$U4eQOXvNVz0K/hX3UtnBluuIkPf9KtQ12GnzVyGDnM37dJ7kKLvcK', 'barber1@example.com', '123-456-3789', '123 Barber St, City', 30, 100, 'Haircutting and Styling');

INSERT INTO users (is_enabled, access_level, user_type, user_name, pass_word, email, phone, address, age, pay_rate, specialty)
VALUES (1, 0, 'Professional', 'barber2', '$2b$12$U4eQOXvNVz0K/hX3UtnBluuIkPf9KtQ12GnzVyGDnM37dJ7kKLvcK', 'barber2@example.com', '987-654-3321', '456 Barber Ave, Town', 35, 120, 'Beard Trimming');

INSERT INTO users (is_enabled, access_level, user_type, user_name, pass_word, email, phone, address, age, pay_rate, specialty)
VALUES (1, 0, 'Professional', 'barber3', '$2b$12$U4eQOXvNVz0K/hX3UtnBluuIkPf9KtQ12GnzVyGDnM37dJ7kKLvcK', 'barber3@example.com', '654-321-1987', '789 Barber Rd, Village', 28, 110, 'Hair Coloring');

INSERT INTO users (is_enabled, access_level, user_type, user_name, pass_word, email, phone, address, age, pay_rate, specialty)
VALUES (1, 0, 'Professional', 'barber4', '$2b$12$U4eQOXvNVz0K/hX3UtnBluuIkPf9KtQ12GnzVyGDnM37dJ7kKLvcK', 'barber4@example.com', '321-987-3654', '101 Barber Blvd, County', 40, 150, 'Shaving');

INSERT INTO users (is_enabled, access_level, user_type, user_name, pass_word, email, phone, address, age, pay_rate, specialty)
VALUES (1, 0, 'Professional', 'barber5', '$2b$12$U4eQOXvNVz0K/hX3UtnBluuIkPf9KtQ12GnzVyGDnM37dJ7kKLvcK', 'barber5@example.com', '789-654-3123', '999 Barber Lane, Hamlet', 32, 130, 'Facial Treatments');

-- Admins
INSERT INTO users (is_enabled, access_level, user_type, user_name, pass_word, email, phone, address, age)
VALUES (1, 1, 'Admin', 'adminuser', '$2b$12$U4eQOXvNVz0K/hX3UtnBluuIkPf9KtQ12GnzVyGDnM37dJ7kKLvcK', 'adminuser@example.com', '123-456-7890', '123 Admin St, City', 30);

INSERT INTO users (is_enabled, access_level, user_type, user_name, pass_word, email, phone, address, age)
VALUES (1, 2, 'Admin', 'adminappointment', '$2b$12$U4eQOXvNVz0K/hX3UtnBluuIkPf9KtQ12GnzVyGDnM37dJ7kKLvcK', 'adminappointment@example.com', '987-654-3210', '456 Admin Ave, Town', 35);

INSERT INTO users (is_enabled, access_level, user_type, user_name, pass_word, email, phone, address, age)
VALUES (1, 3, 'Admin', 'superadmin', '$2b$12$U4eQOXvNVz0K/hX3UtnBluuIkPf9KtQ12GnzVyGDnM37dJ7kKLvcK', 'superadmin@example.com', '654-321-0987', '789 Admin Rd, Village', 28);

-- Services
INSERT INTO services (service_name, service_duration, service_price, service_materials)
VALUES ('Haircut', 30, 50, 'Scissors, Comb, Hair Dryer');

INSERT INTO services (service_name, service_duration, service_price, service_materials)
VALUES ('Head Shave', 20, 25, 'Clippers, Shaving Cream, Razor');

INSERT INTO services (service_name, service_duration, service_price, service_materials)
VALUES ('Hair Styling', 60, 60, 'Curling Iron, Hair Spray, Hair Pins');

INSERT INTO services (service_name, service_duration, service_price, service_materials)
VALUES ('Hair Color', 60, 150, 'Hair Color, Developer, Gloves');

INSERT INTO services (service_name, service_duration, service_price, service_materials)
VALUES ('Highlights', 60, 200, 'Foil, Hair 
Bleach, Developer');

INSERT INTO services (service_name, service_duration, service_price, service_materials)
VALUES ('Perm', 60, 180, 'Perm Solution, Neutralizer');

INSERT INTO services (service_name, service_duration, service_price, service_materials)
VALUES ('Basic Haircut', 30, 30, 'Clippers, Scissors, Comb');

INSERT INTO services (service_name, service_duration, service_price, service_materials)
VALUES ('Beard Trim', 15, 20, 'Clippers, Scissors, Beard Oil');

-- appointments
INSERT INTO appointments (status, date_appointment, slot, venue, client_id, professional_id, service_id, number_services)
VALUES ('Open', TO_DATE('2024-05-15', 'YYYY-MM-DD'), '10:00 - 11:00', 'Venue A', 1, 6, 1, 1);

INSERT INTO appointments (status, date_appointment, slot, venue, client_id, professional_id, service_id, number_services)
VALUES ('Open', TO_DATE('2024-05-16', 'YYYY-MM-DD'), '14:00 - 15:00', 'Venue B', 2, 7, 2, 1);

INSERT INTO appointments (status, date_appointment, slot, venue, client_id, professional_id, service_id, number_services)
VALUES ('Open', TO_DATE('2024-05-17', 'YYYY-MM-DD'), '11:00 - 12:00', 'Venue C', 3, 8, 3, 1);

INSERT INTO appointments (status, date_appointment, slot, venue, client_id, professional_id, service_id, number_services)
VALUES ('Open', TO_DATE('2024-05-18', 'YYYY-MM-DD'), '11:00 - 12:00', 'Venue A', 4, 9, 4, 1);

INSERT INTO appointments (status, date_appointment, slot, venue, client_id, professional_id, service_id, number_services)
VALUES ('Open', TO_DATE('2024-05-19', 'YYYY-MM-DD'), '12:00 - 13:00', 'Venue B', 5, 10, 5, 1);

-- reports
INSERT INTO reports (feedback_client, feedback_professional, date_of_report, appointment_id)
VALUES ('Great service, I am very satisfied.', 'The client was cooperative and easy to work with.', TO_DATE('2024-05-15', 'YYYY-MM-DD'), 1);

INSERT INTO reports (feedback_client, feedback_professional, date_of_report, appointment_id)
VALUES ('Everything went smoothly, I have no complaints.', 'The appointment was well-managed.', TO_DATE('2024-05-16', 'YYYY-MM-DD'), 2);

INSERT INTO reports (feedback_client, feedback_professional, date_of_report, appointment_id)
VALUES ('The service exceeded my expectations.', 'The client was polite and respectful.', TO_DATE('2024-05-17', 'YYYY-MM-DD'), 3);

INSERT INTO reports (feedback_client, feedback_professional, date_of_report, appointment_id)
VALUES ('I am happy with the outcome of the service.', 'The appointment went as planned.', TO_DATE('2024-05-18', 'YYYY-MM-DD'), 4);

INSERT INTO reports (feedback_client, feedback_professional, date_of_report, appointment_id)
VALUES ('The service was fantastic, I will definitely come back.', 'The client was punctual and understanding.', TO_DATE('2024-05-19', 'YYYY-MM-DD'), 5);

COMMIT;
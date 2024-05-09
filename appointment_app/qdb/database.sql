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
    status              VARCHAR2(255)       DEFAULT 'ON GOING' NOT NULL,
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
    admin_name              VARCHAR2(50)        NOT NULL,
    admin_id                NUMBER              NOT NULL,
    
    CONSTRAINT log_id_PK                        PRIMARY KEY (log_id),
    CONSTRAINT admin_id_FK                      FOREIGN KEY (admin_id) REFERENCES users (user_id) ON DELETE CASCADE 
);

INSERT INTO users (is_enabled, access_level, user_type, user_name, pass_word, email, phone, address, age)
VALUES (1, 0, 'Member', 'member1', '$2b$12$U4eQOXvNVz0K/hX3UtnBluuIkPf9KtQ12GnzVyGDnM37dJ7kKLvcK', 'member1@example.com', '123456789', '123 Member St, City', 25);

INSERT INTO users (is_enabled, access_level, user_type, user_name, pass_word, email, phone, address, age)
VALUES (1, 0, 'Member', 'member2', '$2b$12$U4eQOXvNVz0K/hX3UtnBluuIkPf9KtQ12GnzVyGDnM37dJ7kKLvcK', 'member2@example.com', '987654321', '456 Member Ave, Town', 30);

INSERT INTO users (is_enabled, access_level, user_type, user_name, pass_word, email, phone, address, age)
VALUES (1, 0, 'Member', 'member3', '$2b$12$U4eQOXvNVz0K/hX3UtnBluuIkPf9KtQ12GnzVyGDnM37dJ7kKLvcK', 'member3@example.com', '654321987', '789 Member Rd, Village', 28);

INSERT INTO users (is_enabled, access_level, user_type, user_name, pass_word, email, phone, address, age)
VALUES (1, 0, 'Member', 'member4', '$2b$12$U4eQOXvNVz0K/hX3UtnBluuIkPf9KtQ12GnzVyGDnM37dJ7kKLvcK', 'member4@example.com', '321987654', '101 Member Blvd, County', 35);

INSERT INTO users (is_enabled, access_level, user_type, user_name, pass_word, email, phone, address, age)
VALUES (1, 0, 'Member', 'member5', '$2b$12$U4eQOXvNVz0K/hX3UtnBluuIkPf9KtQ12GnzVyGDnM37dJ7kKLvcK', 'member5@example.com', '789654123', '999 Member Lane, Hamlet', 22);

INSERT INTO users (is_enabled, access_level, user_type, user_name, pass_word, email, phone, address, age, pay_rate, specialty)
VALUES (1, 0, 'Professional', 'barber1', '$2b$12$U4eQOXvNVz0K/hX3UtnBluuIkPf9KtQ12GnzVyGDnM37dJ7kKLvcK', 'barber1@example.com', '123456789', '123 Barber St, City', 30, 100, 'Haircutting and Styling');

INSERT INTO users (is_enabled, access_level, user_type, user_name, pass_word, email, phone, address, age, pay_rate, specialty)
VALUES (1, 0, 'Professional', 'barber2', '$2b$12$U4eQOXvNVz0K/hX3UtnBluuIkPf9KtQ12GnzVyGDnM37dJ7kKLvcK', 'barber2@example.com', '987654321', '456 Barber Ave, Town', 35, 120, 'Beard Trimming');

INSERT INTO users (is_enabled, access_level, user_type, user_name, pass_word, email, phone, address, age, pay_rate, specialty)
VALUES (1, 0, 'Professional', 'barber3', '$2b$12$U4eQOXvNVz0K/hX3UtnBluuIkPf9KtQ12GnzVyGDnM37dJ7kKLvcK', 'barber3@example.com', '654321987', '789 Barber Rd, Village', 28, 110, 'Hair Coloring');

INSERT INTO users (is_enabled, access_level, user_type, user_name, pass_word, email, phone, address, age, pay_rate, specialty)
VALUES (1, 0, 'Professional', 'barber4', '$2b$12$U4eQOXvNVz0K/hX3UtnBluuIkPf9KtQ12GnzVyGDnM37dJ7kKLvcK', 'barber4@example.com', '321987654', '101 Barber Blvd, County', 40, 150, 'Shaving');

INSERT INTO users (is_enabled, access_level, user_type, user_name, pass_word, email, phone, address, age, pay_rate, specialty)
VALUES (1, 0, 'Professional', 'barber5', '$2b$12$U4eQOXvNVz0K/hX3UtnBluuIkPf9KtQ12GnzVyGDnM37dJ7kKLvcK', 'barber5@example.com', '789654123', '999 Barber Lane, Hamlet', 32, 130, 'Facial Treatments');


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

COMMIT;
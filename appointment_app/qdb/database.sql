DROP TABLE reports;
DROP TABLE appointments;
DROP TABLE services;
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
    
    
    CONSTRAINT user_id_PK               PRIMARY KEY (user_id),
    CONSTRAINT user_name_Usr            UNIQUE (user_name),
    CONSTRAINT email_Usr                UNIQUE (email)
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
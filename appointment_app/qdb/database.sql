DROP TABLE reports;
DROP TABLE appointments;
DROP TABLE services;
DROP TABLE admins;
DROP TABLE professionals;
DROP TABLE clients;

CREATE TABLE clients (
    client_id       NUMBER              GENERATED ALWAYS AS IDENTITY,
    user_name       VARCHAR2(255)       NOT NULL,
    pass_word       VARCHAR2(255)       NOT NULL,
    email           VARCHAR2(255)       NOT NULL,
    avatar          VARCHAR2(255)       DEFAULT '/static/images/avatar.png' NOT NULL,
    phone           VARCHAR2(255)       NOT NULL,
    
    CONSTRAINT client_id_PK             PRIMARY KEY (client_id),
    CONSTRAINT user_name_U              UNIQUE (user_name),
    CONSTRAINT email_U                  UNIQUE (email)
);

CREATE TABLE professionals (
    professional_id         NUMBER              GENERATED ALWAYS AS IDENTITY,
    professional_name       VARCHAR2(255)       NOT NULL,
    pass_word               VARCHAR2(255)       NOT NULL,
    professional_email      VARCHAR2(255)       NOT NULL,
    avatar                  VARCHAR2(255)       DEFAULT '/static/images/avatar.png' NOT NULL,
    phone                   VARCHAR2(255)       NOT NULL,
    rate                    NUMBER(5,2)         NOT NULL,
    specialty               VARCHAR2(255)       NOT NULL,
    
    CONSTRAINT professional_id_PK               PRIMARY KEY (professional_id),
    CONSTRAINT professional_name_U              UNIQUE (professional_name),
    CONSTRAINT professional_email_U             UNIQUE (professional_email) 
);

CREATE TABLE admins (
    admin_id        NUMBER          GENERATED ALWAYS AS IDENTITY,    
    admin_name      VARCHAR2(255)   NOT NULL,
    pass_word       VARCHAR2(255)   NOT NULL,
    access_lvl      NUMBER(1)       NOT NULL,
    
    CONSTRAINT admin_id_PK          PRIMARY KEY (admin_id),
    CONSTRAINT admin_name_U         UNIQUE (admin_name)
);

CREATE TABLE services (
    service_id          NUMBER          GENERATED ALWAYS AS IDENTITY,
    service_name        VARCHAR2(255)   NOT NULL,
    service_duration    NUMBER(2)       NOT NULL,
    service_price       NUMBER(5,2)     NOT NULL,
    service_materials   VARCHAR2(255)   NOT NULL,
    
    CONSTRAINT service_id_PK            PRIMARY KEY (service_id),
    CONSTRAINT service_name_U           UNIQUE (service_name)
);

CREATE TABLE appointments (
    appointment_id      NUMBER              GENERATED ALWAYS AS IDENTITY,
    status              NUMBER(1)           NOT NULL,
    date_appointment    DATE                NOT NULL,
    slot                VARCHAR2(255)       NOT NULL,
    venue               VARCHAR2(255)       NOT NULL,
    client_id           NUMBER              NOT NULL,
    prof_id             NUMBER              NOT NULL,
    service_id          NUMBER              NOT NULL,
    
    CONSTRAINT appointment_id_PK            PRIMARY KEY (appointment_id),
    CONSTRAINT client_id_FK                 FOREIGN KEY (client_id) REFERENCES clients (client_id) ON DELETE CASCADE,
    CONSTRAINT prof_id_FK                   FOREIGN KEY (prof_id) REFERENCES professionals (professional_id) ON DELETE CASCADE,
    CONSTRAINT service_id_FK                FOREIGN KEY (service_id) REFERENCES services (service_id) ON DELETE CASCADE
);

CREATE TABLE reports (
    report_id               NUMBER              GENERATED ALWAYS AS IDENTITY,
    feedback_client         VARCHAR2(255)       NOT NULL,
    feedback_professional   VARCHAR2(255)       NOT NULL,
    date_of_report          DATE                NOT NULL,
    appointment_id          NUMBER              NOT NULL,
    
    CONSTRAINT report_id_PK                     PRIMARY KEY (report_id),
    CONSTRAINT appointment_id_FK                FOREIGN KEY (appointment_id) REFERENCES appointments (appointment_id) ON DELETE CASCADE 
);
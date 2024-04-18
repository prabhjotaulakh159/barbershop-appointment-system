DROP TABLE clients;
DROP TABLE professionals;
DROP TABLE admins;

CREATE TABLE clients (
    client_id       NUMBER          GENERATED ALWAYS AS IDENTITY,
    user_name       VARCHAR2(255)   NOT NULL,
    pass_word       VARCHAR2(255)   NOT NULL,
    email           VARCHAR2(255)   NOT NULL,
    avatar          VARCHAR2(255)   DEFAULT '/static/images/avatar.png' NOT NULL,
    phone           VARCHAR2(255)   NOT NULL,
    
    CONSTRAINT client_id_PK     PRIMARY KEY (client_id),
    CONSTRAINT user_name_U      UNIQUE (user_name),
    CONSTRAINT email_U          UNIQUE (email)
);

CREATE TABLE professionals (
    prof_id                 NUMBER          GENERATED ALWAYS AS IDENTITY,
    prof_name               VARCHAR2(255)   NOT NULL,
    pass_word               VARCHAR2(255)   NOT NULL,
    prof_email              VARCHAR2(255)   NOT NULL,
    avatar                  VARCHAR2(255)   DEFAULT '/static/images/avatar.png' NOT NULL,
    phone                   VARCHAR2(255)   NOT NULL,
    rate                    NUMBER(5,2)     NOT NULL,
    specialty               VARCHAR2(255)   NOT NULL,
    
    CONSTRAINT prof_id_PK       PRIMARY KEY (prof_id),
    CONSTRAINT prof_name_U      UNIQUE (prof_name),
    CONSTRAINT prof_email_U     UNIQUE (prof_email) 
);

CREATE TABLE admins (
    admin_id        NUMBER          GENERATED ALWAYS AS IDENTITY,    
    admin_name      VARCHAR2(255)   NOT NULL,
    pass_word       VARCHAR2(255)   NOT NULL,
    access_lvl      NUMBER(1)       NOT NULL,
    
    CONSTRAINT admin_id_PK          PRIMARY KEY (admin_id),
    CONSTRAINT admin_name_U         UNIQUE (admin_name),
    CONSTRAINT access_lvl_1_to_3    CHECK (access_lvl BETWEEN 1 AND 3)
);

--CREATE TABLE appointments (
--    appt_id         NUMBER              GENERATED ALWAYS AS IDENTITY,
--    status          NUMBER(1)           NOT NULL,
--    approved        CHAR(1)             NOT NULL,
--    date_appt       DATE                NOT NULL,
--    slot            VARCHAR2(255)       NOT NULL,
--    venue           VARCHAR2(255)       NOT NULL,
--    
--);
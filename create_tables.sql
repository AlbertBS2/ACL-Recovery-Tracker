CREATE TABLE users (
    user_id SERIAL,
    name VARCHAR(50),
    PRIMARY KEY (user_id)
);

CREATE TABLE periodic_logs (
    date DATE,
    time TIME,
    pain SMALLINT,
    flexion SMALLINT,
    swelling VARCHAR(8),
    painkillers BOOLEAN,
    rehab_done BOOLEAN,
    mood VARCHAR(7),
    notes VARCHAR(255), 
    user_id INT,
    PRIMARY KEY (date, time, user_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE daily_logs (
    date DATE,
    sleep_hours NUMERIC(4, 2),
    steps_walked INT,
    user_id INT,
    PRIMARY KEY (date, user_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
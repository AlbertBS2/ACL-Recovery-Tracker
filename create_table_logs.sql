CREATE TABLE logs2 (
date DATE,
time TIME,
sleep_hours NUMERIC(4, 2),
pain INT,
flexion INT,
swelling VARCHAR(8),
painkillers BOOLEAN,
rehab_done BOOLEAN,
mood VARCHAR(7),
notes VARCHAR(255),
PRIMARY KEY (date, time)
);
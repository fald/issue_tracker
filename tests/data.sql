INSERT INTO user (username, password)
VALUES 
    ('fald', null),
    ('zuse', 'aaa'), -- lol plaintext passwords because no auth
    ('russ', null);

INSERT INTO project (name, description)
VALUES
    ('Bug Tracker', 'Track bugs across many projects.'),
    ('Project Manager/', 'Manage many projects'),
    ('Delver', 'Rogue-lite using a hex-grid and tactical turns.'),
    ('EDA Manager', 'Exploratory Data Analysis manager to aid in creating and completing such projects.');

INSERT INTO issue 
    (project_id, title, body, creator_id, target_id, status, priority, created, last_modified)
VALUES
    (1, 'SQL Issues', 'Building SQL queries in Python is ass.', 1, null, 'Open', 'Low', '2016-01-02 00:00:01', CURRENT_TIMESTAMP),
    (1, 'Auth issues', 'Auth module does not work and is not required to edit issues.', 2, 3, 'Open', 'Medium', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    (2, 'No project outline', 'No one knows what the expectations or final product are!!!', 3, null, 'Open', 'High', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    (3, 'FOV System broken', 'Not intended to work with hex-grid.', 1, 1, 'Open', 'Low', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

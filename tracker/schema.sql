/* 
Tables:
    Issue
        ID, FK Project, Title, Body, FK Creator,
        FK Assignee, Status, Priority,
        Creation date, Last modified date
    Project (Simple)
        ID, Name, Description
    User
        ID, Username, Password
*/

DROP TABLE IF EXISTS issue;
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS project;

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT -- This can be null for now for unregistered users
);

CREATE TABLE project (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    description TEXT
);

CREATE TABLE issue (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    body TEXT NOT NULL,
    creator_id INTEGER NOT NULL DEFAULT "fald",
    target_id INTEGER,
    status TEXT DEFAULT "open",
    priority TEXT DEFAULT "low",
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_modified TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES project (id),
    FOREIGN KEY (creator_id) REFERENCES user (id),
    FOREIGN KEY (target_id) REFERENCES user (id)
);

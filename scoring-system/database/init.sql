CREATE TABLE Users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE Challenges (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    description VARCHAR(511),
    totalValue INT NOT NULL,
    category VARCHAR(255)
);

CREATE TABLE Attempts (
    challenge_id INT,
    user_id INT,
    score INT,
    status VARCHAR(255),
    PRIMARY KEY(challenge_id, user_id),
    FOREIGN KEY (challenge_id) REFERENCES Challenges(id),
    FOREIGN KEY (user_id) REFERENCES Users(id)
);

INSERT INTO Users (username, password)
VALUES ('username', 'password');

INSERT INTO Users (username, password)
VALUES ('admin', 'JnAjh2qVCXdkdKu');

INSERT INTO Challenges (name, description, totalValue, category)
VALUES ('SQL Injection Login', 'Bypass the login form using SQL injection', 100, 'Web');
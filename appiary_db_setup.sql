CREATE DATABASE IF NOT EXISTS appiary_db;

CREATE USER IF NOT EXISTS 'appiary_db_user'@'localhost';
GRANT ALL PRIVILEGES ON *.* TO 'appiary_db_user'@'localhost';
ALTER USER 'appiary_db_user'@'localhost' IDENTIFIED BY 'appiary_db_user_pwd';
FLUSH PRIVILEGES;

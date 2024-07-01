-- A script that prepares a MySQL server for the project

CREATE DATABASE IF NOT EXISTS user_db;
CREATE USER IF NOT EXISTS 'vid_stream'@'localhost' IDENTIFIED BY 'vid_stream_pwd';
GRANT USAGE ON *.* TO 'vid_stream'@'localhost';
GRANT ALL PRIVILEGES ON `user_db`.* TO 'vid_stream'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'vid_stream'@'localhost';
FLUSH PRIVILEGES;

# Prasanna_Dani_Accuknox_Assignment

Accuknox Social Media Project Assignment

Installation Guide:

Prerequisite:
1.	Docker
2.	Docker Compose
3.	Postman

Project Structure:

Accuknox_Social_Media/
├── Accuknox Social Media Folder
│   ├── Dockerfile
│   ├── docker-compose.yml
├── env
├── Social_Media (app) ├── Login_Api (Folder for Login APIs)
├                      ├── Relations (Folder for API related to Friend Requests and lists)
└── manage.py

Installation Instructions

1) Clone the repository to your local machine.

•	git clone <repository_url>
•	cd Accuknox_Social_Media/Accuknox Social Media

2) Check whether the Environment Variables are set correctly according to your current computer setup. (docker-compose.yml)

3) Build and Run Docker Containers. Navigate to Accuknox_Social_Media (inner) and the command as mentioned below.

•	docker-compose up –build

This will start 3 services
•	db: PostgreSQL DB Service
•	web: Django Web Application
•	pgadmin: PGAdmin service for UI level management of Database.

4) How to access the application?

•	This Django application will be open and listening at port 8000. You can follow the postman collection been provided and hit your APIs on port 8000 during evaluation. (This project is a Backend Application)

•	To Access PGAdmin, open your browser and go to http://localhost:5050

5) Configuration of PGAdmin on http://localhost:5050:

 Login with the following credentials:
•	Email: admin@admin.com
•	Password: admin
 Add a new server in PGAdmin with the following details:
•	Name: accuknox
•	Host: db
•	Port: 5432
•	Username: postgres
•	Password: root

Please Note: 

•	Ensure Docker and Docker Compose are installed and running on your machine.
•	The db service uses port 5432 for PostgreSQL. If this port is already in use, update the ports configuration in docker-compose.yml and the DB_PORT environment variable accordingly.

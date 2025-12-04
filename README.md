# ProjectMIA_Cosc310
Step-by-Step Deployment and Handover Guide:
Installation Instructions: 
Assuming a recent download of Docker from docker.com, once you have a cloned copy of the project, you need to be in the ProjectMIA_Cosc310 folder.
For the Docker database configuration (in docker-compose.yaml), the current values are set:
Username: projectuser
Password: projectpassword
Database: projectdb
Port 5432
Backend API
Port: 8000
URL: http://localhost:8000
Frontend API
Port: 3000
URL: http://localhost:3000
To build the project, you need to have Docker open and running, then run the following command from the project's root directory (where docker-compose.yaml is located) in a terminal (it builds both frontend and backend):
docker-compose build
To start the services you run:
docker-compose up -d
If you make changes and they aren’t reflected in the Docker container, you can run the following:
docker-compose down
docker-compose up -d –build	
If you need to see the logs, you can run
docker-compose logs -f
Dependencies:
- Backend requirements, per requirements.txt:
﻿annotated-types==0.7.0, anyio==4.11.0, certifi==2025.10.5, click==8.3.0, colorama==0.4.6, dnspython==2.8.0, email-validator==2.3.0, fastapi==0.118.0, fastapi-cli==0.0.13, fastapi-cloud-cli==0.3.0, h11==0.16.0, httpcore==1.0.9, httptools==0.6.4, httpx==0.28.1, idna==3.10, iniconfig==2.3.0, Jinja2==3.1.6, markdown-it-py==4.0.0, MarkupSafe==3.0.3, mdurl==0.1.2, mysql-connector-python==9.5.0, packaging==25.0, pluggy==1.6.0, pydantic==2.11.10, pydantic_core==2.33.2, Pygments==2.19.2, pytest==8.4.2, pytest-mock==3.15.1, python-dotenv==1.1.1, python-multipart==0.0.20, PyYAML==6.0.3, rich==14.1.0, rich-toolkit==0.15.1, rignore==0.7.0, sentry-sdk==2.40.0, shellingham==1.5.4, sniffio==1.3.1, starlette==0.48.0, typer==0.19.2, typing-inspection==0.4.2, typing_extensions==4.15.0, urllib3==2.5.0, uvicorn==0.37.0, watchfiles==1.1.0, websockets==15.0.1
 	- Frontend Requirements:
Node.Js==Latest, Next.js==Latest, react-google-recaptcha==Latest


Maintenance Requirements:


Account credentials:
User Seeded with orders
Id = 1
Email = demo@example.com
Password = demo
Sample Admin:
Id = 9151
Email = admin@admin.com
Password = password
Database management procedures
The backend is currently seeded with data from our sample dataset. This includes a number of products, but also sample users and reviews who were required for continuity. When deploying this backend, it may be desirable to replace this sample data with actual data instead, as these sample accounts lack secure passwords. The user accounts can be safely removed without causing problems.


Configuration of external APIs or service
Frontend public key for reCaptcha is available in app/components/loginModal.tsx at line 109, or in the docker-compose file. This is not securely stored, and should be replaced with a freshly generated API key before deployment.

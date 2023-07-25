# secureChatApp

## Table of Contents

- [Project Description](#project-description)
- [Project Structure](#project-structure)
- [Dependencies](#dependencies)
- [Usage](#usage)
- [Output](#output)
- [About the Author](#about-the-author)
- [License](#license)

## Project Description

secureChatApp is a secure web chat application that uses advanced asymmetric encryption techniques to secure messages, ensuring utmost privacy and confidentiality. The application is built using Python for backend logic, HTML5 for structure, and CSS for styling. The server-side logic is handled by Flask, a lightweight and robust web framework for Python. Data security is further enhanced with itsdangerous, a Python library to deal with JSON Web Signatures and encryption. Cachelib is used for caching functionalities, while Flask-Session manages users' sessions. Blinker provides a fast dispatching system that allows your application to send signals and respond to them.

## Project Structure

The project is organized into several directories, each containing specific components of the application:

- `auth/`: This directory contains the authentication logic for the application.
- `encryption/`: This directory contains the encryption logic for the application.
- `database/`: This directory contains the database models and operations for the application.
- `routes/`: This directory contains the routing logic for the application.
- `static/` and `templates/`: These directories contain the front-end components of the application.

The root directory also contains several important files:

- `app.py`: This is the entry point of the application.
- `create_app.py`: This script creates a new instance of the Flask app with necessary configurations and blueprints.

## Dependencies

The application requires the following Python libraries:

- blinker==1.6.2
- cachelib==0.10.2
- click==8.1.6
- Flask==2.3.2
- Flask-Session==0.5.0
- itsdangerous==2.1.2
- Jinja2==3.1.2
- MarkupSafe==2.1.3
- scapy==2.5.0
- Werkzeug==2.3.6

# Dependencies can be installed by using the requirements.txt

```bash
cd dir_to_proj
pip install -r requirements.txt
```

## Usage

You can run the application by executing the `app.py` script:

```bash 
python app.py --host 127.0.0.1 --port 5000
```


## Output
The application will start a local server that serves the secureChatApp on the specified host and port.

## About the Author
Aditya Varma is a computer science graduate from the University of Wollongong. He has a keen interest in AI, cybersecurity, systems analysis, and web development.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

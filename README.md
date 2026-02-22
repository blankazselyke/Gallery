# Cloud-Based Photo Album Application

## Project Description
This project is a web-based photo album application developed using the Django framework. The main goal of the application is to provide a platform where users can register, log in, and manage their own photo collections in a cloud environment. The application was designed with cloud deployment (PaaS) in mind, ensuring that it can handle multiple users and store data efficiently.

The system allows users to upload images with custom titles. Once uploaded, the images are displayed in a responsive gallery where users can sort them based on different criteria. Security is a key aspect of the project, as the system ensures that only the owners of the photos can delete their own content.

## Key Features

### User Management
The application includes a complete user authentication system. This includes a sign-up page for new users, a login page for existing members, and a logout function. User passwords are encrypted using Django's built-in hashing algorithms to ensure data security.

### Photo Gallery and Uploads
Authenticated users have the ability to upload image files. Each upload requires a title, which is stored in the database along with the image file path and the upload timestamp. The gallery is built using Bootstrap, making it look professional on both desktop and mobile screens.

### Dynamic Sorting
The application provides an interactive sorting feature. Users can view photos in alphabetical order by their titles. Additionally, they can sort photos by date. This date sorting is a toggle function, meaning it can switch between 'Newest First' and 'Oldest First' to help users find their images easily.

### Secure Deletion
To prevent data loss and unauthorized actions, the delete function is protected. A user can only see the delete button for photos they have uploaded themselves. When clicking delete, a confirmation modal (popup) appears to prevent accidental deletions.



## Technical Architecture

### Backend
The backend is powered by Python and the Django web framework. Django follows the Model-View-Template (MVT) architecture, which helps in keeping the data logic, the business logic, and the user interface separate and organized.

### Frontend
The frontend uses HTML5 and CSS3 for structure and styling. Bootstrap 5.3 is used as the primary CSS framework to ensure a modern look and responsive behavior. JavaScript is used for the Bootstrap Modal components that handle the delete confirmations.

### Database
In the local development phase, the application uses an SQLite database. This is a file-based database that is excellent for development. When the application is moved to a PaaS provider like Google Cloud, this can be easily migrated to a managed SQL service.



## Cloud Deployment (PaaS)
The application is ready to be deployed to a Platform-as-a-Service (PaaS) provider, specifically Google Cloud App Engine.

### Requirements for Deployment
- requirements.txt: This file contains all the necessary Python libraries (Django, Pillow, Gunicorn) that the cloud server needs to install.
- app.yaml: This is the configuration file for Google App Engine, defining the Python runtime and the entry point for the web server.

### Continuous Integration
The project is set up to work with GitHub. By connecting the repository to Google Cloud Build, every time a new version of the code is pushed to the main branch, the cloud provider automatically builds and updates the live application.

## Installation for Local Development

1. Clone the repository from GitHub.
2. Create a virtual environment using 'python -m venv .venv'.
3. Activate the virtual environment.
4. Install the requirements using 'pip install -r requirements.txt'.
5. Run 'python manage.py migrate' to set up the local SQLite database.
6. Use 'python manage.py runserver' to start the application at http://127.0.0.1:8000/.

## Security Implementation
The application follows modern security standards:
- CSRF (Cross-Site Request Forgery) tokens are used on all forms to prevent malicious attacks.
- Access decorators like @login_required are used on views to protect pages from unauthenticated access.
- Permission checks are performed in the backend before any data deletion occurs.

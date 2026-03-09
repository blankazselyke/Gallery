# Cloud-Based Photo Album Application

## Project Description
This project is a web-based photo album application developed using the Django framework. The main goal of the application is to provide a platform where users can register, log in, and manage their own photo collections in a cloud environment. The application was designed with cloud deployment (PaaS) in mind, ensuring that it can handle multiple users and store data efficiently.

The system allows users to upload images with custom titles. Once uploaded, the images are displayed in a responsive gallery where users can sort them based on different criteria. Security is a key aspect of the project, as the system ensures that only the owners of the photos can delete their own content.

The applicationcan be accessed at the following address: [https://gallery-488215.ey.r.appspot.com](https://gallery-488215.ey.r.appspot.com)

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
The application utilizes a dual-database approach depending on the environment:
- **Development**: An SQLite database is used locally for rapid development and testing.
- **Production**: A fully managed, serverless **Neon PostgreSQL** database is used to ensure persistent, scalable, and secure data storage in the cloud.

## Cloud Deployment (PaaS)
The application is deployed to **Google Cloud App Engine (Standard Environment)**. This environment provides automatic scaling and a fully managed Python 3.11 runtime.

### Data Storage and Architecture
Google App Engine Standard uses a **read-only file system** for the application directory (`/workspace`). To overcome this limitation and ensure user data persists across server restarts and deployments, the application integrates external managed cloud services:
- **Persistent Database (Neon)**: The application uses a fully managed, serverless **Neon PostgreSQL** database to ensure persistent, scalable, and secure data storage in the cloud. User credentials, photo metadata, and upload logs are securely stored in this remote instance.
- **Cloud Storage (GCS)**: User-uploaded media files are directly routed to a **Google Cloud Storage** bucket. The bucket is configured with Uniform Bucket-Level Access and public read permissions, allowing direct, fast image serving without the need to generate signed URLs dynamically.

### Security and Secret Management
To adhere to modern DevSecOps standards, sensitive credentials are never hardcoded into the repository:
- **Google Secret Manager**: Production secrets—such as the Django `SECRET_KEY`, Neon `DATABASE_URL`, and the GCS bucket name—are stored securely in Google Secret Manager.
- **IAM Authorization**: The App Engine instance leverages its default service account, which is granted the "Secret Manager Secret Accessor" role, to fetch these secrets programmatically at runtime.

### Deployment Configuration Files
The deployment relies on several key configuration files:
- **`app.yaml`**: Defines the Python 3.11 runtime and sets the `entrypoint` to execute a custom shell script instead of the default server command.
- **`requirements.txt`**: Lists all dependencies, including specific cloud libraries (`dj-database-url`, `psycopg2-binary`, `django-storages[google]`, and `google-cloud-secret-manager`).
- **`cloudbuild.yaml`**: Custom build instructions for Google Cloud Build, configured for secure cloud logging.
- **`startup.sh`**: A streamlined shell script executed on boot that:
    1. Runs `python manage.py migrate` to apply database schemas to the remote PostgreSQL instance.
    2. Programmatically creates a default superuser (`admin`) if it doesn't exist.
    3. Starts the production web server using `gunicorn`.

### Continuous Integration & Deployment (CI/CD)
The project utilizes **Google Cloud Build** connected via a GitHub Trigger:
1. **Trigger**: Any push to the `main` branch on GitHub automatically invokes a new build.
2. **Configuration**: The trigger is configured to use the `cloudbuild.yaml` file from the repository.
3. **Automated Deployment**: Cloud Build executes the `gcloud app deploy` command, ensuring the live version always matches the latest stable code.

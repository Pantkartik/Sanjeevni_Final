Sanjeevni - AI-Powered Personal Health Assistant

Overview

Sanjeevni is a web-based, AI-powered personal health assistant designed to improve patient health management in India. It addresses challenges such as late disease detection, mental health neglect, and fragmented health data by providing a unified platform with smart pill reminders, AI-based health risk predictions, and a stress analysis chatbot—all in one patient-friendly dashboard.

Features

- Smart Pill Reminder: Timely medication reminders with pill supply tracking.
- AI Health Predictions: Upload X-rays, eye scans, and skin photos for AI-based disease risk prediction using models like YOLOv8 and EfficientNet.
- Anxiety and Stress Chatbot: A rule-based chatbot that assesses anxiety levels through pre-designed Q&A dialogs.
- Health Dashboard: Consolidated snapshot of medication adherence, AI predictions, and mental health status.

Problem Statement

- Late detection of diseases such as TB, pneumonia, skin infections, and diabetic eye disease due to lack of early screening.
- Mental health issues like anxiety and depression remain untreated because of stigma and limited affordable support.
- Fragmented patient data making it difficult to track medicines, risks, and mental health in one place.

Technology Stack

- Frontend: React.js
- Backend: Django (Python REST API)
- AI/ML: PyTorch, YOLOv8, EfficientNet, rule-based chatbot engine
- Database: PostgreSQL
- Authentication & Notifications: Firebase
- Deployment: Frontend on Netlify, Backend on Render or Railway
- Version Control & Tools: GitHub, REST APIs

Architecture

- Frontend React application for a patient dashboard and chatbot interface.
- Django backend serving API endpoints for reminders, AI predictions, and chatbot logic.
- AI models handle disease prediction using medical images.
- Firebase manages user authentication and notification delivery.
- PostgreSQL stores patient data, pill schedules, and prediction results.

Getting Started

Prerequisites

- Node.js and npm (for frontend)
- Python 3.x and pip (for backend)
- PostgreSQL
- Firebase account (for auth and notifications)
- Git

Installation

1. Clone the repository:

   git clone https://github.com/your-username/sanjeevni.git
   cd sanjeevni

2. Setup backend:

   cd backend
   pip install -r requirements.txt
   # Configure PostgreSQL and Firebase credentials
   python manage.py migrate
   python manage.py runserver

3. Setup frontend:

   cd ../frontend
   npm install
   npm start

4. Access the app at http://localhost:3000

Usage

- Register or login using Firebase authentication.
- Add your medication schedules and receive timely reminders.
- Upload medical images (X-rays, eye scans, skin photos) for AI health risk predictions.
- Chat with the stress assessment chatbot to evaluate your anxiety levels.
- View a consolidated health dashboard tracking your medication adherence and mental health status.

Development Roadmap

- Phase 1: React frontend, Django backend, Firebase login, basic pill reminder.
- Phase 2: AI health prediction models with demo datasets, stress chatbot development.
- Phase 3: Health dashboard integration, notification enhancements, UI polishing, testing.

Contributing

Contributions are welcome! Please fork the repo, create a feature branch, and submit a pull request. For major changes, open an issue first to discuss your ideas.

Documentation

- API endpoints are documented with Swagger/OpenAPI.
- Codebase is modular with clearly defined components for reusability and extensibility.

References

- WHO — Adherence to Long-Term Therapies: Evidence for Action
- Kaggle — TB Chest X-ray, Skin Disease, and Eye Disease Datasets
- Research on Q&A-based stress chatbots and CBT digital therapy
- NITI Aayog — Telemedicine Practice Guidelines in India
- Official documentation of Firebase, Django, React.js

License

This project is open source and available under the MIT License.

Contact

For questions or feedback, contact the project maintainer at your-kartikpant.kp69@gmail.com.

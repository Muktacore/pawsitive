🐾 Pawsitive
Connecting paws and people — share moments, find homes, spread pawsitivity.

Pawsitive is a pet community web application built with Python, Flask, SQLite, HTML, CSS, and JavaScript. It provides a shared space for pet owners and animal lovers to connect, share pet-related moments, keep track of their pets, and discover animals listed for adoption.
🌟 About the Project
Pets bring people together, but pet owners and animal lovers need an easy way to share experiences, stay connected, and help animals find homes. Pawsitive aims to bring these activities into one simple web platform.

Users can create an account, publish posts with photos and captions, interact with posts through likes and comments, maintain information about their pets, and browse or publish pet adoption listings.
✨ Features
- User registration and login – Create an account and sign in securely using password hashing.
- Personal profiles – View and update profile information, including a profile photo and bio.
- Community feed – Share photos and captions and browse posts from other users.
- Likes and comments – Interact with community posts.
- My Pets – Add and view pet details such as name, breed, age, birthday, vaccination, deworming, and veterinarian information.
- Pet adoption listings – Browse available adoption posts and publish a listing with pet details, contact information, location, and a photo.
- Account and content management – Delete your own posts, pet records, adoption listings, or account.
- Dark mode – Switch between light and dark themes, with the selected preference saved in the browser.
- Terms and privacy pages – View the application's terms and privacy information pages.
🛠️ Tech Stack
Technology	Purpose
Python	Main programming language and backend logic
Flask	Web framework and application routing
SQLite	Database for users, posts, pets, adoption listings, likes, and comments
HTML5	Page structure and templates
CSS3	Styling and responsive presentation
JavaScript	Interface interactions and theme switching
Werkzeug	Password hashing and secure filename handling
Pillow (PIL)	Image processing for profile pictures


📁 Project Structure
pawsitive-main/
├── app.py
├── .gitignore
├── static/
│   ├── logo.png
│   ├── style.css
│   ├── js/
│   │   ├── theme.js
│   │   └── ui.js
│   └── uploads/
│       └── .gitkeep
└── templates/
    ├── index.html
    ├── login.html
    ├── register.html
    ├── feed.html
    ├── profile.html
    ├── view_profile.html
    ├── settings.html
    ├── create-post.html
    ├── mypets.html
    ├── add-mypet.html
    ├── adoptions.html
    ├── add-adoption.html
    ├── privacy.html
    └── terms.html
What are these folders?
- app.py – Contains the Flask application, routes, database setup, authentication, and application logic.
- templates/ – Contains the HTML pages rendered by Flask using its Jinja template engine.
- static/ – Stores CSS, JavaScript, the application logo, and uploaded images.
- static/js/ – Contains JavaScript for interface interactions and dark mode.
- static/uploads/ – Stores uploaded profile pictures, post images, pet photos, and adoption images.
- .gitignore – Excludes local databases, uploaded files, Python cache files, virtual environments, and environment files from Git.
⚙️ Getting Started
Follow these steps to run Pawsitive on your local computer.
1. Prerequisites
Make sure you have installed:
- Python 3
- pip (Python package installer)
- Git (optional, for cloning the repository)
2. Clone the repository
git clone <repository-url>
cd pawsitive-main
If you have downloaded the ZIP file instead, extract it and open the project folder in your terminal.
3. Create a virtual environment
python -m venv venv
Activate it:

Windows (PowerShell):
.\venv\Scripts\Activate.ps1
Windows (Command Prompt):
venv\Scripts\activate
macOS / Linux:
source venv/bin/activate
4. Install dependencies
The project currently does not include a requirements.txt file. Install the packages used by the application:
pip install Flask Pillow
5. Run the application
python app.py
Open the local address shown in your terminal (by default):
http://127.0.0.1:5000/
The SQLite database (pawsitive.db) and required database tables are created automatically when the application starts for the first time.
🗄️ Database
Pawsitive uses SQLite for storing application data. The application initializes these tables:
- users – User accounts and profile information.
- posts – Community posts and their captions.
- mypets – Pet information saved by users.
- adoptions – Pet adoption listings and contact details.
- likes – Likes associated with community posts.
- comments – Comments added to posts.
- reminders – A database table reserved for pet reminder information.
The database file is generated locally and is excluded from Git through .gitignore.
🔒 Security and Deployment Notes
- User passwords are stored as password hashes using Werkzeug rather than as plain text.
- Database queries use parameterized statements in the application's main data operations.
- Before deploying publicly, replace the placeholder Flask secret key with a strong secret stored in an environment variable.
- Disable Flask debug mode in production.
- Add appropriate validation and restrictions for uploaded file types and sizes before accepting public uploads.
- Review account-deletion and related-record handling before production use.
🚀 Future Improvements
Potential improvements for future versions include:
- Pet vaccination and veterinary appointment reminders with notifications.
- Adoption request and application workflows.
- Search and filters for adoption listings by location, breed, and other details.
- Improved image upload validation and moderation.
- More accessibility and mobile usability enhancements.
- Automated tests and deployment configuration.
🤝 Contributing
Contributions, suggestions, and bug reports are welcome. If you would like to improve Pawsitive, you can fork the repository, create a branch, make your changes, and submit a pull request.
❤️ Our Goal
Pawsitive is built around a simple idea: every paw deserves care, connection, and a loving home.

Let's make the digital world a little more pawsitive! 🐶🐱

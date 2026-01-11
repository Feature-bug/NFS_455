# 📚 Library Management System

A modern, full-stack Library Management System with CRUD operations using Flask (Python) and MongoDB Atlas.

## 🚀 Features

- ✅ Complete CRUD Operations (Create, Read, Update, Delete)
- ✅ Modern, responsive UI with smooth animations
- ✅ Search functionality (by title or author)
- ✅ Real-time data validation
- ✅ Error handling and user feedback
- ✅ MongoDB Atlas cloud database
- ✅ RESTful API architecture
- ✅ Book availability tracking
- ✅ Copy management

## 📋 Prerequisites

- Python 3.12.4 (installed ✓)
- MongoDB Atlas account (configured ✓)
- Internet connection

## 🛠️ Installation & Setup

### 1. Install Dependencies

Open terminal in the project folder and run:

```bash
pip install -r requirements.txt
```

### 2. Run the Application

```bash
python app.py
```

The application will start on `http://localhost:5000`

### 3. Access the Application

Open your browser and visit:
- **Frontend UI**: http://localhost:5000
- **API Base URL**: http://localhost:5000/api/books

## 📚 Database Schema

### Books Collection

```json
{
  "_id": "ObjectId",
  "title": "string (required)",
  "author": "string (required)",
  "isbn": "string (required)",
  "publication_date": "string (required, YYYY-MM-DD)",
  "genre": "string (required)",
  "description": "string (optional)",
  "available": "boolean (default: true)",
  "copies": "number (default: 1)",
  "created_at": "ISO datetime",
  "updated_at": "ISO datetime"
}
```

## 🔌 API Endpoints

### 1. Health Check
- **GET** `/api/health`
- **Description**: Check API and database connectivity
- **Response**: 200 OK

### 2. Create Book
- **POST** `/api/books`
- **Body**: JSON (see schema above)
- **Response**: 201 Created

### 3. Get All Books
- **GET** `/api/books`
- **Response**: 200 OK with books array

### 4. Get Single Book
- **GET** `/api/books/<book_id>`
- **Response**: 200 OK with book object

### 5. Update Book
- **PUT** `/api/books/<book_id>`
- **Body**: JSON (partial or full update)
- **Response**: 200 OK

### 6. Delete Book
- **DELETE** `/api/books/<book_id>`
- **Response**: 200 OK

### 7. Search Books
- **GET** `/api/books/search?q=<query>`
- **Response**: 200 OK with matching books

## 🧪 Testing

### Using the Frontend
1. Open http://localhost:5000 in your browser
2. Use the form to add books
3. View all books in the grid below
4. Click "Edit" to modify a book
5. Click "Delete" to remove a book
6. Use search to find specific books

### Using Postman

Import these endpoints:

**Create Book:**
```
POST http://localhost:5000/api/books
Content-Type: application/json

{
  "title": "The Great Gatsby",
  "author": "F. Scott Fitzgerald",
  "isbn": "978-0-7432-7356-5",
  "publication_date": "1925-04-10",
  "genre": "Fiction",
  "description": "A classic American novel",
  "copies": 3,
  "available": true
}
```

**Get All Books:**
```
GET http://localhost:5000/api/books
```

**Get Single Book:**
```
GET http://localhost:5000/api/books/<book_id>
```

**Update Book:**
```
PUT http://localhost:5000/api/books/<book_id>
Content-Type: application/json

{
  "title": "Updated Title",
  "copies": 5
}
```

**Delete Book:**
```
DELETE http://localhost:5000/api/books/<book_id>
```

**Search Books:**
```
GET http://localhost:5000/api/books/search?q=gatsby
```

## 📁 Project Structure

```
LibraryManagementSystem/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── API_DOCUMENTATION.md        # Detailed API docs
├── test_endpoints.py           # Testing script
├── templates/
│   └── index.html             # Frontend UI
└── static/
    └── style.css              # Styling
```

## 🔒 Security Notes

- MongoDB connection string is hardcoded (for development only)
- In production, use environment variables
- Enable CORS only for trusted domains
- Add authentication for production use

## 🌐 Deployment

### For Render.com:

1. Create a new Web Service
2. Connect your GitHub repository
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `gunicorn app:app`
5. Add environment variables if needed

### For Railway.app:

1. Connect GitHub repository
2. Railway auto-detects Flask apps
3. Deploy automatically

## 🐛 Troubleshooting

### Issue: Module not found
**Solution**: Run `pip install -r requirements.txt`

### Issue: Can't connect to MongoDB
**Solution**: Check internet connection and MongoDB Atlas network access settings

### Issue: Port already in use
**Solution**: Change port in `app.py` or kill process using port 5000

## 📸 Screenshots Required for Submission

1. ✅ Data insertion (POST request)
2. ✅ Data retrieval (GET request)
3. ✅ Data update (PUT request)
4. ✅ Data deletion (DELETE request)
5. ✅ Frontend verification

## 👥 Team Information

- **Team Name**: [Your Team Name]
- **Platform Used**: Python (Flask) + MongoDB Atlas
- **Task**: Task 1C - Backend CRUD Application

## 📄 License

This project is created for educational purposes.

## 🤝 Support

For issues or questions, please create an issue in the repository.

---

**Built with ❤️ using Flask and MongoDB**
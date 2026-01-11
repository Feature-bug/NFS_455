from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

# MongoDB Configuration
MONGO_URI = "mongodb+srv://ishangmcsb2428_db_user:o8m08eStrl0f4kYw@database.xfdpktq.mongodb.net/?appName=Database"
client = MongoClient(MONGO_URI)
db = client['library_management']
books_collection = db['books']

# Helper function to serialize MongoDB documents
def serialize_book(book):
    book['_id'] = str(book['_id'])
    return book

# Route: Home page (serves frontend)
@app.route('/')
def index():
    return render_template('index.html')

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    try:
        # Test database connection
        client.admin.command('ping')
        return jsonify({
            'status': 'healthy',
            'database': 'connected',
            'timestamp': datetime.utcnow().isoformat()
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'database': 'disconnected',
            'error': str(e)
        }), 500

# API Route: Create a new book (CREATE)
@app.route('/api/books', methods=['POST'])
def create_book():
    try:
        data = request.get_json()
        
        # Validation
        required_fields = ['title', 'author', 'isbn', 'publication_date', 'genre']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'error': f'{field} is required'}), 400
        
        # Create book document
        book = {
            'title': data['title'],
            'author': data['author'],
            'isbn': data['isbn'],
            'publication_date': data['publication_date'],
            'genre': data['genre'],
            'description': data.get('description', ''),
            'available': data.get('available', True),
            'copies': data.get('copies', 1),
            'created_at': datetime.utcnow().isoformat(),
            'updated_at': datetime.utcnow().isoformat()
        }
        
        # Insert into database
        result = books_collection.insert_one(book)
        book['_id'] = str(result.inserted_id)
        
        return jsonify({
            'message': 'Book created successfully',
            'book': book
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# API Route: Get all books (READ)
@app.route('/api/books', methods=['GET'])
def get_all_books():
    try:
        books = list(books_collection.find())
        books = [serialize_book(book) for book in books]
        
        return jsonify({
            'message': 'Books retrieved successfully',
            'count': len(books),
            'books': books
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# API Route: Get single book by ID (READ)
@app.route('/api/books/<book_id>', methods=['GET'])
def get_book(book_id):
    try:
        if not ObjectId.is_valid(book_id):
            return jsonify({'error': 'Invalid book ID'}), 400
        
        book = books_collection.find_one({'_id': ObjectId(book_id)})
        
        if not book:
            return jsonify({'error': 'Book not found'}), 404
        
        return jsonify({
            'message': 'Book retrieved successfully',
            'book': serialize_book(book)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# API Route: Update book by ID (UPDATE)
@app.route('/api/books/<book_id>', methods=['PUT'])
def update_book(book_id):
    try:
        if not ObjectId.is_valid(book_id):
            return jsonify({'error': 'Invalid book ID'}), 400
        
        data = request.get_json()
        
        # Check if book exists
        existing_book = books_collection.find_one({'_id': ObjectId(book_id)})
        if not existing_book:
            return jsonify({'error': 'Book not found'}), 404
        
        # Update fields
        update_data = {}
        allowed_fields = ['title', 'author', 'isbn', 'publication_date', 'genre', 'description', 'available', 'copies']
        
        for field in allowed_fields:
            if field in data:
                update_data[field] = data[field]
        
        update_data['updated_at'] = datetime.utcnow().isoformat()
        
        # Update in database
        books_collection.update_one(
            {'_id': ObjectId(book_id)},
            {'$set': update_data}
        )
        
        # Get updated book
        updated_book = books_collection.find_one({'_id': ObjectId(book_id)})
        
        return jsonify({
            'message': 'Book updated successfully',
            'book': serialize_book(updated_book)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# API Route: Delete book by ID (DELETE)
@app.route('/api/books/<book_id>', methods=['DELETE'])
def delete_book(book_id):
    try:
        if not ObjectId.is_valid(book_id):
            return jsonify({'error': 'Invalid book ID'}), 400
        
        # Check if book exists
        book = books_collection.find_one({'_id': ObjectId(book_id)})
        if not book:
            return jsonify({'error': 'Book not found'}), 404
        
        # Delete from database
        books_collection.delete_one({'_id': ObjectId(book_id)})
        
        return jsonify({
            'message': 'Book deleted successfully',
            'book_id': book_id
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# API Route: Search books by title or author
@app.route('/api/books/search', methods=['GET'])
def search_books():
    try:
        query = request.args.get('q', '')
        
        if not query:
            return jsonify({'error': 'Search query is required'}), 400
        
        # Search in title and author fields
        books = list(books_collection.find({
            '$or': [
                {'title': {'$regex': query, '$options': 'i'}},
                {'author': {'$regex': query, '$options': 'i'}}
            ]
        }))
        
        books = [serialize_book(book) for book in books]
        
        return jsonify({
            'message': 'Search completed',
            'count': len(books),
            'books': books
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
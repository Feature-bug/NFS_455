"""
API Testing Script for Library Management System
Run this after starting the Flask application to test all endpoints
"""

import requests
import json
from datetime import datetime

# Base URL
BASE_URL = "http://localhost:5000/api"

# Color codes for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_header(text):
    print(f"\n{BLUE}{'='*60}")
    print(f"{text}")
    print(f"{'='*60}{RESET}\n")

def print_success(text):
    print(f"{GREEN}✓ {text}{RESET}")

def print_error(text):
    print(f"{RED}✗ {text}{RESET}")

def print_info(text):
    print(f"{YELLOW}ℹ {text}{RESET}")

def test_health_check():
    """Test the health check endpoint"""
    print_header("Test 1: Health Check")
    
    try:
        response = requests.get(f"{BASE_URL}/health")
        
        if response.status_code == 200:
            data = response.json()
            print_success(f"Health check passed")
            print_info(f"Status: {data['status']}")
            print_info(f"Database: {data['database']}")
            return True
        else:
            print_error(f"Health check failed with status {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Health check error: {str(e)}")
        return False

def test_create_book():
    """Test creating a new book"""
    print_header("Test 2: Create Book (POST)")
    
    book_data = {
        "title": "Test Book - Python Testing",
        "author": "Test Author",
        "isbn": "978-0-123-45678-9",
        "publication_date": "2024-01-01",
        "genre": "Technology",
        "description": "A test book for API testing",
        "copies": 5,
        "available": True
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/books",
            json=book_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 201:
            data = response.json()
            book_id = data['book']['_id']
            print_success("Book created successfully")
            print_info(f"Book ID: {book_id}")
            print_info(f"Title: {data['book']['title']}")
            return book_id
        else:
            print_error(f"Failed to create book: {response.json()}")
            return None
    except Exception as e:
        print_error(f"Create book error: {str(e)}")
        return None

def test_get_all_books():
    """Test retrieving all books"""
    print_header("Test 3: Get All Books (GET)")
    
    try:
        response = requests.get(f"{BASE_URL}/books")
        
        if response.status_code == 200:
            data = response.json()
            print_success("Books retrieved successfully")
            print_info(f"Total books: {data['count']}")
            
            if data['count'] > 0:
                print_info("Sample book titles:")
                for book in data['books'][:3]:  # Show first 3 books
                    print(f"  • {book['title']} by {book['author']}")
            return True
        else:
            print_error(f"Failed to get books: {response.json()}")
            return False
    except Exception as e:
        print_error(f"Get books error: {str(e)}")
        return False

def test_get_single_book(book_id):
    """Test retrieving a single book"""
    print_header("Test 4: Get Single Book (GET)")
    
    if not book_id:
        print_error("No book ID provided")
        return False
    
    try:
        response = requests.get(f"{BASE_URL}/books/{book_id}")
        
        if response.status_code == 200:
            data = response.json()
            book = data['book']
            print_success("Book retrieved successfully")
            print_info(f"Title: {book['title']}")
            print_info(f"Author: {book['author']}")
            print_info(f"ISBN: {book['isbn']}")
            print_info(f"Genre: {book['genre']}")
            print_info(f"Copies: {book['copies']}")
            print_info(f"Available: {book['available']}")
            return True
        else:
            print_error(f"Failed to get book: {response.json()}")
            return False
    except Exception as e:
        print_error(f"Get single book error: {str(e)}")
        return False

def test_update_book(book_id):
    """Test updating a book"""
    print_header("Test 5: Update Book (PUT)")
    
    if not book_id:
        print_error("No book ID provided")
        return False
    
    update_data = {
        "title": "Test Book - Updated Title",
        "copies": 10,
        "available": False
    }
    
    try:
        response = requests.put(
            f"{BASE_URL}/books/{book_id}",
            json=update_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            book = data['book']
            print_success("Book updated successfully")
            print_info(f"New title: {book['title']}")
            print_info(f"New copies: {book['copies']}")
            print_info(f"Available: {book['available']}")
            return True
        else:
            print_error(f"Failed to update book: {response.json()}")
            return False
    except Exception as e:
        print_error(f"Update book error: {str(e)}")
        return False

def test_search_books():
    """Test searching books"""
    print_header("Test 6: Search Books (GET)")
    
    search_query = "Test"
    
    try:
        response = requests.get(f"{BASE_URL}/books/search?q={search_query}")
        
        if response.status_code == 200:
            data = response.json()
            print_success(f"Search completed for query: '{search_query}'")
            print_info(f"Found {data['count']} book(s)")
            
            if data['count'] > 0:
                print_info("Matching books:")
                for book in data['books']:
                    print(f"  • {book['title']} by {book['author']}")
            return True
        else:
            print_error(f"Search failed: {response.json()}")
            return False
    except Exception as e:
        print_error(f"Search error: {str(e)}")
        return False

def test_delete_book(book_id):
    """Test deleting a book"""
    print_header("Test 7: Delete Book (DELETE)")
    
    if not book_id:
        print_error("No book ID provided")
        return False
    
    try:
        response = requests.delete(f"{BASE_URL}/books/{book_id}")
        
        if response.status_code == 200:
            data = response.json()
            print_success("Book deleted successfully")
            print_info(f"Deleted book ID: {data['book_id']}")
            return True
        else:
            print_error(f"Failed to delete book: {response.json()}")
            return False
    except Exception as e:
        print_error(f"Delete book error: {str(e)}")
        return False

def test_error_handling():
    """Test error handling"""
    print_header("Test 8: Error Handling")
    
    # Test 1: Invalid book ID
    print_info("Testing invalid book ID...")
    try:
        response = requests.get(f"{BASE_URL}/books/invalid_id")
        if response.status_code == 400:
            print_success("Invalid ID handled correctly (400 Bad Request)")
        else:
            print_error(f"Unexpected status code: {response.status_code}")
    except Exception as e:
        print_error(f"Error test failed: {str(e)}")
    
    # Test 2: Non-existent book
    print_info("Testing non-existent book...")
    try:
        response = requests.get(f"{BASE_URL}/books/507f1f77bcf86cd799439011")
        if response.status_code == 404:
            print_success("Non-existent book handled correctly (404 Not Found)")
        else:
            print_error(f"Unexpected status code: {response.status_code}")
    except Exception as e:
        print_error(f"Error test failed: {str(e)}")
    
    # Test 3: Missing required fields
    print_info("Testing missing required fields...")
    try:
        response = requests.post(
            f"{BASE_URL}/books",
            json={"title": "Incomplete Book"},
            headers={"Content-Type": "application/json"}
        )
        if response.status_code == 400:
            print_success("Missing fields handled correctly (400 Bad Request)")
        else:
            print_error(f"Unexpected status code: {response.status_code}")
    except Exception as e:
        print_error(f"Error test failed: {str(e)}")
    
    return True

def run_all_tests():
    """Run all API tests"""
    print(f"{BLUE}╔═══════════════════════════════════════════════════════════╗")
    print(f"║  Library Management System - API Testing Suite           ║")
    print(f"║  Testing all CRUD operations                              ║")
    print(f"╚═══════════════════════════════════════════════════════════╝{RESET}\n")
    
    results = {
        "passed": 0,
        "failed": 0
    }
    
    # Test 1: Health Check
    if test_health_check():
        results["passed"] += 1
    else:
        results["failed"] += 1
        print_error("Server is not running or database is disconnected!")
        return
    
    # Test 2: Create Book
    book_id = test_create_book()
    if book_id:
        results["passed"] += 1
    else:
        results["failed"] += 1
    
    # Test 3: Get All Books
    if test_get_all_books():
        results["passed"] += 1
    else:
        results["failed"] += 1
    
    # Test 4: Get Single Book
    if test_get_single_book(book_id):
        results["passed"] += 1
    else:
        results["failed"] += 1
    
    # Test 5: Update Book
    if test_update_book(book_id):
        results["passed"] += 1
    else:
        results["failed"] += 1
    
    # Test 6: Search Books
    if test_search_books():
        results["passed"] += 1
    else:
        results["failed"] += 1
    
    # Test 7: Delete Book
    if test_delete_book(book_id):
        results["passed"] += 1
    else:
        results["failed"] += 1
    
    # Test 8: Error Handling
    if test_error_handling():
        results["passed"] += 1
    else:
        results["failed"] += 1
    
    # Print summary
    print_header("Test Summary")
    print(f"{GREEN}Passed: {results['passed']}{RESET}")
    print(f"{RED}Failed: {results['failed']}{RESET}")
    print(f"Total: {results['passed'] + results['failed']}\n")
    
    if results['failed'] == 0:
        print(f"{GREEN}🎉 All tests passed successfully!{RESET}\n")
    else:
        print(f"{YELLOW}⚠ Some tests failed. Check the output above.{RESET}\n")

if __name__ == "__main__":
    print_info("Make sure the Flask application is running on http://localhost:5000")
    print_info("Press Enter to start testing...")
    input()
    
    run_all_tests()
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Enhanced Flask REST API Example
===============================

This script demonstrates a Flask-based RESTful web service with full error handling,
logging, and persistent storage via SQLite. Available endpoints:

  GET    /contacts              -- List all contacts
  POST   /contacts              -- Create a new contact
  GET    /contacts/<id>         -- Retrieve a specific contact
  PUT    /contacts/<id>         -- Update an existing contact
  DELETE /contacts/<id>         -- Delete a contact

Each handler is wrapped with a decorator to catch database and server errors,
and all actions are logged to both a file and the console.

Usage:
  $ python enhanced_flask_api.py
  Then open http://localhost:5000/contacts in your browser or via curl.
"""

Running in Warp Terminal:
1. Open Warp and navigate to your project directory:
     ```bash
     cd /path/to/your/script
     ```
2. (Optional) Create and activate a virtual environment:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
3. Install dependencies:
     ```bash
     pip install flask
     ```
4. Start the Flask server:
     ```bash
     python enhanced_flask_api.py
     ```
5. Warp will display logs in the active pane. To test an endpoint, open a new pane (Option+Enter) and run:
     ```bash
     curl http://localhost:5000/contacts
     ```
6. You can split panes, search command history, and use Warp’s workflow commands for efficient management.

"""

from flask import Flask, request, jsonify
import sqlite3
import logging
import os

app = Flask(__name__)

# Configure logging to file and console
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Path to the SQLite database file
DB_PATH = 'contacts.db'


def get_db():
    """
    Open a new database connection. Use row_factory to access columns by name.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """
    Initialize the database file if it does not exist, creating the contacts table.
    """
    logger.info("Initializing database")
    if not os.path.exists(DB_PATH):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS contacts (
                id    INTEGER PRIMARY KEY AUTOINCREMENT,
                name  TEXT    NOT NULL,
                email TEXT    NOT NULL,
                phone TEXT
            )
        ''')
        conn.commit()
        conn.close()
        logger.info("Database initialized successfully")
    else:
        logger.info("Database already exists")

# Perform initial database setup
init_db()


def handle_exceptions(func):
    """
    Decorator to wrap route handlers in try/except blocks, catching
    SQLite errors and general exceptions to return JSON error responses.
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except sqlite3.Error as e:
            logger.error(f"Database error: {e}")
            return jsonify({"error": f"Database error: {e}"}), 500
        except Exception as e:
            logger.error(f"Server error: {e}")
            return jsonify({"error": f"Server error: {e}"}), 500
    wrapper.__name__ = func.__name__
    return wrapper


@app.route('/contacts', methods=['GET'])
@handle_exceptions
def get_contacts():
    """Retrieve and return all contacts as JSON."""
    logger.info("Fetching all contacts")
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM contacts')
    contacts = [dict(row) for row in cursor.fetchall()]
    conn.close()

    logger.info(f"Returning {len(contacts)} contacts")
    return jsonify(contacts)


@app.route('/contacts', methods=['POST'])
@handle_exceptions
def add_contact():
    """Add a new contact with required fields 'name' and 'email'."""
    logger.info("Adding new contact")
    data = request.get_json()

    # Validate input
    if not data or 'name' not in data or 'email' not in data:
        logger.warning("Invalid request payload")
        return jsonify({"error": "Missing required fields: name, email"}), 400

    name = data['name']
    email = data['email']
    phone = data.get('phone', '')

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO contacts (name, email, phone) VALUES (?, ?, ?)',
        (name, email, phone)
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()

    logger.info(f"Contact created with ID: {new_id}")
    return jsonify({'message': 'Contact created', 'id': new_id}), 201


@app.route('/contacts/<int:contact_id>', methods=['GET'])
@handle_exceptions
def get_contact(contact_id):
    """Retrieve a single contact by its ID."""
    logger.info(f"Fetching contact ID: {contact_id}")
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM contacts WHERE id = ?', (contact_id,))
    row = cursor.fetchone()
    conn.close()

    if row is None:
        logger.warning(f"Contact ID {contact_id} not found")
        return jsonify({"error": "Contact not found"}), 404

    logger.info(f"Returning contact ID: {contact_id}")
    return jsonify(dict(row))


@app.route('/contacts/<int:contact_id>', methods=['PUT'])
@handle_exceptions
def update_contact(contact_id):
    """Update fields of an existing contact. At least one field must be provided."""
    logger.info(f"Updating contact ID: {contact_id}")
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM contacts WHERE id = ?', (contact_id,))
    row = cursor.fetchone()

    if row is None:
        conn.close()
        logger.warning(f"Contact ID {contact_id} not found")
        return jsonify({"error": "Contact not found"}), 404

    data = request.get_json()
    if not data:
        conn.close()
        logger.warning("Invalid request payload for update")
        return jsonify({"error": "No data provided for update"}), 400

    # Prepare updated values, defaulting to existing ones
    current = dict(row)
    name  = data.get('name',  current['name'])
    email = data.get('email', current['email'])
    phone = data.get('phone', current['phone'])

    cursor.execute(
        'UPDATE contacts SET name = ?, email = ?, phone = ? WHERE id = ?',
        (name, email, phone, contact_id)
    )
    conn.commit()
    conn.close()

    logger.info(f"Contact ID {contact_id} updated successfully")
    return jsonify({'message': 'Contact updated'})


@app.route('/contacts/<int:contact_id>', methods=['DELETE'])
@handle_exceptions
def delete_contact(contact_id):
    """Delete the contact with the given ID."""
    logger.info(f"Deleting contact ID: {contact_id}")
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM contacts WHERE id = ?', (contact_id,))
    row = cursor.fetchone()

    if row is None:
        conn.close()
        logger.warning(f"Contact ID {contact_id} not found for deletion")
        return jsonify({"error": "Contact not found"}), 404

    cursor.execute('DELETE FROM contacts WHERE id = ?', (contact_id,))
    conn.commit()
    conn.close()

    logger.info(f"Contact ID {contact_id} deleted")
    return jsonify({'message': 'Contact deleted'})


# Global error handlers
@app.errorhandler(400)
def handle_bad_request(e):
    logger.warning(f"400 Bad Request: {request.path}")
    return jsonify({'error': 'Bad request'}), 400

@app.errorhandler(404)
def handle_not_found(e):
    logger.warning(f"404 Not Found: {request.path}")
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(405)
def handle_method_not_allowed(e):
    logger.warning(f"405 Method Not Allowed: {request.method} {request.path}")
    return jsonify({'error': 'Method not allowed'}), 405

@app.errorhandler(500)
def handle_server_error(e):
    logger.error(f"500 Internal Server Error: {e}")
    return jsonify({'error': 'Internal server error'}), 500

# Catch-all for undefined routes
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    logger.warning(f"Attempted access to undefined route: /{path}")
    return jsonify({'error': 'Route not found'}), 404

if __name__ == '__main__':
    logger.info("Starting Flask application...")
    app.run(debug=True)
    logger.info("Flask application stopped.")

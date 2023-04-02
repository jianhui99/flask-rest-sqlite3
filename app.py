import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

def db_connection():
    conn = None
    try:
        conn = sqlite3.connect('books.sqlite3')
    except sqlite3.error as e:
        print(e)
    return conn


@app.route('/books', methods=['GET', 'POST'])
def books():
    conn = db_connection()
    cursor = conn.cursor()

    if request.method == 'GET':
        cursor = cursor.execute('SELECT * FROM books')
        books = [
            dict(id=row[0], title=row[1], author=row[2], read=row[3])
            for row in cursor.fetchall()
        ]
        if books is not None:
            return jsonify({
                "status": "success",
                "books": books
            })
        else:
            return jsonify({
                "status": "error",
                "message": "No books found."
            }), 404
        
    elif request.method == 'POST':
        data = request.get_json()

        if data is None:
            return jsonify({
                "status": "error",
                "message": "Please provide the data."
            }), 400
        
        if 'title' not in data:
            return jsonify({
                "status": "error",
                "message": "Please provide the title."
            }), 400
        
        if 'author' not in data:
            return jsonify({
                "status": "error",
                "message": "Please provide the author."
            }), 400
        
        if 'read' not in data:
            return jsonify({
                "status": "error",
                "message": "Please provide the read status."
            }), 400
        
        
        sql_query = """INSERT INTO books (title, author, read)
                          VALUES (?, ?, ?)"""
        cursor.execute(sql_query, (data['title'], data['author'], data['read']))
        conn.commit()
        return jsonify({
            "status": "success",
            "message": "Book added successfully."
        })
    
    else:
        return jsonify({
            "status": "error",
            "message": "Invalid request method."
        }), 404
    

@app.route('/books/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def book(id):
    conn = db_connection()
    cursor = conn.cursor()
    book = cursor.execute('SELECT * FROM books WHERE id=?', (id,))
    book = cursor.fetchone()

    if book is None:
        return jsonify({
            "status": "error",
            "message": "Book not found."
        }), 404
    
    if request.method == 'GET':
        book = {
            "id": book[0],
            "title": book[1],
            "author": book[2],
            "read": book[3]
        }

        return jsonify({
            "status": "success",
            "book": book
        })
        
    elif request.method == 'PUT':
        data = request.get_json()

        if data is None:
            return jsonify({
                "status": "error",
                "message": "Please provide the data."
            }), 400
        
        if 'title' not in data:
            return jsonify({
                "status": "error",
                "message": "Please provide the title."
            }), 400
        
        if 'author' not in data:
            return jsonify({
                "status": "error",
                "message": "Please provide the author."
            }), 400
        
        if 'read' not in data:
            return jsonify({
                "status": "error",
                "message": "Please provide the read status."
            }), 400
        
        sql_query = """UPDATE books
                            SET title = ?, author = ?, read = ?
                            WHERE id = ?"""
        cursor.execute(sql_query, (data['title'], data['author'], data['read'], id))
        conn.commit()
        return jsonify({
            "status": "success",
            "message": "Book updated successfully."
        })
        
    elif request.method == 'DELETE':
        cursor.execute('DELETE FROM books WHERE id=?', (id,))
        conn.commit()
        return jsonify({
            "status": "success",
            "message": "Book deleted successfully."
        })
        
    else:
        return jsonify({
            "status": "error",
            "message": "Invalid request method."
        }), 404

if __name__ == '__main__':
    app.run(debug=True)

from pymongo import MongoClient
from flask import Flask, jsonify, request

app = Flask(__name__)

#homepage
@app.route('/')
def index():
    return "Homepage!"

#get all the books
@app.route('/books', methods=['GET'])
def get_all_books():
    collection = client.books.booktitles
    output = []

    for q in collection.find():
        output.append({ '_id' : str(q['_id']), 'isbn': q['isbn'], 'title': q['title'], 'author': q['author'], 'description': q['description'],
                        'pubDate': q['pubDate'], 'publisher': q['publisher'], 'language': q['language'], 'pages': q['pages'],
                        'rating': q['rating'], 'rateCount': q['rateCount']})

    return jsonify({'results' : output})

#get books by specified author
@app.route('/books/author/<name>', methods=['GET'])
def get_one_author(name):
    collection = client.books.booktitles
    output = []

    for q in collection.find({'author' : name}):
        output.append({'_id': str(q['_id']), 'isbn': q['isbn'], 'title': q['title'], 'author': q['author'], 'description': q['description'],
                    'pubDate': q['pubDate'], 'publisher': q['publisher'], 'language': q['language'], 'pages': q['pages'],
                    'rating': q['rating'], 'rateCount': q['rateCount']})

    return jsonify({'results' : output})


@app.route('/books/title/<title>', methods=['GET'])
def get_one_title(title):
    collection = client.books.booktitles

    q = collection.find_one({'title' : title})

    if q:
        output = {'_id' : str(q['_id']), 'isbn' : q['isbn'], 'title' : q['title'] ,'author' : q['author'], 'description' : q['description'],
                  'pubDate' : q['pubDate'], 'publisher': q['publisher'], 'language' : q['language'], 'pages' : q['pages'],
                  'rating' : q['rating'], 'rateCount' : q['rateCount']}
    else:
        output = "No results found"

    return jsonify({'results' : output})


@app.route('/books', methods=['POST'])
def add_book():
    collection = client.books.booktitles

    isbn = request.json['isbn']
    title = request.json['title']
    author = request.json['author']
    description = request.json['description']
    pubDate = request.json['pubDate']
    publisher = request.json['publisher']
    language = request.json['language']
    pages = request.json['pages']
    rating = request.json['rating']
    rateCount = request.json['rateCount']

    insert_id = collection.insert({'isbn' : isbn, 'title' : title ,'author' : author, 'description' : description,
                                   'pubDate' : pubDate, 'publisher' : publisher, 'language' : language, 'pages' : pages,
                                   'rating' : rating, 'rateCount' : rateCount})

    ni = collection.find_one({'_id' : insert_id})

    output = {'isbn' : ni['isbn'], 'title' : ni['title'], 'author' : ni['author'],
              'description' : ni['description'], 'pubDate' : ni['pubDate'], 
              'publisher': ni['publisher'], 'language' : ni['language'], 
              'pages' : ni['pages'], 'rating' : ni['rating'], 
              'rateCount' : ni['rateCount']}

    return jsonify({'results' : output})


@app.route('/books/delete/<int:isbn>', methods = ['DELETE'])
def delete_book(isbn):
    collection = client.books.booktitles

    collection.find_one_and_delete({'isbn': isbn})

    return "Ok"


@app.route('/books/update/<int:isbn>/<field>', methods = ['PUT'])
def update_book(isbn,field):
    collection = client.books.booktitles

    collection.update_one({'isbn':isbn},{'$set':{field:request.json[field]}})

    return str(collection.find_one({'isbn':isbn}))

if __name__ == '__main__':
    client = MongoClient()
    app.run(debug=True)
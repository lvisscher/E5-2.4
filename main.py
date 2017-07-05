from pymongo import MongoClient
from mongoengine import *
from flask import Flask, jsonify, request, send_file
import os
from datetime import datetime
from flask_hashing import Hashing
import string
import random
from flask_cors import CORS
from bson.objectid import ObjectId
import re

app = Flask(__name__)
hashing = Hashing(app)
cors = CORS(app)

app.config['UPLOAD_FOLDER'] = '/var/www/html/book-images/'

app.config['ALLOWED_EXTENSIONS'] = set(['png', 'gif', 'jpg'])

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


#homepage
@app.route('/')
def index():
    return "Homepage!"


@app.errorhandler(500)
def internal_error(error):
    return "500"

#################################################################################
#                                                                               #
#                                   BOOK PART                                   #
#                                                                               #
#################################################################################

#get all the books
@app.route('/books', methods=['GET'])
def get_all_books():
    collection = client.bookreviewer.books
    output = []

    for q in collection.find():
        output.append({ '_id' : str(q['_id']), 'isbn': q['isbn'], 'title': q['title'], 'author': q['author'], 'description': q['description'],
                        'pubDate': q['pubDate'], 'publisher': q['publisher'], 'language': q['language'], 'pages': q['pages'],
                        'rating': q['rating'], 'rateCount': q['rateCount'], 'photoPath': q['photoPath']})

    return jsonify({'results' : output})

@app.route('/books/count' , methods=['GET'])
def get_book_count():
    collection = client.bookreviewer.books

    count = collection.count()

    return str(count)

#get all the books
@app.route('/books/page/<pagenr>', methods=['GET'])
def get_page_books(pagenr):
    collection = client.bookreviewer.books
    output = []

    start = int(pagenr) * 24
    end = start + 24

    for q in collection.find()[start:end]:
        output.append({ '_id' : str(q['_id']), 'isbn': q['isbn'], 'title': q['title'], 'author': q['author'], 'description': q['description'],
                        'pubDate': q['pubDate'], 'publisher': q['publisher'], 'language': q['language'], 'pages': q['pages'],
                        'rating': q['rating'], 'rateCount': q['rateCount'], 'photoPath': q['photoPath']})

    return jsonify({'results' : output})

#get all the books
@app.route('/search/books/<query>', methods=['GET'])
def search_books(query):
    collection = client.bookreviewer.books
    output = []
    regex = re.compile(query, re.IGNORECASE)

    for q in collection.find({"title" : regex}):
        output.append({ '_id' : str(q['_id']), 'isbn': q['isbn'], 'title': q['title'], 'author': q['author'], 'description': q['description'],
                        'pubDate': q['pubDate'], 'publisher': q['publisher'], 'language': q['language'], 'pages': q['pages'],
                        'rating': q['rating'], 'rateCount': q['rateCount'], 'photoPath': q['photoPath']})

    return jsonify({'results' : output})

#get all the books
@app.route('/topbooks', methods=['GET'])
def get_top_books():
    collection = client.bookreviewer.books
    output = []

    for q in collection.find()[0:10].sort("rating", -1):
        output.append({ '_id' : str(q['_id']), 'isbn': q['isbn'], 'title': q['title'], 'author': q['author'], 'description': q['description'],
                        'pubDate': q['pubDate'], 'publisher': q['publisher'], 'language': q['language'], 'pages': q['pages'],
                        'rating': q['rating'], 'rateCount': q['rateCount'], 'photoPath': q['photoPath']})

    return jsonify({'results' : output})


#get all the books
@app.route('/lastAdded/books', methods=['GET'])
def get_last_books():
    collection = client.bookreviewer.books
    output = []

    for q in collection.find()[0:10].sort("_id", -1):
        output.append({ '_id' : str(q['_id']), 'isbn': q['isbn'], 'title': q['title'], 'author': q['author'], 'description': q['description'],
                        'pubDate': q['pubDate'], 'publisher': q['publisher'], 'language': q['language'], 'pages': q['pages'],
                        'rating': q['rating'], 'rateCount': q['rateCount'], 'photoPath': q['photoPath']})

    return jsonify({'results' : output})

#get books by specified author
@app.route('/books/author/<name>', methods=['GET'])
def get_one_author(name):
    collection = client.bookreviewer.books
    output = []

    for q in collection.find({'author' : name}):
        output.append({'_id': str(q['_id']), 'isbn': q['isbn'], 'title': q['title'], 'author': q['author'], 'description': q['description'],
                    'pubDate': q['pubDate'], 'publisher': q['publisher'], 'language': q['language'], 'pages': q['pages'],
                    'rating': q['rating'], 'rateCount': q['rateCount']})

    return jsonify({'results' : output})


@app.route('/books/title/<title>', methods=['GET'])
def get_one_title(title):
    collection = client.bookreviewer.books

    q = collection.find_one({'title' : title})

    if q:
        output = {'_id' : str(q['_id']), 'isbn' : q['isbn'], 'title' : q['title'] ,'author' : q['author'], 'description' : q['description'],
                  'pubDate' : q['pubDate'], 'publisher': q['publisher'], 'language' : q['language'], 'pages' : q['pages'],
                  'rating' : q['rating'], 'rateCount' : q['rateCount']}
    else:
        output = "No results found"

    return jsonify({'results' : output})

#get book by isbn number
@app.route('/books/isbn/<isbn>', methods=['GET'])
def get_one_isbn(isbn):
    collection = client.bookreviewer.books

    q = collection.find_one({'isbn' : isbn})

    if q:
        output = {'_id' : str(q['_id']), 'isbn' : q['isbn'], 'title' : q['title'] ,'author' : q['author'], 'description' : q['description'],
                  'pubDate' : q['pubDate'], 'publisher': q['publisher'], 'language' : q['language'], 'pages' : q['pages'],
                  'rating' : q['rating'], 'rateCount' : q['rateCount'], 'photoPath' : q['photoPath']}
    else:
        output = "No results found"

    return jsonify({'results' : output})

@app.route('/books/rid/<rid>', methods=['GET'])
def get_one_book_by_rid(rid):
    collection = client.bookreviewer.books

    q = collection.find_one({'_id' : ObjectId(rid)})

    if q:
        output = {'_id' : str(q['_id']), 'isbn' : q['isbn'], 'title' : q['title'] ,'author' : q['author'], 'description' : q['description'],
                  'pubDate' : q['pubDate'], 'publisher': q['publisher'], 'language' : q['language'], 'pages' : q['pages'],
                  'rating' : q['rating'], 'rateCount' : q['rateCount'], 'photoPath' : q['photoPath']}
    else:
        output = "No results found"

    return jsonify({'results' : output})


@app.route('/books', methods=['POST'])
def add_book():
    collection = client.bookreviewer.books

    token = request.headers['token']
    username = request.headers['username']


    if verify_token(username, token) and is_admin(username):
        file = request.files['bookPhoto']
        originalFilename = file.filename
        filename, file_extension = os.path.splitext(originalFilename)
        saveFilename = request.form['isbn'] + file_extension

        if file and allowed_file(file.filename):
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], saveFilename))
            photoPath = '/book-images/' + saveFilename

        isbn = request.form['isbn']
        title = request.form['title']
        author = request.form['author']
        description = request.form['description']
        pubDate = request.form['pubDate']
        publisher = request.form['publisher']
        language = request.form['language']
        pages = request.form['pages']
        rating = 0
        rateCount = 0

        insert_id = collection.insert({'isbn' : isbn, 'title' : title ,'author' : author, 'description' : description,
                                       'pubDate' : pubDate, 'publisher' : publisher, 'language' : language, 'pages' : pages,
                                       'rating' : rating, 'rateCount' : rateCount, 'photoPath' : photoPath})

        ni = collection.find_one({'_id' : insert_id})

        output = {'isbn' : ni['isbn'], 'title' : ni['title'], 'author' : ni['author'],
                  'description' : ni['description'], 'pubDate' : ni['pubDate'], 
                  'publisher': ni['publisher'], 'language' : ni['language'], 
                  'pages' : ni['pages'], 'rating' : ni['rating'], 
                  'rateCount' : ni['rateCount'], 'photoPath': photoPath}

        return jsonify({'results' : output})

    return "Admin rights needed"


@app.route('/books/delete/<isbn>', methods = ['DELETE'])
def delete_book(isbn):
    collection = client.bookreviewer.books

    token = request.headers['token']
    username = request.headers['username']

    if verify_token(username, token) and is_admin(username):
        collection.find_one_and_delete({'isbn': isbn})
        return "Ok"

    return "Admin rights needed"




@app.route('/books/update/<int:isbn>/<field>', methods = ['PUT'])
def update_book(isbn,field):
    collection = client.bookreviewer.books

    token = request.headers['token']
    username = request.headers['username']

    if verify_token(username, token) and is_admin(username):
        collection.update_one({'isbn':isbn},{'$set':{field:request.json[field]}})
        return str(collection.find_one({'isbn':isbn}))

    return "Admin rights needed"


@app.route('/books/update_rating/<rid>/<rating>', methods = ['PUT'])
def update_rating_book(rid,rating):
    collection = client.bookreviewer.books

    book = collection.find_one({'_id':ObjectId(rid)})
    token = request.headers['token']
    username_header = request.headers['username']

    if (verify_token(username_header, token)):
        count = book['rateCount']
        ratingDB = book['rating']
        total = (count * ratingDB) + float(rating)
        newCount = count + 1
        newRating = total / newCount
        collection.update_one({'_id':ObjectId(rid)},{'$set':{'rateCount':newCount, 'rating':newRating}})
        return str(collection.find_one({'_id':ObjectId(rid)}))
    
    return "No rights" 


@app.route('/books/update_rating_by_isbn/<isbn>/<rating>', methods = ['PUT'])
def update_rating_book_by_isbn(isbn,rating):
    collection = client.bookreviewer.books
    collection2 = client.bookreviewer.users

    book = collection.find_one({'isbn':isbn})
    token = request.headers['token']
    username_header = request.headers['username']

    if (verify_token(username_header, token)):
        collection2.update_one({'username':username_header},{'$push':{"booksRated":isbn}})
        count = book['rateCount']
        ratingDB = book['rating']
        total = (count * ratingDB) + float(rating)
        newCount = count + 1
        newRating = total / newCount
        collection.update_one({'isbn':isbn},{'$set':{'rateCount':newCount, 'rating':newRating}})
        return str(collection.find_one({'isbn':isbn}))
    
    return "No rights" 

    

#################################################################################
#                                                                               #
#                                   USER PART                                   #
#                                                                               #
#################################################################################


#get all the users
@app.route('/users', methods=['GET'])
def get_all_users():
    collection = client.bookreviewer.users
    output = []

    for q in collection.find():
        if 'profilePicture' in q:
            output.append({'username' : q['username'], 'admin' : q['admin'], 'email' : q['email'], 
                'fname' : q['fname'], 'lname' : q['lname'], 'password' : q['password'], 
                'age': q['age'], 'gender' : q['gender'], 'booksRead' : q['booksRead'], 
                'booksRated' : q['booksRated'], 'reviewsRated' : q['reviewsRated'], 'profilePicture' : q['profilePicture']})
        else:
            output.append({'username' : q['username'], 'admin' : q['admin'], 'email' : q['email'], 
                'fname' : q['fname'], 'lname' : q['lname'], 'password' : q['password'], 
                'age': q['age'], 'gender' : q['gender'], 'booksRead' : q['booksRead'], 
                'booksRated' : q['booksRated'], 'reviewsRated' : q['reviewsRated']})

    return jsonify({'results' : output})


#get all the books
@app.route('/search/users/<query>', methods=['GET'])
def search_users(query):
    collection = client.bookreviewer.users
    output = []
    regex = re.compile(query, re.IGNORECASE)

    for q in collection.find({"username" : regex}):
        if 'profilePicture' in q:
            output.append({'username' : q['username'], 'admin' : q['admin'], 'email' : q['email'], 
                'fname' : q['fname'], 'lname' : q['lname'], 'password' : q['password'], 
                'age': q['age'], 'gender' : q['gender'], 'booksRead' : q['booksRead'], 
                'booksRated' : q['booksRated'], 'reviewsRated' : q['reviewsRated'], 'profilePicture' : q['profilePicture']})
        else:
            output.append({'username' : q['username'], 'admin' : q['admin'], 'email' : q['email'], 
                'fname' : q['fname'], 'lname' : q['lname'], 'password' : q['password'], 
                'age': q['age'], 'gender' : q['gender'], 'booksRead' : q['booksRead'], 
                'booksRated' : q['booksRated'], 'reviewsRated' : q['reviewsRated']})

    return jsonify({'results' : output})


@app.route('/users', methods=['POST'])
def add_user():
    collection = client.bookreviewer.users

    username = request.json['username']
    admin = 0
    email = request.json['email']
    fname = request.json['fname']
    lname = request.json['lname']
    hashed_password = hashing.hash_value(request.json['password'], salt='zout')
    age = request.json['age']
    gender = request.json['gender']
    booksRead = []
    booksRated = []
    reviewsRated = []

    insert_id = collection.insert({'username' : username, 'admin' : admin, 'email' : email ,'fname' : fname, 'lname' : lname,
                                   'password' : hashed_password, 'age' : age, 'gender' : gender, 'booksRead' : booksRead,
                                   'booksRated' : booksRated, 'reviewsRated' : reviewsRated})

    ni = collection.find_one({'_id' : insert_id})

    output = {'username' : ni['username'], 'admin' : ni['admin'], 'email' : ni['email'], 
            'fname' : ni['fname'], 'lname' : ni['lname'], 'password' : ni['password'], 
            'age': ni['age'], 'gender' : ni['gender'], 'booksRead' : ni['booksRead'], 
            'booksRated' : ni['booksRated'], 'reviewsRated' : ni['reviewsRated']}

    return jsonify(output)


@app.route('/users/delete/<username>', methods = ['DELETE'])
def delete_user(username):
    collection = client.bookreviewer.users

    token = request.headers['token']
    username_header = request.headers['username']

    if (verify_token(username_header, token) and username == username_header) or (verify_token(username_header, token) and is_admin(username_header)):
        collection.find_one_and_delete({'username': username})
        return "Ok"

    return "No rights to delete user"


@app.route('/users/deletevar/<username>/<field>', methods = ['PUT'])
def delete_variable(username, field):
    collection = client.bookreviewer.users

    token = request.headers['token']
    username_header = request.headers['username']

    if (verify_token(username_header, token) and username == username_header) or (verify_token(username_header, token) and is_admin(username_header)):
        collection.update_one({'username':username},{'$pull': {field:request.json[field]}})
        return str(collection.find_one({'username':username}))
    
    return "No rights for action"
    


@app.route('/users/makeadmin/<username>', methods = ['PUT'])
def make_admin(username):
    collection = client.bookreviewer.users

    token = request.headers['token']
    username_admin = request.headers['username']

    if verify_token(username_admin, token) and is_admin(username_admin):
        collection.update_one({'username':username},{'$set':{'admin' : 1}})
        return str(collection.find_one({'username':username}))

    return "No rights"


@app.route('/users/update/<username>/<field>', methods = ['PUT'])
def update_user_field(username,field):
    collection = client.bookreviewer.users
    
    token = request.headers['token']
    username_header = request.headers['username']

    if (verify_token(username_header, token) and username == username_header) or (verify_token(username_header, token) and is_admin(username_header)):
        if (field == "booksRead" or field == "booksRated" or field == "reviewsRated"):
            collection.update_one({'username':username},{'$push':{field:request.json[field]}})
        elif (field == "password"):
            hashed_password = hash_password(request.json[field])
            collection.update_one({'username':username},{'$set':{field:hashed_password}})
        elif (field == "admin"):
            ######TODOOOOOOO:------
            pass
        else:
            collection.update_one({'username':username},{'$set':{field:request.json[field]}})

        return str(collection.find_one({'username':username}))

    return "No rights for action"


@app.route('/users/update_user', methods = ['PUT'])
def update_user():
    collection = client.bookreviewer.users
    
    token = request.headers['token']
    username_header = request.headers['username']

    email = request.form['email']
    fname = request.form['fname']
    lname = request.form['lname']
    age = request.form['age']
    gender = request.form['gender']

    if (verify_token(username_header, token)):
        collection.update({'username':username_header},{
            '$set':{'email':email, 
            'fname':fname,
            'lname':lname,
            'age':age,
            'gender':gender}})
        return str(collection.find_one({'username':username_header}))

    return "No rights for action"



@app.route('/users/profile_picture', methods = ['POST'])
def update_profile_picture():
    collection = client.bookreviewer.users
    
    token = request.headers['token']
    username_header = request.headers['username']

    if verify_token(username_header, token):
        file = request.files['profilePicture']
        originalFilename = file.filename
        filename, file_extension = os.path.splitext(originalFilename)
        saveFilename = username_header + file_extension


        if file and allowed_file(file.filename):
            file.save(os.path.join('/var/www/html/profile-pictures/', saveFilename))
            photoPath = '/profile-pictures/' + saveFilename
            collection.update_one({'username':username_header},{'$set':{'profilePicture':photoPath}})
            return str(collection.find_one({'username':username_header}))
    
    return "failed"

#get books by specified author
@app.route('/users/username/<name>', methods=['GET'])
def get_one_user(name):
    collection = client.bookreviewer.users
    output = []

    for q in collection.find({'username' : name}):
        if 'profilePicture' in q:
            output.append({'username' : q['username'], 'admin' : q['admin'], 'email' : q['email'], 
                'fname' : q['fname'], 'lname' : q['lname'], 'password' : q['password'], 
                'age': q['age'], 'gender' : q['gender'], 'booksRead' : q['booksRead'], 
                'booksRated' : q['booksRated'], 'reviewsRated' : q['reviewsRated'], 'profilePicture' : q['profilePicture']})
        else:
            output.append({'username' : q['username'], 'admin' : q['admin'], 'email' : q['email'], 
                'fname' : q['fname'], 'lname' : q['lname'], 'password' : q['password'], 
                'age': q['age'], 'gender' : q['gender'], 'booksRead' : q['booksRead'], 
                'booksRated' : q['booksRated'], 'reviewsRated' : q['reviewsRated']})

    return jsonify({'results' : output})




#################################################################################
#                                                                               #
#                                 REVIEW PART                                   #
#                                                                               #
#################################################################################

@app.route('/review/by_isbn/<isbn>', methods=['GET'])
def get_review_by_ISBN(isbn):
    collection = client.bookreviewer.reviews
    output = []

    for ni in collection.find({'reviewOnBook' : isbn}):
        output.append({'_id': str(ni['_id']), 'reviewTitle' : ni['reviewTitle'], 'reviewBy' : ni['reviewBy'], 'content' : ni['content'],
              'rateCount' : ni['rateCount'], 'rating' : ni['rating'], 'reviewOnBook' : ni['reviewOnBook'], 'bookTitle' : ni['bookTitle'],
              'comments': ni['comments'], 'usersRated': ni['usersRated']})

    return jsonify({'results' : output})



@app.route('/review/by_user/<username>', methods=['GET'])
def get_review_by_user(username):
    collection = client.bookreviewer.reviews
    output = []

    for ni in collection.find({'reviewBy' : username}):
        output.append({'_id': str(ni['_id']), 'reviewTitle' : ni['reviewTitle'], 'reviewBy' : ni['reviewBy'], 'content' : ni['content'],
              'rateCount' : ni['rateCount'], 'rating' : ni['rating'], 'reviewOnBook' : ni['reviewOnBook'], 'bookTitle' : ni['bookTitle'],
              'comments': ni['comments'], 'usersRated': ni['usersRated']})

    return jsonify({'results' : output})


@app.route('/review/by_id/<rid>', methods=['GET'])
def get_review_by_ID(rid):
    collection = client.bookreviewer.reviews
    output = []

    for ni in collection.find({'_id' : ObjectId(rid)}):
        output.append({'_id': str(ni['_id']), 'reviewTitle' : ni['reviewTitle'], 'reviewBy' : ni['reviewBy'], 'content' : ni['content'],
              'rateCount' : ni['rateCount'], 'rating' : ni['rating'], 'reviewOnBook' : ni['reviewOnBook'], 'bookTitle' : ni['bookTitle'],
              'comments': ni['comments'], 'usersRated': ni['usersRated']})

    return jsonify({'results' : output})


#get all the books
@app.route('/reviews', methods=['GET'])
def get_all_reviews():
    collection = client.bookreviewer.reviews
    output = []

    for ni in collection.find():
        output.append({'_id': str(ni['_id']), 'reviewTitle' : ni['reviewTitle'], 'reviewBy' : ni['reviewBy'], 'content' : ni['content'],
              'rateCount' : ni['rateCount'], 'rating' : ni['rating'], 'reviewOnBook' : ni['reviewOnBook'], 'bookTitle' : ni['bookTitle'],
              'comments': ni['comments'], 'usersRated': ni['usersRated']})

    return jsonify({'results' : output})


@app.route('/reviews', methods=['POST'])
def add_review():
    collection = client.bookreviewer.reviews

    token = request.headers['token']
    username_header = request.headers['username']

    if verify_token(username_header, token):
        reviewTitle = request.form['reviewTitle']
        reviewBy = username_header
        content = request.form['reviewContent']
        rateCount = 0
        rating = 0
        reviewOnBook = request.form['reviewOnBook']
        bookTitle = request.form['bookTitle']
        comments = []
        usersRated = [] 

        insert_id = collection.insert({'reviewTitle' : reviewTitle, 'reviewBy' : reviewBy ,'content' : content, 'rating' : rating, 'rateCount' : rateCount,
                                       'reviewOnBook' : reviewOnBook, 'bookTitle' : bookTitle, 'comments' : comments, 'usersRated' : usersRated})

        ni = collection.find_one({'_id' : insert_id})

        output = {'reviewTitle' : ni['reviewTitle'], 'reviewBy' : ni['reviewBy'], 'content' : ni['content'],
                  'rateCount' : ni['rateCount'], 'reviewOnBook' : ni['reviewOnBook'], 'bookTitle' : ni['bookTitle'],
                  'comments': ni['comments']}

        return jsonify({'results' : output})

    return "Not logged in"



@app.route('/reviews/update_rating/<rid>/<rating>', methods = ['PUT'])
def update_rating_review(rid,rating):
    collection = client.bookreviewer.reviews

    review = collection.find_one({'_id':ObjectId(rid)})
    token = request.headers['token']
    username_header = request.headers['username']


    if (verify_token(username_header, token)):
        count = review['rateCount']
        ratingDB = review['rating']
        total = (count * ratingDB) + float(rating)
        newCount = count + 1
        newRating = total / newCount
        collection.update_one({'_id':ObjectId(rid)},{'$set':{'rateCount':newCount, 'rating':newRating}})
        collection.update_one({'_id':ObjectId(rid)},{'$push':{'usersRated':username_header}})
        return str(collection.find_one({'_id':ObjectId(rid)}))
    
    return "No rights or already rated"   




@app.route('/reviews/update/<rid>/<field>', methods = ['PUT'])
def update_review(rid,field):
    collection = client.bookreviewer.reviews

    review = collection.find_one({'_id':ObjectId(rid)})
    token = request.headers['token']
    username_header = request.headers['username']

    if (verify_token(username_header, token) and username_header == review['reviewBy']) or (verify_token(username_header, token) and is_admin(username_header)):
        collection.update_one({'_id':ObjectId(rid)},{'$set':{field:request.json[field]}})
        return str(collection.find_one({'_id':ObjectId(rid)}))
    
    return "No rights"   

    
@app.route('/reviews/delete/<rid>', methods = ['DELETE'])
def delete_review(rid):
    collection = client.bookreviewer.reviews

    token = request.headers['token']
    username = request.headers['username']

    if verify_token(username, token) and is_admin(username):
        collection.find_one_and_delete({'_id': ObjectId(rid)})
        return "Ok"

    return "Admin rights needed"



@app.route('/reviews/updatecomments/<rid>', methods = ['POST'])
def add_comment(rid):
    collection = client.bookreviewer.reviews
    
    token = request.headers['token']
    username_header = request.headers['username']

    if verify_token(username_header, token):
        posted = datetime.utcnow()
        author = username_header
        content = request.form['content']
        comments = []

        comment = {'posted' : posted, 'author' : author, 'content' : content, 'comments': comments}

        collection.update_one({'_id':ObjectId(rid)},{'$push':{'comments':comment}})

        return str(collection.find_one({'_id':ObjectId(rid)}))


@app.route('/reviews/updatecomments/alternative/<rid>', methods = ['POST'])
def add_comment_alternative(rid):
    collection = client.bookreviewer.reviews
    
    token = request.headers['token']
    username_header = request.headers['username']

    if verify_token(username_header, token):
        posted = datetime.utcnow()
        author = username_header
        content = request.json['content']
        comments = []

        comment = {'posted' : posted, 'author' : author, 'content' : content, 'comments': comments}

        collection.update_one({'_id':ObjectId(rid)},{'$push':{'comments':comment}})

        return str(collection.find_one({'_id':ObjectId(rid)}))
    

@app.route('/comments/delete/<rid>/<commentNumber>', methods = ['PUT'])
def delete_comment(rid, commentNumber):
    collection = client.bookreviewer.reviews

    token = request.headers['token']
    username = request.headers['username']

    if verify_token(username, token) and is_admin(username):
        collection.update_one({'_id': ObjectId(rid)}, {'$set': {"comments."+commentNumber+".content" : 'Deleted comment'}})
        return "Ok"

    return "Admin rights needed"




#################################################################################
#                                                                               #
#                                 LOGGING STUFF                                 #
#                                                                               #
#################################################################################

 





#################################################################################
#                                                                               #
#                                 AUTHENTICATION                                #
#                                                                               #
#################################################################################

# some tactics in the hashing and authentication functions are inspired on the following source:
# https://blog.miguelgrinberg.com/post/restful-authentication-with-flask



def verify_password(username, password):
    collection = client.bookreviewer.users

    user = collection.find_one({'username' : username})

    if hashing.check_value(user['password'], password, salt='zout'):
        return True
    return False


def generate_auth_token(username):
    collection = client.bookreviewer.auth_tokens
    #soure random sequence generation:
    #cryptographically more secure version of the top post on:
    #https://stackoverflow.com/questions/2257441/random-string-generation-with-upper-case-letters-and-digits-in-python
    token = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(10))
    
    collection.ensure_index("currentTime", expireAfterSeconds=10800)
    currentTime = datetime.utcnow()

    collection.insert({'currentTime' : currentTime, 'username' : username ,'token' : token})

    return token

def is_admin(username):
    collection = client.bookreviewer.users

    user = collection.find_one({'username' : username})

    if user['admin'] == 1:
        return True

    return False


@app.route('/token', methods=['GET'])
def get_tokens():
    token = request.headers['token']
    username_header = request.headers['username']

    if (verify_token(username_header, token) and is_admin(username_header)):
        collection = client.bookreviewer.auth_tokens
        output = []

        for q in collection.find():
            output.append({'currentTime' : q['currentTime'], 'username' : q['username'], 'token' : q['token']})

        return jsonify({'results' : output})

    return "No admin rights"



def verify_token(username, token):
    collection = client.bookreviewer.auth_tokens

    token_info = collection.find_one({'token' : token})

    if token_info and username == token_info['username']:
        return True
   
    return False



@app.route('/login', methods = ['POST'])
def login():
    username = request.json['username']
    password = request.json['password']

    if (verify_password(username, password)):
        token = generate_auth_token(username)
        return str(token)

    return str('Wrong password')


@app.route('/quick_login', methods = ['GET'])
def quick_login():
    username = request.headers['username']
    password = request.headers['password']

    if (verify_password(username, password)):
        return "true"

    return str('Wrong password')
    

@app.route('/check/login', methods = ['GET'])
def check_login():
    token = request.headers['token']
    username_header = request.headers['username']

    if (verify_token(username_header, token) and is_admin(username_header)):
        return "is_admin"
    elif (verify_token(username_header, token) and not is_admin(username_header)):
        return "is_regular"
    else:
        return "no_login"



if __name__ == '__main__':
    client = MongoClient()
    app.run('0.0.0.0')











from fastapi import FastAPI,Body
from pydantic import BaseModel

app = FastAPI()


BOOKS = [
    {'title':'harryPotter1', 'author':'Harry','category':'magical'},
       {'title':'PowerRangers', 'author':'power','category':'action'},
       {'title':'Ben10', 'author':'Ben Harry','category':'children'},
       {'title':'Kid/Kat', 'author':'Kid','category':'comedy'},
       {'title':'kickbutowski', 'author':'kicku','category':'comedy'},
       {'title':'doremon', 'author':'nobita','category':'fiction'},
       {'title':'sinchan', 'author':'sinchan Hatowri','category':'children drama'},
]


###################GET REUESTS###########################


@app.get("/")
def index():
    return 'Hello World!'

@app.get("/books")
def read_all_books():
    return BOOKS

@app.get("/books/{book_title}")
def read_all_books(book_title:str):
    for book in BOOKS:
        if book.get('title').casefold() == book_title.casefold(): #casefold function converts based on compared cases 
            return book
        
@app.get("/books/")
def read_category_by_query(category):
    books_to_return=[]
    for book in BOOKS:
        if book.get('category').casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return

@app.get("/books/{book_author}/")
def read_author_category_by_query(book_author:str,category:str):
    books_to_return=[]
    for book in BOOKS:
        if book.get('author').casefold() == book_author.casefold() or \
            book.get('category').casefold() == category.casefold():
               books_to_return.append(book)
    return books_to_return 

###################POST REQUESTS#############################

@app.post("/books/create_new_book")
def create_new_book_add(new_book=Body()):
    BOOKS.append(new_book)
    
##################PUT REQUESTS#################################

@app.put("/books/update_book")
def update_book(book_update=Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == book_update.get('title').casefold():
            BOOKS[i]=book_update
            
##############DELETE REQUESTS###################################

@app.delete("/books/delete_book/{book_title}")
def delete_book(book_title:str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == book_title.casefold():
            BOOKS.pop(i)
            break
##################QUERY#################################

'''
Create a new API Endpoint that can fetch all books from a
specific author using either Path Parameters or Query Parameters.
'''

@app.get("/all_books/{author_name}")
def get_all_books_author(author_name:str):
    books_to_return=[]
    for book in BOOKS:
        if book.get("author").casefold() == author_name.casefold():
            books_to_return.append(book)
    return books_to_return    
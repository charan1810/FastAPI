from typing import Optional
from fastapi import FastAPI,Body,Path,Query,HTTPException
from pydantic import BaseModel,Field
from starlette import status

app = FastAPI()

class Book:
    id : int
    title : str
    author : str
    description : str
    rating : float
    published_date:int
    
    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date=published_date

class book_request(BaseModel):
    id : Optional[int]= Field(description='ID is not needed on create',default=None)
    title : str = Field(min_length=3)
    author : str = Field(min_length=1)
    description : str = Field(min_length=1,max_length=100)
    rating : float = Field(gt=-1,lt=6)
    published_date:int=Field(gt=1999,lt=2025)
    model_config={
    "json_schema_extra":{
        "example":{
            "title":"A new Book",
            "author":"FASTAPI",
            "description":"A great book",
            "rating":4,
            "published_date":2003
        }
    }
}
    
BOOKS = [
    Book(1,'3 idiots','chetan bhagat','engineering life','5',2012),
    Book(2,'FastApi','charan','A nice fastapi guide','4.5',2009),
    Book(3,'Python','Hari','Python Complete guide for beginners','4.5',2001),
    Book(4,'3 mistakes of my life','chetan bhagat','friends in life','3.5',2003),
    Book(5,'Django','Rama','A complete guide for intermediate','3.25',2020),
    Book(6,'HarryPotter','Harry','Fictional Drama Book','4.75',2021)
]



@app.get("/books",status_code=status.HTTP_200_OK)
def get_all_books():
    return BOOKS

@app.get("/books/{book_id}",status_code=status.HTTP_200_OK)
def read_book(book_id:int=Path(gt=0 )):
    for book in BOOKS:
        if book.id==book_id:
            return book
    raise HTTPException(status_code=404,detail="Item not found")

@app.get("/books/{book_rating}",status_code=status.HTTP_200_OK)
def read_book_by_rating(book_rating:float):
    books_to_return=[]
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)
    return books_to_return

@app.get("/books/publish/}",status_code=status.HTTP_200_OK)
def read_book_by_published_year(book_published_year:int=Query(gt=1999,lt=2025)):
    books_to_return=[]
    for i in range(len(BOOKS)):
        if BOOKS[i].published_date == book_published_year:
            books_to_return.append(BOOKS[i])
    return books_to_return

@app.post("/create_a_book",status_code=status.HTTP_201_CREATED)
def create_new_book(book_info:book_request):
    new_book = Book(**book_info.dict())
    BOOKS.append(find_id_book(new_book))
def find_id_book(book:Book):
    book.id=1 if len(BOOKS) == 0 else BOOKS[-1].id+1
    return book

@app.put("/update_a_book",status_code=status.HTTP_204_NO_CONTENT)
def update_a_book(book:book_request):
    book_changed=False
    for i in range(len(BOOKS)):
        if BOOKS[i].id==book.id:
            BOOKS[i]=book
            book_changed=True
    if not book_changed:
        raise HTTPException(status_code=404,detail="Item not found")

@app.delete("/books/{book_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_a_book(book_id:int=Path(gt=0)):
    book_changed=False
    for i in range(len(BOOKS)):
        if BOOKS[i].id==book_id:
            BOOKS.pop(i)
            break
    if not book_changed:
        raise HTTPException(status_code=404,detail="Item not found")
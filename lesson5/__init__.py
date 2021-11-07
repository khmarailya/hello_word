from lesson5.data_unit import DataUnit, JSONUser, RezJSONBook, RezJSONUser, CSVBook
from lesson5.rw import JSONUsers, RezJSONUsers, CSVBooks


if __name__ == "__main__":
    books = CSVBooks().read()
    book_count = len(books)
    books_iter = (CSVBook(book) for book in books)

    users = JSONUsers().read()
    user_count = len(users)
    users_iter = (JSONUser(user) for user in users)

    ref_users = RezJSONUsers()
    avr = book_count // user_count
    rest = book_count % user_count

    for ref_book_count in [avr + 1] * rest + [avr] * (user_count - rest):
        ref_user = RezJSONUser().from_user(next(users_iter))

        for j in range(ref_book_count):
            ref_book = RezJSONBook().from_book(next(books_iter))
            ref_user += ref_book

        ref_users += ref_user

    ref_users.write()

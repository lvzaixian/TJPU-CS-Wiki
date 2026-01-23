class Book:
    def __init__(self, title, author, isbn):
        self.title = title
        self.author = author
        self.isbn = isbn
        self._is_borrowed = False
        self.borrower = None

    def is_borrowed(self):
        return self._is_borrowed

    def borrow(self, borrower_name):
        if not self._is_borrowed:
            self._is_borrowed = True
            self.borrower = borrower_name
            print(f"《{self.title}》借阅成功，借阅者：{borrower_name}")
        else:
            print(f"《{self.title}》已被借出，当前借阅者：{self.borrower}")

    def return_book(self):
        if self._is_borrowed:
            print(f"《{self.title}》归还成功，原借阅者：{self.borrower}")
            self._is_borrowed = False
            self.borrower = None
        else:
            print(f"《{self.title}》未被借出，无需归还")


class Library:
    def __init__(self, name):
        self.name = name
        self.books = []

    def add_book(self, book):
        self.books.append(book)
        print(f"图书《{book.title}》添加成功")

    def borrow_book(self, isbn, borrower_name):
        for book in self.books:
            if book.isbn == isbn:
                book.borrow(borrower_name)
                return
        print(f"未找到ISBN为 {isbn} 的图书")

    def return_book(self, isbn):
        for book in self.books:
            if book.isbn == isbn:
                book.return_book()
                return
        print(f"未找到ISBN为 {isbn} 的图书")

    def search_book(self, keyword):
        results = []
        for book in self.books:
            if keyword.lower() in book.title.lower() or keyword.lower() in book.author.lower():
                results.append(book)
        return results

    def display_statistics(self):
        total = len(self.books)
        borrowed = sum(1 for book in self.books if book.is_borrowed())
        available = total - borrowed
        print(f"【{self.name} 统计信息】")
        print(f"总藏书量：{total}")
        print(f"已借出：{borrowed}")
        print(f"可借阅：{available}")

    def display_all_books(self):
        print(f"【{self.name} 所有藏书】")
        for book in self.books:
            status = "已借出" if book.is_borrowed() else "可借阅"
            print(f"《{book.title}》 - {book.author} - {book.isbn} - {status}")


# 测试代码
if __name__ == "__main__":
    lib = Library("计算机图书馆")

    # 添加书籍
    books_info = [
        ("Python编程", "John Smith", "978-1-123456-78-9"),
        ("数据结构", "Jane Doe", "978-1-987654-32-1"),
        ("算法导论", "Robert Johnson", "978-1-111111-11-1")
    ]
    for title, author, isbn in books_info:
        lib.add_book(Book(title, author, isbn))

    print()

    # 展示所有书籍
    lib.display_all_books()
    print()

    # 借书测试
    lib.borrow_book("978-1-123456-78-9", "张三")
    lib.borrow_book("978-1-123456-78-9", "李四")  # 重复借阅
    print()

    # 还书测试
    lib.return_book("978-1-123456-78-9")
    print()

    # 搜索测试
    results = lib.search_book("Python")
    print("搜索 'Python' 结果：")
    for book in results:
        print(f"《{book.title}》 - {book.author}")
    print()

    # 统计信息
    lib.display_statistics()
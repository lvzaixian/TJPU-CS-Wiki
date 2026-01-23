class Book:
    def __init__(self, title, author, isbn):
        self.title = title
        self.author = author
        self.isbn = isbn
        self._is_borrowed = False
        self.borrower = None

    @property
    def is_borrowed(self):
        return self._is_borrowed

    def borrow(self, borrower_name):
        if self._is_borrowed:
            return False, "该书已被借出"

        self._is_borrowed = True
        self.borrower = borrower_name
        return True, f"成功借出《{self.title}》"

    def return_book(self):
        if not self._is_borrowed:
            return False, "该书未被借出"

        self._is_borrowed = False
        borrower = self.borrower
        self.borrower = None
        return True, f"《{self.title}》归还成功，借阅人: {borrower}"

    def __str__(self):
        status = "已借出" if self._is_borrowed else "可借阅"
        borrower_info = f", 借阅人: {self.borrower}" if self._is_borrowed else ""
        return f"《{self.title}》- {self.author} (ISBN: {self.isbn}) [{status}{borrower_info}]"


class Library:
    def __init__(self, name):
        self.name = name
        self._books = {}
        self._borrowed_count = 0

    def add_book(self, book):
        if book.isbn in self._books:
            return False, "该书已存在"

        self._books[book.isbn] = book
        return True, f"成功添加《{book.title}》"

    def borrow_book(self, isbn, borrower_name):
        if isbn not in self._books:
            return False, "该书不存在"

        book = self._books[isbn]
        success, message = book.borrow(borrower_name)
        if success:
            self._borrowed_count += 1
        return success, message

    def return_book(self, isbn):
        if isbn not in self._books:
            return False, "该书不存在"

        book = self._books[isbn]
        success, message = book.return_book()
        if success:
            self._borrowed_count -= 1
        return success, message

    def search_book(self, keyword):
        results = []
        for book in self._books.values():
            if (keyword.lower() in book.title.lower() or
                    keyword.lower() in book.author.lower() or
                    keyword == book.isbn):
                results.append(book)
        return results

    def display_statistics(self):
        total_books = len(self._books)
        available_books = total_books - self._borrowed_count

        print(f"=== {self.name} 统计信息 ===")
        print(f"总图书数量: {total_books}")
        print(f"可借阅数量: {available_books}")
        print(f"已借出数量: {self._borrowed_count}")
        print(f"借阅率: {self._borrowed_count / total_books * 100:.1f}%" if total_books > 0 else "借阅率: 0%")

    def display_all_books(self):
        print(f"=== {self.name} 所有图书 ===")
        for book in self._books.values():
            print(book)


# 测试代码
library = Library("计算机图书馆")

# 添加图书
books_data = [
    Book("Python编程", "John Smith", "978-1-123456-78-9"),
    Book("数据结构", "Jane Doe", "978-1-987654-32-1"),
    Book("算法导论", "Robert Johnson", "978-1-111111-11-1")
]

for book in books_data:
    library.add_book(book)

# 测试功能
library.borrow_book("978-1-123456-78-9", "张三")
library.borrow_book("978-1-987654-32-1", "李四")

library.display_all_books()
library.display_statistics()

# 搜索测试
print("\n=== 搜索 'Python' ===")
results = library.search_book("Python")
for book in results:
    print(book)

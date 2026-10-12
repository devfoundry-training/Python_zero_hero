-- ============================================================
-- Library Manager sample data (generated from the CSV files)
-- ============================================================
-- Run after schema.sql. Do not edit by hand: change the CSV
-- files and run reference/python/tools/make_seed_sql.py.
-- ============================================================

INSERT INTO books (id, title, author, year, genre, copies, format, length) VALUES
    (1, 'Pride and Prejudice', 'Jane Austen', 1813, 'Classic', 3, 'print', 432),
    (2, 'Nineteen Eighty-Four', 'George Orwell', 1949, 'Dystopian', 2, 'print', 328),
    (3, 'The Hobbit', 'J. R. R. Tolkien', 1937, 'Fantasy', 0, 'print', 310),
    (4, 'Dune', 'Frank Herbert', 1965, 'Science Fiction', 4, 'print', 412),
    (5, 'Robinson Crusoe', 'Daniel Defoe', 1719, 'Adventure', 1, 'print', 320),
    (6, 'The Time Machine', 'H. G. Wells', 1895, 'Science Fiction', 2, 'ebook', 118),
    (7, 'Animal Farm', 'George Orwell', 1945, 'Dystopian', 5, 'print', 112),
    (8, 'Emma', 'Jane Austen', 1815, 'Classic', 1, 'audio', 1150),
    (9, 'The Left Hand of Darkness', 'Ursula K. Le Guin', 1969, 'Science Fiction', 0, 'print', 304),
    (10, 'Murder on the Orient Express', 'Agatha Christie', 1934, 'Crime', 2, 'print', 256),
    (11, 'The Murder of Roger Ackroyd', 'Agatha Christie', 1926, 'Crime', 1, 'ebook', 312),
    (12, 'A Wizard of Earthsea', 'Ursula K. Le Guin', 1968, 'Fantasy', 2, 'print', 183),
    (13, 'Brave New World', 'Aldous Huxley', 1932, 'Dystopian', 2, 'audio', 480),
    (14, 'The Martian', 'Andy Weir', 2011, 'Science Fiction', 3, 'print', 369),
    (15, 'Small Island', 'Andrea Levy', 2004, 'Historical', 1, 'print', 441),
    (16, 'Wolf Hall', 'Hilary Mantel', 2009, 'Historical', 2, 'audio', 1440),
    (17, 'The Remains of the Day', 'Kazuo Ishiguro', 1989, 'Literary', 2, 'print', 258),
    (18, 'Never Let Me Go', 'Kazuo Ishiguro', 2005, 'Literary', 1, 'ebook', 288),
    (19, 'Frankenstein', 'Mary Shelley', 1818, 'Gothic', 2, 'print', 280),
    (20, 'The War of the Worlds', 'H. G. Wells', 1898, 'Science Fiction', 3, 'audio', 410);

INSERT INTO members (id, name, email, type, joined) VALUES
    (101, 'Amira Khan', 'amira.khan@example.com', 'standard', '2023-01-15'),
    (102, 'Ben Taylor', 'ben.taylor@example.com', 'student', '2024-09-02'),
    (103, 'Chloe Evans', 'chloe.evans@example.com', 'staff', '2019-05-20'),
    (104, 'Dev Patel', 'dev.patel@example.com', 'student', '2025-09-10'),
    (105, 'Ella Brown', 'ella.brown@example.com', 'standard', '2021-03-08'),
    (106, 'Femi Adeyemi', 'femi.adeyemi@example.com', 'standard', '2022-11-30'),
    (107, 'Grace Wilson', 'grace.wilson@example.com', 'staff', '2018-07-01'),
    (108, 'Harry Jones', 'harry.jones@example.com', 'student', '2026-01-12'),
    (109, 'Ben Taylor', 'ben.taylor2@example.com', 'standard', '2025-02-14');

INSERT INTO loans (id, book_id, member_id, borrowed, returned) VALUES
    (1, 1, 101, '2026-09-01', '2026-09-12'),
    (2, 2, 102, '2026-09-10', '2026-10-05'),
    (3, 4, 103, '2026-09-05', NULL),
    (4, 5, 105, '2026-09-20', NULL),
    (5, 7, 101, '2026-10-01', NULL),
    (6, 10, 104, '2026-08-28', NULL),
    (7, 6, 106, '2026-10-10', NULL),
    (8, 14, 102, '2026-09-15', NULL),
    (9, 13, 107, '2026-08-01', '2026-09-10'),
    (10, 19, 108, '2026-09-21', NULL),
    (11, 1, 105, '2026-09-27', NULL),
    (12, 20, 109, '2026-09-14', '2026-09-30');

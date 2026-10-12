# Task: List Comprehension Practice

num_list = [1, 2, 3, 4, 5, 6, 7, 1, 23, 2135, 5, 6, 67, 65, 3, 346, 7, 4, 84, 4, 12, 23, 8467, 523, 1125]

word_list = [
    "apple", "banana", "grape", "orange", "kiwi", "pineapple", "blueberry",
    "strawberry", "mango", "peach", "watermelon", "apricot", "pear", "cherry",
    "plum", "melon", "fig", "pomegranate", "lemon", "cantaloupe", "papaya",
    "blackberry", "apricot", "raspberry", "kiwifruit", "coconut", "lime",
    "nectarine", "tangerine", "persimmon", "guava", "currant", "date", "elderberry"
]

countries_and_cities = [
    ("USA", "Washington, D.C."),
    ("Canada", "Ottawa"),
    ("Japan", "Tokyo"),
    ("Germany", "Berlin"),
    ("France", "Paris"),
    ("Italy", "Rome"),
    ("Australia", "Canberra"),
    ("India", "New Delhi"),
    ("Brazil", "Brasília"),
    ("Russia", "Moscow")
]

# Create a new list containing only the even numbers from the num_list.
even_list = [x for x in num_list if x % 2 == 0]
# Create a new list containing the squares of the even numbers from the num_list.
squared_even_list = [x ** 2 for x in num_list if x % 2 == 0]
# Create a new list containing only the numbers that are divisible by 3 but not by 5 from the num_list.
div_by_3_list = [x for x in num_list if (x % 3 == 0) and (x % 5 != 0)]
# Create a new list containing words in a sentence that are longer than 4 characters.
four_char_list = [e for e in words_list if len(e) <= 4]
# Create a new list containing the first letter of each word in a sentence.
first_letters = [word[0] for word in words_list]
# Create a dictionary where each country is a key and its capital city is the value.
country_dict = {country: city for country, city in countries_and_cities}

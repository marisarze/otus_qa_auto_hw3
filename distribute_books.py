import time
from typing import OrderedDict


def benchmark(func):
    
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        t = end - start
        print("Execution time: ", t)
        return result
    
    return wrapper


def entry_by_reference(user_info, reference_entry):
    entry = dict()
    for key in reference_entry.keys():
        if key in user_info.keys():
            entry[key] = user_info[key]
        else:
            entry[key] = type(reference_entry[key])()
    return entry


@benchmark
def distribute_books_v1(users, books, reference):
    result = list()
    for user in users:
        result.append(entry_by_reference(user, reference[0]))
    
    users_num = len(users)
    for index, book in enumerate(books):
        result[index % users_num]["books"].append(book)
    return result


def cyclic_index(number):
    while(True):
        for index in range(number):
            yield index


@benchmark
def distribute_books_v2(users, books, reference):
    result = list()
    for user in users:
        result.append(entry_by_reference(user, reference[0]))

    indexes = cyclic_index(len(result))
    for book in books:
        result[next(indexes)]["books"].append(book)
    return result


    
if __name__ == "__main__":
    import json
    import csv
    from collections import OrderedDict

    with open("data/books.csv", "r") as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        headers = next(reader)
        headers = list(map(lambda x: x.lower(), headers))
        books = []
        sample = OrderedDict([("title", str), ("author", str), ("pages", int), ("genre", str)])
        for row in reader:
            entry = dict(zip(headers, row))
            ordered_entry = OrderedDict()
            for key, value_type in sample.items():
                ordered_entry[key] = value_type(entry[key])
            books.append(ordered_entry)
    
    with open("data/users.json", "r") as json_file:
        users = json.load(json_file)

    with open("data/reference.json", "r") as json_file:
        reference = json.load(json_file)
    
    result1 = distribute_books_v1(users, books, reference)
    result2 = distribute_books_v2(users, books, reference)
    print(result1 == result2)

    with open("result.json", "w") as json_file:
        json.dump(result1, json_file, indent=4)


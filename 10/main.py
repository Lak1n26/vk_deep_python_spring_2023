import time
import random
import json
import cjson
import ujson
import faker


def dumps_time_tests(dicts):
    print("Время выполнения сериализации (dumps)")
    t1 = time.time()
    for DICT in dicts:
        res = json.dumps(DICT)
    t2 = time.time()
    print(f"время для JSON: {t2 - t1} sec")

    t1 = time.time()
    for DICT in dicts:
        res = cjson.dumps(DICT)
    t2 = time.time()
    print(f"время для CJSON: {t2 - t1} sec")

    t1 = time.time()
    for DICT in dicts:
        res = ujson.dumps(DICT)
    t2 = time.time()
    print(f"время для UJSON: {t2 - t1} sec")


def loads_time_tests(json_list):
    print("Время выполнения десериализации (loads)")

    t1 = time.time()
    for JSON in json_list:
        res = json.loads(JSON)
    t2 = time.time()
    print(f"время для JSON: {t2 - t1} sec")

    t1 = time.time()
    for JSON in json_list:
        res = cjson.loads(JSON)
    t2 = time.time()
    print(f"время для CJSON: {t2 - t1} sec")

    t1 = time.time()
    for JSON in json_list:
        res = ujson.loads(JSON)
    t2 = time.time()
    print(f"время для UJSON: {t2 - t1} sec")


def main():
    dicts = []
    json_list = []

    fake = faker.Faker()
    for _ in range(60_000):
        dict_object = {
            "name": fake.name(),
            "age": random.randint(20, 50),
            "city": fake.city(),
            "email": fake.email(),
            "phone_number": fake.phone_number(),
            "job": fake.job(),
            "company": fake.company(),
            "wife/husband name": fake.name(),
            "previous city": fake.city(),
            "second phone number": fake.phone_number(),
            "previous job": fake.job(),
            "answer question: best company in the world": fake.company(),
        }
        dicts.append(dict_object)
        json_list.append(json.dumps(dict_object))

    dumps_time_tests(dicts)
    loads_time_tests(json_list)


if __name__ == "__main__":
    main()

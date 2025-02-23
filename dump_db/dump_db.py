import psycopg2

from helper import logger

# from data import db


def dump_data_db():
    logger.warning("обновление дампа...")
    conn1 = psycopg2.connect(dbname="Telegram", host="localhost", user="postgres", password="postgres", port="5432")
    cursor1 = conn1.cursor()

    cursor1.execute("SELECT number, port, seed, id FROM data WHERE work IN (%s, %s) ORDER BY id ASC", ("1", "2",))
    data = cursor1.fetchall()
    cursor1.close()
    conn1.close()

    d = "\ndb = [\n"
    for x in data:
        d += f"    [\"{x[3]}\", \"{str(x[0]).replace(' ', '-')}\", \"{x[1]}\", "
        d += "\"" + str(x[2]).replace('\n', ' ') + "\"], \n"
    d += "]"

    with open("dump_db/data.py", "w") as file:
        file.write(d)
    logger.success("обновление дампа закончено")


# def load_to_db():
#     conn1 = psycopg2.connect(dbname="Telegram", host="localhost", user="postgres", password="postgres", port="5432")
#     cursor1 = conn1.cursor()
#     conn1.autocommit = True
#     for x in db:
#         # print(x[1], x[2], x[3])
#         cursor1.execute("INSERT INTO data(number, port, seed, work) VALUES(%s, %s, %s, %s)", (x[1], x[2], x[3], "1", ))
#     cursor1.close()
#     conn1.close()
#
# load_to_db()
# def dump_data_db():
#     conn1 = psycopg2.connect(dbname="Telegram", host="localhost", user="postgres", password="postgres", port="5432")
#     cursor1 = conn1.cursor()
#     cursor1.execute("SELECT number, port, seed, id FROM FROM data WHERE work = %s ORDER BY id ASC ", ("1",))
#     data = cursor1.fetchall()
#     cursor1.close()
#     conn1.close()
#
#     d = "\ndb = [\n"
#     for x in data:
#         d += f"    [\"{x[3]}\", \"{str(x[0]).replace(' ', '-')}\", \"{x[1]}\", "
#         d += "\"" + str(x[2]).replace('\n', ' ') + "\"], \n"
#     d += "]"
#
#     with open("dump_db/data.py", "w") as file:
#         file.write(d)

import sqlite3
import time
from datetime import datetime


class DbCell:
    def __init__(self, lat, lng, bright, total, iso8601):
        self.lat = lat
        self.lng = lng
        self.bright = bright
        self.total = total
        date = datetime.fromisoformat(iso8601)
        self.date = date

def create():
    conn = sqlite3.connect('coords.db')
    cursor = conn.cursor()
    # All measurements defined from top left of square
    cursor.execute('''CREATE TABLE IF NOT EXISTS coordinates(
    Top_Left_Lat REAL,
    Top_Left_long REAL,
    Bright_pixels REAL,
    Total_pixels REAL,
    Date TEXT); ''')


def delete_db():
    conn = sqlite3.connect('coords.db')
    cursor = conn.cursor()
    cursor.execute('''DROP TABLE coordinates;''')
    conn.commit()
    conn.close()


def write_one(lat, lng, bright, total, date: datetime):
    conn = sqlite3.connect('coords.db')
    cursor = conn.cursor()
    date_iso8601 = date.isoformat()
    cursor.execute(f'''INSERT INTO coordinates VALUES({lat}, {lng}, {bright}, {total}, "{date_iso8601}");''')
    conn.commit()


def get_one(lat, lng):
    conn = sqlite3.connect("coords.db")
    cursor = conn.cursor()
    rows = cursor.execute(f'''SELECT * FROM coordinates WHERE Top_Left_Lat = {lat} AND Top_Left_Long = {lng}''')
    ret = []
    for row in rows:
        print(row)
        ret.append(DbCell(*row))
    return ret


def get_list(lat_longs: list):
    conn = sqlite3.connect("coords.db")
    cursor = conn.cursor()
    ret = []
    for lat_val, long_val in lat_longs:
        ret += get_one(lat_val, long_val)
    return ret


def print_all():
    conn = sqlite3.connect("coords.db")
    cursor = conn.cursor()
    rows = cursor.execute('''SELECT * FROM coordinates''')
    for i in rows:
        print(i)
    conn.close()


def getID(lat, long):
    return lat + " " + long


def check_size():
    conn = sqlite3.connect('coords.db')
    cursor = conn.cursor()
    cursor.execute("PRAGMA page_count;")
    page_count = cursor.fetchone()[0]
    cursor.execute("PRAGMA page_size;")
    page_size = cursor.fetchone()[0]
    db_size = page_count * page_size
    if (db_size > 10*1024*1028*1024):
        print("delete")
        cursor.execute("DELETE FROM coordinates WHERE random() > 5534023222112865485")
    cursor.close()


if __name__ == "__main__":
    delete_db()
    create()
    write_one(1, 2, 3, 4, datetime.now())
    print(get_one(1, 2))
    got = get_one(1, 2)[0]
    print(got.lat)
    '''
    while True:
        check_size()
        time.sleep(2*24*60*60)
    '''
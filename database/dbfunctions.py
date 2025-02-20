import sqlite3


def create():
    conn = sqlite3.connect('coords.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS coordinates(
    Top_Left_Lat REAL,
    Top_Left_long REAL,
    Brightness REAL,
    Lights REAL,
    Year INTEGER,
    Month INTEGER,
    Day INTEGER,
    Hour INTEGER,
    Minute INTEGER,
    Second INTEGER); ''')


def write(data: list):
    conn = sqlite3.connect('coords.db')
    cursor = conn.cursor()
    val = str(data[0]) + ", " + str(data[1]) + ", " + str(data[2]) + ", " + str(data[3]) + ", " + str(data[4]) + \
        ", " + str(data[5]) + ", " + str(data[6]) + ", " + str(data[7]) + ", " + str(data[8]) + ", " + str(data[9])
    cursor.execute(f'''INSERT INTO coordinates VALUES({val}); ''')
    conn.commit()


def get_filter(lat_long: str):
    conn = sqlite3.connect("coords.db")
    cursor = conn.cursor()
    # ind = lat_long.find(" ")
    lat = lat_long.split(" ")[0]
    long = lat_long.split(" ")[1]
    rows = cursor.execute('''SELECT * FROM coordinates WHERE Top_Left_Lat = ''' + lat +  ''' AND Top_Left_Long = ''' + long)
    ret = []
    for i in rows:
        ret.append(i)
    return ret


def get():
    conn = sqlite3.connect("coords.db")
    cursor = conn.cursor()
    rows = cursor.execute('''SELECT * FROM coordinates''')
    for i in rows:
        print(i)
    conn.close()


def getID(lat, long):
    return lat + " " + long
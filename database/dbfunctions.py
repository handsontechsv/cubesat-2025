import sqlite3


def create():
    conn = sqlite3.connect('coords.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE coordinates(
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


def write(data):
    conn = sqlite3.connect('coords.db')
    cursor = conn.cursor()
    val = str(data[0]) + ", " + str(data[1]) + ",` " + str(data[2]) + ", " + str(data[3]) + ", " + str(data[4]) + \
        ", " + str(data[5]) + ", " + str(data[6]) + ", " + str(data[7]) + ", " + str(data[8]) + ", " + str(data[9])
    cursor.execute(f'''INSERT INTO coordinates VALUES({val}); ''')
    conn.commit()


def get_filter(tllat, tllong):
    conn = sqlite3.connect("coords.db")
    cursor = conn.cursor()
    rows = cursor.execute('''SELECT * FROM coordinates WHERE Top_Left_Lat = ''' + str(tllat) +  ''' AND Top_Left_Long 
    = ''' + str(tllong))
    for i in rows:
        print(i)


def get():
    conn = sqlite3.connect("coords.db")
    cursor = conn.cursor()
    rows = cursor.execute('''SELECT * FROM coordinates''')
    for i in rows:
        print(i)
    conn.close()
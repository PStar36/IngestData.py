#! /usr/bin/env python3

import csv
import psycopg2
import sys

db_host = "localhost"  # sys.argv[-5]
db_port = 5432  # sys.argv[-4]
db_name = "Test"  # sys.argv[-3]
db_user = "postgres"  # sys.argv[-2]
db_password = "admin"  # sys.argv[-1]

# names of the csv files which contain the data
AthleteEvents_csv_name = sys.argv[1]  # 'AthleteEvents.csv'
HostCities_csv_name = sys.argv[2]  # 'HostCities.csv'
NOCRegions_csv_name = sys.argv[3]  # 'NOCRegions.csv'

# ------------------------------------------------------------------------------------------------------------------------------------------

# HELP:
'''
---Insertion to database:
   cur.execute('INSERT INTO Table1 (col1, col2) VALUES(%s, %s)', (value1, value2))

---Fetching from database:-----------------------------------------------------------------------------------------------------------------
   cur.execute(query)
   resultSet = cur.fetchall() - to fetch the whole result set
   reultSet = cur.fetchone() - to fetch a single row(does not mean only the first row, it means one row at a time)
-------------------------------------------------------------------------------------------------------------------------------------------
'''
# SQL connection
sql_con = psycopg2.connect(host=db_host, port=db_port, database=db_name, user=db_user, password=db_password)

# cursor, for DB operations
cur = sql_con.cursor()


def csv_to_list(csv_name):
    # gets data from the csv file and puts it into a list of lists
    # for accessing the data: data_list[row_number][column_number]
    data_list = []
    with open(csv_name, 'r', encoding='utf-8') as csvfile:
        data_squads = csv.reader(csvfile)

        for row in data_squads:
            # to remove all the ', to have no collisions in the code later on
            new_row = []
            for element in row:
                if isinstance(element, str):
                    element = element.replace("'", "`")
                new_row.append(element)
            # print(new_row)

            data_list.append(new_row)
        # deletes the fist row, which contains the table heads
        # optional:uncomment if this makes working with the data easier for you
        del data_list[0]
    return data_list


def semicolon_string_to_list(string):
    # interprets all ; of the given string as separator of elements
    # returns a list of strings
    return string.split(';')


# ------------------------------------------------------------------------------------------------------------------------------------------
# def insert_athletes(a_list,cur):
#     #inserts the Athlete data into the table
#     cur.execute("insert into athletes(akey, name, gender , dob , height , weight) values (%i , %s , %c ,")
#
def insert_countries(c_list, cur):
    index = 0

    for row in c_list:
        if c_list[index][0] == '':
            c_list[index][0] = None
        if c_list[index][1] == '':
            c_list[index][1] = None
        if c_list[index][2] == '':
            c_list[index][2] = None
        if c_list[index][3] == '':
            c_list[index][3] = None

        cur.execute("insert into countries(noc,name,population,gdp) values (%s,%s,%s,%s)",
                    (c_list[index][0], c_list[index][1], c_list[index][2], c_list[index][3]))

        index += 1


def insert_cities(c_list, cur):
    index = 0
    for row in c_list:
        if len(c_list[index][0]) <= 3:
            if (c_list[index][2] != c_list[index - 1][2]) and (c_list[index][2] != c_list[index - 2][2]):
                if c_list[index][0] == '':
                    c_list[index][0] = None
                if c_list[index][2] == '':
                    c_list[index][2] = None
                if c_list[index][3] == '':
                    c_list[index][3] = None
                cur.execute("insert into cities(name,noc) values (%s,%s)",
                            (c_list[index][2], c_list[index][0]))
        index += 1


def insert_events(a_list, cur):
    index = 0
    serial = 1
    for row in a_list:
        if a_list[index][12] == '':
            a_list[index][12] = None
        if a_list[index][11] == '':
            a_list[index][11] = None
        if a_list[index][0] == '':
            a_list[index][0] = None
        if a_list[index][1] == '':
            a_list[index][1] = None
        if a_list[index][2] == '':
            a_list[index][2] = None
        if a_list[index][3] == '':
            a_list[index][3] = None
        if a_list[index][4] == '':
            a_list[index][4] = None
        if a_list[index][5] == '':
            a_list[index][5] = None

        if a_list[index][12] != '' or a_list[index][11] != '' or a_list[index][1]:
            cur.execute("INSERT INTO TEMPEVENTS(TEventName,TSportName,TAKey,TName,TGender,TDoB,THeight,TWeight,"
                        "TTName,TTNoc,TTYear) "
                        "values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                        (a_list[index][12], a_list[index][11], a_list[index][0], a_list[index][1], a_list[index][2],
                         a_list[index][3], a_list[index][4], a_list[index][5], a_list[index][6], a_list[index][7],
                         a_list[index][9]))
        index += 1
        serial += 1
    cur.execute("INSERT INTO Events(SportName, EventName) SELECT DISTINCT TSportName, TEventName FROM TEMPEVENTS "
                "WHERE TSportName IS NOT NULL AND TEventName IS NOT NULL;")

    cur.execute("INSERT INTO Athletes(Name,AKey,Gender,DoB,Height,Weight) SELECT DISTINCT TName, TAKey, TGender,"
                "TDoB,THeight,TWeight FROM "
                "TEMPEVENTS WHERE TName IS NOT NULL;")

    cur.execute("INSERT INTO TEMPATH(AName, ANOC , AAKey) SELECT DISTINCT TName ,TTNOC ,TAKey FROM TEMPEVENTS WHERE "
                "TName IS NOT NULL ")


def insert_games(c_list, cur):
    index = 0
    for rows in c_list:
        cur.execute("INSERT INTO Tempgames(TYear,TStartDate,TEndDate, TName) values(%s,%s,%s,%s)",
                    (c_list[index][3], c_list[index][4], c_list[index][5], c_list[index][3] + " Summer"))
        index += 1

    cur.execute("INSERT INTO Games(Year, Name , StartDate, EndDate) SELECT DISTINCT TYear,TName, TStartDate , "
                "TEndDate FROM Tempgames WHERE TName IS NOT NULL AND TStartDate IS NOT NULL AND TEndDate IS NOT NULL;")
    cur.execute("INSERT INTO TEAMS(Name, Noc, Year) SELECT DISTINCT TTName , TTNoc , TTYear FROM TEMPEVENTS WHERE "
                "TTName IS NOT NULL AND TTNoc IS NOT NULL AND TTYear IS NOT NULL;")


def insert_results(a_list, cur):
    index = 0

    cur.execute("SELECT Eventname FROM Events")
    event_list = cur.fetchall()

    for rows in a_list:
        if a_list[index][13] == "Gold":
            a_list[index][13] = "G"
        elif a_list[index][13] == "Silver":
            a_list[index][13] = "S"
        elif a_list[index][13] == "Bronze":
            a_list[index][13] = "B"
        else:
            a_list[index][13] = None
        cur.execute("SELECT ekey FROM events WHERE eventname = %s", (a_list[index][12],))
        eky = cur.fetchall()
        for e in eky:
            temp = e[0]
        cur.execute("INSERT INTO Results (Year , Ekey , AKey , Medal) VALUES (%s,%s,%s,%s)",
                    (a_list[index][9], temp, a_list[index][0], a_list[index][13]))
        index += 1


def insert_gamesin(h_list, cur):
    index = 0
    for rows in h_list:
        cur.execute("INSERT INTO Tgamesin(year, CName) values (%s,%s)", (h_list[index][3], h_list[index][2]))
        cur.execute("SELECT ckey FROM cities WHERE name = %s", (h_list[index][2],))
        ckey = cur.fetchall()
        for e in ckey:
            temp = e[0]
        cur.execute("INSERT INTO GamesIn(year, ckey) VALUES (%s,%s)", (h_list[index][3], temp))
        index += 1


def insert_teamsathletes(a_list):
    global t_tkey
    for counter in range(len(a_list)):
        cur.execute("SELECT Tkey FROM TEAMS WHERE name = %s AND year = %s", (a_list[counter][6], a_list[counter][9]))
        t_tkey = cur.fetchall()
        for e in t_tkey:
            temp = e[0]

        cur.execute("INSERT INTO TempTeamAthletes (tkey, akey) VALUES (%s,%s)", (temp, a_list[counter][0]))
    cur.execute("INSERT INTO TeamAthletes(tkey,akey) SELECT DISTINCT Tkey , Akey FROM TempTeamAthletes")


# Lists from csvs

AthleteEvents_list = csv_to_list(AthleteEvents_csv_name)
NOCRegions_list = csv_to_list(NOCRegions_csv_name)
HostCities_list = csv_to_list(HostCities_csv_name)
insert_countries(NOCRegions_list, cur)
insert_cities(HostCities_list, cur)
insert_events(AthleteEvents_list, cur)
insert_games(HostCities_list, cur)
insert_results(AthleteEvents_list, cur)
insert_gamesin(HostCities_list, cur)
insert_teamsathletes(AthleteEvents_list)

# commit the changes, this makes the database persistent

cur.execute("DROP TABLE IF EXISTS tempevents, TCities , Tgamesin, tempath ,TempTeamAthletes , tempgames;")
sql_con.commit()

# close connections
cur.close()
sql_con.close()

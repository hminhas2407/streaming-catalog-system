import sqlite3


def app():
    print("Welcome to Streaming catalog system!")
    print("1. Create an account")
    print("2. Login into existing account")
    print("3. Exit")
    print("*" * 100)
    choice = int(input("Enter your choice: "))
    print("*" * 100)

    if choice == 1:
        print("1. Create Admin Account")
        print("2. Create User Account")
        print("*" * 100)
        choice1 = int(input("Enter your choice: "))
        print("*" * 100)

        if choice1 == 1:
            print("Lets create an admin account")
            username = input("Enter username: ")
            password = input("Enter password: ")
            print("*" * 100)
            create_admin(username, password)

        if choice1 == 2:
            print("Lets create an user account")
            username = input("Enter username: ")
            password = input("Enter password: ")
            print("*" * 100)
            create_user(username, password)

    if choice == 2:
        print("1. Login into Admin Account")
        print("2. Login into User Account")
        print("*" * 100)
        choice1 = int(input("Enter your choice: "))
        print("*" * 100)

        if choice1 == 1:
            print("Welcome to admin login!")
            username = input("Enter username: ")
            password = input("Enter password: ")
            print("*" * 100)
            admin_login(username, password)


        if choice1 == 2:
            print("Welcome to user login!")
            username = input("Enter username: ")
            password = input("Enter password: ")
            print("*" * 100)
            user_login(username, password)

    elif choice == 3:
        return "break"


def sql_database():
    conn = sqlite3.connect('streamingCatalogSystem.db')
    c = conn.cursor()

    # create tables
    c.execute('''CREATE TABLE IF NOT EXISTS tb_user
                (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                LOGIN VARCHAR NOT NULL,
                PASSWORD VARCHAR NOT NULL
                );''')
    c.execute('''CREATE TABLE IF NOT EXISTS tb_admin
                (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                LOGIN VARCHAR NOT NULL,
                PASSWORD VARCHAR NOT NULL
                );''')
    c.execute('''CREATE TABLE IF NOT EXISTS tb_movies
                (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                NAME VARCHAR NOT NULL,
                DURATION INT NOT NULL,
                CATEGORY VARCHAR NOT NULL
                );''')
    c.execute('''CREATE TABLE IF NOT EXISTS tb_series
                    (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    NAME VARCHAR NOT NULL,
                    NO_OF_SEASON INT NOT NULL,
                    CATEGORY VARCHAR NOT NULL
                    );''')
    c.execute('''CREATE TABLE IF NOT EXISTS tb_userdata
                    (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    LOGIN VARCHAR NOT NULL,
                    SHOW_NAME VARCHAR NOT NULL,
                    TYPE_SHOW VARCHAR NOT NULL,
                    DURATION INT,
                    SEASON INT,
                    TIME VARCHAR NOT NULL
                    );''')

    # commit the changes to db
    conn.commit()
    # close the connection
    conn.close()


def create_admin(username, password):
    admin_data = check_admin(username)
    if len(admin_data) > 0:
        print("Cannot create new admin user because username already exists.")
        return
    conn = sqlite3.connect('streamingCatalogSystem.db')
    cursor = conn.cursor()
    params = (username, password)
    cursor.execute("INSERT INTO tb_admin (LOGIN, PASSWORD) VALUES (?,?)", params)
    conn.commit()
    print('Admin Creation Successful')
    print("*" * 100)
    conn.close()


def check_admin(username):
    query = f"select ID from tb_admin where LOGIN = '{username}'"
    conn = sqlite3.connect('streamingCatalogSystem.db')
    cursor = conn.cursor()
    res = cursor.execute(query)
    result = res.fetchall()
    return result


def create_user(username, password):
    users_data = check_user(username)
    if len(users_data) > 0:
        print("Cannot create new user because username already exists.")
        return
    conn = sqlite3.connect('streamingCatalogSystem.db')
    cursor = conn.cursor()
    params = (username, password)
    cursor.execute("INSERT INTO tb_user (LOGIN, PASSWORD) VALUES (?,?)", params)
    conn.commit()
    print('User Creation Successful')
    print("*" * 100)
    conn.close()


def check_user(username):
    query = f"select ID from tb_user where LOGIN = '{username}'"
    conn = sqlite3.connect('streamingCatalogSystem.db')
    cursor = conn.cursor()
    res = cursor.execute(query)
    result = res.fetchall()
    return result


def user_login(username, password):
    users_data = check_user(username)
    if len(users_data) == 0:
        print("Login unsuccessful because user doesn't exist.")
        print("*" * 100)
        return
    conn = sqlite3.connect('streamingCatalogSystem.db')
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM tb_user WHERE LOGIN ='{username}'")
    data = cur.fetchone()
    if data[2] == password:
        print('******************************')
        print(f"{username} LogIn Successful")
        print('******************************')
        while True:
            data = user_data(username)
            if data == "break":
                break
    else:
        print("Login unsuccessful password incorrect.")
        print("*" * 100)



def user_data(username):
    print("Select what you want to watch")
    print("1. Movies")
    print("2. Series")
    print("3. The shows I have already selected.")
    print("4. Exit")
    user_choice = int(input("Enter your Choice: "))

    if user_choice == 1:
        print("What movie you would like to watch? ")
        conn = sqlite3.connect('streamingCatalogSystem.db')
        cursor = conn.cursor()
        cursor.execute('''SELECT * from tb_movies''')
        movie_row = cursor.fetchall()
        for movie_row in movie_row:
            print(movie_row)

        print("*" * 100)

        movie_choice = int(input("Enter the number for which you want to watch movie: "))

        time = input("At what time will you watch/book the movie? ")
        query = f"select TIME from tb_userdata where LOGIN = '{username}'"
        time_check = cursor.execute(query)
        time_list = time_check.fetchall()
        time_list = [x[0] for x in time_list]
        if time in time_list:
            print("You have already booked at this time select another time")
            return
        movie = "movie"
        conn.close()
        add_moviechoice(username, movie_choice, movie, time)

    elif user_choice == 2:
        print("What series you would like to watch? ")
        conn = sqlite3.connect('streamingCatalogSystem.db')
        cursor = conn.cursor()
        cursor.execute('''SELECT * from tb_series''')
        movie_row = cursor.fetchall()
        for movie_row in movie_row:
            print(movie_row)
        # conn.close()
        print("*" * 100)
        series_choice = int(input("Enter the number for which you want to watch series: "))
        # username = input("Enter your username: ")
        time = input("At what time will you watch/book the series? Please enter in hh:mm am/pm. ")

        query = f"select TIME from tb_userdata where LOGIN = '{username}'"
        time_check = cursor.execute(query)
        time_list = time_check.fetchall()
        time_list = [x[0] for x in time_list]
        if time in time_list:
            print("You have already booked at this time select another time")
            return

        series = "series"
        conn.close()
        add_serieschoice(username, series_choice, series, time)


    elif user_choice == 3:
        print("These are the details of the movies/series you have selected: ")
        conn = sqlite3.connect('streamingCatalogSystem.db')
        cursor = conn.cursor()
        # username = input("Enter your username: ")
        query = f"select * from tb_userdata where LOGIN = '{username}'"
        cursor.execute(query)
        show_row = cursor.fetchall()
        for show_row in show_row:
            print("Id: ", show_row[0])
            print("Your username: ", show_row[1])
            print("Show Name: ", show_row[2])
            print("Show Type: ", show_row[3])
            print("Duration: ",show_row[4])
            print("Season: ", show_row[5])
            print("Time: ", show_row[6])
            print("*" * 100)
#            print(show_row)

        conn.close()
        print("*" * 100)

    elif user_choice == 4:
        return "break"



def add_moviechoice(username, movie_choice, movie, time):
    conn = sqlite3.connect('streamingCatalogSystem.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT NAME, DURATION FROM tb_movies WHERE ID ='{movie_choice}'")
    movie_row = cursor.fetchall()

    for movie_row in movie_row:
        movie_name = movie_row[0]
        dur = movie_row[1]

    params = (username, movie_name, movie, dur, time)
    cursor.execute("INSERT INTO tb_userdata (LOGIN, SHOW_NAME, TYPE_SHOW, DURATION, TIME) VALUES (?,?,?,?,?)", params)
    conn.commit()
    print('Movie time booked')
    conn.close()



def add_serieschoice(username, series_choice, series, time):
    conn = sqlite3.connect('streamingCatalogSystem.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT NAME, NO_OF_SEASON FROM tb_series WHERE ID ='{series_choice}'")
    series_row = cursor.fetchall()
    for series_row in series_row:
        series_name = series_row[0]
        season = series_row[1]
    params = (username, series_name, series, season, time)
    cursor.execute("INSERT INTO tb_userdata (LOGIN, SHOW_NAME, TYPE_SHOW, SEASON, TIME) VALUES (?,?,?,?,?)", params)
    conn.commit()
    print('Series time booked')
    conn.close()


def admin_login(username, password):
    admin_data = check_admin(username)
    if len(admin_data) == 0:
        print("Login unsuccessful because user doesn't exist.")
        print("*" * 100)
        return

    conn = sqlite3.connect('streamingCatalogSystem.db')
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM tb_admin WHERE LOGIN ='{username}'")
    data = cur.fetchone()
    if data[2] == password:
        print('******************************')
        print(f"{username} LogIn Successful")
        # print(f"Number of previous logins:{num_logins}")
        print('******************************')
        # update_access_count(user_data[0][0])
        while True:
            movies_data = movie_data()
            if movies_data == "break":
                break
    else:
        print("Login unsuccessful password incorrect.")
        print("*" * 100)




def movie_data():
    print("What data you would like to add?")
    print("1. Movies")
    print("2. Series")
    print("3. Exit")
    print("*" * 100)
    admin_choice = int(input("Enter your choice"))

    if admin_choice == 1:
        movie_name = input("Enter movie name: ")
        movie_dur = input("Enter movie duration: ")
        movie_cat = input("Enter movie category: ")
        add_movie(movie_name, movie_dur, movie_cat)

    if admin_choice == 2:
        series_name = input("Enter series name: ")
        series_season = input("Enter number of season in this series: ")
        series_cat = input("Enter series category: ")
        add_series(series_name, series_season, series_cat)

    elif admin_choice == 3:
        return "break"


def add_movie(movie_name, movie_dur, movie_cat):
    conn = sqlite3.connect('streamingCatalogSystem.db')
    cursor = conn.cursor()
    params = (movie_name, movie_dur, movie_cat)
    cursor.execute("INSERT INTO tb_movies (NAME, DURATION, CATEGORY) VALUES (?,?,?)", params)
    conn.commit()
    print('MOVIE ADDED!')
    print("*" * 100)
    conn.close()


def add_series(series_name, series_season, series_cat):
    conn = sqlite3.connect('streamingCatalogSystem.db')
    cursor = conn.cursor()
    params = (series_name, series_season, series_cat)
    cursor.execute("INSERT INTO tb_series (NAME, NO_OF_SEASON, CATEGORY) VALUES (?,?,?)", params)
    conn.commit()
    print('SERIES ADDED!')
    print("*" * 100)
    conn.close()



if __name__ == "__main__":
    sql_database()
    while True:
        code = app()
        if code == "break":
            break

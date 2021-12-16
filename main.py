import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
pd.options.mode.chained_assignment = None



def app():
    print( "Welcome to Streaming catalog system!" )
    print( "1. Create an account" )
    print( "2. Login into existing account" )
    print( "3. Exit" )
    print( "*" * 100 )
    choice = int( input( "Enter your choice: " ) )
    print( "*" * 100 )
    try:
        if choice == 1:
            print( "1. Create Admin Account" )
            print( "2. Create User Account" )
            print("-" * 100)
            print("Enter any other key to EXIT!")
            print( "*" * 100 )
            choice1 = int( input( "Enter your choice: " ) )
            print( "*" * 100 )

            if choice1 == 1:
                print( "Lets create an admin account" )
                username = input( "Enter username: " )
                password = input( "Enter password: " )
                print( "*" * 100 )
                create_admin( username, password )

            if choice1 == 2:
                print( "Lets create an user account" )
                username = input( "Enter username: " )
                password = input( "Enter password: " )
                print( "*" * 100 )
                create_user( username, password )

        if choice == 2:
            print( "1. Login into Admin Account" )
            print( "2. Login into User Account" )
            print( "-" * 100 )
            print( "Enter any other key to EXIT!" )
            print( "*" * 100 )
            choice1 = int( input( "Enter your choice: " ) )
            print( "*" * 100 )

            if choice1 == 1:
                print( "Welcome to admin login!" )
                username = input( "Enter username: " )
                password = input( "Enter password: " )
                print( "*" * 100 )
                admin_login( username, password )

            if choice1 == 2:
                print( "Welcome to user login!" )
                username = input( "Enter username: " )
                password = input( "Enter password: " )
                print( "*" * 100 )
                user_login( username, password )

        elif choice == 3:
            return "break"
    except:
        print( "_" * 100 )
        print( " " * 30 + "Exited successfully" )
        print( "_" * 100 )


def sql_database():
    conn = sqlite3.connect( 'streamingCatalogSystem.db' )
    c = conn.cursor()

    # create tables
    c.execute( '''CREATE TABLE IF NOT EXISTS tb_user
                (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                LOGIN VARCHAR NOT NULL,
                PASSWORD VARCHAR NOT NULL
                );''' )

    c.execute( '''CREATE TABLE IF NOT EXISTS tb_admin
                (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                LOGIN VARCHAR NOT NULL,
                PASSWORD VARCHAR NOT NULL
                );''' )

    c.execute( '''CREATE TABLE IF NOT EXISTS tb_movies
                (MOVIE_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                NAME VARCHAR NOT NULL,
                DURATION INT NOT NULL,
                CATEGORY VARCHAR NOT NULL
                );''' )

    c.execute( '''CREATE TABLE IF NOT EXISTS tb_series
                    (SERIES_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    NAME VARCHAR NOT NULL,
                    NO_OF_SEASON INT NOT NULL,
                    CATEGORY VARCHAR NOT NULL
                    );''' )

    c.execute( '''CREATE TABLE IF NOT EXISTS tb_userdata
                    (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    LOGIN VARCHAR NOT NULL,
                    SHOW_NAME VARCHAR NOT NULL,
                    TYPE_SHOW VARCHAR NOT NULL,
                    DURATION INT,
                    SEASON INT,
                    TIME VARCHAR NOT NULL,
                    MOVIE_ID INT,
                    SERIES_ID INT
                    );''' )

    # commit the changes to db
    conn.commit()
    # close the connection
    conn.close()


def create_admin(username, password):
    admin_data = check_admin( username )
    if len( admin_data ) > 0:
        print( "Cannot create new admin user because username already exists." )
        print( '*' * 100 )
        return
    conn = sqlite3.connect( 'streamingCatalogSystem.db' )
    cursor = conn.cursor()
    params = (username, password)
    cursor.execute( "INSERT INTO tb_admin (LOGIN, PASSWORD) VALUES (?,?)", params )
    conn.commit()
    print( 'Admin Creation Successful' )
    print( "*" * 100 )
    conn.close()


def check_admin(username):
    query = f"select ID from tb_admin where LOGIN = '{username}'"
    conn = sqlite3.connect( 'streamingCatalogSystem.db' )
    cursor = conn.cursor()
    res = cursor.execute( query )
    result = res.fetchall()
    return result


def create_user(username, password):
    users_data = check_user( username )
    if len( users_data ) > 0:
        print( "Cannot create new user because username already exists." )
        print( '*' * 100 )
        return
    conn = sqlite3.connect( 'streamingCatalogSystem.db' )
    cursor = conn.cursor()
    params = (username, password)
    cursor.execute( "INSERT INTO tb_user (LOGIN, PASSWORD) VALUES (?,?)", params )
    conn.commit()
    print( 'User Creation Successful' )
    print( "*" * 100 )
    conn.close()


def check_user(username):
    query = f"select ID from tb_user where LOGIN = '{username}'"
    conn = sqlite3.connect( 'streamingCatalogSystem.db' )
    cursor = conn.cursor()
    res = cursor.execute( query )
    result = res.fetchall()
    return result


def user_login(username, password):
    users_data = check_user( username )
    if len( users_data ) == 0:
        print( "Login unsuccessful because user doesn't exist." )
        print( "*" * 100 )
        return
    conn = sqlite3.connect( 'streamingCatalogSystem.db' )
    cur = conn.cursor()
    cur.execute( f"SELECT * FROM tb_user WHERE LOGIN ='{username}'" )
    data = cur.fetchone()
    if data[ 2 ] == password:
        print( '************************************************' )
        print( f"WELCOME {username}!! Your LogIn is Successful" )
        print( '************************************************' )
        while True:
            user_data( username )
            # data = user_data( username )
            # if data == "break":
            #     break
    else:
        print( "Login unsuccessful password incorrect." )
        print( "*" * 100 )


def admin_login(username, password):
    admin_data = check_admin( username )
    if len( admin_data ) == 0:
        print( "Login unsuccessful because user doesn't exist." )
        print( "*" * 100 )
        return

    conn = sqlite3.connect( 'streamingCatalogSystem.db' )
    cur = conn.cursor()
    cur.execute( f"SELECT * FROM tb_admin WHERE LOGIN ='{username}'" )
    data = cur.fetchone()
    if data[ 2 ] == password:
        print( '*************************************************' )
        print( f"WELCOME {username}!! Your LogIn is Successful" )
        print( '*************************************************' )
        while True:
            movie_data()
            # movies_data = movie_data()
            # if movies_data == "break":
            #     break
    else:
        print( "Login unsuccessful password incorrect." )
        print( "*" * 100 )


def user_data(username):
    print( "Select what you want to watch" )
    print( "1. Movies" )
    print( "2. Series" )
    print( "3. Display the shows I have already selected." )
    # print( "4. Exit" )
    print( "_" * 100 )
    print( "Enter any other character to exit" )
    print( "*" * 100 )
    user_choice = int( input( "Enter your Choice: " ) )
    print( "*" * 100 )
    try:
        if user_choice == 1:
            print( "What movie you would like to watch? " )
            conn = sqlite3.connect( 'streamingCatalogSystem.db' )
            cursor = conn.cursor()
            cursor.execute( '''SELECT * from tb_movies''' )
            movie_row = cursor.fetchall()
            for movie_row in movie_row:
                print( "MOVIE ID: ", movie_row[ 0 ] )
                print( "MOVIE NAME: ", movie_row[ 1 ] )
                print( "DURATION IN MINUTES: ", movie_row[ 2 ] )
                print( "CATEGORY: ", movie_row[ 3 ] )
                print( "-" * 30 )
            print( "*" * 100 )

            movie_choice = int( input( "Enter the MOVIE ID for which you want to watch movie: " ) )

            time = input( "At what time will you watch/book the series? Please enter in the format (YYYY/MM/DD HH:MM:SS) Enter the time in 24hrs format: " )
            query = f"select TIME from tb_userdata where LOGIN = '{username}'"
            time_check = cursor.execute( query )
            time_list = time_check.fetchall()
            time_list = [ x[ 0 ] for x in time_list ]
            if time in time_list:
                print( "You have already booked at this time select another time" )
                return
            movie = "movie"
            conn.close()
            add_moviechoice( username, movie_choice, movie, time )

        elif user_choice == 2:
            print( "What series you would like to watch? " )
            conn = sqlite3.connect( 'streamingCatalogSystem.db' )
            cursor = conn.cursor()
            cursor.execute( '''SELECT * from tb_series''' )
            series_row = cursor.fetchall()
            for series_row in series_row:
                print( "SERIES ID: ", series_row[ 0 ] )
                print( "SERIES NAME: ", series_row[ 1 ] )
                print( "NUMBER OF SEASON: ", series_row[ 2 ] )
                print( "CATEGORY: ", series_row[ 3 ] )
                print( "-" * 30 )
            print( "*" * 100 )
            series_choice = int( input( "Enter the SERIES ID for which you want to watch series: " ) )
            # username = input("Enter your username: ")
            time = input( "At what time will you watch/book the series? Please enter in the format (YYYY/MM/DD HH:MM:SS) Enter the time in 24hrs format: " )

            query = f"select TIME from tb_userdata where LOGIN = '{username}'"
            time_check = cursor.execute( query )
            time_list = time_check.fetchall()
            time_list = [ x[ 0 ] for x in time_list ]
            if time in time_list:
                print( "You have already booked at this time select another time" )
                return

            series = "series"
            conn.close()
            add_serieschoice( username, series_choice, series, time )


        elif user_choice == 3:
            print( "These are the details of the movies/series you have selected: " )
            conn = sqlite3.connect( 'streamingCatalogSystem.db' )
            cursor = conn.cursor()
            # username = input("Enter your username: ")
            query = f"select * from tb_userdata where LOGIN = '{username}'"
            cursor.execute( query )
            show_row = cursor.fetchall()
            for show_row in show_row:
                # print("Id: ", show_row[0])
                # print("Your username: ", show_row[1])
                print( "Show Name: ", show_row[ 2 ] )
                print( "Show Type: ", show_row[ 3 ] )
                print( "Duration: ", show_row[ 4 ] )
                print( "Season: ", show_row[ 5 ] )
                print( "Time: ", show_row[ 6 ] )
                print( "*" * 100 )
            #            print(show_row)

            conn.close()
            print( "*" * 100 )

        # elif user_choice == 4:
        #     return "break"
    except:
        print( "_" * 100 )
        print( " " * 30 + "Exited successfully" )
        print( "_" * 100 )


def add_moviechoice(username, movie_choice, movie, time):
    conn = sqlite3.connect( 'streamingCatalogSystem.db' )
    cursor = conn.cursor()
    cursor.execute( f"SELECT NAME, DURATION FROM tb_movies WHERE MOVIE_ID ='{movie_choice}'" )
    movie_row = cursor.fetchall()

    for movie_row in movie_row:
        movie_name = movie_row[ 0 ]
        dur = movie_row[ 1 ]

    params = (username, movie_name, movie, dur, time, movie_choice)
    cursor.execute( "INSERT INTO tb_userdata (LOGIN, SHOW_NAME, TYPE_SHOW, DURATION, TIME, MOVIE_ID) VALUES (?,?,?,?,"
                    "?,?)", params )
    conn.commit()
    print( 'Movie time booked' )
    conn.close()


def add_serieschoice(username, series_choice, series, time):
    conn = sqlite3.connect( 'streamingCatalogSystem.db' )
    cursor = conn.cursor()
    cursor.execute( f"SELECT NAME, NO_OF_SEASON FROM tb_series WHERE SERIES_ID ='{series_choice}'" )
    series_row = cursor.fetchall()
    for series_row in series_row:
        series_name = series_row[ 0 ]
        season = series_row[ 1 ]
    params = (username, series_name, series, season, time, series_choice)
    cursor.execute(
        "INSERT INTO tb_userdata (LOGIN, SHOW_NAME, TYPE_SHOW, SEASON, TIME, SERIES_ID) VALUES (?,?,?,?,?,?)", params )
    conn.commit()
    print( 'Series time booked' )
    conn.close()


# ADMIN FUNCTION FOR ADD, UPDATE, DELETE, SHOW
def movie_data():
    print( "1. Add shows" )
    print( "2. Update shows" )
    print( "3. Delete shows" )
    print( "4. View all shows" )
    print( "5. View user bookings" )
    print( "6. View Reports" )
    print( '-' * 100 )
    print( "Enter any other key to exit" )
    print('*' * 100)

    admin_choice_main = int( input( "Enter your choice: " ) )

    try:

        if admin_choice_main == 1:  # add
            while True:
                print( "What data you would like to add?" )
                print( "1. Movies" )
                print( "2. Series" )
                # print( "3. Exit" )
                print("-" * 100)
                print("Enter any other key to exit")
                print( "*" * 100 )
                admin_choice = int( input( "Enter your choice" ) )
                print( "*" * 100 )

                if admin_choice == 1:
                    movie_name = input( "Enter movie name: " )
                    movie_dur = input( "Enter movie duration(in minutes): " )
                    movie_cat = input( "Enter movie category: " )
                    print( "*" * 100 )
                    add_movie( movie_name, movie_dur, movie_cat )

                if admin_choice == 2:
                    series_name = input( "Enter series name: " )
                    series_season = input( "Enter number of season in this series: " )
                    series_cat = input( "Enter series category: " )
                    print( "*" * 100 )
                    add_series( series_name, series_season, series_cat )

                # elif admin_choice == 3:
                #     break

        if admin_choice_main == 2:  # update
            while True:
                print( "What data you would like to update?" )
                print( "1. Movies" )
                print( "2. Series" )
                # print( "3. Exit" )
                print( "-" * 100 )
                print( "Enter any other key to exit" )
                print( "*" * 100 )
                admin_choice = int( input( "Enter your choice: " ) )
                print( "*" * 100 )
                if admin_choice == 1:
                    conn = sqlite3.connect( 'streamingCatalogSystem.db' )
                    cursor = conn.cursor()
                    cursor.execute( '''SELECT * from tb_movies''' )
                    movie_row = cursor.fetchall()
                    for movie_row in movie_row:
                        print( movie_row )  # show all movies
                    print( "*" * 100 )
                    movie_id = int( input( "Enter the id number of the movie which you want to update: " ) )
                    conn.close()
                    update_movie( movie_id )

                if admin_choice == 2:  # seriesupdate
                    conn = sqlite3.connect( 'streamingCatalogSystem.db' )
                    cursor = conn.cursor()
                    cursor.execute( '''SELECT * from tb_series''' )
                    series_row = cursor.fetchall()
                    for series_row in series_row:
                        print( series_row )
                    print( "*" * 100 )
                    series_id = int( input( "Enter the id number of the series which you want to update: " ) )
                    conn.close()
                    update_series( series_id )

                # elif admin_choice == 3:
                #     break

        if admin_choice_main == 3:  # delete show
            while True:
                print( "What data you would like to delete?" )
                print( "1. Movies" )
                print( "2. Series" )
                # print( "3. Exit" )
                print( "-" * 100 )
                print( "Enter any other key to exit" )
                print( "*" * 100 )
                admin_choice = int( input( "Enter your choice: " ) )
                print( "*" * 100 )
                if admin_choice == 1:
                    conn = sqlite3.connect( 'streamingCatalogSystem.db' )
                    cursor = conn.cursor()
                    cursor.execute( '''SELECT * from tb_movies''' )
                    movie_row = cursor.fetchall()
                    for movie_row in movie_row:
                        print( "MOVIE ID: ", movie_row[ 0 ] )
                        print( "MOVIE NAME: ", movie_row[ 1 ] )
                        print( "DURATION IN MINUTES: ", movie_row[ 2 ] )
                        print( "CATEGORY: ", movie_row[ 3 ] )
                        print( "-" * 30 )
                    print( "*" * 100 )  # show all movies
                    movie_id = int( input( "Enter the movie id of the movie which you want to DELETE: " ) )
                    conn.close()
                    delete_movies( movie_id )

                if admin_choice == 2:
                    conn = sqlite3.connect( 'streamingCatalogSystem.db' )
                    cursor = conn.cursor()
                    cursor.execute( '''SELECT * from tb_series''' )
                    series_row = cursor.fetchall()
                    for series_row in series_row:
                        print( "SERIES ID: ", series_row[ 0 ] )
                        print( "SERIES NAME: ", series_row[ 1 ] )
                        print( "NUMBER OF SEASON: ", series_row[ 2 ] )
                        print( "CATEGORY: ", series_row[ 3 ] )
                        print( "-" * 30 )
                    print( "*" * 100 )  # show all movies
                    series_id = int( input( "Enter the series id of the series which you want to DELETE: " ) )
                    conn.close()
                    delete_series( series_id )


                # elif admin_choice == 3:
                #     break

        if admin_choice_main == 4:  # view all shows
            conn = sqlite3.connect( 'streamingCatalogSystem.db' )
            cursor = conn.cursor()
            cursor.execute( '''SELECT * from tb_movies''' )
            movie_row = cursor.fetchall()
            print( "All the movies in the database are as follows:" )
            for movie_row in movie_row:
                # print(movie_row)   show all movies
                print( "MOVIE ID: ", movie_row[ 0 ] )
                print( "MOVIE NAME: ", movie_row[ 1 ] )
                print( "DURATION IN MINUTES: ", movie_row[ 2 ] )
                print( "CATEGORY: ", movie_row[ 3 ] )
                print( "-" * 30 )
                # PRINT EACH COLUMN PENDING
            print( "*" * 100 )
            cursor.execute( '''SELECT * from tb_series''' )
            series_row = cursor.fetchall()
            print( "All the series in the database are as follows:" )
            for series_row in series_row:
                # print(series_row)
                print( "SERIES ID: ", series_row[ 0 ] )
                print( "SERIES NAME: ", series_row[ 1 ] )
                print( "NUMBER OF SEASON: ", series_row[ 2 ] )
                print( "CATEGORY: ", series_row[ 3 ] )
                print( "-" * 30 )
                # PRINT EACH COLUMN PENDING
            print( "*" * 100 )
            conn.close()

        if admin_choice_main == 5:
            while True:
                conn = sqlite3.connect( 'streamingCatalogSystem.db' )
                cursor = conn.cursor()

                query = f"select * from tb_userdata "
                cursor.execute( query )
                show_row = cursor.fetchall()
                for show_row in show_row:
                    print( "_" * 100 )
                    print( "Id: ", show_row[ 0 ] )
                    print( "Username: ", show_row[ 1 ] )
                    print( "Show Name: ", show_row[ 2 ] )
                    print( "Show Type: ", show_row[ 3 ] )
                    print( "Time: ", show_row[ 6 ] )
                    print( "_" * 100 )
                break
            # while True:
            #     movie_data()
                # movies_data = movie_data()
                # if movies_data == "break":
                #     break

        if admin_choice_main == 6:
            while True:
                print( "Report 1: Top 5 most watched movie of the year 2021" )
                print( "Report 2: Top 5 most watched series of the 4th quarter of year 2021" )
                print( "Report 3: Top 5 most watched show of December 2021" )
                print( "Report 4: Top 5 least watched show of the year 2021" )
                print( "Report 5: Top 5 least watched show of the 4th quarter of year 2021" )
                print( "_" * 100 )
                print( "Enter any other character to exit" )
                print( "_" * 100 )
                rchoice = int( input( "Enter your choice: " ) )
                print( "*" * 100 )
                if rchoice == 1:
                    top_5_movie_year()
                    print( "*" * 100 )

                if rchoice == 2:
                    top_5_series_q4()
                    print( "*" * 100 )

                if rchoice == 3:
                    top_5_show_december()
                    print( "*" * 100 )

                if rchoice == 4:
                    least_watched_year()
                    print( "*" * 100 )

                if rchoice == 5:
                    least_watched_show_quarter()
                    print( "*" * 100 )

    except:
        print( "_" * 100 )
        print( " " * 30 + "Exited successfully" )
        print( "_" * 100 )


def add_movie(movie_name, movie_dur, movie_cat):
    conn = sqlite3.connect( 'streamingCatalogSystem.db' )
    cursor = conn.cursor()
    params = (movie_name, movie_dur, movie_cat)
    cursor.execute( "INSERT INTO tb_movies (NAME, DURATION, CATEGORY) VALUES (?,?,?)", params )
    conn.commit()
    print( 'MOVIE ADDED!' )
    print( "*" * 100 )
    conn.close()


def add_series(series_name, series_season, series_cat):
    conn = sqlite3.connect( 'streamingCatalogSystem.db' )
    cursor = conn.cursor()
    params = (series_name, series_season, series_cat)
    cursor.execute( "INSERT INTO tb_series (NAME, NO_OF_SEASON, CATEGORY) VALUES (?,?,?)", params )
    conn.commit()
    print( 'SERIES ADDED!' )
    print( "*" * 100 )
    conn.close()


def update_movie(movie_id):
    conn = sqlite3.connect( 'streamingCatalogSystem.db' )
    cursor = conn.cursor()
    query = f"select TIME from tb_userdata where MOVIE_ID = '{movie_id}'"
    movie_check = cursor.execute( query )
    result = movie_check.fetchall()
    time_list = [ x[ 0 ] for x in result ]
    td = datetime.now()
    for time_entry in time_list:
        yr_td = datetime.strptime( time_entry, "%Y/%m/%d %H:%M:%S" )
        if yr_td >= td:
            print( "You cannot update the movie as it is booked by the user." )
            print( "*" * 100 )
            return

    query = f"select MOVIE_ID from tb_movies where MOVIE_ID = '{movie_id}'"
    movie_check = cursor.execute( query )
    result = movie_check.fetchall()
    time_list = [ x[ 0 ] for x in result ]
    if movie_id in time_list:
        movie_name = input( "Enter updated movie name : " )
        movie_dur = input( "Enter updated movie duration(in minutes): " )
        movie_cat = input( "Enter updated movie category: " )
        params = (movie_name, movie_dur, movie_cat, movie_id)
        cursor.execute( '''UPDATE tb_movies SET NAME = ?, DURATION = ?, CATEGORY = ? WHERE MOVIE_ID = ? ''', params )
        conn.commit()
        print( 'MOVIE UPDATED!' )
        print( "*" * 100 )
    else:
        print( "Movie does not in exist Table." )
        print( '*' * 100 )
    conn.close()


def update_series(series_id):
    conn = sqlite3.connect( 'streamingCatalogSystem.db' )
    cursor = conn.cursor()
    query = f"select TIME from tb_userdata where SERIES_ID = '{series_id}'"
    series_check = cursor.execute( query )
    result = series_check.fetchall()
    series_list = [ x[ 0 ] for x in result ]
    td = datetime.now()
    for time_entry in series_list:
        yr_td = datetime.strptime( time_entry, "%Y/%m/%d %H:%M:%S" )
        if yr_td >= td:
            print( "You cannot update the series as it is booked by the user." )
            print( "*" * 100 )
            return

    query = f"select SERIES_ID from tb_series where SERIES_ID = '{series_id}'"
    series_check = cursor.execute( query )
    result = series_check.fetchall()
    series_list = [ x[ 0 ] for x in result ]
    if series_id in series_list:
        series_name = input( "Enter series name: " )
        series_season = input( "Enter number of season in this series: " )
        series_cat = input( "Enter series category: " )
        params = (series_name, series_season, series_cat, series_id)
        cursor.execute( "UPDATE tb_series SET NAME = ?, NO_OF_SEASON = ?, CATEGORY = ? WHERE SERIES_ID = ?", params )
        conn.commit()
        print( 'SERIES UPDATED!' )
        print( "*" * 100 )
    else:
        print( "Series does not in exist Table." )
        print( '*' * 100 )
    conn.close()


def delete_movies(movie_id):
    conn = sqlite3.connect( 'streamingCatalogSystem.db' )
    cursor = conn.cursor()
    query = f"select TIME from tb_userdata where MOVIE_ID = '{movie_id}'"
    movie_check = cursor.execute( query )
    result = movie_check.fetchall()
    time_list = [ x[ 0 ] for x in result ]
    td = datetime.now()
    for time_entry in time_list:
        yr_td = datetime.strptime( time_entry, "%Y/%m/%d %H:%M:%S" )
        if yr_td >= td:
            print( "You cannot delete the movie as it is booked by the user." )
            print( "*" * 100 )
            return
    query = f"select MOVIE_ID from tb_movies where MOVIE_ID = '{movie_id}'"
    movie_check = cursor.execute( query )
    result = movie_check.fetchall()
    movie_list = [ x[ 0 ] for x in result ]
    if movie_id in movie_list:
        query = f"DELETE FROM tb_movies where MOVIE_ID = '{movie_id}'"
        cursor.execute( query )
        conn.commit()
        print( "Movie Deleted!" )
        print( "*" * 100 )
    else:
        print( "Movie does not in exist Table." )
        print( '*' * 100 )
    conn.close()


def delete_series(series_id):
    conn = sqlite3.connect( 'streamingCatalogSystem.db' )
    cursor = conn.cursor()
    query = f"select TIME from tb_userdata where SERIES_ID = '{series_id}'"
    series_check = cursor.execute( query )
    result = series_check.fetchall()
    series_list = [ x[ 0 ] for x in result ]
    td = datetime.now()
    for time_entry in series_list:
        yr_td = datetime.strptime( time_entry, "%Y/%m/%d %H:%M:%S" )
        if yr_td >= td:
            print( "You cannot delete the series as it is booked by the user." )
            print( "*" * 100 )
            return
    query = f"select SERIES_ID from tb_series where SERIES_ID = '{series_id}'"
    series_check = cursor.execute( query )
    result = series_check.fetchall()
    series_list = [ x[ 0 ] for x in result ]
    if series_id in series_list:
        query = f"DELETE FROM tb_series where SERIES_ID = '{series_id}'"
        cursor.execute( query )
        conn.commit()
        print( "Series Deleted!" )
        print( "*" * 100 )
    else:
        print("Series does not in exist Table.")
        print('*' * 100)

    conn.close()


def top_5_movie_year():
    conn = sqlite3.connect( 'streamingCatalogSystem.db' )
    orig = pd.read_sql( "select * from tb_userdata", con=conn )
    df = orig
    df[ 'TIME' ] = pd.to_datetime( df[ 'TIME' ] )
    df[ 'Year' ] = df[ 'TIME' ].dt.year
    movie = df[ df.TYPE_SHOW == "movie" ]
    movie.drop( [ 'ID', 'LOGIN', 'TYPE_SHOW', 'DURATION', 'SEASON', 'MOVIE_ID', 'SERIES_ID' ], axis=1, inplace=True )
    r1 = movie.groupby( [ 'Year', 'SHOW_NAME' ], as_index=False ).count().pivot( 'Year', 'SHOW_NAME' ).fillna( 0 )
    r1 = r1.T.sort_values( 2021, ascending=False ).T
    cu = len( r1.columns )
    cols = list( range( 5, cu ) )
    r1.drop( r1.columns[ cols ], axis=1, inplace=True )
    print( r1 )
    r1.plot.bar()
    plt.xlabel( 'Year' )
    plt.ylabel( 'No of times watched' )
    plt.show()
    conn.close()


def top_5_series_q4():
    conn = sqlite3.connect( 'streamingCatalogSystem.db' )
    orig1 = pd.read_sql( "select * from tb_userdata", con=conn )
    df1 = orig1
    df1[ 'TIME' ] = pd.to_datetime( df1[ 'TIME' ] )
    df1[ 'Quarter' ] = df1[ 'TIME' ].dt.quarter
    seriesq4 = df1[ df1.TYPE_SHOW == "series" ]
    seriesq4.drop( [ 'ID', 'LOGIN', 'TYPE_SHOW', 'DURATION', 'SEASON', 'MOVIE_ID', 'SERIES_ID' ], axis=1, inplace=True )
    r2 = seriesq4.groupby( [ 'Quarter', 'SHOW_NAME' ], as_index=False ).count().pivot( 'Quarter', 'SHOW_NAME' ).fillna(
        0 )
    r2 = r2.T.sort_values( 4, ascending=False ).T
    cu = len( r2.columns )
    cols = list( range( 5, cu ) )
    r2.drop( r2.columns[ cols ], axis=1, inplace=True )
    print( r2 )
    r2.plot.bar()
    plt.xlabel( 'Quarter' )
    plt.ylabel( 'No of times watched' )
    plt.show()
    conn.close()


def top_5_show_december():
    conn = sqlite3.connect( 'streamingCatalogSystem.db' )
    orig2 = pd.read_sql( "select * from tb_userdata", con=conn )
    df2 = orig2
    df2[ 'TIME' ] = pd.to_datetime( df2[ 'TIME' ] )
    df2[ 'Month' ] = df2[ 'TIME' ].dt.month
    show = df2[ df2.Month == 12 ]
    show.drop( [ 'ID', 'LOGIN', 'TYPE_SHOW', 'DURATION', 'SEASON', 'MOVIE_ID', 'SERIES_ID' ], axis=1, inplace=True )
    r3 = show.groupby( [ 'Month', 'SHOW_NAME' ], as_index=False ).count().pivot( 'Month', 'SHOW_NAME' ).fillna( 0 )
    r3 = r3.T.sort_values( 12, ascending=False ).T
    cu = len( r3.columns )
    cols = list( range( 5, cu ) )
    r3.drop( r3.columns[ cols ], axis=1, inplace=True )
    print( r3 )
    r3.plot.bar()
    plt.xlabel( 'Month' )
    plt.ylabel( 'No of times watched' )
    plt.show()


def least_watched_year():
    conn = sqlite3.connect( 'streamingCatalogSystem.db' )
    orig = pd.read_sql( "select * from tb_userdata", con=conn )
    df = orig
    df[ 'TIME' ] = pd.to_datetime( df[ 'TIME' ] )
    df[ 'Year' ] = df[ 'TIME' ].dt.year
    movie = df
    movie.drop( [ 'ID', 'LOGIN', 'TYPE_SHOW', 'DURATION', 'SEASON', 'MOVIE_ID', 'SERIES_ID' ], axis=1, inplace=True )
    r1 = movie.groupby( [ 'Year', 'SHOW_NAME' ], as_index=False ).count().pivot( 'Year', 'SHOW_NAME' ).fillna( 0 )
    r1 = r1.T.sort_values( 2021, ascending=True ).T
    cu = len( r1.columns )
    cols = list( range( 5, cu ) )
    r1.drop( r1.columns[ cols ], axis=1, inplace=True )
    print( r1 )
    r1.plot.bar()
    plt.xlabel( 'Year' )
    plt.ylabel( 'No of times watched' )
    plt.show()
    conn.close()


def least_watched_show_quarter():
    conn = sqlite3.connect( 'streamingCatalogSystem.db' )
    orig1 = pd.read_sql( "select * from tb_userdata", con=conn )
    df1 = orig1
    df1[ 'TIME' ] = pd.to_datetime( df1[ 'TIME' ] )
    df1[ 'Quarter' ] = df1[ 'TIME' ].dt.quarter
    seriesq4 = df1[ df1.Quarter == 4 ]
    seriesq4.drop( [ 'ID', 'LOGIN', 'TYPE_SHOW', 'DURATION', 'SEASON', 'MOVIE_ID', 'SERIES_ID' ], axis=1, inplace=True )
    r2 = seriesq4.groupby( [ 'Quarter', 'SHOW_NAME' ], as_index=False ).count().pivot( 'Quarter', 'SHOW_NAME' ).fillna(
        0 )
    r2 = r2.T.sort_values( 4, ascending=True ).T
    cu = len( r2.columns )
    cols = list( range( 5, cu ) )
    r2.drop( r2.columns[ cols ], axis=1, inplace=True )
    print( r2 )
    r2.plot.bar()
    plt.xlabel( 'Quarter' )
    plt.ylabel( 'No of times watched' )
    plt.show()
    conn.close()


if __name__ == "__main__":
    sql_database()
    try:
        while True:
            code = app()
            if code == "break":
                break
    except:
        print( "*" * 100 )
        # print( " " * 30 + "Exited successfully" )
        print( " " * 30 + "Enter Correct number: 1,2 or 3!" )
        print( "*" * 100 )
        while True:
            code = app()
            if code == "break":
                break

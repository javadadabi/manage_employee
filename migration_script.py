import psycopg2
import getpass
from psycopg2 import sql


class MyDbMigrator:
    def __init__(self, dbname="postgres", host="localhost", user="postgres", password=None, port="5432"):

        self.db_name = dbname
        self.host = host
        self.user = user
        self.password = password
        self.port = port
        self.conn, self.cursor = None, None

    def connect_to_db(self, dbname="postgres", host="localhost", user="postgres", password=None, port="5432"):
        try:
            connection = psycopg2.connect(
                database=dbname,
                host=host,
                user=user,
                password=password,
                port=port)
            cursor = connection.cursor()
            print('Connected to {} successfully.'.format(dbname))
            initial_settings = """SET statement_timeout = 0;
                                SET lock_timeout = 0;
                                SET idle_in_transaction_session_timeout = 0;
                                SET client_encoding = 'UTF8';
                                SET standard_conforming_strings = on;
                                SELECT pg_catalog.set_config('search_path', '', false);
                                SET check_function_bodies = false;
                                SET xmloption = content;
                                SET client_min_messages = warning;
                                SET row_security = off;
                                SET default_tablespace = '';
                                SET default_table_access_method = heap;"""
            cursor.execute(initial_settings)
            print('Settings initialization was done.')
            return connection, cursor

        except (Exception, psycopg2.Error) as error1:
            print('Error while initializing some settings: ', error1)

    def drop_db(self, database_name):
        try:
            old_isolation_level = self.conn.isolation_level
            self.conn.set_isolation_level(0)
            drop_query = sql.SQL("DROP DATABASE IF EXISTS {}").format(sql.Identifier(database_name))
            # query = "DROP DATABASE IF EXISTS employee_manager3"#
            self.cursor.execute(drop_query)
            self.conn.set_isolation_level(old_isolation_level)
        except psycopg2.Error as drop_error:
            return drop_error

    def create_db(self, database_name):
        try:
            old_isolation_level = self.conn.isolation_level
            self.conn.set_isolation_level(0)
            drop_query = sql.SQL("CREATE DATABASE {} WITH TEMPLATE = template0 ENCODING ="
                                 " 'UTF8' LC_COLLATE = 'en_US.UTF-8' LC_CTYPE = 'en_US.UTF-8';").format \
                (sql.Identifier(database_name))
            self.cursor.execute(drop_query)
            self.conn.set_isolation_level(old_isolation_level)
        except psycopg2.Error as db_creation_error:
            return db_creation_error

    def create_user(self, database_to_grant):

        # The road is open, lets go.
        # So, let me to create a new user:
        username = input('Please enter a user name to create for your database:')
        # Check if there is no user with that name in postgresql
        check_user = "SELECT 1 FROM pg_roles WHERE rolname=%s"
        self.cursor.execute(check_user, (username,))
        user_exist = self.cursor.fetchone()
        if user_exist:
            print('User already exists.')
            password = getpass.getpass('Please enter {} password:'.format(username))
            # self.cursor.close()
            # self.conn.close()
        else:
            password_mismatch = True
            while password_mismatch:
                password_1 = getpass.getpass('Please type your password:')
                password_2 = getpass.getpass('Please retype your password')
                if password_1 != password_2:
                    print('Password mismatch')
                    # Get password again
                    continue
                else:
                    password_mismatch = False
                    password = password_1
            try:
                old_isolation_level = self.conn.isolation_level
                self.conn.set_isolation_level(0)
                create_user_query = sql.SQL("CREATE USER {} WITH PASSWORD %s;").format \
                    (sql.Identifier(username))
                self.cursor.execute(create_user_query, (password,))
                grant_database_owner_q = sql.SQL("ALTER DATABASE {} OWNER TO {};").format \
                    (sql.Identifier(database_to_grant), sql.Identifier(username))
                self.cursor.execute(grant_database_owner_q)
                self.conn.set_isolation_level(old_isolation_level)
            except psycopg2.Error as create_user_error:
                print('Error while creating user:', create_user_error)
        try:
            old_isolation_level = self.conn.isolation_level
            self.conn.set_isolation_level(0)
            grant_database_owner_q = sql.SQL("ALTER DATABASE {} OWNER TO {};").format \
                (sql.Identifier(database_to_grant), sql.Identifier(username))
            self.cursor.execute(grant_database_owner_q)
            self.conn.set_isolation_level(old_isolation_level)
        except psycopg2.Error as grant_database_owner_error:
            print('Error while granting database owner:', grant_database_owner_error)
        finally:
            print('User {} created successfully and {} owner granted to it.'.format(username, database_to_grant))
        return username, password

    def create_employee_manager_schema(self):
        try:
            old_isolation_level = self.conn.isolation_level
            self.conn.set_isolation_level(0)
            with self.cursor as cursor:
                employee_manager_schema_sql = open("employee_manager_schema.sql", "r").read(). \
                    replace('OWNER TO employee_manager', 'OWNER TO ' + self.user_name)
                # print(employee_manager_schema_sql)
                employee_manager_schema_sql = sql.SQL(employee_manager_schema_sql)
                cursor.execute(employee_manager_schema_sql)
                self.conn.set_isolation_level(old_isolation_level)
            print('Database schema created successfully.')
        except psycopg2.Error as schema_creations_error:
            print('Error occurred while creating database schema:', schema_creations_error)
            return schema_creations_error

    def db_check_drop_if_exists(self):
        try:
            database_name = input('pLease insert database name you want to be checked or created:')
            check_database = "SELECT 1 FROM pg_database WHERE datname=%s"
            self.cursor.execute(check_database, (database_name,))
            db_exist = self.cursor.fetchone()
            if db_exist:
                drop_database_or_not = input('Warning, a database with name: {dbname} exists.'
                                             ' Do you want to drop it(it will be drop and a new one will'
                                             ' be created) Y/N?'.
                                             format(dbname=database_name))
                if drop_database_or_not.upper() == 'Y':
                    terminate_db_connections = """SELECT pg_terminate_backend(pid) FROM pg_stat_activity 
                                 WHERE 
                                    pid <> pg_backend_pid()
                                    AND 
                                    datname = %s
                                    ;"""
                    self.cursor.execute(terminate_db_connections, (database_name,))
                    # cursor.close()
                    print(database_name, ' connection terminated successfully.')
                    # drop_db = sql.SQL("DROP DATABASE IF EXISTS {}").format(sql.Identifier(database_name))
                    drop_result = self.drop_db(database_name)
                    if drop_result:
                        print('Error while dropping db', drop_result)
                    else:
                        print('Database dropped successfully.')
                else:
                    return self.db_check_drop_if_exists()
            db_creation_result = self.create_db(database_name)
            if db_creation_result:
                print('Error while creating db ', db_creation_result)
            else:
                print(database_name, ' created successfully.')
                return database_name
        except psycopg2.Error as error2:
            print('Error while checking existence  or dropping:', database_name, error2)

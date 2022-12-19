import getpass


def main():
    try:
        from migration_script import MyDbMigrator
        print('Class imported successfully.')
        postgres_password = getpass.getpass('Enter postgres password:')
        db_migrator_instance = MyDbMigrator(password=postgres_password)
        db_migrator_instance.conn, db_migrator_instance.cursor = db_migrator_instance.connect_to_db(password=postgres_password)
        db_migrator_instance.db_name = db_migrator_instance.db_check_drop_if_exists()
        db_migrator_instance.user_name, db_migrator_instance.password = db_migrator_instance.create_user(db_migrator_instance.db_name)
        db_migrator_instance.cursor.close()
        db_migrator_instance.conn.close()
        db_migrator_instance.conn, db_migrator_instance.cursor = db_migrator_instance.connect_to_db(
            dbname=db_migrator_instance.db_name, user=db_migrator_instance.user_name, password=db_migrator_instance.password)
        has_error = db_migrator_instance.create_employee_manager_schema()
        if not has_error:
            print('Database, schema and username created successfully, now you can change your settings based on:\n'
                  'NAME:', db_migrator_instance.db_name+'\n', 'USER:', db_migrator_instance.user_name+'\n', 'PASSWORD:***')
    except ImportError as exc:
        print("Couldn't import MyDbMigrator.")


if __name__ == '__main__':
    main()

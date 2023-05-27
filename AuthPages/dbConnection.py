import datetime
import cx_Oracle

#tools to connect to oracle database
cx_Oracle.init_oracle_client(lib_dir=r"C:\OracleXE213_Win64\instantclient_21_9")
connStr = '''sys/"Fati@2001"@localhost:1521/XEPDB1'''
def connectionDB(email, code):
    conn = None
    try:
        conn = cx_Oracle.connect(connStr, mode=cx_Oracle.SYSDBA)
        cur = conn.cursor()

        sqlText = 'SELECT * FROM "pfa_user".USERS WHERE user_email=:email'
        print('selecting...')
        cur.execute(sqlText, {'email': email})

        conn.commit()
        result = cur.fetchone()
        if result:
            print('the result not null start of the test...')
            if result[2] is None:
                print('password null...')
                sqlText = 'UPDATE "pfa_user".USERS SET user_password=:1 WHERE user_email=:2'
                cur.execute(sqlText, (code, email))
                conn.commit()
                print("user updated successfully")
            else:
                code = result[2]
        else:
            print('the selected result null')
            date = datetime.datetime.now()
            sqlText = 'INSERT INTO "pfa_user".USERS(user_email, user_password, guest, time_connect) VALUES (:1,:2,:3,:4)'
            cur.execute(sqlText, (email, code, 'yes', date))
            conn.commit()
            print("user inserted successfully")

    except Exception as err:
        print('Error while connection to the db')
        print(err)
    finally:
        if conn:
            cur.close()
            conn.close()
    print("execution complete!")
    return code

# To detect if the member is from ensa or not we use it in the guest pagey
# and to detemine if we should redirect to userlifeconnection progressbar
def query_select(email,status) :
    conn = None
    try:
        conn = cx_Oracle.connect(connStr, mode=cx_Oracle.SYSDBA)
        cur = conn.cursor()
        sqlText = f'SELECT * FROM "pfa_user".USERS WHERE user_email=:email and guest=:status'
        cur.execute(sqlText, {'email': email, 'status': status})
        conn.commit()
        result = cur.fetchone()
        if result:
            return result[3]

    except Exception as err:
        print('Error while connection to the db')
        print(err)
    finally:
        if conn:
            cur.close()
            conn.close()
    print("execution complete!")


# use it in ENSAF2
def query_select_code(email, code) :
    conn = None
    print(email)
    print(code)
    try:
        conn = cx_Oracle.connect(connStr, mode=cx_Oracle.SYSDBA)
        cur = conn.cursor()
        sqlText = f'SELECT * FROM "pfa_user".USERS WHERE user_email=:email and user_password=:password'
        cur.execute(sqlText, {'email': email, 'password': code})
        conn.commit()
        result = cur.fetchone()
        if result:
            return True
        else:
            return False

    except Exception as err:
        print('Error while connection to the db')
        print(err)
    finally:
        if conn:
            cur.close()
            conn.close()
    print("execution complete!")


def query_select_time(email) :
    conn = None
    try:
        conn = cx_Oracle.connect(connStr, mode=cx_Oracle.SYSDBA)
        cur = conn.cursor()
        sqlText = 'SELECT * FROM "pfa_user".USERS WHERE user_email=:email and guest=\'yes\''
        cur.execute(sqlText, {'email': email})
        conn.commit()
        result = cur.fetchone()
        if result:
            return result[4]
        else:
            return

    except Exception as err:
        print('Error while connection to the db')
        print(err)
    finally:
        if conn:
            cur.close()
            conn.close()
    print("execution complete!")

def delete_user_ended_time(email):
        print("start")
        conn = None
        try:
            conn = cx_Oracle.connect(connStr, mode=cx_Oracle.SYSDBA)
            cur = conn.cursor()
            # Define the SQL statement to delete users created before one day from now
            sqlText = f"DELETE FROM \"pfa_user\".USERS WHERE guest='yes' and user_email='{email}' "
            cur.execute(sqlText)
            conn.commit()
            print("finished...")

        except Exception as err:
            print('Error while connection to the db')
            print(err)
        finally:
            if conn:
                cur.close()
                conn.close()
        print("execution complete!")


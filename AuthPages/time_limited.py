import datetime

import cx_Oracle

cx_Oracle.init_oracle_client(lib_dir=r"C:\OracleXE213_Win64\instantclient_21_9")
connStr = '''sys/"Fati@2001"@localhost:1521/XEPDB1'''

print("start")
conn = None
try:
        conn = cx_Oracle.connect(connStr, mode=cx_Oracle.SYSDBA)
        cur = conn.cursor()

        one_day_from_now = datetime.datetime.now() - datetime.timedelta(days=1)
        print(one_day_from_now)
        # Convert the date to Oracle date format
        one_day_from_now_string = one_day_from_now.strftime('%Y-%m-%d %H:%M:%S')
        print(one_day_from_now)
        # Define the SQL statement to delete users created before one day from now
        sqlText = f"DELETE FROM \"pfa_user\".USERS WHERE guest='yes' and time_connect <= TO_DATE('{one_day_from_now_string}', 'YYYY-MM-DD HH24:MI:SS')"
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



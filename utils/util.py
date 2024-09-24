from functools import wraps
import time
import os
import pyodbc
import sys
import json
from datetime import datetime
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2 import IntegrityError 
import logging
import ctypes


class Utilities():
    def __init__(self):
        pass
        # if not os.path.exists("/home/dev/RMS_APPDATA/logs"):
        #     os.mkdir("/home/dev/RMS_APPDATA/logs")
        # logging.basicConfig(filename=f"""/home/dev/RMS_APPDATA/logs/DB_LOG_FILE_{str(datetime.now().strftime('%Y%m%d'))}.log""",
        #                     filemode='a',
        #                     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        # super().__init__()

    def fix_json_file(self, file_path):
        with open(file_path, 'r') as f:
            content = f.read()

        # Remove line breaks and spaces to simplify parsing
        content = content.replace('\n', '').replace(' ', '')

        # Check for missing commas between elements in arrays and dictionaries
        content = content.replace('}{', '},{')  # Add missing comma between adjacent dictionaries
        content = content.replace('][', '],[')  # Add missing comma between adjacent arrays

        # Check for missing opening and closing brackets
        if content.startswith('{') and not content.endswith('}'):
            content += '}'
        elif content.startswith('[') and not content.endswith(']'):
            content += ']'

        try:
            fixed_json = json.loads(content)
            print_green("Json file fixed at ", file_path)
            return fixed_json
        except json.JSONDecodeError as e:
            print(f"Unable to fix the JSON file: {e}")
            return None
        
    def set_thread_affinity(self,thread_id, core_id):
        libc = ctypes.CDLL("libc.so.6")  # Linux-specific, adjust for other platforms
        mask = 1 << core_id
        
        # Create a ctypes c_ulong instance for the mask
        mask_ptr = ctypes.pointer(ctypes.c_ulong(mask))
        
        # Call the syscall to set CPU affinity
        libc.syscall(203, thread_id, ctypes.sizeof(ctypes.c_ulong), mask_ptr)

    def read_json(self, file_path):
        """Read json file from given path"""
        try:
            with open(file_path, "r") as file_contents:
                jsonfile_content = file_contents.read()
                try: 
                    if jsonfile_content:
                        return json.loads(jsonfile_content)
                    else:
                        data = {}
                        return data
                except:
                    return self.fix_json_file(file_path)
        except FileNotFoundError:
            print_red(f"File not found: " + file_path)
            data = {}
            with open(file_path, 'w') as file:
                json.dump(data, file, indent=4)
            print_green(f"Created a new file: " + file_path)
            return data

        except Exception as e:
            print(file_path)
            print_red("[Error] in (utils.util,read_json) msg: ", str(e))
    
    def load_settings(self, path, section):
        """Return settings.json or section if specified"""
        try:
            with open(path, 'r') as file:
                json_data = file.read()
                data = json.loads(json_data)
            return data.get(section)
        except Exception as e:
            print_red("[Error] in (utils.util,load_settings) msg: ", str(e))


class DatabaseConnection(Utilities):
    def __init__(self) -> None:
        super().__init__()
        pass
        # self.ms_con = self.db_connection_dst()
        # self.pg_con = self.pg_connection()
        # self.pg_con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        
    def db_connection_dst(self):
        """Connect to MS SQL destination database"""
        try:
            cnxn = pyodbc.connect(
                "DRIVER="
                + os.getenv("driver")
                + ";SERVER="
                + os.getenv("ip")
                + ";UID="
                + os.getenv("username")
                + ";PWD="
                + os.getenv("password")
                + ";TrustServerCertificate=yes"
            )
            return cnxn

        except Exception as e:
            print_red("[Error] in (utils.util,db_connection_dst) msg: ", str(e))
            sys.exit(1)

    def _forFetchingJson(self, query,one=False):
        """ Fetch data from MS SQL database in JSON format"""
        try :
            cur =self.ms_con.cursor()
            cur.execute(query)
            r = [dict((cur.description[i][0].lower(), value) \
                    for i, value in enumerate(row)) for row in cur.fetchall()]
            cur.close()
            return (r[0] if r else None) if one else r
        except Exception as e :
            print(query)
            print("[Error] in (utils.util,_forFetchingJson) msg: ",str(e))

    def _forFetchingJsonPG(self, query,one=False):
        """ Fetch data from PG SQL database in JSON format"""
        try :
            cur =self.pg_con.cursor()
            cur.execute(query)
            r = [dict((cur.description[i][0].lower(), value) \
                    for i, value in enumerate(row)) for row in cur.fetchall()]
            cur.close()
            return (r[0] if r else None) if one else r
        except Exception as e :
            print(query)
            print("[Error] in (utils.util,_forFetchingJson) msg: ",str(e))
                        
    def pg_connection(connection_string):
        """Postgres connection to database"""
        try:
            cnxn = psycopg2.connect(
                host= connection_string.get("db_host"),
                port = connection_string.get("pg_port"),
                database =  connection_string.get("db_name"),
                user= connection_string.get("db_user"),
                password= connection_string.get("db_password"))
            return cnxn
        except Exception as e:
            print_red("[Error] in (utils.util,pg_connection) msg: ", str(e))
            sys.exit(1)

    def executeQueryPG(connection, query):
        """Execute a query in Pg database"""
        try:
            # print(query)
            # print_blue(connection)
            cur = connection.cursor()
            cur.execute(query)
            connection.commit()
            print_green("================== data has beeen stored =================")
            # cur.close()
        except IntegrityError as ie:
            print_red(ie)
            connection.rollback()
        except Exception as ex:
            print_red(query)
            print_red("\n[Error] in (utils.util,executeQueryPG) msg: ", str(ex))                                     
            logging.warning("ERROR"+str(ex)+"****"+query)
            connection.rollback()
            
    def _executeQuery(self, query) -> None:
        """Execute a query in Destination Database without return value"""
        try:
            cur = self.ms_con.cursor()
            cur.execute(query)
            self.ms_con.commit()
            cur.close()
        except pyodbc.Error as ex:
                sqlstate = ex.args[0]
                if not sqlstate == '23000':
                    print_red(query)
                    print_red("\n[Error] in (utils.util,_executeQuery) msg: ", str(ex))
    
    def fetch_id(self, value, col_name, tb):
        """ Fetch ID from Destination database"""
        try:
            cur = self.pg_con.cursor()
            query = f"""SELECT id FROM "{tb}" WHERE {col_name} = '{value}'"""
            cur.execute(query)

            result = cur.fetchone()
            if result:
                return result[0]
            cur.close()
        except Exception as e:
            print_red(query)
            print_red("\n[Error] in (utils.util,fetch_id) msg: ", str(e))

    def _createNotificationAlert(self,data):
        self.executeQueryPG(f"""
                            INSERT INTO public.notification(
                                createddate, updateddate, date, name, type, description)
                                VALUES ('{datetime.now()}', '{datetime.now()}', '{data.get('date')}', '{data.get('name')}', '{data.get('type')}', '{data.get('description')}');
                            """)



def timer(func):
    """helper function to estimate view execution time"""
    @wraps(func)  # used for copying func metadata
    def wrapper(*args, **kwargs):
        # record start time
        start = time.time()

        # func execution
        result = func(*args, **kwargs)
        
        duration = (time.time() - start) * 1000
        # output execution time to console
        print('{} {:.2f} ms'.format(func.__name__, duration))
        return result
    return wrapper




class ColorPrint:
    def __init__(self, *args, color_code="0"):
        self.args = args
        self.color_code = color_code

    def __str__(self):
        text = " ".join(str(arg) for arg in self.args)
        return f"\033[{self.color_code}m{text}\033[0m"
    
def print_red(*args):
    red_print = ColorPrint(*args, color_code="31")
    print(red_print)

def print_green(*args):
    green_print = ColorPrint(*args, color_code="32")
    print(green_print)
    
def print_yellow(*args):
    yellow_print = ColorPrint(*args, color_code="33")
    print(yellow_print)

def print_blue(*args):
    blue_print = ColorPrint(*args, color_code="34")
    print(blue_print)

def print_magenta(*args):
    magenta_print = ColorPrint(*args, color_code="35")
    print(magenta_print)
    
def print_cyan(*args):
    cyan_print = ColorPrint(*args, color_code="36")
    print(cyan_print)

    
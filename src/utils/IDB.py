from typing import List, Union, Tuple
import numbers
from utils.DB_enum import TableNames
from utils.DB_types import Column
import os
from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
from utils.configuration import USE_DEBUG_DB

#export KEY_VAULT_NAME=redditKeys 
#export AZURE_TENANT_ID={"e99647dc-1b08-454a-bf8c-699181b389ab"}
#export AZURE_CLIENT_ID={"1e20a665-6170-4f7e-86c2-ed8f8c1429d6"}
#export AZURE_CLIENT_SECRET={tPt8wiHYFt9k-ljI-QhLJsPInTPvWYsA8A}

conn = None

class DB_Connection:
    def __init__(self):
        self.conn = self.connect_to_DB()

    def exec_query(self, query: str, show_result=False):
        result = None
        try:
            result = self.try_exec_query(query, show_result)
        except:
            # in case the connsection is not anymore valid, try again to connect
            try:
                self.conn = self.connect_to_DB()
                result = self.try_exec_query(query, show_result)
            except:
                pass
        return result

    def try_exec_query(self, query: str, show_result=False):
        with self.conn.cursor() as cursor:
            cursor.execute(query)
            if show_result:
                from decimal import Decimal
                result = []
                row = cursor.fetchone()
                while row:
                    result.append(list(row))
                    # print(str(row[0]) + " " + str(row[1]))
                    row = cursor.fetchone()
                for row in range(len(result)):
                    for col in range(len(result[row])):
                        if isinstance(result[row][col], Decimal):
                            result[row][col] = float(result[row][col])
                return result
            else:
                return None


    def connect_to_DB(self):
        import pyodbc
        server = 'slr-server.database.windows.net'
        database = 'ScalRelSys'
        if USE_DEBUG_DB:
            database = 'testDB'

        #username = 'slr_best_admin_ever'
        #password = '{vium4tBuK5DBjKv}'
        driver = 'ODBC Driver 17 for SQL Server'

        #Acquisisco i segreti da Azure key vault
        #è necessario impostare le variabili d'ambiente
        # AZURE_CLIENT_ID
        # AZURE_CLIENT_SECRET
        # AZURE_TENANT_ID
        # KEY_VAULT_NAME

        keyVaultName = os.environ["KEY_VAULT_NAME"]
        KVUri = f"https://{keyVaultName}.vault.azure.net"

        credential = DefaultAzureCredential()
        client = SecretClient(vault_url=KVUri, credential=credential)
        username = "DBUsername"
        password = "DBPassword"


        username = client.get_secret(username)
        password = client.get_secret(password)

        return pyodbc.connect('DRIVER=' + driver + ';SERVER=tcp:' + server + ';PORT=1433;DATABASE=' + database + ';UID=' + username.value + ';PWD=' + password.value, autocommit=True)


    def crate_table(self, table_name: TableNames, id_name: str, id_type: str, col_list: List[Column], autogen=True):
        query = f"CREATE TABLE {table_name.value} ("
        query += f"{id_name} {id_type} "
        if id_type == "int" and autogen:
            query += "IDENTITY(1,1)"
        for col in col_list:
            query += f", {col.name} {col.type}"
        query += f", PRIMARY KEY ({id_name})"
        query += ")"
        self.exec_query(query)


    def show_tables(self):
        query = "SELECT * from sys.tables"
        return self.exec_query(query, show_result=True)


    def get_all_values(self, table_name: TableNames):
        query = f"SELECT * from {table_name.value}"
        return self.exec_query(query, show_result=True)


    def delete_table(self, table_name: Union[TableNames, str]):
        value = table_name.value if type(table_name) == TableNames else table_name
        query = f"DROP TABLE {value}"
        self.exec_query(query)


    def get_values(self, table_name: TableNames, request_values: List[str], condition: str = None, order_by: List[str] = None, order_by_asc=True, unique=False):
        query = "SELECT DISTINCT " if unique else "SELECT "
        query += f"{', '.join(request_values)} FROM {table_name.value}"
        if condition is not None:
            query += f" WHERE {condition}"
        if order_by is not None:
            query += " ORDER BY " + ", ".join(order_by)
            query += " ASC " if order_by_asc else " DESC "
        values = self.exec_query(query, show_result=True)
        return values


    def update_value(self, table_name: TableNames, value_name, new_value, condition: str):
        query = f"UPDATE {table_name.value} SET {value_name} = {clean_value_to_str(new_value)} WHERE {condition}"
        self.exec_query(query, show_result=False)


    def update_values(self, table_name: TableNames, condition: str, *values: Tuple[str, any]):
        query = f"UPDATE {table_name.value} SET "
        query += ", ".join([f"{v[0]} = {clean_value_to_str(v[1])}" for v in values])
        query += f" WHERE {condition}"
        self.exec_query(query, show_result=False)


    def delete(self, table_name: TableNames, condition: str):
        query = f"DELETE FROM {table_name.value} WHERE {condition}"
        self.exec_query(query, show_result=False)


    def add_object_to_table(self, table_name: TableNames, *values: Tuple[str, any]):
        query = f"INSERT INTO {table_name.value} ("
        query += ", ".join([v[0] for v in values])
        query += ") VALUES ("
        query += ", ".join([clean_value_to_str(v[1]) for v in values])
        query += ")"
        print(query)
        self.exec_query(query)


    def delete_all_tables(self):
        tables = self.show_tables()
        for table in tables:
            self.delete_table(table[0])


def clean_value_to_str(val):
    if isinstance(val, numbers.Number) and not isinstance(val, int):
        val = "{:.5f}".format(val)
    elif isinstance(val, str):
        val = f"'{val}'"
    return str(val)




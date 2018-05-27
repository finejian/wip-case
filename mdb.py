
import pyodbc
import mdb_query as query

def doQuery(func, args):

    DBfile = r"L:\SDC FIN\WIP transfer\WIP Record\Data\WIP.mdb"
    conn = pyodbc.connect(r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=" + DBfile + ";Uid=;Pwd=;")
    cursor = conn.cursor()

    result = func(cursor, args)

    cursor.close()
    conn.close()

    return result


def __test():
    args1 = ["Viking Wu", "2018/05/27 15:09"]
    print("args1: ", args1)
    rows1 = doQuery(query.queryHistories, args1)
    print("rows1 count: ", len(rows1))
    print("rows1: ", rows1)


if __name__ == '__main__':
    __test()

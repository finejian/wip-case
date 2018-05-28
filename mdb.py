
import pyodbc
import mdb_query as query

def doQuery(func, args):

    DBfile = r"D:\repo\python\wip-case\WIP.mdb"
    conn = pyodbc.connect(r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=" + DBfile + ";Uid=;Pwd=;")
    cursor = conn.cursor()

    if len(args) == 0:
        result = func(cursor)
    else:
        result = func(cursor, args)

    cursor.close()
    conn.close()

    return result


def __test_queryHistories():
    args = ["test", "2017/12/29 15:17"]
    print("test queryHistories args: ", args)
    rows = doQuery(query.queryHistories, args)
    print("queryHistories result count: ", len(rows))
    print("result: ", rows)


def __test_insertCase():
    print("test insertCase: ")
    doQuery(query.insertCase, [])


if __name__ == '__main__':
    __test_queryHistories()
    # __test_insertCase()

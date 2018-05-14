#encoding=utf-8
import json,time,datetime,requests,pymysql
from lxml import etree
class insert(object):
        dbConn = object
        def __init__(self):
            self.dbConn = pymysql.connect(
                user='root',
                port=3306,
                passwd='123456',
                host='localhost',
                db='test',
                charset='utf8'
            )

        # .向数据库插入数据
        def insert(self, tableName, mapx):
            cur = self.dbConn.cursor()
            try:
                cur.execute(self.getInsertStr(tableName, mapx))
                self.dbConn.commit()
                insertId = cur.lastrowid
                cur.close()
                return insertId
            except:
                print('数据库保存失败')
                cur.close()
            finally:
                cur.close()

        def getInsertStr(self, table, mapx):
            sql = "INSERT INTO " + str(table) + "(@keys) " + "VALUE(@vals)"
            keys = ''
            vals = ''
            i = 0
            for x in mapx:
                if i != 0:
                    keys += ',' + str(x)
                    vals += ",'" + str(mapx[x]) + "'"
                else:
                    keys += str(x)
                    vals += "'" + str(mapx[x]) + "'"
                i = i + 1
            return sql.replace('@keys', keys).replace('@vals', vals)
# هذا الفايل اللي اتعامل مع الداتابيس من خلاله


# def insertMultipleRecords(recordList):
#       try:
#           conn = sqlite3.connect('advisors.db')
#           cursor = conn.cursor()
#           print("Connected to SQLite")
#           sql = '''INSERT INTO advisors
#                             (advisor_id, name, email, officeNumber, departmentName) 
#                             VALUES (?, ?, ?, ?, ?);'''
#           cursor.executemany(sql, recordList)
#           conn.commit()
#           print("Total", cursor.rowcount, "Records inserted successfully into advisors table")
#           conn.commit()
#           cursor.close()

#       except sqlite3.Error as error:
#           print("Failed to insert", error)
#       finally:
#           if conn:
#               conn.close()
#               print("The SQLite connection is closed")

#   recordsToInsert = [(53, 'فريق ارشدني', 'arshidniksu@gmail.com', 'WEB', 'نظم المعلومات'),
#                      (54, 'فريق ارشدني', 'arshidniksu@gmail.com', 'WEB', 'تقنية المعلومات'),
#                      (55, 'فريق ارشدني', 'arshidniksu@gmail.com', 'WEB', 'علوم الحاسب'),
#                      (56, 'فريق ارشدني', 'arshidniksu@gmail.com', 'WEB', 'هندسة البرمجيات')]

#   insertMultipleRecords(recordsToInsert)


from translator import database_cred, response_further_test
import mysql.connector as mc
db = database_cred(mc)

cursor = db.cursor()
cursor.execute("INSERT INTO card (test_t_t,name,description,price,precondition,reporting) VALUES (%s,%s,%s,%s,%s,%s)",('xray',response_further_test['imaging-test']['xray'][0],response_further_test['imaging-test']['xray'][1],response_further_test['imaging-test']['xray'][2],response_further_test['imaging-test']['xray'][3],response_further_test['imaging-test']['xray'][4]))
db.commit()
cursor.close()
db.close()
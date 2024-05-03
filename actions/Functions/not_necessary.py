from actions.Functions.translator import database_cred, response_further_test
import mysql.connector as mc
db = database_cred(mc)

cursor = db.cursor()
cursor.execute("INSERT INTO card (test_t_t,name,description,price,precondition,reporting) VALUES (%s,%s,%s,%s,%s,%s)",('rbc',response_further_test['blood-test']['rbc'][0],response_further_test['blood-test']['rbc'][1],response_further_test['blood-test']['rbc'][2],response_further_test['blood-test']['rbc'][3],response_further_test['blood-test']['rbc'][4]))
db.commit()
cursor.close()
db.close()
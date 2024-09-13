#CONNECTING PYTHON AND MYSQL

import mysql.connector
from tabulate import tabulate
mydb = mysql.connector.connect(host="localhost", user="root", password="pandey")

#CREATING DATABASE

mycursor = mydb.cursor()
mycursor.execute("create database if not exists doctor_appointment")
mycursor.execute("use doctor_appointment")
mycursor.execute("create table if not exists user(user_name varchar(20) primary key,password varchar(20))")
mycursor.execute("create table if not exists doctor(doctor_name varchar(20) primary key,password varchar(20))")
mycursor.execute("create table if not exists doctor_details(doctor_name varchar(20),dept_id varchar(5) primary key ,doctor_department varchar(20) ,doctor_phone varchar(11),doctor_available varchar(20))")
print("\n")
print("************************ WELCOME TO DOCTOR APPOINTMENT BOOKING SYSTEM ************************")

#LOGIN OR SIGN UP
run=True
while(run==True):
    print("SIGN UP / LOGIN AS A")
    print("1. PATIENT ")
    print("2. DOCTOR ")
    choice_user = int(input("ENTER YOUR CHOICE : "))
    if(choice_user==1):
        print("1. SIGN UP ")
        print("2. LOG IN ")
        choice_login=int(input("ENTER YOUR CHOICE : "))
        if(choice_login==1):
            username = input("ENTER YOUR USERNAME : ")
            password = input("ENTER YOUR PASSWORD : ")
            mycursor.execute("insert into user(user_name , password) values('"+username+"','"+password+"')")
            mydb.commit()
            print("************************ SIGN UP SUCCESSFULL ************************")
        elif (choice_login ==2):
            username = input("ENTER YOUR USERNAME : ")
            mycursor.execute("select user_name from user where user_name = '"+username+"'")
            pot=mycursor.fetchone()
            
            if pot is not None:
                print("VALID USERNAME")
                password = input("ENTER PASSWORD : ")
                mycursor.execute("select password from user where password = '"+password+"'")
                pot1=mycursor.fetchone()
                if pot1 is not None:
                    print("\n")
                    print("************************ LOGIN SUCCESSFULL ************************")
                    print("\n")
                    print("**************************** WELCOME ******************************")
                    run = False
                else:
                    print("************************ INVALID PASSWORD ************************")
            else:
                print("************************ INVALID USER NAME ************************")
    elif(choice_user==2):
        print("1. SIGN UP ")
        print("2. LOG IN ")
        choice_login=int(input("ENTER YOUR CHOICE "))
        if(choice_login==1):
            username_doc = input("ENTER YOUR USERNAME : ")
            password_doc = input("ENTER YOUR PASSWORD : ")
            mycursor.execute("insert into doctor(doctor_name , password) values('"+username_doc+"','"+password_doc+"')")
            mydb.commit()
            print("#########SIGN UP SUCCESSFULL######")
        elif (choice_login ==2):
            username_doc = input("ENTER YOUR USERNAME : ")
            mycursor.execute("select doctor_name from doctor where doctor_name = '"+username_doc+"'")
            pot_doc=mycursor.fetchone()
            
            if pot_doc is not None:
                print("VALID USERNAME")
                password_doc = input("ENTER PASSWORD : ")
                mycursor.execute("select password from doctor where password = '"+password_doc+"'")
                pot1_doc=mycursor.fetchone()
                if pot1_doc is not None:
                    print("#########LOGIN SUCCESSFULL######")
                    print("######### WELCOME ##############")
                    run = False
                else:
                    print("INVALID PASSWORD")
            else:
                print("INVALID USER NAME ")

                
# ADD APPOINTMENT 
def add_appointment():
    print("\n")
    mycursor.execute("create table if not exists appointment(patient_phno varchar(11) primary key , patient_name varchar(20),department_code varchar(5),date_of_appointment date)")
    patient_phno = input("ENTER PATIENT PHONE NUMBER : ")
    print("")
    name_patient=input("ENTER PATIENT NAME : ")
    print(" ")
    dept_code=input("ENTER DEPARTMENT CODE : ")
    print("")
    date_of_appointment=input("ENTER DATE OF APPOINTMENT (YYYY-MM-DD) : ")
    print("")
    mycursor.execute("select count(date_of_appointment) from appointment where date_of_appointment='"+date_of_appointment+"' and department_code = '"+dept_code+"'")
    result=mycursor.fetchone()
    res = int(result[0])
    if(res>=10):
        print("******************************** SLOT FULLL ************************************")
    else:
        mycursor.execute("insert into appointment values('"+patient_phno+"','"+name_patient+"','"+dept_code+"','"+date_of_appointment+"')")
        mydb.commit()
        print("************************ APPOINTMENT SUCCESSFULLY REGISTERED ************************")


# DELETE APPOINTMENT
def delete_appointment():
    print("\n")
    phone=input("ENTER PHONE NUMBER : ")
    print("")
    mycursor.execute("select * from appointment where patient_phno='"+phone+"'")
    pot_delete = mycursor.fetchall()
    if pot_delete is None :
        print("************************ DATA NOT EXIST ************************")
    else:
        mycursor.execute("delete from appointment where patient_phno='"+phone+"'")
        mydb.commit()
        print("*********************** APPOINTMENT DELETED SUCCESSFULLY ***************************")
    print('\n')


# MODIFY APPOINTMENT
def modify_appointment():
    print("\n")
    phone=input("ENTER PHONE NUMBER : ")
    print("")
    mycursor.execute("select * from appointment where patient_phno='"+phone+"'")
    pot_modify=mycursor.fetchone()
    if pot_modify is None:
        print("************************ DATA NOT EXIT ************************")
    else:
        go=True
        while(go==True):
            print('\n')
            print("************************ MODIFY ************************")
            print(" 1 : PHONE NUMBER ")
            print(" 2 : PATIENT NAME ")
            print(" 3 : DEPARTMENT CODE ")
            print(" 4 : DATE OF APPOINTMENT ")
            print(" 5 : EXIT ")
            choice_modify=int(input("ENTER YOUR CHOICE : "))
            print('')
            if(choice_modify==1):
                new_phno=input("ENTER PHONE NUMBER : ")
                mycursor.execute(" update appointment set patient_phno='"+new_phno+"' where patient_phno='"+phone+"';")
                mydb.commit()
                print("************************ UPDATED ************************")
                print('\n')
            elif(choice_modify==2):
                new_name=input("ENTER NAME : ")
                mycursor.execute(" update appointment set patient_name='"+new_name+"' where patient_phno='"+phone+"';")
                mydb.commit()
                print("************************ UPDATED ************************")
                print('\n')
            elif(choice_modify==3):   
                mycursor.execute("SELECT dept_id ,doctor_department ,doctor_available from doctor_details")
                myresult = mycursor.fetchall()
                print(tabulate(myresult, headers=['DEPT_ID', 'DEPARTMENT','AVAILABILITY'], tablefmt='psql'))
                new_dept=input("ENTER DEPARTMENT ID : ")
                mycursor.execute(" update appointment set department_code='"+new_dept+"' where patient_phno='"+phone+"';")
                mydb.commit()
                print("************************ UPDATED ************************")
                print('\n')
            elif(choice_modify==4):
                mycursor.execute("SELECT dept_id ,doctor_department ,doctor_available from doctor_details")
                myresult = mycursor.fetchall()
                print(tabulate(myresult, headers=['DEPT_ID', 'DEPARTMENT','AVAILABILITY'], tablefmt='psql'))
                new_date=input("ENTER APPOINTMENT DATE (YYYY-MM-DD) : ")
                mycursor.execute(" update appointment set date_of_appointment='"+new_date+"' where patient_phno='"+phone+"';")
                mydb.commit()
                print("************************ UPDATED ************************")
                print('\n')
            else:
                go=False
         
                
# ADD DOCTOR
def add_doc():
    print('\n')
    doc_name=input("ENTER DOCTOR NAME : ")
    doc_dept=input("ENTER DEPARTMENT CODE : ")
    dept_name=input("ENTER DEPARTMENT NAME : ")
    doc_phno=input("ENTER DOCTOR PHONE NUMBER : ")
    doc_avi=input("ENTER DOCTOR AVAILABILITY (DAY-DAY) : ")
    mycursor.execute("insert into doctor_details values('"+doc_name+"','"+doc_dept+"','"+dept_name+"','"+doc_phno+"','"+doc_avi+"')")
    mydb.commit()
    print("####### DETAILS SUCCESSFULLY REGISTERED#########")
    print('\n')
      
      
# CHECK APPOINTMENT
def see_appointment():
    dept=input("ENTER DOCTOR DEPARTMENT ID : ")
    date_=input("ENTER DATE OF APPOINTMENT : ")
    mycursor.execute("select patient_name,department_code,date_of_appointment from appointment where department_code = '"+dept+"' and date_of_appointment = '"+date_+"'")
    myresult = mycursor.fetchall()
    if myresult is None:
        print("-------------------NO APPOINTMENT----------------------------")
    else:
        print(tabulate(myresult, headers=['PATIENT NAME', 'DEPARTMENT','AVAILABILITY'], tablefmt='psql'))
    print('\n')              


# MODIFY DOCTOR DETAILS 
def modify_doc_details():
    dept=input("ENTER DOCTOR DEPARTMENT ID : ")    
    mycursor.execute("select * from doctor_details where dept_id='"+dept+"'")
    pot_doc_modify=mycursor.fetchall()
    if pot_doc_modify is None:
        print("##### DATA NOT EXIT ##########")
    else:
        go_=True
        while(go_==True):
            print('\n')
            print("---------------------MODIFY-----------------------")
            print('\n')
            print(" 1 : DOCTOR NAME ")
            print(" 2 : DEPARTMENT ID ")
            print(" 3 : DEPARTMENT NAME ")
            print(" 4 : DOCTOR PHONE NUMBER ")
            print(" 5 : DOCTOR AVAILABILITY ")
            print(" 6 : EXIT ")
            choice_doc_modify=int(input("ENTER YOUR CHOICE : "))
            if(choice_doc_modify==1):
                new_doc_name=input("ENTER NAME : ")
                mycursor.execute(" update doctor_details set doctor_name ='"+new_doc_name+"' where dept_id='"+dept+"'")
                mydb.commit()
                print("----------UPDATED-----------")
                print('\n')
            elif(choice_doc_modify==2):
                new_dept=input("ENTER DEPARTMENT ID : ")
                mycursor.execute("select * from doctor_details where dept_id='"+new_dept+"'")
                result=mycursor.fetchall()
                if result is not None:
                    print("--------DATA ALREADY EXIST-----------")
                    print('\n')
                else:
                    mycursor.execute("update doctor_details set dept_id='"+new_dept+"' where dept_id='"+dept+"'")
                    mydb.commit()
                    print("----------UPDATED-----------")
                    print('\n')
            elif(choice_doc_modify==3):
                new_dept_name=input("ENTER DEPARTMENT NAME : ")
                mycursor.execute("update doctor_details set doctor_department ='"+new_dept_name+"' where dept_id='"+dept+"'")
                mydb.commit()
                print("----------UPDATED-----------")
                print('\n')
            elif(choice_doc_modify==4):
                new_doc_phno=input("ENTER PHONE NUMBER : ")
                mycursor.execute("update doctor_details set doctor_department ='"+new_doc_phno+"' where dept_id='"+dept+"'")
                mydb.commit()
                print("----------UPDATED-----------")
                print('\n')
            elif(choice_doc_modify==5):
                new_doc_avai=input("ENTER AVAILABILITY (DAY-DAY): ")
                mycursor.execute("update doctor_details set doctor_department ='"+new_doc_avai+"' where dept_id='"+dept+"'")
                mydb.commit()
                print("----------UPDATED-----------")
                print('\n')
            elif(choice_doc_modify==6):
                go_=False


# SEARCH DOCTOR 
def search_doc():
    dept_=input("ENTER DEPARTMENT ID  : ")    
    mycursor.execute("select * from doctor_details where dept_id ='"+dept_+"'")
    pot_doc_details=mycursor.fetchall()
    if pot_doc_details is None:
        print("##### DATA NOT EXIT ##########")
    else:
        print(tabulate(pot_doc_details, headers=['NAME','DEPARTMENT ID','DEPARTMENT NAME','PHONE NUMBER','AVAILABILITY'], tablefmt='psql'))
    print('\n')


# DELETE DOCTOR 
def delete_doc():
    dept_=input("DEPARTMENT ID : ")
    mycursor.execute("select * from doctor_details where dept_id='"+dept_+"'")
    pot_delete = mycursor.fetchall()
    if pot_delete is None :
        print("#####  DATA NOT EXIST ######")
    else:
        mycursor.execute("delete from doctor_details where dept_id='"+dept_+"'")
        mydb.commit()
        print("##################DOCTOR DETAILS DELETED SUCCESSFULLY#######################")
    print('\n')
    

# TREATMENT
def treatment():
    mycursor.execute("create table if not exists record(patient_phno varchar(11) , patient_name varchar(20),department_code varchar(5),date_of_appointment date)")
    phno=input("ENTER PHONE NUMBER OF PATIENT : ")
    mycursor.execute("select * from appointment where patient_phno = '"+phno+"'")
    myresult=mycursor.fetchall()
    if myresult is None :
        print("###### No Patient Exist ########")
    print(tabulate(myresult,headers=['PHONE NUMBER ','PATIENT NAME','DEPARTMENT CODE','DATE OF APPOINTMENT'],tablefmt='psql'))
    print('\n')
    print("******************************************************")
    print(" 1 : TREATMENT CLOSED ")
    print(" 2 : APPOINT NEW DATE")
    choice_treatment=int(input("ENTER YOUR CHOICE : "))
    if(choice_treatment==1):
        mycursor.execute("insert into record select * from appointment where patient_phno='"+phno+"'")
        mycursor.execute("delete from appointment where patient_phno='"+phno+"'")
        mydb.commit()
    elif(choice_treatment==2):
        new_date=input("ENTER APPOINTMENT DATE (YYYY-MM-DD) : ")
        mycursor.execute(" update appointment set date_of_appointment='"+new_date+"' where patient_phno='"+phno+"';")
        mydb.commit()
        print("----------UPDATED-----------")
    print('\n')

# RECORD 
def record():
    mycursor.execute("SELECT * FROM RECORD")
    myresult=mycursor.fetchall()
    print(tabulate(myresult, headers=['PHONE NUMBER ','PATIENT NAME','DEPARTMENT CODE','DATE OF APPOINTMENT'],tablefmt='psql'))

if(choice_user==1):
    while(run==False):
        print("\n")
        print(" 1 : ADD APPOINTMENT ")
        print(" 2 : DELETE AN APPOINTMENT ")
        print(" 3 : MODIFY AN APPOINTMENT ")
        print(" 4 : SEARCH AN APPOINTMENT ")
        print(" 5 : EXIT ")
        choice_patient = int(input("ENTER YOUR CHOICE : "))
        if(choice_patient==1):
            mycursor.execute("SELECT dept_id ,doctor_department ,doctor_available from doctor_details")
            myresult = mycursor.fetchall()
            print(tabulate(myresult, headers=['DEPT_ID', 'DEPARTMENT','AVAILABILITY'], tablefmt='psql'))
            add_appointment()
            
        
        elif(choice_patient==2):   
            delete_appointment()
            
            
        elif(choice_patient==3):
            modify_appointment()
        
        
        elif(choice_patient==4):
            key=input("ENTER REGISTER PHONE NUMBER : ")
            mycursor.execute("select * from appointment where patient_phno='"+key+"'")
            pot_patient = mycursor.fetchone()
            if pot_patient is None :
                print("##############DATA NOT EXIST#################")
            else:
                mycursor.execute("select patient_phno,patient_name,department_code,date_of_appointment from appointment where patient_phno = '"+key+"'")
                myresult = mycursor.fetchall()
                print(tabulate(myresult, headers=['PHONE_NO','PATIENT_NAME','DEPARTMENT','DATE_OF_APPOINTMENT'], tablefmt='psql'))
        elif(choice_patient==5):
            print("-------------- THANK YOU -----------------")
            run=True   


elif(choice_user==2): 
    run_=True
    while(run_==True):
        print("\n")
        print(" 1 : ADD DOCTOR ")
        print(" 2 : APPOINTMENTS ")
        print(" 3 : MODIFY DETAILS ")
        print(" 4 : SEARCH DOCTOR DETAILS ")
        print(" 5 : DELETE DOCTOR DETAILS ")
        print(" 6 : TREATMENT ")
        print(" 7 : RECORD ")
        print(" 8 : EXIT ")
        choice_doc=int(input("ENTER YOUR CHOICE : "))
        if(choice_doc==1):
            add_doc()
        elif(choice_doc==2):
            see_appointment()
        elif(choice_doc==3):
            modify_doc_details()
        elif(choice_doc==4):
            search_doc()
        elif(choice_doc==5):
            delete_doc()
        elif(choice_doc==6):
            treatment()
        elif(choice_doc==7):
            record()
        elif(choice_doc==8):
            print("-------------------- THANK YOU -------------------------")
            run_=False
                
                
                
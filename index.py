import pandas as pd
import matplotlib.pyplot as plt


def login():
    uname = input("Enter username :")
    pwd = input("Enter password:")
    df = pd.read_csv("username.csv")
    df=df.loc[df["username"]==uname]
    if df.empty:
        print("Invalid Password")
        return False
    else:
        print("Username and Password matched successfully")
        getchoice()
def pmenu():
    print("\t\t\t +--------------------------+")
    print("\t\t\t |     PATIENT MAIN MENU    |")
    print("\t\t\t +--------------------------+")
    print("\t\t\t |1. New Patiet Registration|")
    print("\t\t\t |2. Update Patient Details |")
    print("\t\t\t |3. Remove Patient         |")
    print("\t\t\t |4. Search Patient by PNo  |")
    print("\t\t\t |5. All Patient List       |")
    print("\t\t\t |6. Graphs Representation  |")
    print("\t\t\t |7. EXIT                   |")
    print("\t\t\t +--------------------------+")
    print()



def patRegister():
    patdf = pd.read_csv("csvfile\\patientnew.csv", index_col = 0)
    rno = len(patdf)
    while True:
        print("Please Enter Patient Details")
        pid = int(input("Patient Id : "))
        if serPatientbyId(pid)> 0 :
            print("Duplicate Patient Id, ENTER A VALID PATIENT ID")        
        else:
            break
    
    name = input("Name : ")
    age = input("Age : ")
    weight = input("Weight : ")
    gender = input("Gender : ")
    address = input("Address : ")
    phoneno = input("Phone Number : ")
    disease = input("Disease : ")
    patdf.loc[pid,:] = [pid,name,age,weight,gender,address,phoneno,disease]
    #print(patdf)
    patdf.to_csv("csvfile\\patientnew.csv", mode='w')
    print('Patient Registerd Successsfully')


def patUpdate():
    patdf = pd.read_csv("csvfile\\patientnew.csv", index_col = 0)
    pid = int(input("Enter Patient Id to Update: "))

    if serPatientbyId(pid)> 0 :
        print("Patient Found")
        print("Enter details to update patient")
        name = input("Name : ")
        age = input("Age : ")
        weight = input("Weight : ")
        gender = input("Gender : ")
        address = input("Address : ")
        phoneno = input("Phone Number : ")
        disease = input("Disease : ")
        patdf.loc[patdf.loc[patdf['pid'] == pid].index,:] = [pid,name,age,weight,gender,address,phoneno,disease]
        
        patdf.to_csv("csvfile\\patientnew.csv", mode='w')
        print("Patient Updated Successfully")
    else:
        print("Invaid Patient ID")


          
def patRemove():
    patdf = pd.read_csv("csvfile\\patientnew.csv", index_col = 0)
    pid = int(input("Enter Patient Id to Delete: "))
    patdf.drop(patdf.loc[patdf['pid']==pid].index, inplace=True) #Remove
    
    patdf.to_csv("csvfile\\patientnew.csv", mode='w')
    print("Patient Removed Successfully")
    


def dispPatient():
    patdf = pd.read_csv("patientnew.csv", index_col= 0)
    print(patdf)



def serPatientbyId(pid):
    global patdf
    patdf = pd.read_csv("patientnew.csv", index_col = 0)
    if patdf.empty:
        return 0
    else:
        return len(patdf.loc[patdf['pid'] == pid])

def getPatient(pid):
    global patdf
    patdf = pd.read_csv("patientnew.csv", index_col = 0)
    if patdf.empty:
        return "Invalid ID"
    else:
        return patdf.loc[patdf['pid'] == pid]



def getPatientName(pid):
    patdf = pd.read_csv("patientnew.csv", index_col = 0)
    if patdf.empty:
        return "Invalid ID"
    else:
        return patdf.iat[0,1]



def serPatientbyName():
    global patdf
    patdf = pd.read_csv("patientnew.csv", index_col = 0)
    pname  = input("Patient Name :: ")
    print(patdf.loc[patdf['name'] == pname])

def serPatientbyIDPrint():
    global patdf
    patdf = pd.read_csv("patientnew.csv", index_col = 0)
    tid  = int(input("Patient ID :: "))
    print(patdf.loc[patdf['pid'] == tid])

def graph():
    while True:
        print('\nGRAPH MENU ')
        print('_'*100)
        print('1.   LINE Graph\n')
        print('2.   Bar Graph\n')
        print('3.   Scatter Graph\n')
        print('4.   Pie Chart\n')
        print('5.  Back                \n')
        ch = int(input('Enter your choice:'))

        if ch == 1:
            df = pd.read_csv("csvfile\\patientnew.csv")
            x = df['name']
            y = df['age']
            plt.xticks(rotation='vertical')
            plt.xlabel('Name')
            plt.ylabel('Age ')
            plt.title('Name And Age wise')
            plt.grid(True)
            plt.plot(x,y)  #line graph
            plt.show()

        if ch == 2:
            df = pd.read_csv("csvfile\\patientnew.csv")
            x = df['age']
            y = df['disease']
            #plt.xticks(rotation='vertical')
            plt.xlabel('Age')
            plt.ylabel('disease')
            plt.title('Name And Age wise')
            plt.bar(x, y)  #bar graph
            plt.grid(True)
            plt.show()
            wait = input()

        if ch == 3:
            df = pd.read_csv("csvfile\\patientnew.csv")
            x = df['weight']
            y = df['name']
            plt.xticks(rotation='vertical')
            plt.xlabel('Weight')
            plt.ylabel('Names')
            plt.title('Name And Weight wise')
            plt.grid(True)
            plt.scatter(x, y)
            plt.show()
            wait = input()

        if ch == 4:
            df = pd.read_csv("csvfile\\patientnew.csv")
            x = df['age']
            y = df['name']
            plt.pie(x, labels=y, autopct='% .2f', startangle=90)  #pie graph
            plt.xticks(rotation='vertical')
            plt.show()
            
        elif ch == 5:
            break



def getchoice():
    while True:
        pmenu()
        ch = input("\t\t\t Enter Your Choice : ")
        if ch == '1':
            print("PATIENT REGISTRATION")
            patRegister()
        elif ch=='2':
            print("PATIENT UPDATION")
            patUpdate()
        elif ch=='3':
            print("PATIENT DELETION")
            patRemove()
        elif ch=='4':
            print("PATIENT SEARCHING")
            print("1. By ID")
            print("2. By Name")
            ch = input("Enter your search criteria :: ")
            if ch == '1':
                serPatientbyIDPrint()
                print()
                print()
            elif ch == '2':
                serPatientbyName()
                print()
                print()
        elif ch=='5':
            print("\t\tLIST OF PATIENTS")
            print("----------------------------------------")
            dispPatient()
        elif ch=='6':
            graph()
        elif ch == '7':
            print('THANKS FOR USING OUR APP!!')
            break
        else:
            print("INVALID CHOICE")

        input("Press ENTER KEY to continue.....")

#main

login()

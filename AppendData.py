import pyodbc

connectionString = "Driver={ODBC Driver 18 for SQL Server};Server=tcp:p4passwordmanager.database.windows.net,1433;Database=P4PasswordManager;Uid={Insert_Username};Pwd={Insert_Password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"

def ConnectToDb():
    conn = pyodbc.connect(connectionString) #Connect to the database using the connectionstring
    cursor = conn.cursor() #Create a cursor

    return cursor, conn

def AppendData():

    cursor, conn = ConnectToDb()

    cursor.execute("SELECT COUNT(ID) FROM MainTable") #Get the number of passwords
    IDnumber = cursor.fetchone() # Fetch the number of passwords
    print("Number of IDs:", IDnumber[0]) # Print the number of passwords

    Platform = input("Input the platform you want to add: ")
    Password = input("Input the password you want: ")
    cursor.execute("INSERT INTO MainTable (ID, PLatform, Password) VALUES (?, ?, ?)", (IDnumber[0] + 1, Platform, Password)) #Sql command with the user input
    conn.commit()  # Commit the transaction
    print("Data inserted")



def DeletaData():
    cursor, conn = ConnectToDb()

    PasswordsInDb = cursor.execute("SELECT * FROM [dbo].[MainTable]") #Append the SQL commando to get the entire DB
    rows = PasswordsInDb.fetchall() # Get the entire DB

    if not rows: 
        print ("No passwords found")
    else: 
        print("ID,   Website,     Password")
        for row in rows: #Print all of the rows in the DB
            print(row)

    IdDelete = input("Select the password you want to delte based on the ID number: ") #Get user input for the password to delete
            
    PasswordToDelete = conn.execute("SELECT Password FROM [dbo].[MainTable] WHERE ID = (?)" , (IdDelete)) #Verify that the password exist

    Delete = PasswordToDelete.fetchone() #Fetch the sepcific password to be deleted
    for row in Delete: # Get the password that should be deleted
        print("The following password will get deleted: ")
        print(row) #Print the password


    cursor.execute("DELETE FROM [dbo].[MainTable] WHERE ID = (?)", (IdDelete)) #Delete the specified password
    cursor.commit() #Commit the transaction

    print("Password deleted succsesfully")

def ShowPasswords():

    conn, cursor = ConnectToDb()

    FetchAllPasswords = cursor.execute("SELECT * FROM [dbo].[MainTable]") #SQL commando to fetch all passwords  

    rows = FetchAllPasswords.fetchall() #Fetch All passwords

    if not rows:
        print("No passwords found")
    else: 
        print( "ID,    Website,    Passwords")
        for row in rows:
            print(row) #Print all the fetched passwords



def DeleteAddOrShowPasswords():

    while (True):
        conn = ConnectToDb()
        userInput = input("To add a password type 'Add'. To Delete a password type 'Delete'. To show all passwords type 'Show'. To exit type 'Exit': ")
        match userInput:

            case 'Add': #Calls the appendData
                AppendData()

            case 'Delete': #Calls the Delete data
                DeletaData()

            case 'Show': #Calls the show data
                ShowPasswords()

            case 'Exit': #Exit the application
                
                
                break

            case '':
                break


def main():

    DeleteAddOrShowPasswords()


if __name__ == "__main__":
    main()



    

                                                                                                # funkcja do przesy³ania linków do google sheets na podstawie znalezionego kodu kreskowego
																				                # funkcja zlicza iloœæ dostêpnych danych 

link2 = [0] * 7
record = [0] * 7

serial = [0]
index = [0]
indexValue = [0]
barCodeID = [0]
indexExist = [0]
headingIndexValue = [0]
param = [0]
def barCodeFinder(barCode):        
    
    import gspread
    from oauth2client.service_account import ServiceAccountCredentials
    
                                                                                                # use creds to create a client to interact with the Google Drive API and the Google Sheets API
                                                                                                # JSON file in the same folder with API account
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)

                                                                                                # Found sheets - Name 
                                                                                                # sheet1 - Panel
                                                                                                # sheet2 - data from tests
    global record 
    global link2
    global index
    global indexValue
    global barCodeID
    global headingIndexValue

    ws2 = client.open("Excel")
    work = ws2.worksheet("Test")
    ws = ws2.worksheet("Panel")
                                                                                                # Searching for insert barCode in database
    cell = ws.find(barCode)
    record = ws.row_values(1) 
    headingIndexValue = work.row_values(1)                                                                 
    if cell != None:
        barCodeID = ws.row_values(cell.row)                                                     # barCodeID - array with values from row with searched barCode
        print("barCodeID", barCodeID)
        index = [0] * len(barCodeID)                                                            # index - array for tests' dates
        indexValue = [0] * len(barCodeID)
        if len(barCodeID) > 8:                                                                  # finding rows form sheet2 with dates from index
             for i in range(8, len(barCodeID)):
                 index[i-8] = work.find(barCodeID[i])
                 if work.cell(index[i-8].row, 2).value != barCode:
                     index[i-8] = "none"
                 else:
                     indexValue[i-8] = work.row_values(index[i-8].row)
    
    
        
    for i in range(1, 8):                                                                       # save data to the array with parameters from sheet1 and sheet2
        if cell != None:
             link2[i-1] = ws.cell(cell.row, cell.col+i-1).value
        else:
             link2[i-1] = "no data"            


def dataSearch(dateTest):
    import gspread
    from oauth2client.service_account import ServiceAccountCredentials
    
                                                                                                # use creds to create a client to interact with the Google Drive API and the Google Sheets API
                                                                                                # JSON file in the same folder with API account
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)

                                                                                                # Found sheets - Name 
    global param                                                                                            # sheet1 - Panel
                                                                                                # sheet2 - data from tests
    ws2 = client.open("Excel")
    work = ws2.worksheet("Test")
    param = [0] * len(headingIndexValue)
    testParam = work.find(dateTest)
    for i in range(0, len(headingIndexValue)):                                                                 # save data to the array with parameters from sheet1 and sheet2
        if testParam != None:
             param[i] = work.cell(testParam.row, testParam.col+i).value
        else:
             param[i] = "no data"
        
        


                                                                                                # function for finding available names and types of panels
def serialNo():
    import gspread
    from oauth2client.service_account import ServiceAccountCredentials
    
                                                                                                # use creds to create a client to interact with the Google Drive API and the Google Sheets API
                                                                                                # JSON file in the same folder with API account
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)

                                                                                                
                                                                                                # sheet1 = "Panel"
    ws = client.open("Excel").sheet1

    global serial
    serial = ws.col_values(2)

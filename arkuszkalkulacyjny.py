                                                                                                # funkcja do przesy³ania linków do google sheets na podstawie znalezionego kodu kreskowego
																				                # funkcja zlicza iloœæ dostêpnych danych 

link2 = [0, 0, 0, 0, 0, 0, 0]

def barCodeFinder(barCode):        
    
    import gspread
    from oauth2client.service_account import ServiceAccountCredentials
    
                                                                                                # use creds to create a client to interact with the Google Drive API and the Google Sheets API
                                                                                                # JSON file in the same folder with API account
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)

                                                                                                # Znalezienie arkusza - NAZWA + ARKUSZ
                                                                                                # sheet1 = Panel
    ws = client.open("Excel").sheet1
                                                                                                # Znalezienie kodu zczytanego i powi¹zanie go z kodem z bazy 
    cell = ws.find(barCode)
                                                                                                # Wyœwietlenie linku do sharepoint'a (jeœli istnieje)
    if cell != None:
        serialNo = ws.cell(cell.row, cell.col).value
        v = ws.cell(cell.row, cell.col+1).value
        I = ws.cell(cell.row, cell.col+2).value
        Pm = ws.cell(cell.row, cell.col+3).value
        Vpm = ws.cell(cell.row, cell.col+4).value
        Ipm = ws.cell(cell.row, cell.col+5).value
        FF = ws.cell(cell.row, cell.col+6).value
        link = [serialNo, v, I, Pm, Vpm, Ipm, FF]
        
    else:
        link = ["brak danych", 0, 0, 0, 0, 0, 0]

    global link2 
    link2 = link
    
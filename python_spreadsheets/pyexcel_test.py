import xlrd

#----------------------------------------------------------------------

def ping_spreadsheet(file_path):
	ss = xlrd.open_workbook(file_path)
	print(ss.nsheets)
	
    # print sheet names
	print ss.sheet_names()

    # get the first worksheet
	first_sheet = ss.sheet_by_index(0)  # by index
	first_sheet = ss.sheet_by_name(ss.sheet_names()[0]) # by sheet name


    # read a row
	print first_sheet.row_values(0)

    # read a cell
	cell = first_sheet.cell(0,0)
	print cell  
	print cell.value

    # read a row slice
	print first_sheet.row_slice(rowx=0, start_colx=0, end_colx=2)

#----------------------------------------------------------------------

if __name__ == "__main__":
	filename = "election-2000.xlsx"
	ping_spreadsheet(filename)
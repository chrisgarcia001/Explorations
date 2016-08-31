# Roo reads Excel spreadsheets as well as CSV files, etc.
# See the following resources for examples/documentation:
#    https://github.com/roo-rb/roo

require 'rubygems'
require 'roo'

include Roo

# ss = Roo::Spreadsheet.open('election-2000.xlsx')  Read in XLSX and CSV the same
ss = Roo::Spreadsheet.open('election-2000.csv')
puts 'Sheets: ' + ss.sheets.inspect
p ss.sheets.first  # Note that this is just the text title of the worksheet
ss.default_sheet = ss.sheets.first  # Use worksheet names to set current sheet.

ss.first_row.upto(ss.last_row) do |line|
	puts "----- Line #{line} ---------"
	puts ss.cell(line,'A')
	puts ss.cell(line,'B')
	puts ss.cell(line,'C')
	puts ss.cell(line,'D')
end







import xlrd,xlsxwriter,os

def concat(newfile,row):
    total_data = []
    for filename in os.listdir():
        endsName = filename.split(".")[1]
        if(endsName in ["xlsx","xls"]):
            workbook = xlrd.open_workbook(filename)
            worksheet = workbook.sheets()[0]
            result = worksheet.row_values(row-1)
            total_data.append(result)

    newworkbook = xlsxwriter.Workbook(newfile)
    newworksheet = newworkbook.add_worksheet()
    rows = 0
    for data in total_data:
        cols = 0
        for number in data:
            print(number)
            newworksheet.write(rows,cols,number)
            cols += 1
        rows += 1
    newworkbook.close()

def main():
    row = input("请输入你要提取第几行的数据:")
    row = int(row)
    newfile = "inputData/1/data.xlsx"
    concat(newfile,row)

if __name__ == '__main__':
    main()
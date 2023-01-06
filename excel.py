import xlsxwriter

with xlsxwriter.Workbook('排課資料.xlsx') as workbook:
    worksheet = workbook.add_worksheet()

    for i in range(1, 7):
        worksheet.write(chr(65 + i) + '1', i)

    for i in range(1, 15):
        worksheet.write('A' + str(i + 1), i)

with open('./my_courses.txt', 'r') as file:
    ls = []

    for line in file:
        line = line.replace('\n', '')
        line = line.split('.')
        ls.append(line)
        print(line)

# if __name__ == "__main__":
#     pass

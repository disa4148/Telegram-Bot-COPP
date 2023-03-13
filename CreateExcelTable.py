import xlsxwriter
import EmailSender

def InsertTable(name,surname,number,email,age,user_status,addr_to):
    if user_status == 'authorized':
        Collected_Data = (
        ['Имя', name], ['Фамилия', surname], ['Номер телефона', number], ['Адрес эл. почты', email], ['Возраст', age])
        workbook = xlsxwriter.Workbook('C:/Users/7/Desktop/Collected_info_user.xlsx')
        worksheet = workbook.add_worksheet("Лист 1")

        for i, (item, information) in enumerate(Collected_Data, start=1):  # Создание Exel таблицы
            worksheet.write(f'A{i}', item)
            worksheet.write(f'B{i}', information)
        workbook.close()

        files = ["C:/Users/7/Desktop/Collected_info_user.xlsx"]

        EmailSender.send_email(addr_to, "Test Exel", "А вот и текст:)", files)  # Почта находится в файле ForEmail.py


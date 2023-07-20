import requests
from bs4 import BeautifulSoup
import openpyxl


url = 'https://www.bookvoed.ru/books?genre=212'
req = requests.get(url)
soup = BeautifulSoup(req.text, 'lxml')
print(soup.title.text)
books = soup.find('div', class_='fF').find_all('div', class_='Rh')
book_number=0
#___________excel___________
new_book = openpyxl.Workbook()
list = new_book.active
list['A1'] = 'номер'
list['B1'] = 'название'
list['C1'] = 'автор'
list['D1'] = 'аннотация'

#___________excel___________
for item in books:
    book_number+=1
    print(book_number)
    book = item.find('div', class_='ns')
    try:
        book_name = book.find('div', class_='ls ms').find('a').text.strip()
        print('Книга: "'+ book_name+'"')      
    except AttributeError:
        print('Ошибка класса книги')
    try:
        book_author = book.find('div', class_='ps').text.strip()
        print('Автор ', book_author)   
    except:
        print('Ошибка класса книги')
    href = item.find('div', class_='hs').find('a', class_='is js').get('href')
    #print(href)
    req = requests.get(href)
    page = BeautifulSoup(req.text, 'lxml')
    annotation = page.find('div', class_='SD').text
    print('Аннотация: ', annotation, '\n')
    list['A'+str(book_number+1)] = book_number
    list['B'+str(book_number+1)] = book_name
    list['C'+str(book_number+1)] = book_author
    list['D'+str(book_number+1)] = annotation
    book_name = ''
    book_author = ''
    annotation = ''
    
#___________excel___________
new_book.save('books_parsing_result.xlsx')
new_book.close()
#___________excel___________

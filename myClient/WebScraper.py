import requests
from bs4 import BeautifulSoup
import time
import string
from collections import Counter

class WebScraper:
    inverted_index = []
    choice="enter"
    while not choice == 'exit':
        choice = input("Choose- build, load, print, find or exit\n")
        if choice == 'build':
            url='http://example.python-scraping.com/'
            baseurl='http://example.python-scraping.com'
            r = requests.get(url)
            main_queue = []
            current_queue = []
            indices = []
            ctr = 1;

            soup = BeautifulSoup(r.text, 'html.parser')
            for link in soup.find_all('a'):
                    if link.get('href').find('iso') == -1:
                        main_queue.append(baseurl+link.get('href'))
                        current_queue.append(baseurl+link.get('href'))
            time.sleep(5)

            while len(current_queue) != 0:

                item = current_queue.pop(0)
                print(str(ctr)+") Current link- "+item)
                ctr+=1
                inner_r = requests.get(item)
                inner_soup = soup = BeautifulSoup(inner_r.text, 'html.parser')
                strings = []
                index = []
                for each_string in inner_soup.stripped_strings:
                    new_string = each_string.translate(str.maketrans('', '', string.punctuation))
                    seperate = new_string.split(" ")
                    for word in seperate:
                        if len(word) > 2 and not word.isnumeric():
                            word = word.replace('\n','')
                            strings.append(word)
                frequency = dict(Counter(strings))
                index.append(frequency)
                index.append(item)
                indices.append(index)
                for link in inner_soup.find_all('a'):
                    check = baseurl+link.get('href')
                    if check not in main_queue and check.find('/user/') == -1 and check.find('/iso/') == -1 and check.find('/edit/') == -1:
                        main_queue.append(baseurl + link.get('href'))
                        current_queue.append(baseurl + link.get('href'))
                time.sleep(5)

            output = open('inverted_index.txt','w')
            for index in indices:
                temp_url = index[1]
                for key in index[0]:
                    output.write(str(key)+" "+str(index[0][key])+" "+temp_url+"\n")
            output.close()

        elif choice == 'load':
            with open('inverted_index.txt', 'r') as f:
                for line in f:
                    index = []
                    seperate = line.split(" ")
                    for word in seperate:
                        index.append(word)
                    inverted_index.append(index)

        elif choice == 'print':
            print_term = input('Enter search term\n')
            check = False
            if not inverted_index:
                print("Index is empty, please call 'load' function")
            for index in inverted_index:
                if index[0] == print_term:
                    print("Term- "+index[0]+"  Frequency- "+index[1]+"  url- "+index[2]+"\n")
                    check = True
            if not check:
                print("Term not found\n")

        elif choice == 'find':

            words = []
            print_term = input('Enter search term\n')
            check = False
            seperate = print_term.split(" ")
            if not inverted_index:
                print("Index is empty, please call 'load' function")
            for word in seperate:
                words.append(word)
            for word in words:
                for index in inverted_index:
                    if index[0] == word:
                        print("Term- " + index[0] + "  url- " + index[2] + "\n")
                        check = True
            if not check:
                print("Term not found\n")
                
        elif choice == 'exit':
            break

        else:
            print("Not a valid option, remember to use lowercase and avoid spaces")










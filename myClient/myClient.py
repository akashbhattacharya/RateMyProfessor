import requests


class MyClient:
    inp = ''
    while True:
        inp = input("\nregister, login or exit\n")
        if inp == 'register':
            username = input('Enter your username ')
            email = input('Enter your email address ')
            password = input('Enter your password ')
            payload = {'username': username, 'email': email, 'password': password}
            r = requests.post('http://127.0.0.1:8000/register/', data=payload)
            print(r.text)
        elif inp == 'login':
            username = input('Enter your username ')
            password = input('Enter your password ')
            payload = {'username': username, 'password': password}
            r = requests.post('http://127.0.0.1:8000/login/', data=payload)
            print(r.text)
            if r.text == 'Successfully logged in':
                while True:
                    inp2 = input('\nlist, view, average, rate or logout\n')
                    if inp2 == 'logout':
                        r = requests.get('http://127.0.0.1:8000/logout/')
                        print(r.text)
                        break
                    elif inp2 == 'list':
                        r = requests.get('http://127.0.0.1:8000/list/')
                        print(r.text)
                    elif inp2 == 'view':
                        r = requests.get('http://127.0.0.1:8000/view/')
                        print(r.text)
                    elif inp2 == 'average':
                        mid = input('Enter module id ')
                        pid = input('Enter professor id ')
                        payload = {'mid': mid, 'pid': pid}
                        r = requests.post('http://127.0.0.1:8000/average/', data=payload)
                        print(r.text)
                    elif inp2 == 'rate':
                        mid = input('Enter module id ')
                        pid = input('Enter professor id ')
                        year = input('Enter year ')
                        sem = input('Enter semester ')
                        rate = input('Enter your rating ')
                        payload = {'mid': mid, 'pid': pid, 'year': year, 'sem': sem, 'rate': rate}
                        r = requests.post('http://127.0.0.1:8000/rate/', data=payload)
                        print(r.text)
                    else:
                        print('Not a valid command')

        elif inp == 'exit':
            break
        else:
            print("Not a valid command")

import os

def get_file():
    print('Enter file path')
    print('Example: C:\Music.mp3, /home/document/file.txt')
    path = input('>>> ')
    file_name = str(os.path.basename(path))
    print('Your file name is : ' + str(file_name))
    print('If it is wrong enter file name manually')
    print("\n1 - it's correct continue")
    print("2 - It's wrong")
    action = input('>>> ')
    if action == '1':
        pass
    elif action == '2':
        file_name = input('Enter your file name: ')
    else:
        print('Input is incorrect. Try again.')
        get_file()
    file_name = 'file name = ' + file_name
    return file_name, path

#Server actions

def server_file_namefu(con):
    data = con.recv(1024)
    while not data:
        data = con.recv(1024)
    if 'file name = ' in data.decode():
        file_name = str(data.decode()[12:])
    return file_name

def server_send(con):
    file_name, path = get_file()
    con.send(file_name.encode()) 
    file = open(path, 'rb')
    content = file.read(1024)
    while content:
        con.send(content)
        content = file.read(1024)
    print('Done sending')    

def server_receive(con):
    print('Ready to receive') 
    file_name = '/' + server_file_namefu(con)
    save_path = str(os.path.dirname(os.path.realpath(__file__))) + '/ReceivedFiles' + file_name
    with open(save_path, 'wb') as outfile:
        while True:
            print('Receiving data... ')
            data = con.recv(1024)
            if not data:
                break
            outfile.write(data)
    outfile.close()
    print('Successfully get the file')


#Client actions

def client_file_namefu(client):
    data = client.recv(1024)
    while not data:
        data = client.recv(1024)
    if 'file name = ' in data.decode():
        file_name = str(data.decode()[12:])
    return file_name

def client_send(client):
    file_name, path = get_file()
    client.send(file_name.encode()) 
    file = open(path, 'rb')
    content = file.read(1024)
    while content:
        client.send(content)
        content = file.read(1024)
    print('Done sending')  

def client_receive(client): 
    print('Ready to receive')
    file_name = '/' + client_file_namefu(client)
    save_path = str(os.path.dirname(os.path.realpath(__file__))) + '/ReceivedFiles' + file_name
    with open(save_path, 'wb') as outfile:
        while True:
            print('Receiving data... ')
            data = client.recv(1024)
            if not data:
                break
            outfile.write(data)
    outfile.close()
    print('Successfully get the file')
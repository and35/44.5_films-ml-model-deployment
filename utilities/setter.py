import os
from base64 import b64decode

def main():
    key = os.environ.get('SERVICE_ACCOUNT_KEY') # accesdemos a la variable del sistema que definimos en github secrets 
    with open('path.json','w') as json_file:
        json_file.write(b64decode(key).decode()) # pasamos el contenido de base64 > formato json 
    print(os.path.realpath('path.json')) # testing.yaml espera una respuesta en forma de texto asi que le regresamos en print 

if __name__ == '__main__':
    main()
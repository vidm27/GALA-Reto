# Script de Asignar Ubicación a cada participante


La versión de python que estoy utilizando como minimo es `python 3.10` y con gestor de dependencias es `pipenv`,
si no tienes instalado este paquete lo puedes hacer utilizando `pip install pipenv`. Este paquete esta valido tanto en windows,Macs y Linux

Una vez instalado el paquete, puedes crear el entorno virtual con el siguiente comando: `pipenv shell` automaticamente
crea el entorno virtual en tu maquina.

Para instalar las dependencias utiliza el comando `pipenv install` el cual buscara los archivos Pipfile y Pipfile.lock para
sincronizar el entorno virtual de tu maquina con las dependencias que requiere el proyecto. Si todo resulto exitoso procedemos a 
ejecutar el script, tenemos dos opciones:
`pipenv run python main.py` o `python main.py`

#### Opcion 2 (Utilizar virutalenv)
En caso de que este utilizando un sistema operativo linux, utiliza los siguientes comando:
```
sudo apt-get install python3-pip -y
sudo pip3 install virtualenv
virtualenv env
source env/bin/activate
pip install -r requirements.txt
```
**Windows**
```
pip install virtualenv
virtualenv env
.\env\Scripts\activate
pip install -r requirements.txt
```

Luego correr el script con el comando `python main.py`

## Ejecutar los test unitarios
Para la ejecución de los test unitarios se requiere del paquete pytest que en el caso del archivo `requirements.txt`
no aparece que esta dependencia es de desarrollo. Si está utilizando la opcion 2 de instalacion debes instalarlo con: 
`pip install pytest pytest-asyncio`

Para realizar la ejecucion de los test unitarios ejecuda los siguientes comando:
```
cd  tests/

pytest -svv test_location_participant.py
```


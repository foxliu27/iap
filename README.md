# Fuel Cost Api

The project is a Fastapi API to calculate the fuel cost of a vessel.

## Setup Env

Details see: [Doc](https://fastapi.tiangolo.com/virtual-environments/)

Execute the following commands in the project directory(`/fuel-cost`):
1. Create a virtual environment
```bash
python3 -m venv venv
```

2. Activate the virtual environment
```bash
source venv/bin/activate
```

3. Install the dependencies
```bash
pip install -r requirements.txt
```

4. Run dev environment
```bash
fastapi dev
```
 
## Setup DB

1. Create a mysql database using docker
```bash
docker run --name mysql -e MYSQL_ROOT_PASSWORD=123456 -e MYSQL_DATABASE=db -p 3306:3306 -d mysql
```
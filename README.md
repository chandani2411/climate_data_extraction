create a python3 virtual environment using command "virtualenv -p python3 "(on linux)

activate the environment using command "source /bin/activate"(on linux)

install requirements from requirements.txt using command "pip install -r requirements.txt".

go to the folder which has manage.py.

run command "python manage.py runserver"
http://localhost:8000/download_files(get)- To download all the files specified in assignment from the given url.This will store downloaded files in media.


http://localhost:8000/yearwise_data(get)- For storing all the data of  downloaded text files into database using ORM.

http://localhost:8000/export_csv/id(file_id) - This url will export data of model objects having fie_id equals to id into csv file 
and create a chart for that csv file using d3 js.

from "http://localhost:8000/export_csv/id(file_id)"  url user can see chart of any file he wants to see.
Thanks

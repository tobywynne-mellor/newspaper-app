# newspaper-app

## Contributions
- Huu Duy Nguyen
    - 
- Aivaras Voleika
    -
- Toby Wynne-Mellor
    - 

## Populate Database

```bash
# flush database before inserting to avoid errors    
./manage.py flush
./manage.py migrate
./manage.py loaddata newspaper_data 
```


```bash
python manage.py dumpdata -e contenttypes > fixtures/newspaper_data.json
python manage.py loaddata fixtures/newspaper_data.json
```

## Run Development Server

```bash
    ./manage.py runserver
```


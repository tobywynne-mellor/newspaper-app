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

## Run Development Server

```bash
    ./manage.py runserver
```


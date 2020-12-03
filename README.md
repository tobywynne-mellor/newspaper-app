# newspaper-app

## Contributions
- Huu Duy Nguyen
    - Article Model
    - User Like View
    - User Comment View
    - User Profile Picture View
    - Likes Model
    - Comments Model
    - Welcome email
    - User Profile View functions
    - Users & Profile Model 
    - Account Creation Test

- Aivaras Voleika
    - Home template style
    - Create Account Template
    - Login Template
    - Profile Template + Ajax

Liking Test
- Toby Wynne-Mellor
    - Article & User Data
    - Home template Skeleton
    - User Like View
    - User Comment View
    - Add comment to the skeleton
    - Remove Comment Ajax
    - Edit Comment Ajax
    - Add Comment Ajax
    - Add likes to template
    - Remove Like Ajax
    - Add Like Ajax
    - Commenting Test
    - Deploy

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


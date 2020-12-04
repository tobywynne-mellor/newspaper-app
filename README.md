# Group 64 Newspaper Web App

[https://group64-group64.apps.okd.eecs.qmul.ac.uk/](https://group64-group64.apps.okd.eecs.qmul.ac.uk/)

## User Accounts
### Test Users
```bash
1)
username: aivaras
password: aivarasaivaras

2)
username: duy
password: duyduyduy

3)
username: poppy
password: poppypoppy
```
### Admin User
```bash
username: tobywm
password: tobytoby
```

## Contributions
- Huu Duy Nguyen [h.nguyen@se17.qmul.ac.uk](mailto:h.nguyen@se17.qmul.ac.uk)
    - Article, Likes, Comments, Profile models
    - Like view function (POST)
    - Comment view functions (GET, POST)
    - Profile view functions (GET, POST, DELETE)
    - Welcome email functionality
    - Account creation Selenium test

- Aivaras Voleika [ec18258@qmul.ac.uk](mailto:ec18258@qmul.ac.uk)
    - Home template CSS 
    - Register Template + CSS + JS 
    - Login Template + CSS
    - Profile Template, CSS + AJAX
    - Like Selenium Test

- Toby Wynne-Mellor [ec17142@qmul.ac.uk](mailto:ec17142@qmul.ac.uk)
    - Article & User Data
    - Home template HTML
    - Comment HTML, AJAX & view functions (PUT, DELETE) 
    - Like HTML, CSS, AJAX & view functions (DELETE)
    - Comment Selenium test
    - Deployment

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


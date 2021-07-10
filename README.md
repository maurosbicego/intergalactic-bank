# intergalactic-bank

## Project setup for frontend
```
npm install
```
### Set variable VUE_APP_BACKEND in .env file
For example:
```
VUE_APP_BACKEND=http://127.0.0.1:5000
```

### Compiles and hot-reloads for development
```
npm run serve
```

### Compiles and minifies for production
```
npm run build
```

### Lints and fixes files
```
npm run lint
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).


## Setup backend
### Create python.env file
```
database_url="mongodb+srv://{URL}"
flag="spacememes{please_dont_race_with_your_spaceship}"
jwt_secret="{SECRET}"
```
### Run the backend
```
python3 -m flask run
```

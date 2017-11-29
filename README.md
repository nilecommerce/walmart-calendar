<img src="https://s3-us-west-2.amazonaws.com/bambi-data/bambi-engine.png" width="250" align="right">

# Bambi Engine

### Getting Started

*Note: This project uses pipenv, follow [these](https://docs.pipenv.org/) directions to install it.

1. Setup virtualenv and install dependencies
```bash
pipenv install
```

2. Add .env patterned after the [.env.example](/env.example) file in the root directory

3. Activate virtualenv
```bash
pipenv shell
```
  * If you change anything during in the .env file while developing you will need to
    restart the virtualenv as the .env variables are loaded when the virtual env is activated.

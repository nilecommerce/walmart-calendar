<img src="https://s3-us-west-2.amazonaws.com/bambi-data/bambi-engine.png" width="250" align="right">

# Bambi Engine

### Getting Started
1. Add virtualenv
```bash
virtualenv env
```

2. Add the following to the bottom of the virtualenv activate script
```bash
# using /env/bin/activate

export FLASK_APP=app.py
export FLASK_DEBUG=1
```

3. Add .env patterned after the .env.example file in the root directory

4. Install dependencies 
```bash
pip3 install -r requirement.txt
```

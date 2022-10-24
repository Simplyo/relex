# relex
Relex solutions homework assignment

# Requirements and installation:
1. Python, version 3.10.8 recommended
    For example on Ubuntu Linux:
    
    sudo apt update
    sudo apt install python3.

2. Pip

    sudo apt install python3-pip

3. SQLite, version 3.37.2 recommended

   sudo apt install sqlite3

4. Choose a local folder, 'relex' for example and obtaining the Code from GitHub:

    git clone https://github.com/Simplyo/relex ~/relex

5. Install required python libraries:

    switch to the project directory
    cd ~/relex    

    and run
    pip install -r requirements.txt

6. set environment variable PYTHONPATH:

   PYTHONPATH=$PYTHONPATH:~/relex

7. Create sqlite development and testing databases:

    switch to ~/relex/sql and run:

    sqlite3 relex.db <schema.sql
    sqlite3 relex_test.db <schema.sql

8. Switch to project home
    
    cd ~/relex and start project development server by:
    
    flask --app app/run.py run --host=0.0.0.0

    You will see something like that:
    
   * Serving Flask app 'app/run.py'
   * Debug mode: off 
   * WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
   * Running on all addresses (0.0.0.0)
   * Running on http://127.0.0.1:5000
   * Running on http://10.0.0.118:5000
   * Press CTRL+C to quit

9. The server running on port 5000. Make sure that iptables don't deny access to 
the server on that port.

Now you can send POST requests to the server 
http://127.0.0.1:5000/process_report
with JSON reports like that:

{
"server_name": "t-094553234599HH",
"start_time": "2021-05-17T10:12:33Z",
"end_time": "2021-05-17T10:23:33Z"
}

get mean/standard deviation requests 
http://127.0.0.1:5000/process_statistics

and outliers requests
http://127.0.0.1:5000/process_outliers

# Production

Regarding the production it's better to understand technical details about
the system usage. Approximate number of simultaneous requests with server info
and timestamps etc. 
In common words it's required:
1. Running the project with a production WSGI server instead.
    Gunicorn for example and run it in several processes. 
2. Using caching, Flask-Caching for example.
3. Using one of production databases instead of sqlite. For example Redis or PostgreSql, 
it's also depends on technical requirements to the system.
4. Better to use customizing system configuration file config.py
because threshold constants are defined in code now. 
5. Logging system also will be useful.

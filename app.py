import pymysql.cursors
import flask
import os

app = flask.Flask(__name__)

config = {
    'host': os.environ.get('CLEARDB_DATABASE_HOST', 'localhost'),
    'user': os.environ.get('CLEARDB_DATABASE_USER', 'test123'),
    'pwd': os.environ.get('CLEARDB_DATABASE_PWD', 'test123'),
    'db': os.environ.get('CLEARDB_DATABASE_DB', 'lightdb')
}

def pymsqlConnect():
    conn = pymysql.connect(host=config['host'], user=config['user'],
                    passwd=config['pwd'], db=config['db'])
    return conn

@app.route("/getLocation")
def getLocation():
    conn = pymsqlConnect()

    # using `pymysql.cursors.DictCursor` is like
    # mysqli->fetch_all(MYSQLI_ASSOC) in PHP
    c = conn.cursor(pymysql.cursors.DictCursor)
    c.execute("SELECT DISTINCT address, name FROM light")
    res = c.fetchall()
    c.close()
    
    return flask.jsonify(res)

@app.route('/database_map', methods = ['GET'])
def getDataByAddress():
    add = flask.request.args.get('add')
    conn = pymsqlConnect()
    c = conn.cursor(pymysql.cursors.DictCursor)
    c.execute('''SELECT value, time, address FROM light 
               WHERE address = "%s" ORDER BY time ASC''' % (add))
    res = c.fetchall()
    c.close()
    return flask.jsonify(res)

@app.route('/main.js')
def mainJS():
    return flask.send_from_directory('./', 'main.js')

@app.route("/highchart.html")
def highChart():
    return flask.render_template('highchart.html')

@app.route("/")
def index():
    return flask.render_template('index.html')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

import pymysql.cursors
import flask

app = flask.Flask(__name__)

config = {
    'host': 'localhost',
    'user': 'test123',
    'pwd': 'test123',
    'db': 'lightdb'
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
    app.run(host='0.0.0.0', port='1450')

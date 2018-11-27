nstall and Start MariaDBPermalink
sudo yum install mariadb-server
Enable MariaDB to start on boot and then start the service:

sudo systemctl enable mariadb
sudo systemctl start mariadb
MariaDB will bind to localhost (127.0.0.1) by default. For information on connecting to a remote database using SSH, see our MySQL remote access guide, which also applies to MariaDB.

Note
Allowing unrestricted access to MariaDB on a public IP not advised but you may change the address it listens on by modifying the bind-address parameter in /etc/my.cnf. If you decide to bind MariaDB to your public IP, you should implement firewall rules that only allow connections from specific IP addresses.
Harden MariaDB ServerPermalink
Run the mysql_secure_installation script to address several security concerns in a default MariaDB installation:

sudo mysql_secure_installation

create database <database_name> character set UTF8 collate utf8_bin


[root@localhost guotou]# python
Python 3.6.5 (default, Apr 10 2018, 17:08:37) 
[GCC 4.8.5 20150623 (Red Hat 4.8.5-16)] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from flaskblog import db, create_app
>>> db.create_all(app=create_app())     
/usr/lib64/python3.6/site-packages/flask_sqlalchemy/__init__.py:794: FSADeprecationWarning: SQLALCHEMY_TRACK_MODIFICATIONS adds significant overhead and will be disabled by default in the future.  Set it to True or False to suppress this warning.
  'SQLALCHEMY_TRACK_MODIFICATIONS adds significant overhead and '
>>> 


https://stackoverflow.com/questions/20848300/unable-to-create-autoincrementing-primary-key-with-flask-sqlalchemy
id = db.Column(db.Integer, primary_key=True, default=lambda: uuid.uuid4().hex)

https://stackoverflow.com/questions/10494033/setting-sqlalchemy-autoincrement-start-value/10495449

from sqlalchemy import event
from sqlalchemy import DDL
event.listen(
    Article.__table__,
    "after_create",
    DDL("ALTER TABLE %(table)s AUTO_INCREMENT = 1001;")
)

It works! Thanks very much. – Gorthon May 9 '12 at 5:42
1
Is there a way to exclude this from getting executed depending on the db provider? The ALTER ... AUTO_INCREMENT works fine for MySQL (and most other dbs I think), however, this SQL is apparently unsupported for SQLITE. The closest workaround I could find is to do an insert/delete: stackoverflow.com/questions/692856/… – coderfi May 19 '14 at 20:00 
1
Answered my own question. Poking through the code, I found the solution, which is documented by: docs.sqlalchemy.org/en/rel_0_8/core/… The above could be rewritten as event.listen( Article.__table__, "after_create", DDL("ALTER TABLE %(table)s AUTO_INCREMENT = 1001;").execute_if(dialect=('postgresql', 'mysql')) ) which gets me around the sqlite problem. – coderfi May 19 '14 at 20:08

#miaohf
from sqlalchemy import event
from sqlalchemy import DDL
event.listen(
    Article.__table__,
    "after_create",
    DDL("ALTER TABLE %(table)s AUTO_INCREMENT = 1001;")
)#only mysql

event.listen(
	Article.__table__, 
	"after_create", 
	DDL("ALTER TABLE %(table)s AUTO_INCREMENT = 1001;").execute_if(dialect=('postgresql', 'mysql'))
	) # mysql sqlite


#mysql
MariaDB [(none)]> drop database tuozhanrms;create database tuozhanrms character set UTF8 collate utf8_bin;                                      
Query OK, 4 rows affected (0.00 sec)




               // good coding
                {% for point in points %}
                    var i = 0;
                    var p = '{{point.coordinate}}'.split(',');
                    var marker = new BMap.Marker(new BMap.Point(p[0], p[1])); // 创建点
                    map.addOverlay(marker); //增加点
                    pointArray[i] = new BMap.Point(p[0], p[1]);
                    var content ='{{point}}';
                    addClickHandler(content, marker);
                    i++;
                {% endfor %}


## raw python for multi file upload
import os
from flask import Flask, request, redirect, url_for
from werkzeug import secure_filename
import sys
sys.path.insert(0, '/home/muteb/Desktop/test')

UPLOAD_FOLDER = '/home/muteb/Desktop/test/'


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file1 = request.files['file1']
        file2 = request.files['file2']
        if file1 > 0:
            filename1 = secure_filename(file1.filename)
            file1.save(os.path.join(UPLOAD_FOLDER , filename1))
        if file2 > 0:
            filename2 = secure_filename(file2.filename)
            file2.save(os.path.join(UPLOAD_FOLDER , filename2))
            return redirect(url_for('index'))
    return """
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file1>
          <input type=file name=file2>
         <input type=submit value=Upload>
    </form>
    <p>%s</p>
    """ % "<br>".join(os.listdir(app.config['UPLOAD_FOLDER'],))

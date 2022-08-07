from flask import Flask,redirect,session,request,render_template
import os,sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = "fsidf8923j2323j235232kj23345909"
session_key='sdjfoi8235235j23592y3k2qdpaaamf'

#homepage
@app.route("/")
def home_page():
	try:
		conn = sqlite3.connect("db.db")
		con = conn.cursor()
		files = conn.execute("""SELECT * FROM files ORDER BY title ASC """)
		con.close()
		return render_template("index.html",files=files,os=os.listdir("static/media/files"))
	except:
		return render_template("index.html")

# admin
@app.route("/admin")
def admin():
	if(session.get(session_key)):
		try:
			conn = sqlite3.connect("db.db")
			con = conn.cursor()
			files = conn.execute(""" SELECT * FROM files ORDER BY title ASC """)
			con.close()
			return render_template("admin.html",files=files,os=os.listdir("static/media/files"))
		except:
			return render_template("admin.html",username=session.get(session_key))
	else:
		return redirect("/login")

# c_panel
@app.route("/login",methods=['GET','POST'])
def login():
	if(session.get(session_key)):
		return redirect("/admin")
	elif(request.method=='POST'):
		conn = sqlite3.connect("db.db")
		con = conn.cursor()
		username = request.form['username']
		password = request.form['password']
		conn.execute("CREATE TABLE if not exists user_credential(sno INTEGER NOT NULL UNIQUE,username text NOT NULL UNIQUE,password text,primary key('sno' autoincrement)) ")
		res = conn.execute(f"""SELECT * FROM user_credential where username='{username}' and password='{password}' """)
		if(res.fetchall()):
			con.close()
			session[session_key] = username
			return render_template("admin.html",res=username)
		else:
			conn.execute("INSERT INTO user_credential(username,password) VALUES('adminbk108705','12345678bk108705') ")
			conn.commit()
			con.close()
			return render_template("c_panel.html",loging_failed="invalid username or password")
	else:
		return render_template("c_panel.html")

# upload files
@app.route("/upload-files",methods=['GET','POST'])
def upload_files():
	if(session.get(session_key)):
		if(request.method=='POST'):
			file = request.files['file']
			file_title = request.form['title']
			file_size = request.form['size']
			file_type = request.form['type']
			conn = sqlite3.connect("db.db")
			con = conn.cursor()
			try:
				if((file_title and file_size  and file) and (int(file_size) <= 6 )):
					if(file and file_title):
						if(os.path.exists("static/media")):
							pass
						else:
							os.mkdir("static/media")
						if(os.path.exists("static/media/files")):
							file.save(f"static/media/files/{file.filename}")
						else:
							os.mkdir("static/media/files")
							file.save(f"static/media/files/{file.filename}")
						conn.execute("CREATE TABLE if not exists files (sno INTEGER NOT NULL UNIQUE,name TEXT,title TEXT,size INTEGER ,type text,primary key('sno' autoincrement)) ")
						conn.execute(f"""INSERT INTO files (name,title,size,type) VALUES ('{file.filename}','{file_title}','{file_size}','{file_type}') """)
						conn.commit()
						con.close()
						return redirect("/admin")
					else:
						con.close()
						return render_template("admin.html",upload_error="Select file and Write file name.")
				else:
					con.close()
					return render_template("admin.html",file_error=f"File Size Maximum 5MB. and Uploaded File Size {file_size}MB")
			except Exception as errror :
				con.close()
				return render_template("admin.html",upload_error=f'Internal Server EOFError{errror}')
		else:
			return redirect("/admin")
	else:
		return redirect("/login")

	# delete
@app.route("/delete/<file_name>")
def delete_files(file_name):
	if(session.get(session_key)):
		conn = sqlite3.connect('db.db')
		con = conn.cursor()
		try:
			conn.execute(f"""DELETE FROM files where name='{file_name}' """)
			conn.commit()
			con.close()
			os.remove(f"""static/media/files/{file_name}""")
			return redirect("/admin")
		except:
			con.close()
			return redirect("/admin")
	else:
		return redirect("/login")


# logout
@app.route("/logout")
def logout():
	if(session.get(session_key)):
		session.pop(session_key)
		return redirect("/")
	else:
		return redirect("/login")

if __name__ == '__main__':
	app.run()
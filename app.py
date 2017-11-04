from flask import Flask, flash, render_template, json, request, redirect, url_for
from flask.ext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash

mysql = MySQL()
app = Flask(__name__)
app.secret_key='some_secret'


# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'kurkure'
app.config['MYSQL_DATABASE_DB'] = 'payroll'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


@app.route('/')
def home():
	return render_template('index.html')

@app.route('/index')
def main():
    return render_template('index.html')

@app.route('/showLogin')
def showLogin():
	return render_template('login.html')

@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')


@app.route('/showAdminhome')
def showAdminhome():
	return render_template('adminhome.html')


@app.route('/login',methods=['POST','GET'])
def login():
		_username = request.form['inputusername']
		_password = request.form['inputPassword']
		global usn
		usn=request.form['inputusername']

		conn = mysql.connect()
		cursor=conn.cursor()
		cursor.execute("SELECT * from Usernames where user_name='" + _username + "' and user_pass='"+_password+"'")
		data=cursor.fetchone()
		if data is not None:		
				
			print('Logged in successfully')
			return json.dumps({'success':True}),200,{'message':'Logged in successfully'}
		else :

			print('Username or password is wrong')
			return json.dumps({'success':False}), 400, {'error':'not Logged in successfully'}

@app.route('/showProfile')
def showProfile():
	print(usn)
	conn=mysql.connect()
	cursor=conn.cursor()
	cursor.execute("SELECT Employee_ID from Usernames where user_name='"+usn+"'")
	data=cursor.fetchone()
	key=data[0]
	print(key)
	cursor.execute("SELECT * from Employee where Employee_ID='"+str(key)+"'")
	data = cursor.fetchall()
	a,birthdate,fn,mn,ln,des,con = data[0]

	cursor.execute("SELECT * from Salary where Employee_ID='"+str(key)+"'")
	data=cursor.fetchall()
	b,foodall,medicall,basicsal,otcomp,hrall,dall,call,perf=data[0]

	cursor.execute("SELECT * from Deductions where Employee_ID='"+str(key)+"'")
	data=cursor.fetchall()
	c,ins,prot,inct,provf,vprovf,leapen = data[0]

	cursor.execute("SELECT * from Net_Salary where Employee_ID='"+str(key)+"'")
	data=cursor.fetchall()
	d,gro,ded = data[0]

	net=gro-ded

	return render_template('profile.html',fn=fn,mn=mn,ln=ln,key=key,con=con,birthdate=birthdate, basicsal=basicsal, foodall=foodall, medicall=medicall, otcomp=otcomp,hrall=hrall,dall=dall,call=call,perf=perf,ins=ins,prot=prot,inct=inct,provf=provf,vprovf=vprovf,leapen=leapen,gro=gro,ded=ded,net=net)

@app.route('/showReport')
def showReport():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(Insurance) from DEDUCTIONS");
    data =cursor.fetchone()
    sumIns=(int(data[0])) 
    cursor.execute("SELECT SUM(Professional_Tax) from DEDUCTIONS");
    data =cursor.fetchone()
    sumPt=(int(data[0]))           
    cursor.execute("SELECT SUM(Income_Tax) from DEDUCTIONS");
    data =cursor.fetchone()
    sumIt=(int(data[0]))
    cursor.execute("SELECT SUM(Provisional_Fund) from DEDUCTIONS");
    data =cursor.fetchone()
    sumPf=(int(data[0]))
    bale=1000000+sumIns+sumPt+sumIt+sumPf
    return render_template('Report.html',sumIns=sumIns,sumPf=sumPf,sumPt=sumPt,sumIt=sumIt,fund=1000000,bale=bale)
			



@app.route('/adminlogin',methods=['POST','GET'])
def adminlogin():
	try:
		_username = request.form['inputusername']
		_password = request.form['inputPassword']

		if _username == 'admin' and _password =='password':
			return json.dumps({'success':True}),200,{'message':'Logged in successfully'}

		else:
			return json.dumps({'success':False}), 400, {'error':'not Logged in successfully'}
			
	except Exception as e:
		return json.dumps({'error':str(e)})
	





@app.route('/signUp',methods=['POST','GET'])
def signUp():
    try:
        _fname = request.form['inputFName']
        _mname = request.form['inputMName']
        _lname = request.form['inputLName']
        _design = request.form['inputDesignation']
        _id = request.form['inputID']
        _dob = request.form['inputDOB']
        _contact = request.form['inputContact']
        _basic = request.form['inputBasic']
        _overtime = request.form['inputOvertime']
        _vpf = request.form['inputVPF']
        _medico = request.form['inputMedico']
        _leavepen = request.form['inputLeavepen']
        _insurance = request.form['inputInsurance']
        _peer= request.form['inputPeer']
        _manager = request.form['inputManager']

        _email = request.form['inputEmail']
        _password = request.form['inputPassword']

        '''print(_fname)
        print(_mname)
        print(_lname)
        print(_design)
        print(_id)
        print(_dob)
        print(_contact)
        print(_basic)
        print(_overtime)
        print(_vpf)
        print(_medico)
        print(_leavepen)
        print(_insurance)
        print(_email)
        print(_password)
        print(_peer)
        print(_manager)'''

        basic = float(_basic)
        medico= float(_medico)
        overtime= float(_overtime)
        leavepen=float(_leavepen)
        vpf=float(_vpf)
        insurance=float(_insurance)
        peer=float(_peer)
        manager=float(_manager)

        if medico>(0.5*basic):
        	medico=0.5*basic



        _food=0.05*basic
        _food=str(_food)
        _hra=0.4*basic
        _hra=str(_hra)
        _da=0.2*basic
        _da=str(_da)
        _ca=0.05*basic
        _ca=str(_ca)
        _mc=medico
        _mc=str(_mc)
        _ot=overtime*0.05*basic
        _ot=str(_ot)

        _pf=0.12*basic
        _pf=str(_pf)
        _pt=100.0
        _pt=str(_pt)
        _it=0.1*basic
        _it=str(_it)
        if leavepen>=4:
        	_lp=leavepen*0.05*basic
        else:
        	_lp=0.0
        _lp=str(_lp)
        _vpf=vpf/100*basic
        _vpf=str(_vpf)
        _insurance=str(_insurance)

        
        _pb=10.0
        rating=(peer+manager)/2
        if rating>=5:
        	_pb=0.05*basic

        if rating>=7:
        	_pb=0.07*basic

        if rating>=8:
        	_pb=0.1*basic

       	_pb=str(_pb)


       	_gross=float(_food)+float(_hra)+float(_da)+float(_ca)+float(_mc)+float(_ot)+float(_pb)+float(_basic)
       	_gross=str(_gross)

       	'''if float(float(_gross)*12)<250000:
       		_it=0.0
       	elif float(float(_gross)*12)<500000:
       		_it=0.05*(float(_gross)-food)
       	elif float(float(_gross)*12)<1000000:
       		_it=0.1*(float(_gross)-float(food))
       	else:
       		_it=0.3*(float(_gross)-float(food)

       	_it=str(_it)'''

       	_deductions=float(_pf)+float(_pt)+float(_it)+float(_lp)+float(_vpf)+float(_insurance)
        _deductions=str(_deductions)





        # validate the received values
        if _fname and _email and _password:
            
            # All Good, let's call MySQL

            
            conn = mysql.connect()
            cursor = conn.cursor()
            _hashed_password = generate_password_hash(_password)            
                 
            cursor.execute("INSERT into EMPLOYEE(First_Name,Middle_Name,Last_Name,Designation, Employee_ID,Date_of_Birth, Contact_Number)values('"+_fname+"','"+_mname+"','"+_lname+"','"+_design+"',"+_id+",'"+_dob+"',"+_contact+")")
            #cursor.callproc('sp_createUser',(_name,_email,_password))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
            else:
                return json.dumps({'error':str(data[0])})

            cursor.execute("INSERT into SALARY(Employee_ID,Food_Allowance, Medical_Compensation, Overtime_Compensation, HRA,Dearness_Allowance,Conveyance_Allowance, Basic_Salary, Performance_Bonus)values("+_id+","+_food+","+_mc+","+_ot+","+_hra+","+_da+","+_ca+","+_basic+","+_pb+")")
            data =cursor.fetchall()
            if len(data) is 0:
            	conn.commit()
            else:
            	return json.dumps({'html':'<span>Enter the required fields</span>'})

            cursor.execute("INSERT into DEDUCTIONS(Employee_ID,Insurance, Professional_Tax, Income_Tax, Provisional_Fund, VPF, Leave_Penalty)values("+_id+","+_insurance+","+_pt+","+_it+","+_pf+","+_vpf+","+_lp+")")
            data =cursor.fetchall()
            if len(data) is 0:
            	conn.commit()
            else:
            	return json.dumps({'html':'<span>Enter the required fields</span>'})

           	
            cursor.execute("INSERT into Net_Salary(Employee_ID,Gross_Salary, Total_Deductions)values("+_id+","+_gross+","+_deductions+")")
            data =cursor.fetchall()
            if len(data) is 0:
            	conn.commit()
            else:
            	return json.dumps({'html':'<span>Enter the required fields</span>'})

            cursor.execute("INSERT into Usernames(Employee_ID,user_name,user_pass)values("+_id+",'"+_email+"','"+_password+"')")
            data =cursor.fetchall()
            if len(data) is 0:
            	conn.commit()
            else:
            	return json.dumps({'html':'<span>Enter the required fields</span>'})

            cursor.execute("SELECT SUM(Insurance) from DEDUCTIONS");
            data =cursor.fetchone()
            sumIns=(int(data[0]))            
            cursor.execute("SELECT SUM(Professional_Tax) from DEDUCTIONS");
            data =cursor.fetchone()
            sumPt=(int(data[0]))           
            cursor.execute("SELECT SUM(Income_Tax) from DEDUCTIONS");
            data =cursor.fetchone()
            sumIt=(int(data[0]))
            cursor.execute("SELECT SUM(Provisional_Fund) from DEDUCTIONS");
            data =cursor.fetchone()
            sumPf=(int(data[0]))

            fund=1000000                         
            cursor.execute("INSERT INTO Employer(Total_Insurance,Total_Professional_Tax, Total_Provisional_Fund,Total_Income_Tax, Account_Balance) values ('"+str(sumIns)+"','"+str(sumPt)+"','"+str(sumPf)+"','"+str(sumIt)+"',"+str(fund)+")")
            
            if len(data) is not 0:
            	conn.commit()
            	return json.dumps({'message':'User Added!'})
            else:
            	return json.dumps({'html':'<span>Enter the required fields</span>'})

    except Exception as e:
        return json.dumps({'error':str(e)})
    #finally:
      #  cursor.close() 
      #  conn.close()

if __name__ == "__main__":
    app.run(debug=True,port=5002)

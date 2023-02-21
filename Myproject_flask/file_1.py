from flask import Flask,render_template,request,flash,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os
from datetime import date
import dateutil.parser 


upload_folder='static/upload'
app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]='sqlite:///data.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['IMAGE_UPLOADS']="./static/p"

db=SQLAlchemy(app)
app.config['SECRET_KEY'] = "random string"
app.app_context().push()

class contact_list(db.Model):
    __tablename__="contact"
    id=db.Column(db.Integer,primary_key=True)
    img_name = db.Column(db.String(255), nullable=False)
    name=db.Column(db.Text,nullable=False)
    phone=db.Column(db.Text,nullable=False)
    email=db.Column(db.Text,nullable=False)
    address=db.Column(db.Text,nullable=False)
    company=db.Column(db.Text,nullable=False)
    dateofbirth=db.Column(db.DateTime,nullable=False)
    
    
    def __init__(self,name,img_name,phone,email,address,company,dateofbirth):
        self.name=name
        self.img_name=img_name
        self.phone=phone
        self.email=email
        self.address=address
        self.company=company
        self.dateofbirth=dateofbirth

    def __repr__(self):
        return "{} -{}".format(self.name,self.phone)    
        
db.create_all()



@app.route('/',methods=['GET','POST'])
def show():
    if (request.method=="POST"):
        name1=request.form.get('name')
        Pic=request.files['pic']
        filename=secure_filename(Pic.filename)
        if not Pic and not filename:pass
        else:
            Pic.save(os.path.join(app.config['IMAGE_UPLOADS'],filename))
        name=name1.capitalize()
        phone=request.form.get('phone')
        email=request.form.get('email')
        address=request.form.get('address')
        company=request.form.get('company')
        date=dateutil.parser.parse(request.form['birthday']).date()
        
        print(date)
        
        entry=contact_list(name=name,img_name=filename,phone=phone,email=email,address=address,company=company,dateofbirth=date)

        db.session.add(entry)   
        db.session.commit()
        
        flash("record added successfully")
        return redirect(url_for('show'))
    else:

        all_contact=contact_list.query.order_by(contact_list.name).paginate(per_page=2,)
        return render_template('show.html',contact=all_contact)
@app.route("/delete/<id>/",methods=['GET',"POST"])
def delete(id):
    my_data=contact_list.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("employee data deleted successfully","error")
    return redirect(url_for("show"))

@app.route('/update',methods=['GET',"POST"])
def update():
    if request.method=="POST":
        my_data=contact_list.query.get(request.form.get('id'))    
        my_data.name=request.form['name'].capitalize()
        my_data.phone=request.form['phone']
        db.session.commit()
        flash('employee updated successfully','success')
        return redirect(url_for('show'))
    else:
        return redirect(url_for("show"))

@app.route('/search',methods=["POST","GET"])
def search():
    if request.method=="POST":
        text_duplicate=request.form.get('search_text')
        text_real=text_duplicate.capitalize()
        if text_real.isalpha():
            search_t=contact_list.query.filter(contact_list.name.like('%'+text_real+'%')).paginate(per_page=2)
            #search_t=contact_list.query.filter_by(name=text_real).paginate(per_page=2,)
            return render_template('show.html',contact=search_t)
        elif text_real.isdigit():
            search_p=contact_list.query.filter_by(phone=text_real).paginate(per_page=2,)
            return render_template('show.html',contact=search_p) 
    return redirect(url_for('show'))
#for uploading image
app.run(debug=True) 
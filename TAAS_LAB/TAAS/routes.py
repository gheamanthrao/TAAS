from TAAS import app
from flask import render_template, request, redirect, url_for
from TAAS import db
from TAAS.models import Customers, Administrator, Car, Journey, Booking, CModel, Statistics
from datetime import datetime


@app.route("/")
def index():
    return render_template('logreg.html')


@app.route('/about')
def About():
    return render_template('about.html')


@app.route('/contact')
def Contact():
    return render_template('contact.html')


@app.route('/login', methods=["POST", "GET"])
def Login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        cust = Customers.query.filter_by(uname=username).first()
        check = request.form.getlist('adminis')

        if len(check) != 0 and check[0] == 'checked':
            admn = Administrator.query.filter_by(
                uname=username, password=password).first()
            if admn is None:  # if admin is not found
                return redirect('/')
            elif password == admn.password:
                # response.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
                return redirect('/adminstr')
            else:  # if password is wrong
                return redirect('/')

        else:
            cust = Customers.query.filter_by(uname=username).first()
            if cust is None:  # if wrong username
                return redirect("/")
            elif password == cust.password:
                # response.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
                return render_template('customer.html', customer=cust)
            else:  # if password is wrong
                return redirect("/")

    return redirect("/")


@app.route('/customer_register', methods=["POST", "GET"])
def customer_register():
    if request.method == "POST":
        name = request.form['name']
        uname = request.form['uname']
        password = request.form['pswd']
        cust = Customers.query.filter_by(uname=uname).first()
        if cust is None:  # if no such customer already exist
            pjrny = 0
            new_customer = Customers(
                name=name, uname=uname, password=password, pjrny=pjrny, jdate=datetime.utcnow())
            db.session.add(new_customer)
            db.session.commit()
            return render_template('customer.html', customer=new_customer)

    return redirect('/')


@app.route('/adminstr')
def adminstr():
    return render_template('adminstr.html')


@app.route('/customer/<int:id>')
def customer(id):
    cust = Customers.query.filter_by(id=id).first()
    return render_template('customer.html', customer=cust)


@app.route('/customerlist')
def customerlist():
    customers = Customers.query.all()
    return render_template('customerlist.html', customers=customers)


@app.route('/carlist')
def carlist():
    cmdl = CModel.query.all()
    return render_template('carlist.html', cmdl=cmdl)


@app.route('/bookcar/<int:id>')
def bookcar(id):
    cust = Customers.query.filter_by(id=id).first()
    if cust.bcar == 0:
        models = CModel.query.all()
        return render_template('bookcar.html', customer=cust, models=models)
    else:
        return render_template('customer.html', customer=cust)


@app.route('/book/<int:idc>/<int:idm>', methods=["POST", "GET"])
def book(idc, idm):
    if request.method == "POST":
        advance = request.form['advance']
        date_in = request.form['return']
        date_processing = date_in.replace(
            'T', '-').replace(':', '-').split('-')
        date_processing = [int(v) for v in date_processing]
        date_out = datetime(*date_processing)
        check = request.form.getlist('ac')

        cust = Customers.query.filter_by(id=idc).first()
        cmodel = CModel.query.filter_by(mno=idm).first()
        ad = Administrator.query.filter_by(uname="Admin").first()

        if len(check) != 0 and check[0] == 'checked':
            ac = 1
        else:
            ac = 0

        car = Car.query.filter_by(avl=0, ac=ac, mname=cmodel.mname).first()
        if car is None:
            print("none")
            return redirect('/bookcar/'+str(idc))
        booking = Booking(cust=idc, car=car.id, cmodel=car.mname,
                          advance=advance, ereturn=date_out)
        cust.bcar = car.id
        ad.rvnu += int(advance)
        car.avl = 1
        if ac == 1:
            cmodel.accar -= 1
        else:
            cmodel.naccar -= 1
        db.session.add(cust)
        db.session.add(ad)
        db.session.add(cmodel)
        db.session.add(car)
        db.session.add(booking)
        db.session.commit()
    return render_template('customer.html', customer=cust)


@app.route('/booking/<int:idc>/<int:idm>')
def booking(idc, idm):
    cust = Customers.query.filter_by(id=idc).first()
    models = CModel.query.all()
    cmodel = CModel.query.filter_by(mno=idm).first()
    return render_template('book.html', customer=cust, models=models, model=cmodel)


@app.route('/stats')
def stats():
    statlist = Statistics.query.all()
    ad = Administrator.query.filter_by(uname="Admin").first()
    return render_template('stats.html', admin=ad, statlist=statlist)


@app.route('/addCar', methods=["POST", "GET"])
def add_Car():
    if(request.method == "POST"):
        carname = request.form['carname']
        quantity = int(request.form['quantity'])
        type = request.form['dog-names']
        cost_h = request.form['cost_h']
        cost_k = request.form['cost_k']
        if type == "AC":
            cmdl = CModel.query.filter_by(mname=carname).first()
            if cmdl is None:
                cmdl = CModel(mname=carname, accar=quantity,
                              naccar=0, rent_h=cost_h, rent_k=cost_k)
                sts = Statistics(mname=cmdl.mname, demand=0, rvnu=0,
                                 feedback=5, mntnc=0, fuel=0)
                db.session.add(sts)
            else:
                cmdl.accar += quantity
            db.session.add(cmdl)
            db.session.commit()
            for i in range(int(quantity)):
                car = Car(mname=carname, model=cmdl.mno,
                          kms=0, ac=True, avl=0, fuel=0)
                db.session.add(car)
            db.session.commit()
            db.session.commit()
        else:
            cmdl = CModel.query.filter_by(mname=carname).first()
            if cmdl is None:
                cmdl = CModel(mname=carname, accar=0, naccar=quantity,
                              rent_h=cost_h, rent_k=cost_k)
                sts = Statistics(mname=cmdl.mname, demand=0, rvnu=0,
                                 feedback=5, mntnc=0, fuel=0)
                db.session.add(sts)
            else:
                cmdl.naccar += quantity
            db.session.add(cmdl)
            db.session.commit()
            for i in range(int(quantity)):
                car = Car(mname=carname, model=cmdl.mno,
                          kms=0, ac=False, avl=0, fuel=0)
                db.session.add(car)
            db.session.commit()
            db.session.commit()
        return redirect('/carlist')
    return render_template('addCar.html')


@app.route('/addC')
def addC():
    return render_template('addCar.html')


@app.route('/repair_snd')
def repair_S():
    cars = Car.query.filter_by(avl=0)
    cmdel = CModel.query.all()
    return render_template('repair_snd.html', cars=cars, cmdel=cmdel)


@app.route('/repair_get')
def repair_G():
    cars = Car.query.filter_by(avl=2)
    cmdel = CModel.query.all()
    return render_template('repair_get.html', cars=cars, cmdel=cmdel)

# 0 -> Available, 1 -> Rented, 2 -> Repair


@app.route('/sendrepair/<int:id>')
def sendrepair(id):
    car = Car.query.filter_by(id=id).first()
    mdl = car.mname
    if car.avl == 0:
        cmdl = CModel.query.filter_by(mname=mdl).first()
        if car.ac == True:
            cmdl.accar -= 1
        else:
            cmdl.naccar -= 1

        db.session.add(cmdl)
        db.session.commit()

        car.avl = 2
        db.session.add(car)
        db.session.commit()
    return redirect('/adminstr')


@app.route('/getrepair/<int:id>')
def getrepair(id):
    car = Car.query.filter_by(id=id).first()
    mdl = car.mname
    cmdl = CModel.query.filter_by(mname=mdl).first()
    ad = Administrator.query.filter_by(uname="Admin").first()
    if car.ac == True:
        cmdl.accar += 1
    else:
        cmdl.naccar += 1

    db.session.add(cmdl)
    db.session.commit()
    sts = Statistics.query.filter_by(mname=cmdl.mname).first()
    sts.mntnc += 500
    ad.rvnu -= 500
    db.session.add(ad)
    db.session.add(sts)

    car.avl = 0
    db.session.add(car)
    db.session.commit()
    return redirect('/adminstr')


@app.route('/change_rent/<int:mno>', methods=["POST", "GET"])
def change_rent(mno):
    if request.method == "POST":
        cmdl = CModel.query.filter_by(mno=mno).first()
        cmdl.rent_h = request.form['rent_h']
        cmdl.rent_k = request.form['rent_k']
        db.session.add(cmdl)
        db.session.commit()
        return redirect('/carlist')
    else:
        cmdl = CModel.query.filter_by(mno=mno).first()
        return render_template('change_rent.html', cmdl=cmdl)


@app.route('/delete_account/<int:id>')
def delete_account(id):
    customer = Customers.query.filter_by(id=id).first()
    if customer.bcar == 0:
        db.session.delete(customer)
        pvjrny = Journey.query.filter_by(cust = id)
        for jrn in pvjrny:
            db.session.delete(jrn)
        db.session.commit()
        return redirect('/')
    else:
        return render_template('customer.html', customer=customer)


@app.route('/delete')
def delete():
    car = Car.query.filter_by(avl=0)
    cmdl = CModel.query.all()
    return render_template('delete.html', car=car, cmdl=cmdl)


@app.route('/delete/<int:id>')
def deleting(id):
    car_to_delete = Car.query.filter_by(id=id).first()
    try:
        mdl = car_to_delete.mname
        cmdl = CModel.query.filter_by(mname=mdl).first()
        if car_to_delete.ac == True:
            cmdl.accar -= 1
        else:
            cmdl.naccar -= 1
        db.session.delete(car_to_delete)
        db.session.commit()
        if (cmdl.accar == 0 and cmdl.naccar == 0):
            db.session.delete(cmdl)
            db.session.commit()
        return redirect('/delete')
    except:
        return "There is a problem in deleting"


@app.route('/returning/<int:idc>')
def returning(idc):
    cust = Customers.query.filter_by(id=idc).first()
    if(cust.bcar == 0):
        return render_template('customer.html', customer=cust)
    return render_template('returncar.html', customer=cust)


@app.route('/return/<int:id>', methods=["POST", "GET"])
def returncar(id):
    cust = Customers.query.filter_by(id=id).first()
    kms = request.form['kms']
    rating = request.form['rating']
    car = Car.query.filter_by(id=cust.bcar).first()
    cmdl = CModel.query.filter_by(mno=car.model).first()
    bkng = Booking.query.filter_by(cust=id).first()
    stat = Statistics.query.filter_by(mname=car.mname).first()
    ad = Administrator.query.filter_by(uname="Admin").first()
    rate_km = cmdl.rent_k
    rate_hr = cmdl.rent_h
    date = datetime.utcnow()
    bdate = bkng.bdate
    diff = date - bdate
    hrs = diff.seconds/3600
    car.kms += int(kms)

    if car.ac == True:
        rate_km += 150

    if car.ac == True:
        cmdl.accar += 1

    else:
        cmdl.naccar += 1

    fare = rate_hr * 4
    fare2 = rate_hr * hrs

    if fare2 > fare:
        fare = fare2

    fare2 = rate_km * int(kms)

    if fare2 > fare:
        fare = fare2

    ad.rvnu = ad.rvnu + fare - bkng.advance
    stat.rvnu += int(fare)
    f = stat.feedback * stat.demand
    stat.demand += 1
    stat.feedback = (f + int(rating))/stat.demand
    stat.feedback = "{:.2f}".format(stat.feedback)
    cmdl.feedback = stat.feedback
    jrny = Journey(cust=id, car=car.id, cmodel=cmdl.mname, bdate=bkng.bdate,
                   rdate=date, fare=fare)

    cust.bcar = 0
    car.avl = 0
    cust.pjrny += 1
    jrny.kms = int(kms)
    db.session.delete(bkng)
    db.session.add(cust)
    db.session.add(cmdl)
    db.session.add(jrny)
    db.session.add(car)
    db.session.add(stat)
    db.session.add(ad)
    db.session.commit()
    return redirect('/prev/'+str(id))


@app.route('/prev/<int:id>')
def prev(id):
    jrny = Journey.query.filter_by(cust=id)
    cust = Customers.query.filter_by(id=id).first()
    return render_template('prev_jrny.html', jrny=jrny, customer=cust)

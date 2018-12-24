import os, uuid
from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint, Response) 
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Post, Garden, Resource, House, Customer, Landlord, Contract, Contractype, Maintenanceunit, Maintenancerec, Contractbill, User, Contractype
from flaskblog.posts.forms import PostForm, GardenForm, ResourceForm, UpdateResourceForm, HouseForm, UpdateHouseForm, CustomerForm, LandlordForm, ContractForm, ContractypeForm, UpdateContractForm, TerminateContractForm, MaintenanceunitForm, MaintenancerecForm, TerminateMaintenancerecForm, ContractbillForm, PaybillForm, RenewalContractForm
from sqlalchemy import func, extract, desc, or_
from datetime import datetime, timedelta
from flask import current_app as app



posts = Blueprint('posts', __name__)




@posts.route("/post/dashboard")
@login_required
def dashboard():
    thisYear = datetime.today().year    
    thisMonth = datetime.today().month
    lastYear = (datetime.today()-timedelta(days=365)).year
    lastMonth = (datetime.today()-timedelta(days=30)).month

    contract_counts = Contract.query.count()
    contract_expired_30d = Contract.query.filter_by(status=0).filter(Contract.end_time < datetime.now()+timedelta(days=30)).count()
    contract_expired_7d = Contract.query.filter_by(status=0).filter(Contract.end_time < datetime.now()+timedelta(days=7)).count()
    contract_expired = Contract.query.filter_by(status=0).filter(Contract.end_time < datetime.now()).count()
    house_counts = House.query.count()
    house_free_counts = House.query.filter_by(status=0).count()

    user_counts = User.query.count()
    users_recently_visited = User.query.with_entities(User.username,User.image_file,User.last_login,User.login_ip).all() 
    security_deposits = Contract.query.with_entities(Contract.security_deposit).all() 

    billamounts_lastyear = Contractbill.query.filter(extract('year', Contractbill.bill_date) == lastYear).with_entities(Contractbill.bill_amount).all()
    unpaid_lastyear = Contractbill.query.filter(extract('year', Contractbill.bill_date) == lastYear).filter_by(status=0).with_entities(Contractbill.bill_amount).all()
    paid_lastyear = Contractbill.query.filter(extract('year', Contractbill.bill_date) == lastYear).filter_by(status=1).with_entities(Contractbill.bill_amount).all()
    billamounts_thisyear = Contractbill.query.filter(extract('year', Contractbill.bill_date) == thisYear).with_entities(Contractbill.bill_amount).all()
    unpaid_thisyear = Contractbill.query.filter(extract('year', Contractbill.bill_date) == thisYear).filter_by(status=0).with_entities(Contractbill.bill_amount).all()
    paid_thisyear = Contractbill.query.filter(extract('year', Contractbill.bill_date) == thisYear).filter_by(status=1).with_entities(Contractbill.bill_amount).all()

    billamounts_thismonth = Contractbill.query.filter(extract('year', Contractbill.bill_date) == thisYear).\
    filter(extract('month', Contractbill.bill_date) == thisMonth).with_entities(Contractbill.bill_amount).all()

    paid_billamounts_thismonth = Contractbill.query.\
    filter(extract('year', Contractbill.update_time) == thisYear).filter(extract('month', Contractbill.update_time) == thisMonth).\
    filter(extract('year', Contractbill.bill_date)+extract('month', Contractbill.bill_date) == thisYear+thisMonth).\
    filter_by(status=1).with_entities(Contractbill.bill_amount)

    paid_billamounts_notthismonth = Contractbill.query.\
    filter(extract('year', Contractbill.update_time) == thisYear).filter(extract('month', Contractbill.update_time) == thisMonth).\
    filter(extract('year', Contractbill.bill_date)+extract('month', Contractbill.bill_date) != thisYear+thisMonth).\
    filter_by(status=1).with_entities(Contractbill.bill_amount)

    unpaid_billamounts_thismonth = Contractbill.query.filter(extract('year', Contractbill.bill_date) == thisYear).filter(extract('month', Contractbill.bill_date) == thisMonth).\
    filter_by(status=0).with_entities(Contractbill.bill_amount)

    maintenanceRecs = Maintenancerec.query.filter_by(status=0).count()
    maintenancedRecs = Maintenancerec.query.filter_by(status=1).count()
    maintenancedRecFee = Maintenancerec.query.filter_by(status=1).with_entities(Maintenancerec.price).all()

    resourcePrices = Resource.query.with_entities(Resource.price).all() 
    resourceArea1s = Resource.query.with_entities(Resource.area1).all() 
    resourceArea2s = Resource.query.with_entities(Resource.area2).all() 
        
    return render_template('dashboard.html', contract_counts=contract_counts, 
        contract_expired_30d=contract_expired_30d,
        contract_expired_7d=contract_expired_7d,
        contract_expired=contract_expired,
        house_free_counts=house_free_counts, 
        house_counts = house_counts,
        user_counts=user_counts, 

        billamounts_thisyear=str(sum([sum(i) for i in billamounts_thisyear])/10000),
        unpaid_lastyear=str(sum([sum(i) for i in unpaid_lastyear])/10000),
        paid_lastyear=str(sum([sum(i) for i in paid_lastyear])/10000),

        billamounts_lastyear=str(sum([sum(i) for i in billamounts_lastyear])/10000),
        unpaid_thisyear=str(sum([sum(i) for i in unpaid_thisyear])/10000),
        paid_thisyear=str(sum([sum(i) for i in paid_thisyear])/10000),

        billamounts_thismonth=str(sum([sum(i) for i in billamounts_thismonth])/10000), 
        paid_billamounts_thismonth=str(sum([sum(i) for i in paid_billamounts_thismonth])/10000),
        paid_billamounts_notthismonth=str(sum([sum(i) for i in paid_billamounts_notthismonth])/10000),
        unpaid_billamounts_thismonth=str(sum([sum(i) for i in unpaid_billamounts_thismonth])/10000),
         
        security_deposits=str(sum([sum(i) for i in security_deposits])/10000), 
        users_recently_visited=users_recently_visited,
        
        maintenanceRecs=maintenanceRecs,
        maintenancedRecs=maintenancedRecs,
        maintenancedRecFee=str(sum([sum(i) for i in maintenancedRecFee])),

        thisYear = thisYear,
        thisMonth = thisMonth,
        lastYear = lastYear,
        lastMonth = lastMonth,

        resourcePriceSum=str(sum([sum(i) for i in resourcePrices])),
        resourceArea1Sum=str(sum([sum(i) for i in resourceArea1s])),
        resourceArea2Sum=str(sum([sum(i) for i in resourceArea2s])),
        title='我的黑板')


@posts.route("/post/position")
@login_required
def position():
    return render_template('position.html', title='获取坐标')


@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, \
            content=form.content.data, \
            author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post', form=form)


@posts.route("/post/<int:post_id>")
@login_required
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post', form=form)


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))


# added on 20181017
@posts.route("/post/garden", methods=['GET', 'POST'])
@login_required
def new_garden():
    form = GardenForm()
    if form.validate_on_submit():
        post = Garden(name=form.name.data, \
            coordinate=form.coordinate.data, \
            note=form.note.data)
        db.session.add(post)
        db.session.commit()
        flash('新小区节点创建完成,请继续新增资产!', 'success')
        return redirect(url_for('posts.new_resource'))
    return render_template('create_garden.html', title='小区录入', form=form)


@posts.route("/post/create_resource", methods=['GET', 'POST'])
@login_required
def new_resource():
    form = ResourceForm()

    choicesgarden = [("0", "------请选择------ ")]
    for s in Garden.query.with_entities(Garden.id, Garden.name).all():
        choicesgarden.append((s[0], s[1])) 
    form.garden_id.choices = choicesgarden

    choiceslandlord = [("0", "------请选择------ ")]
    for s in Landlord.query.with_entities(Landlord.id, Landlord.name).all():
        choiceslandlord.append((s[0], s[1])) 
    form.landlord_id.choices = choiceslandlord

    # form.garden_id.choices = db.session.query(Garden.id, Garden.name)
    if form.validate_on_submit():
        # single file upload
        f = form.pictures.data
        filename = uuid.uuid4().hex + os.path.splitext(f.filename)[1] 
        f.save(os.path.join(app.config['UPLOAD_PATH'], filename))
        post = Resource(landlord_id = form.landlord_id.data, \
            garden_id = form.garden_id.data, \
            address = form.address.data, \
            price = form.price.data, \
            pictures = filename, \
            area1 = form.area1.data, \
            area2 = form.area2.data, \
            cardid = form.cardid.data, \
            note = form.note.data )
        db.session.add(post)
        db.session.commit()
        flash('新资产登记成功，请继续登记房源!', 'success')
        return redirect(url_for('posts.new_house'))
    return render_template('create_resource.html', title='资产新增', form=form)


@posts.route("/post/resource/<int:resource_id>/update", methods=['GET', 'POST'])
@login_required
def update_resource(resource_id):
    form = UpdateResourceForm()
    choiceslandlord = [("0", "------请选择------ ")]
    for s in Landlord.query.with_entities(Landlord.id, Landlord.name).all():
        choiceslandlord.append((s[0], s[1])) 
    form.landlord_id.choices = choiceslandlord
    resource = Resource.query.filter_by(id=resource_id).first()
    if form.validate_on_submit():
        if form.pictures.data:
            f = form.pictures.data
            filename = uuid.uuid4().hex + os.path.splitext(f.filename)[1] 
            f.save(os.path.join(app.config['UPLOAD_PATH'], filename))
        resource.landlord_id = form.landlord_id.data
        resource.address = form.address.data
        resource.price = form.price.data
        resource.pictures = filename
        resource.area1 = form.area1.data
        resource.area2 = form.area2.data
        resource.cardid = form.cardid.data
        resource.note = form.note.data
        db.session.commit()
        flash('资产信息已经更新，请继续登记房源!', 'success')
        return redirect(url_for('posts.resource_info', resource_id=resource.id))       
    elif request.method == 'GET':
        form.landlord_id.data = resource.landlord_id
        form.garden_id.data = resource.garden_id
        form.address.data = resource.address
        form.price.data = resource.price
        filename = resource.pictures
        form.area1.data = resource.area1
        form.area2.data = resource.area2
        form.cardid.data = resource.cardid
        form.note.data = resource.note
        return render_template('create_resource.html', title='资产更新', form=form)


@posts.route("/post/create_house", methods=['GET', 'POST'])
@login_required
def new_house():
    form = HouseForm()
    choices = [("0", "------请选择------ ")]
    for s in Resource.query.with_entities(Resource.id, Resource.cardid+'*'+Resource.address).all():
        choices.append((s[0], s[1])) 
    form.resource_id.choices = choices
    # form.resource_id.choices = db.session.query(Resource.id, '权证:'+Resource.cardid+','+Resource.address)   
    if form.validate_on_submit():
        # multi files upload
        filenames = []
        all_pictures_name = ''
        for f in request.files.getlist('pictures'):
            filename = uuid.uuid4().hex + os.path.splitext(f.filename)[1] 
            f.save(os.path.join(app.config['UPLOAD_PATH'], filename))
            filenames.append(filename)

        for i in filenames:
            all_pictures_name=all_pictures_name +'|' + i 

        # single file upload
        # f = form.pictures.data
        # filename = uuid.uuid4().hex + os.path.splitext(f.filename)[1] 
        # f.save(os.path.join(app.config['UPLOAD_PATH'], filename))

        post = House(address=form.address.data, \
            resource_id=form.resource_id.data, \
            area=form.area.data, \
            pictures=all_pictures_name, \
            # pictures = photos.save(form.photo.data), \
            note=form.note.data)
        db.session.add(post)
        db.session.commit()
        flash('新房源登记成功!', 'success')

        return redirect(url_for('posts.house_list'))
    return render_template('create_house.html', form=form, title='房源登记')



@posts.route("/post/house/<int:house_id>/update", methods=['GET', 'POST'])
@login_required
def update_house(house_id):
    form = UpdateHouseForm()
    house = House.query.filter_by(id=house_id).first()
    # house = House.query.filter(House.id==house_id).first()
    if form.validate_on_submit():
        filenames = []
        all_pictures_name = ''
        for f in request.files.getlist('pictures'):
            filename = uuid.uuid4().hex + os.path.splitext(f.filename)[1] 
            f.save(os.path.join(app.config['UPLOAD_PATH'], filename))
            filenames.append(filename)
        for i in filenames:
            all_pictures_name=all_pictures_name +'|' + i 
        house.area=form.area.data
        house.pictures=house.pictures+all_pictures_name
        house.note=form.note.data
        db.session.commit()
        flash('房源信息已更新!', 'success')
        return redirect(url_for('posts.house_list'))
    elif request.method == 'GET':
        form.resource_id.data = house.resource_id
        form.address.data = house.address
        form.area.data = house.area
        form.note.data = house.note
        form.pictures.data = house.pictures
        return render_template('create_house.html', title='房源更新', form=form)
        

@posts.route("/post/create_customer", methods=['GET', 'POST'])
@login_required
def new_customer():
    form = CustomerForm()
    if form.validate_on_submit():
        f = form.pictures.data
        filename = uuid.uuid4().hex + os.path.splitext(f.filename)[1] 
        f.save(os.path.join(app.config['UPLOAD_PATH'], filename))
        post = Customer(name=form.name.data, \
            phone=form.phone.data, \
            address=form.address.data, \
            cardid=form.cardid.data, \
            pictures=filename, \
            postcode=form.postcode.data, \
            note=form.note.data)
        db.session.add(post)
        db.session.commit()
        flash('新的租户登记完成!', 'success')
        return redirect(url_for('posts.customer_list'))
    return render_template('create_customer.html', title='租户登记', form=form)


@posts.route("/post/create_landlord", methods=['GET', 'POST'])
@login_required
def new_landlord():
    form = LandlordForm()
    if form.validate_on_submit():
        f = form.pictures.data
        filename = uuid.uuid4().hex + os.path.splitext(f.filename)[1] 
        f.save(os.path.join(app.config['UPLOAD_PATH'], filename))
        post = Landlord(name=form.name.data, \
            phone=form.phone.data, \
            address=form.address.data, \
            cardid=form.cardid.data, \
            pictures=filename, \
            note=form.note.data)
        db.session.add(post)
        db.session.commit()
        flash('产权人登记完成!', 'success')
        return redirect(url_for('posts.landlord_list'))
    return render_template('create_landlord.html', title='权利人登记', form=form)


@posts.route("/post/create_contract", methods=['GET', 'POST'])
@login_required
def new_contract():
    form = ContractForm()
    choicesHouseid = [("0", "------请选择------ ")]
    for s in House.query.with_entities(House.id, House.address).filter(House.status!=1).all():
        choicesHouseid.append((s[0], s[1])) 
    form.house_id.choices = choicesHouseid

    choicesCustomerid = [("0", "------请选择------ ")]
    for s in Customer.query.with_entities(Customer.id, Customer.name).all():
        choicesCustomerid.append((s[0], s[1])) 
    form.customer_id.choices = choicesCustomerid

    choicesType = [("0", "------请选择------ ")]
    for s in Contractype.query.filter(Contractype.name!='续租').with_entities(Contractype.id, Contractype.name).all():
        choicesType.append((s[0], s[1])) 
    form.type.choices = choicesType

    # form.house_id.choices = db.session.query(House.id, House.address).filter_by(status=0).all()
    # form.customer_id.choices = db.session.query(Customer.id, Customer.name)
    # form.type.choices = db.session.query(Contractype.id, Contractype.name)
    if form.validate_on_submit():     
        # f = request.form
        # for key in f.keys():
        #     for value in f.getlist(key):
        #         print(key,":",value)
        # if form.contract_pics.data:
        #     f = form.contract_pics.data
        #     filename1 = uuid.uuid4().hex + os.path.splitext(f.filename)[1] 
        #     f.save(os.path.join(app.config['UPLOAD_PATH'], filename1))
        
        # multi files upload
        
        if form.contract_pics.data:
            filenames = []
            all_pictures_name = ''
            for f in request.files.getlist('contract_pics'):
                filename = uuid.uuid4().hex + os.path.splitext(f.filename)[1] 
                f.save(os.path.join(app.config['UPLOAD_PATH'], filename))
                filenames.append(filename)
            for i in filenames:
                all_pictures_name=all_pictures_name +'|' + i 
        else:
            all_pictures_name = 'default_contract.jpg'

        if form.approval_pics.data:
            f = form.approval_pics.data
            filename2 = uuid.uuid4().hex + os.path.splitext(f.filename)[1] 
            f.save(os.path.join(app.config['UPLOAD_PATH'], filename2))
        if form.auction_announcement.data:
            f = form.auction_announcement.data
            filename3 = uuid.uuid4().hex + os.path.splitext(f.filename)[1] 
            f.save(os.path.join(app.config['UPLOAD_PATH'], filename3))
        if form.auction_confirmation.data:
            f = form.auction_confirmation.data
            filename4 = uuid.uuid4().hex + os.path.splitext(f.filename)[1] 
            f.save(os.path.join(app.config['UPLOAD_PATH'], filename4))

        post = Contract(name=form.name.data, \
            house_id=form.house_id.data, \
            customer_id=form.customer_id.data, \
            type=form.type.data, \
            auction_date=form.auction_date.data, \
            start_time=form.start.data, \
            end_time=form.end.data, \
            useof=form.useof.data, \
            security_deposit=form.security_deposit.data, \
            annual_rent=form.annual_rent.data, \
            contract_pics=all_pictures_name, \
            approval_pics=filename2, \
            auction_announcement=filename3, \
            auction_confirmation=filename4, \
            note=form.note.data,\
            user_id=current_user.id)
        #修改House.status
        house = House.query.filter(House.id == form.house_id.data).first()
        house.status = '1'
        db.session.add(post)
        db.session.commit()
        flash('合同已经创建，请继续打印合同、完成签字并录入!', 'success')
        return redirect(url_for('posts.contract_normal'))
    return render_template('create_contract.html', title='合同登记', form=form)


@posts.route("/post/contract/<int:contract_id>/renewal", methods=['GET', 'POST'])
@login_required
def renewal_contract(contract_id):
    form = RenewalContractForm()
    contract = Contract.query.filter(Contract.id == contract_id).first()
    contractype = Contractype.query.filter(Contractype.id ==contract.type).with_entities(Contractype.name).first()
    
    if contractype.name == '拍租':
        yearsCovered = 1
    elif contractype.name == '续租':
        # yearsCovered= round((datetime.now()-contract.start_time).days/365)
        yearsCovered = 3
    
    contractype_renewal = Contractype.query.filter(Contractype.name == '续租').with_entities(Contractype.id, Contractype.name).first()

    choices = [("0", "------请选择------ ")]
    for s in Contractype.query.with_entities(Contractype.id, Contractype.name).all():
        choices.append((s[0], s[1])) 
    form.type.choices = choices

    if form.validate_on_submit():
        if form.contract_pics.data:
            filenames = []
            all_pictures_name = ''
            for f in request.files.getlist('contract_pics'):
                filename = uuid.uuid4().hex + os.path.splitext(f.filename)[1] 
                f.save(os.path.join(app.config['UPLOAD_PATH'], filename))
                filenames.append(filename)
            for i in filenames:
                all_pictures_name=all_pictures_name +'|' + i 
            contract.contract_pics = all_pictures_name
        else:
            all_pictures_name = 'default_contract.jpg'
        post = Contract(name=form.name.data, \
            house_id=form.house_id.data, \
            customer_id=form.customer_id.data, \
            type= contractype_renewal.id, \
            is_xuzu=1,\
            auction_date=form.auction_date.data, \
            start_time=form.start.data, \
            end_time=form.end.data, \
            useof=form.useof.data, \
            security_deposit=form.security_deposit.data, \
            annual_rent=form.annual_rent.data, \
            contract_pics=all_pictures_name, \
            approval_pics=form.approval_pics.data, \
            auction_announcement=form.auction_announcement.data, \
            auction_confirmation=form.auction_confirmation.data, \
            origin_contract_id = contract_id, \
            note=form.note.data,\
            user_id=current_user.id)
        #修改House.status
        house = House.query.filter(House.id == form.house_id.data).first()
        house.status = '1'
        db.session.add(post)
        db.session.commit()
        flash('续签合同创建完成!', 'success')
        return redirect(url_for('posts.contract_normal'))
    elif request.method == 'GET':   
        form.name.data = contract.name
        form.house_id.data = contract.house_id
        form.customer_id.data = contract.customer_id
        form.type.data = contractype_renewal.name
        form.auction_date.data = contract.auction_date
        form.security_deposit.data = contract.security_deposit
        form.useof.data = contract.useof
        form.annual_rent.data = round(contract.annual_rent * (1.03**yearsCovered))
        # form.annual_rent.data = (datetime.now()-contract.create_time)
        form.approval_pics.data = contract.approval_pics
        form.auction_announcement.data = contract.auction_announcement
        form.auction_confirmation.data = contract.auction_confirmation        
        form.note.data = contract.note
        return render_template('create_contract.html', title='合同续签', form=form)


@posts.route("/post/contract/<int:contract_id>/update", methods=['GET', 'POST'])
@login_required
def update_contract(contract_id):
    contract = Contract.query.filter(Contract.id == contract_id).first()
    if contract.contract_pics == 'default_contract.jpg':
        form = UpdateContractForm()
    else:
        form = TerminateContractForm()
        form.contract_pics.data = contract.contract_pics
    house = House.query.filter(House.id == contract.house_id).first()
    choices = [("0", "------请选择------ ")]
    for s in Contractype.query.with_entities(Contractype.id, Contractype.name).all():
        choices.append((s[0], s[1])) 
    form.type.choices = choices

    if form.validate_on_submit():
        if form.status.data == '1':           
            house.status = 2
        if form.contract_pics.data:
            filenames = []
            all_pictures_name = ''
            for f in request.files.getlist('contract_pics'):
                filename = uuid.uuid4().hex + os.path.splitext(f.filename)[1] 
                f.save(os.path.join(app.config['UPLOAD_PATH'], filename))
                filenames.append(filename)
            for i in filenames:
                all_pictures_name = all_pictures_name +'|' + i 
            contract.contract_pics = all_pictures_name        
        contract.status = form.status.data                  
        contract.name = form.name.data
        contract.house_id = form.house_id.data
        contract.customer_id = form.customer_id.data
        contract.type = form.type.data
        contract.auction_date = form.auction_date.data
        contract.start_time = form.start.data
        contract.end_time = form.end.data
        contract.annual_rent = form.annual_rent.data
        contract.note = form.note.data
        contract.user_id = current_user.id
        db.session.commit()
        flash('合同已经更新!', 'success')
        return redirect(url_for('posts.contract_normal'))
    elif request.method == 'GET':   
        form.name.data = contract.name
        form.house_id.data = contract.house_id
        form.customer_id.data = contract.customer_id
        form.type.data = contract.type
        form.auction_date.data = contract.auction_date
        form.start.data = contract.start_time
        form.end.data = contract.end_time
        form.security_deposit.data = contract.security_deposit
        form.useof.data = contract.useof
        form.annual_rent.data = contract.annual_rent
        form.approval_pics.data = contract.approval_pics
        form.auction_announcement.data = contract.auction_announcement
        form.auction_confirmation.data = contract.auction_confirmation
        form.note.data = contract.note
        return render_template('update_contract.html', title='合同变更', form=form)


@posts.route("/post/contractype", methods=['GET', 'POST'])
@login_required
def contract_type():
    form = ContractypeForm()
    if form.validate_on_submit():
        post = Contractype(name=form.name.data, note=form.note.data)
        db.session.add(post)
        db.session.commit()
        flash('合同类型录入成功', 'success')
        return redirect(url_for('posts.contractype_list'))
    return render_template('create_type.html', title='合同类型', form=form )


@posts.route("/post/maintenanceunit", methods=['GET', 'POST'])
@login_required
def new_maintenanceunit():
    form = MaintenanceunitForm()
    if form.validate_on_submit():
        post = Maintenanceunit(name=form.name.data, note=form.note.data, phone=form.phone.data)
        db.session.add(post)
        db.session.commit()
        flash('维修单位登记成功', 'success')
        return redirect(url_for('posts.maintenanceunit_list'))
    return render_template('create_maintenanceunit.html', title='维修单位', form=form)


@posts.route("/post/maintenancerec/<int:house_id>", methods=['GET', 'POST'])
@login_required
def new_maintenancerec(house_id):
    form = MaintenancerecForm()
    form.maintenanceunit_id.choices = db.session.query(Maintenanceunit.id, Maintenanceunit.name)
    form.house_id.data = house_id
    if form.validate_on_submit():
        post = Maintenancerec(house_id = form.house_id.data, \
            maintenanceunit_id = form.maintenanceunit_id.data, \
            price = form.price.data, \
            note = form.note.data)
        db.session.add(post)
        db.session.commit()
        flash('维修登记成功!', 'success')
        return redirect(url_for('posts.new_maintenancerec', house_id=house_id) )
        # return redirect(url_for('posts.maintenanceunit_list'))
    return render_template('create_maintenancerec.html', title='维修登记', house_id=house_id, form=form)


@posts.route("/post/maintenancerec/<int:maintenancerec_id>/update", methods=['GET', 'POST'])
@login_required
def update_maintenancerec(maintenancerec_id):
    form = TerminateMaintenancerecForm()
    maintenancerec = Maintenancerec.query.get_or_404(maintenancerec_id)
    form.maintenanceunit_id.choices = db.session.query(Maintenanceunit.id, Maintenanceunit.name)
    # if post.author != current_user:
    #     abort(403)
    if form.validate_on_submit():
        maintenancerec.status = 1
        maintenancerec.maintenance_note = form.maintenance_note.data
        db.session.commit()
        flash('维修记录已更新!', 'success')
        return redirect(url_for('posts.maintenancerec_list'))
    elif request.method == 'GET':
        form.house_id.data = maintenancerec.house_id
        form.maintenanceunit_id.data = maintenancerec.id
        form.note.data = maintenancerec.note

    return render_template('create_maintenancerec.html', title='维修记录更新', form=form, maintenancerec_id=maintenancerec_id)


@posts.route("/post/generate_bill", methods=['GET', 'POST'])
@login_required
def new_contractbill():
    form = ContractbillForm()
    contracts = Contract.query.filter_by(status=0).filter_by(bill_status=0)#.filter_by(Contract.start_time>form.start.data).filter_by(Contract.start_time<form.end.data)
    if form.validate_on_submit():
        for contract in contracts:
            i=0
            while (contract.start_time + timedelta(367*i)).strftime("%Y-%m-%d") < contract.end_time.strftime("%Y-%m-%d"):
                isXuzu = Contractype.query.filter_by(id=contract.type).filter_by(name='续租').first() is not None
                if isXuzu:
                    billamount = contract.annual_rent*(1.03)**i
                else:
                    billamount = contract.annual_rent
                post = Contractbill(contract_id=contract.id, \
                    contract_type=contract.type, \
                    contract_create=contract.create_time, \
                    bill_sequence=contract.id*10+i+1, \
                    bill_date=contract.start_time + timedelta(365*i), \
                    bill_amount=billamount)
                db.session.add(post)
                # db.session.commit()
                i+=1
            # 修改Contract.bill_status
            # contract = Contract.query.filter(Contract.id == contract.id).first()
            contract.bill_status = '1'
            db.session.commit()
        flash('帐单生成成功!', 'success')
        # return redirect(url_for('posts.new_contractbill'))
        # return isXuzu
    return render_template('create_contractbill.html', form=form, title='生成帐单' )


@posts.route("/post/house_list")
@login_required
def house_list():
    lists = Garden.query.outerjoin(Resource,Resource.garden_id==Garden.id).outerjoin(House,House.resource_id==Resource.id).\
    with_entities(Garden.id.label('garden_id'), \
        Garden.name.label('garden_name'), \
        Resource.id.label('resource_id'), \
        Resource.cardid.label('resource_cardid'), \
        House.id.label('house_id'), \
        House.address.label('house_address'), \
        Resource.area1.label('resource_area'),\
        House.status.label('house_status')
        )
    return render_template('house_list.html', lists=lists, title='房源查询')


@posts.route("/post/resource_list")
@login_required
def resource_list():
    lists = Garden.query.outerjoin(Resource,Resource.garden_id==Garden.id).outerjoin(Landlord,Landlord.id==Resource.landlord_id).\
    with_entities(Garden.id.label('garden_id'), \
        Garden.name.label('garden_name'), \
        Landlord.name.label('landlord_name'), \
        Resource.id.label('resource_id'), \
        Resource.cardid, \
        Resource.price, \
        Resource.address, \
        Resource.area1, \
        Resource.area2
        )
    return render_template('resource_list.html', lists=lists, title='资产查询')


@posts.route("/post/customer_list")
@login_required
def customer_list():
    customers = Customer.query.all()
    return render_template('customer_list.html', customers=customers, title='租户查询')


@posts.route("/post/landlord_list")
@login_required
def landlord_list():
    landlords = Landlord.query.all()
    return render_template('landlord_list.html', landlords=landlords, title='产权持有人查询')


@posts.route("/post/normal_contract")
@login_required
def contract_normal():
    contracts = Contract.query.filter_by(status=0).join(House,Contract.house_id==House.id).join(Customer,Contract.customer_id==Customer.id).join(Contractype,Contractype.id==Contract.type).\
    with_entities(Contract.id, \
        House.id.label('house_id'), \
        House.address, \
        Customer.id.label('customer_id'), \
        Customer.name.label('customer_name'), \
        Contractype.name.label('contractype_name'), \
        Contract.annual_rent, \
        Contract.start_time, \
        Contract.end_time \
        ).order_by(desc(Contract.end_time))
    current_time  = datetime.now()
    return render_template('contract_list.html', contracts=contracts, current_time=current_time, title='生效租赁')


@posts.route("/post/terminated_contract")
@login_required
def contract_isTerminated():
    contracts = Contract.query.filter_by(status=1).join(House,Contract.house_id==House.id).join(Customer,Contract.customer_id==Customer.id).join(Contractype,Contractype.id==Contract.type).\
    with_entities(Contract.id, \
        House.id.label('house_id'), \
        House.address, \
        Customer.id.label('customer_id'), \
        Customer.name.label('customer_name'), \
        Contractype.name.label('contractype_name'), \
        Contract.annual_rent, \
        Contract.start_time, \
        Contract.end_time \
        ).order_by(desc(Contract.end_time))
    current_time  = datetime.now()
    return render_template('contract_list.html', contracts=contracts, current_time=current_time, title='历史租赁')


@posts.route("/post/all_list")
@login_required
def all_list():
    allResults = Resource.query.outerjoin(House,House.resource_id==Resource.id).outerjoin(Contract,Contract.house_id==House.id).outerjoin(Customer,Customer.id==Contract.customer_id).outerjoin(Landlord,Landlord.id==Resource.landlord_id).\
    outerjoin(Contractbill,Contractbill.contract_id==Contract.id).outerjoin(Contractype,Contractype.id==Contract.type).filter(Contract.status==0).\
    with_entities(Resource.id.label('resource_id'), \
        Resource.cardid.label('resource_cardid'), \
        Landlord.name.label('landlord_name'), \
        House.id.label('house_id'), \
        House.address.label('house_address'), \
        House.area.label('house_area'), \
        House.status.label('house_status'), \
        Customer.id.label('customer_id'), \
        Customer.name.label('customer_name'), \
        Customer.phone.label('customer_phone'), \
        Contract.id.label('contract_id'), \
        Contractype.name.label('contract_type'), \
        Contract.start_time.label('contract_start'), \
        Contract.end_time.label('contract_end'), \
        Contractbill.id.label('contractbill_id'), \
        Contractbill.bill_date.label('bill_date'), \
        Contractbill.bill_amount.label('bill_amount'), \
        Contractbill.status.label('bill_status'), \
        Contractbill.update_time.label('paid_date')
        )
    return render_template('all_list.html', allResults=allResults, title='综合查询')




@posts.route("/post/maintenanceunit_list")
@login_required
def maintenanceunit_list():
    maintenanceunits = Maintenanceunit.query.all()
    return render_template('maintenanceunit_list.html', maintenanceunits=maintenanceunits, title='维修单位')


@posts.route("/post/maintenancerec_list")
@login_required
def maintenancerec_list():
    maintenancerecs = Maintenancerec.query.join(House, House.id==Maintenancerec.house_id).join(Maintenanceunit, Maintenanceunit.id==Maintenancerec.maintenanceunit_id).\
        with_entities(House.id.label('house_id'), \
        House.address.label('house_address'), \
        Maintenanceunit.id.label('maintenanceunit_id'), \
        Maintenanceunit.name.label('maintenanceunit_name'), \
        Maintenanceunit.phone.label('maintenanceunit_phone'), \
        Maintenancerec.id, \
        Maintenancerec.status, \
        Maintenancerec.price, \
        Maintenancerec.note, \
        Maintenancerec.maintenance_note, \
        Maintenancerec.create_time, \
        Maintenancerec.update_time 
        )
    return render_template('maintenancerec_list.html', maintenancerecs=maintenancerecs, title='维修记录')


@posts.route("/post/bills/thisMonth", methods=['GET', 'POST'])
@login_required
def bills_thismonth():
    form = ContractbillForm()
    contracts = Contract.query.filter_by(status=0).filter_by(bill_status=0)
    contractbills_thisyear = Contractbill.query.filter(extract('year', Contractbill.bill_date) == datetime.today().year).filter(extract('month', Contractbill.bill_date) == datetime.today().month).join(Contractype, Contractype.id == Contractbill.contract_type).join(Contract, Contract.id==Contractbill.contract_id).join(House, House.id==Contract.house_id).join(Customer, Customer.id==Contract.customer_id).\
        with_entities(Contractbill.id, \
        Contractbill.contract_id, \
        Contractype.name.label('contract_type'), \
        Contractbill.bill_sequence, \
        Contractbill.bill_date, \
        Contractbill.bill_amount, \
        Contractbill.status, \
        Contractbill.note, \
        Contractbill.create_time, \
        Contractbill.update_time, \
        Contract.start_time.label('contract_start_time'), \
        Contract.end_time.label('contract_end_time'), \
        House.address.label('house_address'),
        House.area.label('house_area'),
        Customer.name.label('customer_name')
        )
   
    if form.validate_on_submit():
        for contract in contracts:
            i=0
            while (contract.start_time + timedelta(367*i)).strftime("%Y-%m-%d") < contract.end_time.strftime("%Y-%m-%d"):
                isXuzu = Contractype.query.filter_by(id=contract.type).filter_by(name='续租').first() is not None
                if isXuzu:
                    billamount = contract.annual_rent*(1.03)**i
                else:
                    billamount = contract.annual_rent
                post = Contractbill(contract_id=contract.id, \
                    contract_type=contract.type, \
                    contract_create=contract.create_time, \
                    bill_sequence=contract.id*10+i+1, \
                    bill_date=contract.start_time + timedelta(365*i), \
                    bill_amount=billamount)
                db.session.add(post)
                i+=1
            contract.bill_status = '1'
            db.session.commit()
        flash('帐单已经更新!', 'success')
        return redirect(url_for('posts.bills_thisyear'))
    elif request.method == 'GET':
        return render_template('bill_list.html', contractbills=contractbills_thisyear, form=form, title='当月帐单')


@posts.route("/post/bills/thisYear", methods=['GET', 'POST'])
@login_required
def bills_thisyear():
    form = ContractbillForm()
    contracts = Contract.query.filter_by(status=0).filter_by(bill_status=0)
    contractbills_thisyear = Contractbill.query.filter(extract('year', Contractbill.bill_date) == datetime.today().year).join(Contractype, Contractype.id == Contractbill.contract_type).join(Contract, Contract.id==Contractbill.contract_id).join(House, House.id==Contract.house_id).join(Customer, Customer.id==Contract.customer_id).\
        with_entities(Contractbill.id, \
        Contractbill.contract_id, \
        Contractype.name.label('contract_type'), \
        Contractbill.bill_sequence, \
        Contractbill.bill_date, \
        Contractbill.bill_amount, \
        Contractbill.status, \
        Contractbill.note, \
        Contractbill.create_time, \
        Contractbill.update_time, \
        Contract.start_time.label('contract_start_time'), \
        Contract.end_time.label('contract_end_time'), \
        House.address.label('house_address'),
        House.area.label('house_area'),
        Customer.name.label('customer_name')
        )
   
    if form.validate_on_submit():
        for contract in contracts:
            i=0
            while (contract.start_time + timedelta(367*i)).strftime("%Y-%m-%d") < contract.end_time.strftime("%Y-%m-%d"):
                isXuzu = Contractype.query.filter_by(id=contract.type).filter_by(name='续租').first() is not None
                if isXuzu:
                    billamount = contract.annual_rent*(1.03)**i
                else:
                    billamount = contract.annual_rent
                post = Contractbill(contract_id=contract.id, \
                    contract_type=contract.type, \
                    contract_create=contract.create_time, \
                    bill_sequence=contract.id*10+i+1, \
                    bill_date=contract.start_time + timedelta(365*i), \
                    bill_amount=billamount)
                db.session.add(post)
                i+=1
            contract.bill_status = '1'
            db.session.commit()
        flash('帐单已经更新!', 'success')
        return redirect(url_for('posts.bills_thisyear'))
    elif request.method == 'GET':
        return render_template('bill_list.html', contractbills=contractbills_thisyear, form=form, title='年度帐单')


@posts.route("/post/bills/AllofThem",  methods=['GET', 'POST'])
@login_required
def bills_all():
    form = ContractbillForm()
    contracts = Contract.query.filter_by(status=0).filter_by(bill_status=0)
    contractbills_all = Contractbill.query.join(Contractype, Contractype.id == Contractbill.contract_type).join(Contract, Contract.id==Contractbill.contract_id).\
    join(House, House.id==Contract.house_id).join(Customer, Customer.id==Contract.customer_id).\
        with_entities(Contractbill.id, \
        Contractbill.contract_id, \
        Contractype.name.label('contract_type'), \
        Contractbill.bill_sequence, \
        Contractbill.bill_date, \
        Contractbill.bill_amount, \
        Contractbill.status, \
        Contractbill.note, \
        Contractbill.create_time, \
        Contractbill.update_time, \
        Contract.start_time.label('contract_start_time'), \
        Contract.end_time.label('contract_end_time'), \
        House.address.label('house_address'),
        House.area.label('house_area'),
        Customer.name.label('customer_name')
        )
    if form.validate_on_submit():
        for contract in contracts:
            i=0
            while (contract.start_time + timedelta(365*i)).strftime("%Y-%m-%d") < contract.end_time.strftime("%Y-%m-%d"):
                isXuzu = Contractype.query.filter_by(id=contract.type).filter_by(name='续租').first() is not None
                if isXuzu:
                    billamount = contract.annual_rent*(1.03)**i
                else:
                    billamount = contract.annual_rent
                post = Contractbill(contract_id=contract.id, \
                    contract_type=contract.type, \
                    contract_create=contract.create_time, \
                    bill_sequence=contract.id*10+i+1, \
                    bill_date=contract.start_time + timedelta(365*i), \
                    bill_amount=billamount)
                db.session.add(post)
                i+=1
            contract.bill_status = '1'
            db.session.commit()
        flash('帐单已经更新!', 'success')
        return redirect(url_for('posts.bills_all'))
    elif request.method == 'GET':
        return render_template('bill_list.html', contractbills=contractbills_all, form=form, title='所有帐单')


@posts.route("/post/account_list")
@login_required
def account_list():
    accounts = User.query.all()
    return render_template('account_list.html', accounts=accounts, title='账户查询')


@posts.route("/post/contractype_list")
@login_required
def contractype_list():
    contractypes = Contractype.query.all()
    return render_template('contractype_list.html', contractypes=contractypes, title='合同类型')


@posts.route("/post/resource_info/<int:resource_id>")
@login_required
def resource_info(resource_id):
    exist_or_not = Resource.query.get_or_404(resource_id)
    resource = Resource.query.filter_by(id=resource_id).join(Landlord,Landlord.id==Resource.landlord_id).\
    with_entities(Resource.id.label('resource_id'), \
        Resource.address.label('resource_address'), \
        Resource.area1.label('resource_area1'), \
        Resource.area2.label('resource_area2'), \
        Resource.price.label('resource_price'), \
        Resource.pictures.label('resource_pictures'), \
        Resource.cardid.label('resource_cardid'), \
        Resource.note.label('resource_note'), \
        Landlord.id.label('landlord_id'), \
        Landlord.name.label('landlord_name')
        ).first()
    houses = House.query.filter_by(resource_id=resource_id)
    # return str(resource)
    return render_template('resource_info.html', resource=resource, houses=houses, title='资产信息' )


@posts.route("/post/house_info/<int:house_id>")
@login_required
def house_info(house_id):
    exist_or_not = House.query.get_or_404(house_id)
    house = House.query.filter_by(id=house_id).first()
    # contracts = Contract.query.filter_by(house_id=house_id)
    contracts = Contract.query.filter_by(house_id=house_id).filter_by(status=0).join(House,Contract.house_id==House.id).join(Customer,Contract.customer_id==Customer.id).\
    with_entities(Contract.id, \
        Customer.id.label('customer_id'), \
        Customer.name.label('customer_name'), \
        Customer.phone.label('customer_phone'), \
        Contract.annual_rent, \
        Contract.start_time, \
        Contract.end_time \
        )
    contracts_his = Contract.query.filter_by(house_id=house_id).filter_by(status=1).join(House,Contract.house_id==House.id).join(Customer,Contract.customer_id==Customer.id).\
    with_entities(Contract.id, \
        Customer.id.label('customer_id'), \
        Customer.name.label('customer_name'), \
        Customer.phone.label('customer_phone'), \
        Contract.annual_rent, \
        Contract.start_time, \
        Contract.end_time \
        )

    maintenancerecs = Maintenancerec.query.filter_by(house_id=house_id).join(House, House.id==Maintenancerec.house_id).join(Maintenanceunit, Maintenanceunit.id==Maintenancerec.maintenanceunit_id).\
        with_entities(House.id.label('house_id'), \
        House.address.label('house_address'), \
        Maintenanceunit.id.label('maintenanceunit_id'), \
        Maintenanceunit.name.label('maintenanceunit_name'), \
        Maintenanceunit.phone.label('maintenanceunit_phone'), \
        Maintenancerec.status, \
        Maintenancerec.note, \
        Maintenancerec.create_time, \
        Maintenancerec.update_time 
        )

    pictures = house.pictures.split("|")[1:]
    # return pictures
    return render_template('house_info.html', house=house, contracts=contracts, contracts_his=contracts_his, pictures=pictures, maintenancerecs=maintenancerecs, title='房源资料')


@posts.route("/post/customer_info/<int:customer_id>")
@login_required
def customer_info(customer_id):
    exist_or_not = Customer.query.get_or_404(customer_id)
    customers = Customer.query.filter_by(id=customer_id)
    contracts = Contract.query.filter_by(customer_id=customer_id).filter_by(status=0)
    contracts_his = Contract.query.filter_by(customer_id=customer_id).filter_by(status=1)
    return render_template('customer_info.html', title='租户资料', customers=customers, contracts=contracts, contracts_his=contracts_his)


@posts.route("/post/contract_info/<int:contract_id>")
@login_required
def contract_info(contract_id):
    exist_or_not = Contract.query.get_or_404(contract_id)
    contract = Contract.query.filter_by(id=contract_id).join(Customer, Customer.id==Contract.customer_id).join(House, House.id==Contract.house_id).join(Contractype, Contractype.id==Contract.type).\
    with_entities(Contract.id.label('id'), \
        Contract.name.label('contract_name'), \
        Contract.annual_rent.label('contract_annual_rent'), \
        Contract.status.label('contract_status'), \
        Contractype.name.label('contract_typename'), \
        Contract.start_time.label('contract_start_time'), \
        Contract.end_time.label('contract_end_time'), \
        Contract.contract_pics.label('contract_pics'), \
        Contract.approval_pics.label('approval_pics'), \
        Contract.auction_announcement.label('auction_announcement'), \
        Contract.auction_confirmation.label('auction_confirmation'), \
        Customer.id.label('customer_id'), \
        Customer.name.label('customer_name'), \
        Customer.id.label('customer_id'), \
        Customer.phone.label('customer_phone'), \
        Customer.cardid.label('customer_cardid'), \
        Customer.address.label('customer_address') , \
        Customer.postcode.label('customer_postcode') , \
        House.id.label('house_id') , \
        House.address.label('house_address') , \
        House.pictures.label('house_pictures') 
        ).first()
    contract_pics = contract.contract_pics.split("|")[1:]
    contractbills = Contractbill.query.filter_by(contract_id=contract.id)
    current_time  = datetime.now()
    return render_template('contract_info.html', title='合同资料', contract=contract, contract_pics=contract_pics, contractbills=contractbills, current_time=current_time)
    # points = json.dumps([ row._asdict() for row in contracts ])
    # return points

@posts.route("/post/bill/<int:bill_id>/topay", methods=['GET', 'POST'])
@login_required
def pay_bill(bill_id):
    bill = Contractbill.query.filter_by(id=bill_id).first()
    form = PaybillForm()
    if form.validate_on_submit():
        bill.status=1
        bill.note=form.note.data
        bill.opid=current_user.id
        db.session.commit()
        flash('帐单状态已经更新!', 'success')
        return redirect(url_for('posts.bills_thisyear'))
    elif request.method == 'GET':
        form.contract_id.data=bill.contract_id
        form.bill_amount.data=bill.bill_amount
        form.bill_sequence.data=bill.bill_sequence
        form.bill_date.data=bill.bill_date.strftime("%Y-%m-%d")
    return render_template('paybill.html', title='帐单管理', bill=bill, form=form )


@posts.route("/posts/contract/<int:contract_id>/print")
@login_required
def print_contract(contract_id):
    contract = Contract.query.filter_by(id=contract_id).join(Customer, Customer.id==Contract.customer_id).join(House, House.id==Contract.house_id).join(Resource, Resource.id==House.resource_id).join(Contractype, Contractype.id==Contract.type).join(Landlord, Landlord.id==Resource.landlord_id).\
    with_entities(Contract.id.label('contract_id'), \
        Contract.name.label('contract_name'), \
        Contractype.name.label('type_name'), \
        Contract.is_xuzu.label('is_xuzu'), \
        Contract.start_time.label('start_time'), \
        Contract.end_time.label('end_time'), \
        Contract.annual_rent.label('annual_rent'), \
        Contract.useof.label('useof'), \
        Contract.security_deposit.label('security_deposit'), \
        Contract.contract_pics.label('contract_pics'), \
        Contract.note.label('note'), \
        Customer.id.label('customer_id'), \
        Customer.name.label('customer_name'), \
        Customer.phone.label('customer_phone'), \
        Customer.cardid.label('customer_cardid'), \
        Customer.address.label('customer_address') , \
        Customer.postcode.label('customer_postcode') , \
        House.address.label('house_address') , \
        House.area.label('house_area') , \
        House.pictures.label('house_pictures'), \
        Landlord.name.label('landlord_name'), \
        Landlord.cardid.label('landlord_cardid'), \
        Landlord.phone.label('landlord_phone'), \
        Landlord.address.label('landlord_address')
        ).first()    

    if contract.is_xuzu == 1:
        firstbillamount = contract.annual_rent
        secondbillamount = round(contract.annual_rent*1.03)
        thirdbillamount = round(contract.annual_rent*1.03**2)
    else:
        firstbillamount = contract.annual_rent
        secondbillamount = contract.annual_rent
        thirdbillamount = contract.annual_rent

    totalamount = firstbillamount + secondbillamount + thirdbillamount
    totalamount_CN = number_to_chinese(totalamount)
    firstbillamount_CN = number_to_chinese(firstbillamount)

    TopayFirst = contract.start_time.strftime("%Y年%m月%d日")
    TopaySecond= (contract.start_time + timedelta(days=365*1)).strftime("%Y年%m月%d日")
    TopayThird = (contract.start_time + timedelta(days=365*2)).strftime("%Y年%m月%d日")

    durationYear= round((contract.end_time-contract.start_time).days/365)
    annual_rentin_CN = number_to_chinese(contract.annual_rent)
    security_deposit_CN = number_to_chinese(contract.security_deposit)

    if contract.is_xuzu == 1:
        return render_template('contract_xz.html', title='.', footer='.', 
        contract=contract, 
        TopayFirst=TopayFirst,
        TopaySecond=TopaySecond,
        TopayThird=TopayThird,
        durationYear=durationYear, 
        annual_rentin_CN=annual_rentin_CN, 
        security_deposit_CN=security_deposit_CN,
        firstbillamount = firstbillamount,
        secondbillamount = secondbillamount,
        thirdbillamount = thirdbillamount,
        totalamount = totalamount,
        totalamount_CN = totalamount_CN,
        firstbillamount_CN = firstbillamount_CN)

    elif contract.type_name == '拍租':
        return render_template('contract_pz.html', title='.', footer='.', 
        contract=contract, 
        TopayFirst=TopayFirst,
        TopaySecond=TopaySecond,
        TopayThird=TopayThird,
        durationYear=durationYear, 
        annual_rentin_CN=annual_rentin_CN, 
        security_deposit_CN=security_deposit_CN,
        firstbillamount = contract.annual_rent,
        secondbillamount = contract.annual_rent,
        thirdbillamount = contract.annual_rent,
        totalamount = totalamount,
        totalamount_CN = totalamount_CN,
        firstbillamount_CN = firstbillamount_CN)

    elif contract.type_name == '协议':
        return render_template('contract_xy.html', title='.', footer='.', 
        contract=contract, 
        TopayFirst=TopayFirst,
        TopaySecond=TopaySecond,
        TopayThird=TopayThird,
        durationYear=durationYear, 
        annual_rentin_CN=annual_rentin_CN, 
        security_deposit_CN=security_deposit_CN,
        firstbillamount = contract.annual_rent,
        secondbillamount = contract.annual_rent,
        thirdbillamount = contract.annual_rent,
        totalamount = totalamount,
        totalamount_CN = totalamount_CN,
        firstbillamount_CN = firstbillamount_CN)

    


@posts.route("/posts/map")
@login_required
def map():
    points = Garden.query.group_by(Garden.name,Garden.coordinate).join(Resource,Resource.garden_id==Garden.id).join(House,House.resource_id==Resource.id).\
    with_entities(
        Garden.name,\
        Garden.coordinate,\
        func.count(Garden.name).label('count')
        )
    return render_template('bdmap.html', title='房源分布', points=points)
    # points = json.dumps([ row._asdict() for row in query ])
    # return points


# for number_to_chinese test
@posts.route("/posts/contract_demo1")
@login_required
def contract_demo1():
    return number_to_chinese(1000010)


# from string to chinese 
CHINESE_NEGATIVE = '负'
CHINESE_ZERO = '零'
CHINESE_DIGITS = ['', '壹', '贰', '叁', '肆', '伍', '陆', '柒', '捌', '玖']
CHINESE_UNITS = ['', '拾', '佰', '仟']
CHINESE_GROUP_UNITS = ['', '万', '亿', '兆']

def _enumerate_digits(number):
    position = 0
    while number > 0:
        digit = number % 10
        number //= 10
        yield position, digit
        position += 1

def number_to_chinese(number):
    if not isinstance(number, int) and not isinstance(number, long):
        raise ValueError('number must be integer')
    if number == 0:
        return CHINESE_ZERO
    words = []
    if number < 0:
        words.append(CHINESE_NEGATIVE)
        number = -number

    group_is_zero = True
    need_zero = False
    for position, digit in reversed(list(_enumerate_digits(number))):
        unit = position % len(CHINESE_UNITS)
        group = position // len(CHINESE_UNITS)

        if digit != 0:
            if need_zero:
                words.append(CHINESE_ZERO)
            if digit != 1 or unit != 1 or not group_is_zero or (group == 0 and need_zero):
                words.append(CHINESE_DIGITS[digit])
            words.append(CHINESE_UNITS[unit])
        group_is_zero = group_is_zero and digit == 0
        if unit == 0 and not group_is_zero:
            words.append(CHINESE_GROUP_UNITS[group])
        need_zero = (digit == 0 and (unit != 0 or group_is_zero))
        if unit == 0:
            group_is_zero = True

    # End core loop.

    return ''.join(words)# Begin core loop.                                      
#print(number_to_chinese(10000001))



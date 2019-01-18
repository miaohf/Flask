
from flask import Blueprint
from flask import current_app as app
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Contractbill, House, Customer, Contract
from datetime import datetime, timedelta



from yunpian_python_sdk.model import constant as YC
from yunpian_python_sdk.ypclient import YunpianClient
import time



sms = Blueprint('sms', __name__)
clnt = YunpianClient('9930e55281443d213f58729a32db572a')

@sms.route('/sms')
@login_required
def run_tasks():
    bills = Contractbill.query.filter(Contractbill.status==0).join(Contract, Contract.id==Contractbill.contract_id).join(House, House.id==Contract.house_id).join(Customer, Customer.id==Contract.customer_id).\
    with_entities(Contractbill.id, \
        Contractbill.bill_date, \
        Contractbill.bill_amount, \
        House.address.label('house_address'), \
        Customer.name.label('customer_name'), \
        Customer.phone.label('customer_phone')
        ).all()

    for bill in bills:
    	if (datetime.today()+timedelta(days=7)).strftime('%Y-%m-%d')==bill.bill_date.strftime('%Y-%m-%d') or (datetime.today()+timedelta(days=41)).strftime('%Y-%m-%d')==bill.bill_date.strftime('%Y-%m-%d'):
            text = '【拓展时代】尊敬的承租户' + str(bill.customer_name) + '，您所承租的（' + str(bill.house_address) + '）房屋，根据合同约定应于' + str(bill.bill_date.strftime("%Y-%m-%d")) + '前支付租金' + str(bill.bill_amount) +'元，请及时缴纳。详情咨询84111813。'
            # text = '【拓展时代】尊敬的承租户许跃伟，您所承租的（车站南路888号）房屋，根据合同约定应于2019年2月28日前支付租金23600元，请及时缴纳。详情咨询84111813。'
            message1 = {YC.MOBILE:'13819063105',YC.TEXT:text}  #接受号码固定
            message2 = {YC.MOBILE:'13605838464',YC.TEXT:text}  #接受号码固定
            # message3 = {YC.MOBILE:'bill.customer_phone',YC.TEXT:text}  #接受号码固定
            # app.apscheduler.add_job(func=scheduled_task, trigger='date', args=[message], id=str(bill.id)) # does work
            # app.apscheduler.add_job(func=scheduled_task, trigger='cron', args=[message], id=str(bill.id), hour='02', minute='48')  #not work
            app.apscheduler.add_job(func=scheduled_task, trigger='interval', args=[message1], id=str(bill.id)+'1',  hours=3)  
            app.apscheduler.add_job(func=scheduled_task, trigger='interval', args=[message2], id=str(bill.id)+'2',  hours=3) 
            # app.apscheduler.add_job(func=scheduled_task, trigger='interval', args=[message3], id=str(bill.id)+'3',  hours=3) 
    return '定时任务已经启动', 200

    
 
def scheduled_task(message):
    r = clnt.sms().single_send(message)
    print(message)



# scheduler demo01

# @app.route('/run-tasks')
# def run_tasks():
#     for i in range(10):
#         app.apscheduler.add_job(func=scheduled_task, trigger='date', args=[i], id='j'+str(i))
 
#     return 'Scheduled several long running tasks.', 200
 
# def scheduled_task(task_id):
#     for i in range(10):
#         time.sleep(1)
#         print('Task {} running iteration {}'.format(task_id, i))


# scheduler demo02

# scheduler = BlockingScheduler()
# scheduler.add_job(func=aps_test, args=('定时任务',), trigger='cron', second='*/5')
# scheduler.add_job(func=aps_test, args=('一次性任务',), next_run_time=datetime.datetime.now() + datetime.timedelta(seconds=12))
# scheduler.add_job(func=aps_test, args=('循环任务',), trigger='interval', seconds=3, id='interval_task')

# scheduler.start()



from flask import Blueprint
from flask import current_app as app
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Contractbill, House, Customer, Contract, Sms
from datetime import datetime, timedelta

# from flask_apscheduler import APScheduler
# from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler


from yunpian_python_sdk.model import constant as YC
from yunpian_python_sdk.ypclient import YunpianClient
import time



sms = Blueprint('sms', __name__)

# # scheduler = APScheduler()
scheduler = BackgroundScheduler()
# scheduler.init_app(app)
scheduler.start()


@sms.route('/scheduler')
# @login_required
def run_scheduler():

    bills = Contractbill.query.filter(Contractbill.status==0).join(Contract, Contract.id==Contractbill.contract_id).join(House, House.id==Contract.house_id).join(Customer, Customer.id==Contract.customer_id).\
    with_entities(Contractbill.bill_sequence, \
        Contractbill.bill_date, \
        Contractbill.bill_amount, \
        House.address.label('house_address'), \
        Customer.name.label('customer_name'), \
        Customer.phone.label('customer_phone')
        ).all()

    for bill in bills:
        # if (datetime.today()+timedelta(days=7)).strftime('%Y-%m-%d')==bill.bill_date.strftime('%Y-%m-%d') or (datetime.today()+timedelta(days=30)).strftime('%Y-%m-%d')==bill.bill_date.strftime('%Y-%m-%d'):
        # if bill.bill_date.strftime('%Y-%m-%d') < (datetime.today()+timedelta(days=600)).strftime('%Y-%m-%d'):
        if (datetime.today()+timedelta(days=30)).strftime('%Y-%m-%d')==bill.bill_date.strftime('%Y-%m-%d'):
            content = '【拓展时代】尊敬的承租户' + str(bill.customer_name) + '，您所承租的（' + str(bill.house_address) + '）房屋，根据合同约定应于' + str(bill.bill_date.strftime("%Y-%m-%d")) + '前支付租金' + str(bill.bill_amount) +'元，请及时缴纳。详情咨询84111813。'
            sms = Sms(phone = bill.customer_phone, \
                bill_sequence = bill.bill_sequence, \
                content = content )
            db.session.add(sms)
            db.session.commit()

    smses = Sms.query.filter(Sms.status==0).all()
    for sms in smses:
        scheduler.add_job(func=sms_send_task, trigger='date', args=[ {YC.MOBILE:sms.phone,YC.TEXT:sms.content} ], id=str(sms.bill_sequence))
        scheduler.add_job(func=sms_send_task, trigger='date', args=[ {YC.MOBILE:'13605838464',YC.TEXT:sms.content} ], id='13605838464')
        # scheduler.add_job(func=sms_send_task, trigger='date', args=[ {YC.MOBILE:13819063105,YC.TEXT:sms.content} ], id='13819063105')
        sms.status = 1
        db.session.commit()
        time.sleep(15)

    return '定时任务已经启动', 200
        # try:
    #     # This is here to simulate application activity (which keeps the main thread alive).
    #     while True:
    #         time.sleep(5)
    # except (KeyboardInterrupt, SystemExit):
    #     # Not strictly necessary if daemonic mode is enabled but should be done if possible
    #     scheduler.shutdown()


# def sms_generation_task():
#     with app.app_context():
#         bills = Contractbill.query.filter(Contractbill.status==0).join(Contract, Contract.id==Contractbill.contract_id).join(House, House.id==Contract.house_id).join(Customer, Customer.id==Contract.customer_id).\
#         with_entities(Contractbill.bill_sequence, \
#             Contractbill.bill_date, \
#             Contractbill.bill_amount, \
#             House.address.label('house_address'), \
#             Customer.name.label('customer_name'), \
#             Customer.phone.label('customer_phone')
#             ).all()

#         for bill in bills:
#         # if (datetime.today()+timedelta(days=7)).strftime('%Y-%m-%d')==bill.bill_date.strftime('%Y-%m-%d') or (datetime.today()+timedelta(days=30)).strftime('%Y-%m-%d')==bill.bill_date.strftime('%Y-%m-%d'):
#             if bill.bill_date.strftime('%Y-%m-%d') < (datetime.today()+timedelta(days=600)).strftime('%Y-%m-%d'):
#                 content = '【拓展时代】尊敬的承租户' + str(bill.customer_name) + '，您所承租的（' + str(bill.house_address) + '）房屋，根据合同约定应于' + str(bill.bill_date.strftime("%Y-%m-%d")) + '前支付租金' + str(bill.bill_amount) +'元，请及时缴纳。详情咨询84111813。'
#                 sms = Sms(phone = bill.customer_phone, \
#                     bill_sequence1 = bill.bill_sequence, \
#                     content = content )
#                 db.session.add(sms)
#                 db.session.commit()


def sms_send_task(message):
    clnt = YunpianClient('9930e55281443d213f58729a32db572a')
    r = clnt.sms().single_send(message)
    print(message)



# def sms_generation_job():
#     scheduler.add_job(func=sms_generation_task, trigger='date', args=[], id='88123456')


# def sms_send_job():
#     with app.app_context():
#         smses = Sms.query.filter(Sms.status==0).all()
#         for sms in smses:
#             # app.apscheduler.add_job(func=scheduled_task, trigger='date', args=[message], id=str(bill.id)) # do work
#             # app.apscheduler.add_job(func=scheduled_task, trigger='cron', args=[message], id=str(bill.id), hour='02', minute='48')  #not work
#             # scheduler.add_job(func=scheduled_task, trigger='interval', args=[message3], id=str(bill.id)+'3',  hours=24)  do work
#             scheduler.add_job(func=sms_send_task, trigger='date', args=[ {YC.MOBILE:sms.phone,YC.TEXT:sms.content} ], id=str(sms.bill_sequence))
#             # scheduler.add_job(func=sms_send_task, trigger='date', args=[ {YC.MOBILE:'13819063105',YC.TEXT:sms.content} ], id='13819063105')
#             sms.status = 1
#             db.session.commit()
#             time.sleep(15)

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


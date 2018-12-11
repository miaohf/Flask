from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, DateField, FileField, RadioField, validators
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileField, FileAllowed, FileRequired


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')


class GardenForm(FlaskForm):
    name = StringField('小区名称', validators=[DataRequired(), Length(min=4, max=20)], render_kw={"placeholder": '九色鹿庄园'})
    coordinate = StringField('地图坐标',validators=[DataRequired(), Length(min=16, max=21)], render_kw={"placeholder": '120.927049,30.838363'})
    note = StringField('备注信息', render_kw={"placeholder": '九色鹿网络技术'})
    submit = SubmitField('确定')


class ResourceForm(FlaskForm):
    landlord_id=SelectField('产权持有人', choices=[], coerce=int, validators=[DataRequired(message=u"小区编号不能为空")])
    garden_id=SelectField('所在小区', choices=[], coerce=int, validators=[DataRequired(message=u"小区编号不能为空")])
    cardid = StringField('产证编号', validators=[DataRequired(), Length(7)], render_kw={"placeholder": '浙(2017)嘉善县不动产权第0049447号'})
    address = StringField('产证地址', validators=[DataRequired(), Length(min=4, max=40)], render_kw={"placeholder": '嘉善九色鹿大道888号'})
    price = StringField('市场估值(万元)', validators=[DataRequired(), Length(min=2, max=8)], render_kw={"placeholder": '308'})
    pictures = FileField('产证照片', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'pdf'])], render_kw={'multiple': True})
    area1 = StringField('建筑面积㎡', validators=[DataRequired(), Length(min=2, max=8)], render_kw={"placeholder": '168.4'})
    area2 = StringField('土地使用权面积㎡', validators=[DataRequired(), Length(min=2, max=8)], render_kw={"placeholder": '75'})
    note = StringField('备注信息', render_kw={"placeholder": '九色鹿网络技术'})
    submit = SubmitField('确定')	


class UpdateResourceForm(FlaskForm):
    company = StringField('所属单位', validators=[DataRequired(), Length(min=4, max=20)], render_kw={"placeholder": '嘉善九色鹿科技有限公司'})
    garden_id=StringField('小区编号',render_kw={'readonly': True})
    address = StringField('详细地址', validators=[DataRequired(), Length(min=4, max=40)], render_kw={"placeholder": '嘉善九色鹿大道888号'})
    price = StringField('市场估值(万元)', validators=[DataRequired(), Length(min=2, max=8)], render_kw={"placeholder": '308'})
    pictures = FileField('不动产证', validators=[FileRequired(), FileAllowed(['jpg', 'png'])], render_kw={'multiple': True})
    area1 = StringField('建筑面积(㎡)', validators=[DataRequired(), Length(min=2, max=8)], render_kw={"placeholder": '168.4'})
    area2 = StringField('土地使用权面积(㎡)', validators=[DataRequired(), Length(min=2, max=8)], render_kw={"placeholder": '75'})
    cardid = StringField('不动产编号', validators=[DataRequired(), Length(7)], render_kw={"placeholder": '浙(2017)嘉善县不动产权第0049888号'})
    note = StringField('备注信息', render_kw={"placeholder": '九色鹿网络技术'})
    submit = SubmitField('确定')  


class HouseForm(FlaskForm):
    address = StringField('详细地址', validators=[DataRequired(), Length(min=4, max=40)], render_kw={"placeholder": '嘉善九色鹿大道888号'})
    resource_id=SelectField('资产编号', choices=[], coerce=int, validators=[DataRequired(message=u"资产编号不能为空")])
    # resource_id=SelectField('资产编号', choices=[], coerce=int, validators=[DataRequired(message=u"资产编号不能为空")], default=(0,'80400002'))
    area =StringField('房源面积(㎡)', validators=[DataRequired(), Length(min=2, max=8)], render_kw={"placeholder": '178'})
    pictures = FileField('现场照片', validators=[FileRequired(), FileAllowed(['jpg', 'png'])], render_kw={'multiple': True})
    # pictures = FileField('现场照片', validators=[FileRequired(u'文件未选择！'), FileAllowed(photos, u'只能上传图片！')], render_kw={'multiple': True})
    note = StringField('备注信息', render_kw={"placeholder": '九色鹿网络技术'})
    submit = SubmitField('确定')

class UpdateHouseForm(FlaskForm):
    address = StringField('详细地址', render_kw={'readonly': True})
    resource_id = StringField('资产编号', render_kw={'readonly': True})
    area =StringField('房源面积(㎡)', validators=[DataRequired(), Length(min=2, max=8)], render_kw={"placeholder": '178'})
    pictures = FileField('新增照片', validators=[FileRequired(), FileAllowed(['jpg', 'png'])], render_kw={'multiple': True})
    note = StringField('备注信息', render_kw={"placeholder": '九色鹿网络技术'})
    submit = SubmitField('确定')
    

class CustomerForm(FlaskForm):
    name = StringField('租户名称', validators=[DataRequired(), Length(min=2, max=20)], render_kw={"placeholder": '九色神鹿/嘉善九色鹿科技有限公司'})
    # phone = StringField('联系电话', validators=[DataRequired(), Length(11)], render_kw={"data-inputmask": "'alias': 'phonebe'"})
    phone = StringField('联系电话', validators=[DataRequired(), Length(11)], render_kw={"placeholder": '13858003606'})
    address = StringField('详细地址', validators=[DataRequired(), Length(min=4, max=40)], render_kw={"placeholder": '九色鹿庄园88幢1-401#'})
    cardid = StringField('证件号码', validators=[DataRequired(), Length(17)], render_kw={"placeholder": '33042119780716153Y'})
    pictures = FileField('证件照片', validators=[FileRequired(), FileAllowed(['jpg', 'png'])], render_kw={'multiple': True})
    postcode = StringField('邮政编码', validators=[DataRequired(), Length(6)], render_kw={"placeholder": '314100'})
    note = StringField('备注信息', render_kw={"placeholder": '无特殊情况'})
    submit = SubmitField('确定')  


class LandlordForm(FlaskForm):
    name = StringField('产证持有人', validators=[DataRequired(), Length(min=2, max=20)], render_kw={"placeholder": '嘉善国有资产投资有限公司'})
    # phone = StringField('联系电话', validators=[DataRequired(), Length(11)], render_kw={"data-inputmask": "'alias': 'phonebe'"})
    phone = StringField('联系电话', validators=[DataRequired(), Length(8,12)], render_kw={"placeholder": '13858003606/057384055550'})
    address = StringField('详细地址', validators=[DataRequired(), Length(min=4, max=40)], render_kw={"placeholder": '嘉善县地址魏塘镇解放东路318号'})
    cardid = StringField('证件号码', validators=[DataRequired(), Length(17)], render_kw={"placeholder": '91330421730907405U'})
    pictures = FileField('证件照片', validators=[FileRequired(), FileAllowed(['jpg', 'png'])], render_kw={'multiple': True})
    note = StringField('备注信息', render_kw={"placeholder": '无特殊情况'})
    submit = SubmitField('确定') 


class ContractForm(FlaskForm):
    name = StringField('合同名称', validators=[DataRequired(), Length(min=4, max=20)], render_kw={"placeholder": 'XXXX合同'})
    house_id=SelectField('选择房源', choices=[], coerce=int, validators=[DataRequired(message=u"房源编号不能为空")])
    customer_id=SelectField('租户编号', choices=[], coerce=int, validators=[DataRequired(message=u"租户编号不能为空")])
    type=SelectField('选择类型', choices=[], coerce=int, validators=[DataRequired(message=u"合同类型不能为空")])
    auction_date = DateField('拍卖日期', id="auction-datepicker", format='%m/%d/%Y', validators=(validators.Optional(),)) 
    start = DateField('合同开始', id="start-datepicker", format='%m/%d/%Y', validators=[DataRequired()]) 
    end = DateField('合同结束', id="end-datepicker", format='%m/%d/%Y', validators=[DataRequired()]) 
    useof = StringField('用途', render_kw={"placeholder": '办公用途'}, validators=[DataRequired(), Length(min=2, max=20)])
    security_deposit = StringField('保证金', render_kw={"placeholder": '50000'}, validators=[DataRequired(), Length(min=4, max=20)])
    annual_rent = StringField('年租金', render_kw={"placeholder": '50000'}, validators=[DataRequired(), Length(min=4, max=20)])
    contract_pics = FileField('合同附件', validators=[FileAllowed(['jpg', 'png', 'pdf'])], render_kw={'multiple': True})
    approval_pics = FileField('出租审批表', validators=[FileRequired(), FileAllowed(['jpg', 'png'])], render_kw={'multiple': True})
    auction_announcement = FileField('拍卖公告', validators=[FileRequired(), FileAllowed(['jpg', 'png'])], render_kw={'multiple': True})
    auction_confirmation = FileField('拍卖成交确认书', validators=[FileRequired(), FileAllowed(['jpg', 'png'])], render_kw={'multiple': True})
    note = StringField('备注信息', render_kw={"placeholder": '九色鹿网络技术'})
    # reason = StringField('终止原因', render_kw={'readonly': True})
    # status = RadioField('合同状态', choices=[('0','正常'),('1','终止')], default='0')
    submit = SubmitField('确定')


class UpdateContractForm(FlaskForm):
    name = StringField('合同名称', validators=[DataRequired(), Length(min=4, max=20)], render_kw={"placeholder": '九色鹿庄园壹号合同'})
    house_id = StringField('选择房源', render_kw={'readonly': True})
    customer_id = StringField('租户编号', render_kw={'readonly': True})
    type = SelectField('选择类型', choices=[], coerce=int, validators=[DataRequired(message=u"合同类型不能为空")])
    auction_date = DateField('拍卖日期', id="auction-datepicker", format='%m/%d/%Y', validators=(validators.Optional(),)) 
    start = DateField('开始日期', id="datepicker-popup", format='%m/%d/%Y', validators=[DataRequired()]) 
    end = DateField('结束日期', id="inline-datepicker", format='%m/%d/%Y', validators=[DataRequired()]) 
    useof = StringField('用途', render_kw={"placeholder": '办公用途'}, validators=[DataRequired(), Length(min=2, max=20)])
    security_deposit = StringField('保证金', render_kw={"placeholder": '50000'}, validators=[DataRequired(), Length(min=4, max=20)])
    annual_rent = StringField('年租金', render_kw={"placeholder": '50000'}, validators=[DataRequired(), Length(min=4, max=20)])
    # contract_pics = FileField('合同附件', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'pdf'])], render_kw={'multiple': True})
    contract_pics = FileField('合同附件', validators=[FileAllowed(['jpg', 'png', 'pdf'])], render_kw={'multiple': True})
    approval_pics = StringField('出租审批表', render_kw={'readonly': True})
    auction_announcement = StringField('拍卖公告', render_kw={'readonly': True})
    auction_confirmation = StringField('拍卖成交确认书', render_kw={'readonly': True})
    note = StringField('备注信息', render_kw={"placeholder": '九色鹿网络技术'})
    reason = StringField('终止原因', render_kw={'readonly': True})
    status = RadioField('合同状态', choices=[('0','正常'),('1','终止')], default='0')
    submit = SubmitField('确定')


class TerminateContractForm(FlaskForm):
    name = StringField('合同名称', render_kw={'readonly': True})
    house_id = StringField('选择房源', render_kw={'readonly': True})
    customer_id = StringField('租户编号', render_kw={'readonly': True})
    type = StringField('选择类型', render_kw={'readonly': True})
    auction_date = StringField('拍卖日期', render_kw={'readonly': True})
    start = StringField('开始日期', render_kw={'readonly': True})
    end = StringField('结束日期', render_kw={'readonly': True})
    useof = StringField('用途', render_kw={'readonly': True})
    security_deposit = StringField('保证金', render_kw={'readonly': True})
    annual_rent = StringField('年租金', render_kw={'readonly': True})
    contract_pics = StringField('合同附件', render_kw={'readonly': True})
    approval_pics = StringField('出租审批表', render_kw={'readonly': True})
    auction_announcement = StringField('拍卖公告', render_kw={'readonly': True})
    auction_confirmation = StringField('拍卖成交确认书', render_kw={'readonly': True})
    note = StringField('备注信息', render_kw={"placeholder": '九色鹿网络技术'})
    reason = StringField('终止原因',  validators=[DataRequired(), Length(min=4, max=40)], render_kw={"placeholder": '合同到期未续约'})
    status = RadioField('合同状态', choices=[('0','正常'),('1','终止')], default='0')
    submit = SubmitField('确定')


class RenewalContractForm(FlaskForm):
    name = StringField('合同名称', validators=[DataRequired(), Length(min=4, max=20)], render_kw={"placeholder": '九色鹿庄园壹号合同'})
    house_id = StringField('选择房源', render_kw={'readonly': True})
    customer_id = StringField('租户编号', render_kw={'readonly': True})
    type = StringField('选择类型', render_kw={'readonly': True})
    auction_date = DateField('拍卖日期', render_kw={'readonly': True})
    start = DateField('开始日期', id="renewalstart-datepicker", format='%m/%d/%Y', validators=[DataRequired()]) 
    end = DateField('结束日期', id="renewalend-datepicker", format='%m/%d/%Y', validators=[DataRequired()]) 
    useof = StringField('用途', render_kw={"placeholder": '办公用途'}, validators=[DataRequired(), Length(min=2, max=20)])
    security_deposit = StringField('保证金', render_kw={"placeholder": '50000'}, validators=[DataRequired(), Length(min=4, max=20)])
    annual_rent = StringField('年租金',  render_kw={'readonly': True})
    contract_pics = FileField('合同附件', validators=[FileAllowed(['jpg', 'png', 'pdf'])], render_kw={'multiple': True})
    approval_pics = StringField('出租审批表', render_kw={'readonly': True})
    auction_announcement = StringField('拍卖公告', render_kw={'readonly': True})
    auction_confirmation = StringField('拍卖成交确认书', render_kw={'readonly': True})
    note = StringField('备注信息', render_kw={"placeholder": '九色鹿网络技术'})
    reason = StringField('终止原因', render_kw={'readonly': True})
    status = RadioField('合同状态', choices=[('0','正常'),('1','终止')], default='0')
    submit = SubmitField('确定')



class ContractypeForm(FlaskForm):
    name = StringField('合同类型', validators=[DataRequired(), Length(min=2, max=20)], render_kw={"placeholder": '协议|拍租|续租'})
    note = StringField('备注信息', render_kw={"placeholder": '九色鹿网络技术'})
    submit = SubmitField('确定')


class MaintenanceunitForm(FlaskForm):
    name = StringField('维修单位', validators=[DataRequired(), Length(min=2, max=20)], render_kw={"placeholder": '九色鹿专业维修公司'})
    phone = StringField('联系电话', validators=[DataRequired(), Length(min=11, max=12)], render_kw={"placeholder": '13858003606/057384055550'})
    note = StringField('备注信息', render_kw={"placeholder": '九色鹿网络技术'})
    submit = SubmitField('确定')


class MaintenancerecForm(FlaskForm):
    house_id = StringField('房源编号', render_kw={'readonly': True})
    maintenanceunit_id = SelectField('维修单位', choices=[], coerce=int, validators=[DataRequired(message=u"维修单位不能为空")])
    note = StringField('具体情况', validators=[DataRequired(message=u"处理结果不能为空")], render_kw={"placeholder": '屋顶漏水'})
    maintenance_note = StringField('处理结果', render_kw={'readonly': True})
    submit = SubmitField('确定')


class TerminateMaintenancerecForm(FlaskForm):
    house_id = StringField('房源编号', render_kw={'readonly': True})
    maintenanceunit_id = SelectField('维修单位', choices=[], coerce=int, validators=[DataRequired(message=u"维修单位不能为空")])
    note = StringField('具体情况', render_kw={"placeholder": '屋顶漏水'})
    maintenance_note = StringField('处理结果', validators=[DataRequired(message=u"处理结果不能为空")], render_kw={"placeholder": '填入维修结果'})
    submit = SubmitField('结单')


class ContractbillForm(FlaskForm):
    submit = SubmitField('帐单更新')
    

class PaybillForm(FlaskForm):
    contract_id = StringField('合同编号', render_kw={'readonly': True})
    bill_amount = StringField('帐单金额', render_kw={'readonly': True})
    bill_sequence = StringField('帐单期号', render_kw={'readonly': True})
    bill_date = StringField('帐单日期', render_kw={'readonly': True})
    note = StringField('备注信息', validators=[DataRequired(message=u"缴费备注信息为必填字段"), Length(min=4, max=40)], render_kw={"placeholder": '确认到帐金额正确'})
    submit = SubmitField('缴费提交')

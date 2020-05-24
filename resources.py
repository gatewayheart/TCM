from flask_restful import Resource, reqparse
import psycopg2
import pandas as pd
from pandas.io.json import json_normalize
import cx_Oracle
from sqlalchemy import create_engine
import datetime
import numpy as np
import json
import re
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)



#Epidemiological zoning request
Epidemiological=reqparse.RequestParser()
Epidemiological.add_argument('type',help = 'This field cannot be blank', required = True)

# yeu cau lay nguon nuoc
#nn=reqparse.RequestParser()
#nn.add_argument('type',help = 'This field cannot be blank', required = True)


def epidemiology(value):
    df=pd.read_csv(r"data.csv",encoding='utf-8')
    with open(r'datajson.json', 'r') as myfile:
        datajson=myfile.read()
    #data=df
    data=df.query("LOAI2=='%s'"%value) #quyre theo loai
    #data=df.query("LOAI=='%s'"%value) #quyre theo loai
    statesdata = json.loads(datajson)
    districts = statesdata['features']
    for i,obj in enumerate(districts) :
        district_name = obj['properties']['name']
        data_district = data.query("Huyen=='%s'"%district_name)
        statesdata['features'][i]['properties']['density'] = len(data_district)
        # Bắt đàu đặt biến lấy theo huyện
        # Ngày 24/5/2020 Tắt option chọn nguồn nước
        #dataNguonnuoc1 = data_district 
        #Query số tổng số theo nguồn nước bằng nước máy
        #statesdata['features'][i]['properties']['nuocMay'] = len(dataNguonnuoc1.query("Nguonnuoc=='Nuoc may'"))
        #dataNguonNuoc2 = data_district
        #statesdata['features'][i]['properties']['nuocGiengKhoan'] = len(dataNguonNuoc2.query("Nguonnuoc=='Nuoc gieng khoan'"))
        #dataNguonNuoc3 = data_district
        #statesdata['features'][i]['properties']['nuocTuNhien'] = len(dataNguonNuoc3.query("Nguonnuoc=='Nuoc tu nhien'"))
        # Bắt đàu đặt biết lấy loai ca bệnh theo huyện
        dataChangeCaBenh1 = data_district
        #Query số tổng số theo loại ca bệnh theo tan phat
        statesdata['features'][i]['properties']['tanPhat'] = len(dataChangeCaBenh1.query("Loaicabenh=='Tan phat'"))
        # Bắt đàu đặt biết lấy loai dương tính EV71 theo huyện
        dataDuongTinhEV71 = data_district
        #Query số tổng số theo loại ca bệnh theo EV71
        statesdata['features'][i]['properties']['EV71'] = len(dataDuongTinhEV71.query("LOAI=='EV71'"))
        dataDuongTinhCA16 = data_district
        #Query số tổng số theo loại ca bệnh theo CA16
        statesdata['features'][i]['properties']['CA16'] = len(dataDuongTinhCA16.query("LOAI=='CA16'"))
        dataDuongTinhChungKhac = data_district
        #Query số tổng số theo loại ca bệnh theo Chung khac
        #statesdata['features'][i]['properties']['CHUNGKHAC'] = len(dataDuongTinhChungKhac.query("LOAI=='Non EV71 va CA16'"))
        statesdata['features'][i]['properties']['CHUNGKHAC'] = len(dataDuongTinhChungKhac.query("LOAI =='A6' or LOAI =='A10' or LOAI =='A2'"))
        #Query số tổng số theo loại ca bệnh theo Chung A10
        dataDuongTinhA10 = data_district
        statesdata['features'][i]['properties']['A10'] = len(dataDuongTinhChungKhac.query("LOAI=='A10'"))    
        #Query số tổng số theo loại ca bệnh theo Chung A2
        dataDuongTinhA2 = data_district
        statesdata['features'][i]['properties']['A2'] = len(dataDuongTinhChungKhac.query("LOAI=='A2'"))    
        #Query số tổng số theo loại ca bệnh theo Chung A6
        dataDuongTinhA6 = data_district
        statesdata['features'][i]['properties']['A6'] = len(dataDuongTinhChungKhac.query("LOAI=='A6'"))           
         #Bổ sung ngày 20200411 Số ca xét nghiệm dương tính
        dataDuongTinh = data_district
        #Query số tổng số theo loại ca bệnh theo Ca dương tính
        statesdata['features'][i]['properties']['DuongTinh'] = len(dataDuongTinh.query("LOAI=='EV71' or LOAI=='CA16' or LOAI=='Non EV71 va CA16' or LOAI =='A6' or LOAI =='A10' or LOAI =='A2'"))

    return {'status':'SUCCESS','message':'The number of positive cases is located in the area of ​​Binh Dinh province','data':statesdata}


class EpidemiologicalZoning(Resource):
    def post(self):
        data = Epidemiological.parse_args()
        if data['type']=='Positive':
            df=pd.read_csv(r"data.csv",encoding='utf-8')
            with open(r'datajson.json', 'r') as myfile:
                datajson=myfile.read()
            data=df
            #data=df.query("KQXetNghiemTCM=='Duong Tinh'")
            statesdata = json.loads(datajson)
            districts = statesdata['features']
            for i,obj in enumerate(districts) :
                district_name = obj['properties']['name']
                data_district = data.query("Huyen=='%s'"%district_name)
                statesdata['features'][i]['properties']['density'] = len(data_district)
                # Bắt đàu đặt biết lấy theo huyện
                # Ngày 24/5/2020 Tắt option chọn nguồn nước
                # dataNguonnuoc1 = data_district 
                #Query số tổng số theo nguồn nước bằng nước máy
                #statesdata['features'][i]['properties']['nuocMay'] = len(dataNguonnuoc1.query("Nguonnuoc=='Nuoc may'"))
                #dataNguonNuoc2 = data_district
                #statesdata['features'][i]['properties']['nuocGiengKhoan'] = len(dataNguonNuoc2.query("Nguonnuoc=='Nuoc gieng khoan'"))
                #dataNguonNuoc3 = data_district
                #statesdata['features'][i]['properties']['nuocTuNhien'] = len(dataNguonNuoc3.query("Nguonnuoc=='Nuoc tu nhien'"))
                # Bắt đàu đặt biết lấy loai ca bệnh theo huyện
                #dataChangeCaBenh1 = data_district
                #Query số tổng số theo loại ca bệnh theo tan phat
                #statesdata['features'][i]['properties']['tanPhat'] = len(dataChangeCaBenh1.query("Loaicabenh=='Tan phat'"))
                # Bắt đàu đặt biết lấy loai dương tính EV71 theo huyện
                dataDuongTinhEV71 = data_district
                #Query số tổng số theo loại ca bệnh theo tan phat
                statesdata['features'][i]['properties']['EV71'] = len(dataDuongTinhEV71.query("LOAI=='EV71'"))
                dataDuongTinhCA16 = data_district
                #Query số tổng số theo loại ca bệnh theo tan phat
                statesdata['features'][i]['properties']['CA16'] = len(dataDuongTinhCA16.query("LOAI=='CA16'"))
                dataDuongTinhChungKhac = data_district
                #Query số tổng số theo loại ca bệnh theo tan phat
                statesdata['features'][i]['properties']['CHUNGKHAC'] = len(dataDuongTinhChungKhac.query("LOAI=='Non EV71 va CA16'"))
                #Query số tổng số theo loại ca bệnh theo Chung A10
                dataDuongTinhA10 = data_district
                statesdata['features'][i]['properties']['A10'] = len(dataDuongTinhChungKhac.query("LOAI=='A10'"))    
                #Query số tổng số theo loại ca bệnh theo Chung A2
                dataDuongTinhA2 = data_district
                statesdata['features'][i]['properties']['A2'] = len(dataDuongTinhChungKhac.query("LOAI=='A2'"))    
                #Query số tổng số theo loại ca bệnh theo Chung A6
                dataDuongTinhA6 = data_district
                statesdata['features'][i]['properties']['A6'] = len(dataDuongTinhChungKhac.query("LOAI=='A6'"))           
                #Bổ sung ngày 20200411 Số ca xét nghiệm dương tính
                dataDuongTinh = data_district
                #Query số tổng số theo loại ca bệnh theo Ca dương tính
                statesdata['features'][i]['properties']['DuongTinh'] = len(dataDuongTinh.query("LOAI=='EV71' or LOAI=='CA16' or LOAI=='Non EV71 va CA16' or LOAI =='A6' or LOAI =='A10' or LOAI =='A2'"))
   
            return {'status':'SUCCESS','message':'The number of positive cases is located in the area of ​​Binh Dinh province','data':statesdata}
        else:
            if data['type']!='':
                return epidemiology(data['type'])
            else:
                return {'message':'Something went wrong'}

def nguonnuoc(type):
    df=pd.read_csv(r"data.csv",encoding='utf-8')
    with open(r'datajson.json', 'r') as myfile:
        datajson=myfile.read()
    data=df.query("Nguonnuoc=='%s'"%type)
    statesdata = json.loads(datajson)
    districts = statesdata['features']
    for i,obj in enumerate(districts) :
        district_name = obj['properties']['name']
        statesdata['features'][i]['properties']['density'] = len(data.query("Huyen=='%s'"%district_name))
        #statesdata['features'][i]['properties']['whatever'] = 3
    return {'status':'SUCCESS','message':'The number of positive cases is located in the area of ​​Binh Dinh province','data':statesdata}


class layNguonNuoc(Resource):
     def post(self):
        data = nn.parse_args()
        if data['type']!='':
            return nguonnuoc(data['type'])
        else:
            return {'message':'Something went wrong'}


# -*- coding: utf-8 -*-
"""
伊利股份(600887.SH)近一年行情数据可视化面板生成脚本
数据来源：Tushare MCP
"""
import json
import csv
import os

# Tushare返回的日线行情数据（按日期倒序）
raw_data = [
    {"ts_code":"600887.SH","trade_date":"20260630","open":24.47,"high":24.49,"low":23.9,"close":23.96,"pre_close":24.58,"change":-0.62,"pct_chg":-2.5224,"vol":623024.64,"amount":1499377.936},
    {"ts_code":"600887.SH","trade_date":"20260629","open":24.3,"high":24.8,"low":23.82,"close":24.58,"pre_close":24.27,"change":0.31,"pct_chg":1.2773,"vol":663515.29,"amount":1619823.489},
    {"ts_code":"600887.SH","trade_date":"20260626","open":24.61,"high":24.68,"low":24.27,"close":24.27,"pre_close":24.61,"change":-0.34,"pct_chg":-1.3816,"vol":485383.6,"amount":1185934.672},
    {"ts_code":"600887.SH","trade_date":"20260625","open":24.4,"high":25.04,"low":24.28,"close":24.61,"pre_close":24.4,"change":0.21,"pct_chg":0.8607,"vol":733145.79,"amount":1804917.729},
    {"ts_code":"600887.SH","trade_date":"20260624","open":24.71,"high":25.05,"low":24.36,"close":24.4,"pre_close":24.46,"change":-0.06,"pct_chg":-0.2453,"vol":669087.59,"amount":1649161.03},
    {"ts_code":"600887.SH","trade_date":"20260623","open":24.56,"high":25.11,"low":24.4,"close":24.46,"pre_close":24.63,"change":-0.17,"pct_chg":-0.6902,"vol":549122.82,"amount":1356153.75},
    {"ts_code":"600887.SH","trade_date":"20260622","open":24.2,"high":24.83,"low":23.86,"close":24.63,"pre_close":24.26,"change":0.37,"pct_chg":1.5251,"vol":775685.58,"amount":1887393.623},
    {"ts_code":"600887.SH","trade_date":"20260618","open":24.67,"high":24.72,"low":24.21,"close":24.26,"pre_close":24.67,"change":-0.41,"pct_chg":-1.6619,"vol":505503.12,"amount":1232827.198},
    {"ts_code":"600887.SH","trade_date":"20260617","open":24.85,"high":24.89,"low":24.51,"close":24.67,"pre_close":24.8,"change":-0.13,"pct_chg":-0.5242,"vol":535185.24,"amount":1319337.173},
    {"ts_code":"600887.SH","trade_date":"20260616","open":25.33,"high":25.33,"low":24.6,"close":24.8,"pre_close":25.41,"change":-0.61,"pct_chg":-2.4006,"vol":730116.0,"amount":1820681.157},
    {"ts_code":"600887.SH","trade_date":"20260615","open":25.75,"high":25.82,"low":25.26,"close":25.41,"pre_close":25.71,"change":-0.3,"pct_chg":-1.1669,"vol":612747.6,"amount":1561234.414},
    {"ts_code":"600887.SH","trade_date":"20260612","open":25.64,"high":25.96,"low":25.45,"close":25.71,"pre_close":25.61,"change":0.1,"pct_chg":0.3905,"vol":606878.81,"amount":1557689.694},
    {"ts_code":"600887.SH","trade_date":"20260611","open":25.55,"high":25.79,"low":25.37,"close":25.61,"pre_close":25.58,"change":0.03,"pct_chg":0.1173,"vol":378921.62,"amount":969593.727},
    {"ts_code":"600887.SH","trade_date":"20260610","open":25.03,"high":25.64,"low":24.98,"close":25.58,"pre_close":25.12,"change":0.46,"pct_chg":1.8312,"vol":484110.41,"amount":1229111.249},
    {"ts_code":"600887.SH","trade_date":"20260609","open":25.37,"high":25.7,"low":25.02,"close":25.12,"pre_close":25.37,"change":-0.25,"pct_chg":-0.9854,"vol":583312.43,"amount":1473213.378},
    {"ts_code":"600887.SH","trade_date":"20260608","open":25.76,"high":26.1,"low":25.18,"close":25.37,"pre_close":25.67,"change":-0.3,"pct_chg":-1.1687,"vol":575758.26,"amount":1470714.333},
    {"ts_code":"600887.SH","trade_date":"20260605","open":25.72,"high":26.25,"low":25.59,"close":25.67,"pre_close":25.66,"change":0.01,"pct_chg":0.039,"vol":616359.07,"amount":1592799.01},
    {"ts_code":"600887.SH","trade_date":"20260604","open":26.61,"high":26.85,"low":26.47,"close":26.56,"pre_close":26.72,"change":-0.16,"pct_chg":-0.5988,"vol":474756.37,"amount":1263704.666},
    {"ts_code":"600887.SH","trade_date":"20260603","open":26.81,"high":26.93,"low":26.34,"close":26.72,"pre_close":26.86,"change":-0.14,"pct_chg":-0.5212,"vol":634925.69,"amount":1689005.116},
    {"ts_code":"600887.SH","trade_date":"20260602","open":26.95,"high":27.12,"low":26.8,"close":26.86,"pre_close":27.0,"change":-0.14,"pct_chg":-0.5185,"vol":415202.19,"amount":1117322.837},
    {"ts_code":"600887.SH","trade_date":"20260601","open":26.7,"high":27.03,"low":26.58,"close":27.0,"pre_close":26.92,"change":0.08,"pct_chg":0.2972,"vol":684616.66,"amount":1839883.296},
    {"ts_code":"600887.SH","trade_date":"20260529","open":25.9,"high":27.08,"low":25.9,"close":26.92,"pre_close":26.0,"change":0.92,"pct_chg":3.5385,"vol":715261.37,"amount":1906594.603},
    {"ts_code":"600887.SH","trade_date":"20260528","open":26.5,"high":26.68,"low":25.94,"close":26.0,"pre_close":26.62,"change":-0.62,"pct_chg":-2.3291,"vol":631666.86,"amount":1651764.278},
    {"ts_code":"600887.SH","trade_date":"20260527","open":26.43,"high":26.99,"low":26.07,"close":26.62,"pre_close":26.58,"change":0.04,"pct_chg":0.1505,"vol":578239.25,"amount":1532144.356},
    {"ts_code":"600887.SH","trade_date":"20260526","open":26.3,"high":26.67,"low":26.15,"close":26.58,"pre_close":26.27,"change":0.31,"pct_chg":1.1801,"vol":479542.15,"amount":1269389.378},
    {"ts_code":"600887.SH","trade_date":"20260525","open":26.21,"high":26.57,"low":26.01,"close":26.27,"pre_close":26.2,"change":0.07,"pct_chg":0.2672,"vol":459181.61,"amount":1208937.241},
    {"ts_code":"600887.SH","trade_date":"20260522","open":26.95,"high":26.95,"low":26.19,"close":26.2,"pre_close":26.76,"change":-0.56,"pct_chg":-2.0927,"vol":640561.63,"amount":1691599.954},
    {"ts_code":"600887.SH","trade_date":"20260521","open":27.12,"high":27.31,"low":26.7,"close":26.76,"pre_close":27.12,"change":-0.36,"pct_chg":-1.3274,"vol":545917.47,"amount":1473216.946},
    {"ts_code":"600887.SH","trade_date":"20260520","open":27.25,"high":27.38,"low":27.04,"close":27.12,"pre_close":27.23,"change":-0.11,"pct_chg":-0.404,"vol":361020.64,"amount":981928.663},
    {"ts_code":"600887.SH","trade_date":"20260519","open":27.29,"high":27.6,"low":27.17,"close":27.23,"pre_close":27.29,"change":-0.06,"pct_chg":-0.2199,"vol":397583.04,"amount":1086660.19},
    {"ts_code":"600887.SH","trade_date":"20260518","open":27.53,"high":27.65,"low":27.1,"close":27.29,"pre_close":27.61,"change":-0.32,"pct_chg":-1.159,"vol":431388.94,"amount":1176318.731},
    {"ts_code":"600887.SH","trade_date":"20260515","open":27.77,"high":27.99,"low":27.49,"close":27.61,"pre_close":27.78,"change":-0.17,"pct_chg":-0.612,"vol":483371.65,"amount":1340536.763},
    {"ts_code":"600887.SH","trade_date":"20260514","open":27.83,"high":27.97,"low":27.56,"close":27.78,"pre_close":27.9,"change":-0.12,"pct_chg":-0.4301,"vol":505209.82,"amount":1401655.122},
    {"ts_code":"600887.SH","trade_date":"20260513","open":28.13,"high":28.22,"low":27.66,"close":27.9,"pre_close":28.01,"change":-0.11,"pct_chg":-0.3927,"vol":616711.13,"amount":1716424.481},
    {"ts_code":"600887.SH","trade_date":"20260512","open":28.0,"high":28.4,"low":27.89,"close":28.01,"pre_close":28.06,"change":-0.05,"pct_chg":-0.1782,"vol":739490.47,"amount":2075872.034},
    {"ts_code":"600887.SH","trade_date":"20260511","open":27.7,"high":28.2,"low":27.36,"close":28.06,"pre_close":27.52,"change":0.54,"pct_chg":1.9622,"vol":895348.94,"amount":2500080.896},
    {"ts_code":"600887.SH","trade_date":"20260508","open":27.53,"high":27.74,"low":27.39,"close":27.52,"pre_close":27.53,"change":-0.01,"pct_chg":-0.0363,"vol":569714.79,"amount":1570843.72},
    {"ts_code":"600887.SH","trade_date":"20260507","open":27.44,"high":27.83,"low":27.28,"close":27.53,"pre_close":27.45,"change":0.08,"pct_chg":0.2914,"vol":708829.73,"amount":1957673.075},
    {"ts_code":"600887.SH","trade_date":"20260506","open":27.45,"high":27.49,"low":27.01,"close":27.45,"pre_close":27.46,"change":-0.01,"pct_chg":-0.0364,"vol":1051342.9,"amount":2869648.528},
    {"ts_code":"600887.SH","trade_date":"20260430","open":27.5,"high":27.99,"low":27.11,"close":27.46,"pre_close":26.57,"change":0.89,"pct_chg":3.3496,"vol":2144097.38,"amount":5900016.973},
    {"ts_code":"600887.SH","trade_date":"20260429","open":25.55,"high":26.59,"low":25.5,"close":26.57,"pre_close":25.49,"change":1.08,"pct_chg":4.237,"vol":1261714.9,"amount":3306441.892},
    {"ts_code":"600887.SH","trade_date":"20260428","open":25.21,"high":25.79,"low":25.18,"close":25.49,"pre_close":25.25,"change":0.24,"pct_chg":0.9505,"vol":817282.97,"amount":2081892.317},
    {"ts_code":"600887.SH","trade_date":"20260427","open":25.24,"high":25.44,"low":25.15,"close":25.25,"pre_close":25.25,"change":0.0,"pct_chg":0.0,"vol":432063.86,"amount":1091147.141},
    {"ts_code":"600887.SH","trade_date":"20260424","open":25.23,"high":25.39,"low":25.15,"close":25.25,"pre_close":25.27,"change":-0.02,"pct_chg":-0.0791,"vol":389217.94,"amount":982873.447},
    {"ts_code":"600887.SH","trade_date":"20260423","open":25.3,"high":25.43,"low":25.13,"close":25.27,"pre_close":25.29,"change":-0.02,"pct_chg":-0.0791,"vol":407311.59,"amount":1029788.345},
    {"ts_code":"600887.SH","trade_date":"20260422","open":25.58,"high":25.58,"low":25.28,"close":25.29,"pre_close":25.56,"change":-0.27,"pct_chg":-1.0563,"vol":444459.29,"amount":1127169.284},
    {"ts_code":"600887.SH","trade_date":"20260421","open":25.5,"high":25.69,"low":25.42,"close":25.56,"pre_close":25.51,"change":0.05,"pct_chg":0.196,"vol":322193.41,"amount":822585.093},
    {"ts_code":"600887.SH","trade_date":"20260420","open":25.35,"high":25.57,"low":25.28,"close":25.51,"pre_close":25.39,"change":0.12,"pct_chg":0.4726,"vol":397331.88,"amount":1010952.939},
    {"ts_code":"600887.SH","trade_date":"20260417","open":25.59,"high":25.6,"low":25.32,"close":25.39,"pre_close":25.6,"change":-0.21,"pct_chg":-0.8203,"vol":503403.76,"amount":1278607.423},
    {"ts_code":"600887.SH","trade_date":"20260416","open":25.7,"high":25.73,"low":25.56,"close":25.6,"pre_close":25.69,"change":-0.09,"pct_chg":-0.3503,"vol":465138.5,"amount":1190913.072},
    {"ts_code":"600887.SH","trade_date":"20260415","open":25.97,"high":26.07,"low":25.69,"close":25.69,"pre_close":25.99,"change":-0.3,"pct_chg":-1.1543,"vol":479381.94,"amount":1236094.369},
    {"ts_code":"600887.SH","trade_date":"20260414","open":26.01,"high":26.24,"low":25.88,"close":25.99,"pre_close":25.96,"change":0.03,"pct_chg":0.1156,"vol":235528.54,"amount":612034.745},
    {"ts_code":"600887.SH","trade_date":"20260413","open":26.09,"high":26.1,"low":25.84,"close":25.96,"pre_close":26.14,"change":-0.18,"pct_chg":-0.6886,"vol":302057.36,"amount":783868.153},
    {"ts_code":"600887.SH","trade_date":"20260410","open":26.25,"high":26.48,"low":26.1,"close":26.14,"pre_close":26.12,"change":0.02,"pct_chg":0.0766,"vol":280610.54,"amount":738245.207},
    {"ts_code":"600887.SH","trade_date":"20260409","open":26.35,"high":26.36,"low":26.02,"close":26.12,"pre_close":26.44,"change":-0.32,"pct_chg":-1.2103,"vol":262384.08,"amount":685638.151},
    {"ts_code":"600887.SH","trade_date":"20260408","open":26.38,"high":26.55,"low":26.32,"close":26.44,"pre_close":26.33,"change":0.11,"pct_chg":0.4178,"vol":437845.33,"amount":1158284.739},
    {"ts_code":"600887.SH","trade_date":"20260407","open":26.31,"high":26.42,"low":26.08,"close":26.33,"pre_close":26.31,"change":0.02,"pct_chg":0.076,"vol":268232.2,"amount":704556.531},
    {"ts_code":"600887.SH","trade_date":"20260403","open":26.38,"high":26.43,"low":26.15,"close":26.31,"pre_close":26.43,"change":-0.12,"pct_chg":-0.454,"vol":223320.65,"amount":587515.505},
    {"ts_code":"600887.SH","trade_date":"20260402","open":26.31,"high":26.5,"low":26.23,"close":26.43,"pre_close":26.33,"change":0.1,"pct_chg":0.3798,"vol":247444.08,"amount":652316.984},
    {"ts_code":"600887.SH","trade_date":"20260401","open":26.58,"high":26.58,"low":26.18,"close":26.33,"pre_close":26.35,"change":-0.02,"pct_chg":-0.0759,"vol":291632.43,"amount":768508.691},
    {"ts_code":"600887.SH","trade_date":"20260331","open":26.48,"high":26.73,"low":26.32,"close":26.35,"pre_close":26.4,"change":-0.05,"pct_chg":-0.1894,"vol":259876.79,"amount":688545.191},
    {"ts_code":"600887.SH","trade_date":"20260330","open":25.97,"high":26.47,"low":25.93,"close":26.4,"pre_close":26.16,"change":0.24,"pct_chg":0.9174,"vol":319601.99,"amount":841098.941},
    {"ts_code":"600887.SH","trade_date":"20260327","open":25.83,"high":26.23,"low":25.81,"close":26.16,"pre_close":25.95,"change":0.21,"pct_chg":0.8092,"vol":266420.24,"amount":696018.781},
    {"ts_code":"600887.SH","trade_date":"20260326","open":25.81,"high":26.25,"low":25.8,"close":25.95,"pre_close":25.88,"change":0.07,"pct_chg":0.2705,"vol":290238.26,"amount":755975.233},
    {"ts_code":"600887.SH","trade_date":"20260325","open":25.83,"high":25.97,"low":25.73,"close":25.88,"pre_close":25.7,"change":0.18,"pct_chg":0.7004,"vol":264519.62,"amount":684607.12},
    {"ts_code":"600887.SH","trade_date":"20260324","open":25.6,"high":25.73,"low":25.41,"close":25.7,"pre_close":25.49,"change":0.21,"pct_chg":0.8239,"vol":389076.78,"amount":996535.348},
    {"ts_code":"600887.SH","trade_date":"20260323","open":26.2,"high":26.23,"low":25.35,"close":25.49,"pre_close":26.39,"change":-0.9,"pct_chg":-3.4104,"vol":640461.88,"amount":1645709.736},
    {"ts_code":"600887.SH","trade_date":"20260320","open":26.45,"high":26.71,"low":26.39,"close":26.39,"pre_close":26.44,"change":-0.05,"pct_chg":-0.1891,"vol":348564.05,"amount":925873.983},
    {"ts_code":"600887.SH","trade_date":"20260319","open":26.66,"high":26.84,"low":26.4,"close":26.44,"pre_close":26.68,"change":-0.24,"pct_chg":-0.8996,"vol":368799.04,"amount":980549.684},
    {"ts_code":"600887.SH","trade_date":"20260318","open":27.03,"high":27.05,"low":26.51,"close":26.68,"pre_close":26.87,"change":-0.19,"pct_chg":-0.7071,"vol":453638.62,"amount":1210458.286},
    {"ts_code":"600887.SH","trade_date":"20260317","open":26.84,"high":27.05,"low":26.71,"close":26.87,"pre_close":26.84,"change":0.03,"pct_chg":0.1118,"vol":516425.64,"amount":1391233.598},
    {"ts_code":"600887.SH","trade_date":"20260316","open":26.71,"high":26.95,"low":26.65,"close":26.84,"pre_close":26.71,"change":0.13,"pct_chg":0.4867,"vol":388305.48,"amount":1042004.019},
    {"ts_code":"600887.SH","trade_date":"20260313","open":26.71,"high":26.94,"low":26.61,"close":26.71,"pre_close":26.71,"change":0.0,"pct_chg":0.0,"vol":494171.44,"amount":1324445.003},
    {"ts_code":"600887.SH","trade_date":"20260312","open":26.43,"high":26.76,"low":26.28,"close":26.71,"pre_close":26.44,"change":0.27,"pct_chg":1.0212,"vol":532049.61,"amount":1412913.344},
    {"ts_code":"600887.SH","trade_date":"20260311","open":26.46,"high":26.46,"low":26.23,"close":26.44,"pre_close":26.4,"change":0.04,"pct_chg":0.1515,"vol":301538.77,"amount":795350.78},
    {"ts_code":"600887.SH","trade_date":"20260310","open":26.28,"high":26.54,"low":26.25,"close":26.4,"pre_close":26.28,"change":0.12,"pct_chg":0.4566,"vol":485923.56,"amount":1284899.026},
    {"ts_code":"600887.SH","trade_date":"20260309","open":26.04,"high":26.4,"low":25.85,"close":26.28,"pre_close":26.21,"change":0.07,"pct_chg":0.2671,"vol":578504.58,"amount":1512953.329},
    {"ts_code":"600887.SH","trade_date":"20260306","open":25.62,"high":26.28,"low":25.58,"close":26.21,"pre_close":25.67,"change":0.54,"pct_chg":2.1036,"vol":548649.24,"amount":1428036.788},
    {"ts_code":"600887.SH","trade_date":"20260305","open":25.69,"high":26.04,"low":25.61,"close":25.67,"pre_close":25.62,"change":0.05,"pct_chg":0.1952,"vol":354656.51,"amount":914400.192},
    {"ts_code":"600887.SH","trade_date":"20260304","open":25.81,"high":25.85,"low":25.45,"close":25.62,"pre_close":25.93,"change":-0.31,"pct_chg":-1.1955,"vol":525141.87,"amount":1345636.228},
    {"ts_code":"600887.SH","trade_date":"20260303","open":26.0,"high":26.26,"low":25.78,"close":25.93,"pre_close":26.0,"change":-0.07,"pct_chg":-0.2692,"vol":552891.65,"amount":1436052.974},
    {"ts_code":"600887.SH","trade_date":"20260302","open":25.95,"high":26.14,"low":25.66,"close":26.0,"pre_close":26.08,"change":-0.08,"pct_chg":-0.3067,"vol":577905.63,"amount":1496480.387},
    {"ts_code":"600887.SH","trade_date":"20260227","open":26.13,"high":26.26,"low":26.01,"close":26.08,"pre_close":26.12,"change":-0.04,"pct_chg":-0.1531,"vol":395340.29,"amount":1033896.673},
    {"ts_code":"600887.SH","trade_date":"20260226","open":26.31,"high":26.35,"low":26.08,"close":26.12,"pre_close":26.3,"change":-0.18,"pct_chg":-0.6844,"vol":444622.87,"amount":1162878.489},
    {"ts_code":"600887.SH","trade_date":"20260225","open":26.37,"high":26.65,"low":26.22,"close":26.3,"pre_close":26.37,"change":-0.07,"pct_chg":-0.2655,"vol":484888.82,"amount":1280621.826},
    {"ts_code":"600887.SH","trade_date":"20260224","open":26.61,"high":26.63,"low":26.16,"close":26.37,"pre_close":26.48,"change":-0.11,"pct_chg":-0.4154,"vol":435220.38,"amount":1146178.66},
    {"ts_code":"600887.SH","trade_date":"20260213","open":26.7,"high":26.7,"low":26.46,"close":26.48,"pre_close":26.61,"change":-0.13,"pct_chg":-0.4885,"vol":334695.0,"amount":888806.487},
    {"ts_code":"600887.SH","trade_date":"20260212","open":26.84,"high":26.86,"low":26.56,"close":26.61,"pre_close":26.87,"change":-0.26,"pct_chg":-0.9676,"vol":344479.75,"amount":917793.226},
    {"ts_code":"600887.SH","trade_date":"20260211","open":26.8,"high":26.98,"low":26.69,"close":26.87,"pre_close":26.75,"change":0.12,"pct_chg":0.4486,"vol":366051.57,"amount":982348.099},
    {"ts_code":"600887.SH","trade_date":"20260210","open":27.03,"high":27.03,"low":26.64,"close":26.75,"pre_close":27.08,"change":-0.33,"pct_chg":-1.2186,"vol":564764.85,"amount":1510541.822},
    {"ts_code":"600887.SH","trade_date":"20260209","open":27.0,"high":27.28,"low":26.98,"close":27.08,"pre_close":27.08,"change":0.0,"pct_chg":0.0,"vol":431552.73,"amount":1168224.785},
    {"ts_code":"600887.SH","trade_date":"20260206","open":27.24,"high":27.48,"low":27.0,"close":27.08,"pre_close":27.21,"change":-0.13,"pct_chg":-0.4778,"vol":567769.04,"amount":1541138.984},
    {"ts_code":"600887.SH","trade_date":"20260205","open":27.1,"high":27.35,"low":26.95,"close":27.21,"pre_close":27.01,"change":0.2,"pct_chg":0.7405,"vol":675579.38,"amount":1835439.251},
    {"ts_code":"600887.SH","trade_date":"20260204","open":26.64,"high":27.04,"low":26.61,"close":27.01,"pre_close":26.6,"change":0.41,"pct_chg":1.5414,"vol":609688.29,"amount":1638579.098},
    {"ts_code":"600887.SH","trade_date":"20260203","open":26.42,"high":26.73,"low":26.37,"close":26.6,"pre_close":26.45,"change":0.15,"pct_chg":0.5671,"vol":571566.33,"amount":1517772.06},
    {"ts_code":"600887.SH","trade_date":"20260202","open":26.67,"high":26.84,"low":26.36,"close":26.45,"pre_close":26.34,"change":0.11,"pct_chg":0.4176,"vol":741014.17,"amount":1975230.961},
    {"ts_code":"600887.SH","trade_date":"20260130","open":26.7,"high":26.8,"low":26.33,"close":26.34,"pre_close":26.83,"change":-0.49,"pct_chg":-1.8263,"vol":777336.95,"amount":2060727.989},
    {"ts_code":"600887.SH","trade_date":"20260129","open":26.1,"high":26.84,"low":25.8,"close":26.83,"pre_close":26.14,"change":0.69,"pct_chg":2.6396,"vol":1458164.33,"amount":3824110.006},
    {"ts_code":"600887.SH","trade_date":"20260128","open":26.43,"high":26.48,"low":26.08,"close":26.14,"pre_close":26.37,"change":-0.23,"pct_chg":-0.8722,"vol":816135.72,"amount":2139880.003},
    {"ts_code":"600887.SH","trade_date":"20260127","open":26.69,"high":26.78,"low":26.37,"close":26.37,"pre_close":26.68,"change":-0.31,"pct_chg":-1.1619,"vol":678267.3,"amount":1798337.886},
    {"ts_code":"600887.SH","trade_date":"20260126","open":26.83,"high":26.98,"low":26.52,"close":26.68,"pre_close":26.82,"change":-0.14,"pct_chg":-0.522,"vol":760417.26,"amount":2032739.797},
    {"ts_code":"600887.SH","trade_date":"20260123","open":26.81,"high":26.99,"low":26.75,"close":26.82,"pre_close":26.81,"change":0.01,"pct_chg":0.0373,"vol":656849.76,"amount":1765509.067},
    {"ts_code":"600887.SH","trade_date":"20260122","open":26.84,"high":27.06,"low":26.74,"close":26.81,"pre_close":26.84,"change":-0.03,"pct_chg":-0.1118,"vol":538626.57,"amount":1447590.671},
    {"ts_code":"600887.SH","trade_date":"20260121","open":27.25,"high":27.25,"low":26.77,"close":26.84,"pre_close":27.18,"change":-0.34,"pct_chg":-1.2509,"vol":719789.43,"amount":1940325.232},
    {"ts_code":"600887.SH","trade_date":"20260120","open":27.12,"high":27.26,"low":26.95,"close":27.18,"pre_close":27.09,"change":0.09,"pct_chg":0.3322,"vol":480489.13,"amount":1303433.704},
    {"ts_code":"600887.SH","trade_date":"20260119","open":27.0,"high":27.18,"low":26.96,"close":27.09,"pre_close":26.97,"change":0.12,"pct_chg":0.4449,"vol":458355.09,"amount":1240407.442},
    {"ts_code":"600887.SH","trade_date":"20260116","open":27.34,"high":27.34,"low":26.92,"close":26.97,"pre_close":27.22,"change":-0.25,"pct_chg":-0.9184,"vol":588316.24,"amount":1594121.537},
    {"ts_code":"600887.SH","trade_date":"20260115","open":27.4,"high":27.58,"low":27.18,"close":27.22,"pre_close":27.4,"change":-0.18,"pct_chg":-0.6569,"vol":483085.85,"amount":1320320.585},
    {"ts_code":"600887.SH","trade_date":"20260114","open":27.51,"high":27.66,"low":27.35,"close":27.4,"pre_close":27.53,"change":-0.13,"pct_chg":-0.4722,"vol":614521.93,"amount":1688191.48},
    {"ts_code":"600887.SH","trade_date":"20260113","open":27.74,"high":28.09,"low":27.44,"close":27.53,"pre_close":27.74,"change":-0.21,"pct_chg":-0.757,"vol":557667.02,"amount":1547123.552},
    {"ts_code":"600887.SH","trade_date":"20260112","open":27.68,"high":27.78,"low":27.41,"close":27.74,"pre_close":27.68,"change":0.06,"pct_chg":0.2168,"vol":610974.22,"amount":1685870.213},
    {"ts_code":"600887.SH","trade_date":"20260109","open":27.21,"high":27.7,"low":27.2,"close":27.68,"pre_close":27.26,"change":0.42,"pct_chg":1.5407,"vol":872358.6,"amount":2399189.017},
    {"ts_code":"600887.SH","trade_date":"20260108","open":27.9,"high":27.9,"low":27.11,"close":27.26,"pre_close":28.42,"change":-1.16,"pct_chg":-4.0816,"vol":1635151.81,"amount":4471049.1},
    {"ts_code":"600887.SH","trade_date":"20260107","open":28.65,"high":28.78,"low":28.38,"close":28.42,"pre_close":28.62,"change":-0.2,"pct_chg":-0.6988,"vol":409209.06,"amount":1166508.273},
    {"ts_code":"600887.SH","trade_date":"20260106","open":28.55,"high":28.69,"low":28.21,"close":28.62,"pre_close":28.61,"change":0.01,"pct_chg":0.035,"vol":495809.78,"amount":1413869.797},
    {"ts_code":"600887.SH","trade_date":"20260105","open":28.6,"high":28.91,"low":28.55,"close":28.61,"pre_close":28.6,"change":0.01,"pct_chg":0.035,"vol":496361.37,"amount":1423103.319},
    {"ts_code":"600887.SH","trade_date":"20251231","open":28.77,"high":28.88,"low":28.56,"close":28.6,"pre_close":28.69,"change":-0.09,"pct_chg":-0.3137,"vol":266727.02,"amount":764372.855},
    {"ts_code":"600887.SH","trade_date":"20251230","open":28.76,"high":28.9,"low":28.61,"close":28.69,"pre_close":28.87,"change":-0.18,"pct_chg":-0.6235,"vol":390498.03,"amount":1121585.94},
    {"ts_code":"600887.SH","trade_date":"20251229","open":29.09,"high":29.11,"low":28.67,"close":28.87,"pre_close":29.1,"change":-0.23,"pct_chg":-0.7904,"vol":379126.27,"amount":1094914.598},
    {"ts_code":"600887.SH","trade_date":"20251226","open":29.26,"high":29.35,"low":28.93,"close":29.1,"pre_close":29.2,"change":-0.1,"pct_chg":-0.3425,"vol":291279.82,"amount":847358.126},
    {"ts_code":"600887.SH","trade_date":"20251225","open":28.9,"high":29.3,"low":28.83,"close":29.2,"pre_close":28.88,"change":0.32,"pct_chg":1.108,"vol":331841.55,"amount":966379.471},
    {"ts_code":"600887.SH","trade_date":"20251224","open":28.81,"high":28.99,"low":28.7,"close":28.88,"pre_close":28.93,"change":-0.05,"pct_chg":-0.1728,"vol":296213.04,"amount":854061.69},
    {"ts_code":"600887.SH","trade_date":"20251223","open":29.31,"high":29.5,"low":28.81,"close":28.93,"pre_close":29.1,"change":-0.17,"pct_chg":-0.5842,"vol":427338.4,"amount":1242898.335},
    {"ts_code":"600887.SH","trade_date":"20251222","open":29.05,"high":29.32,"low":28.93,"close":29.1,"pre_close":29.18,"change":-0.08,"pct_chg":-0.2742,"vol":401872.51,"amount":1170602.861},
    {"ts_code":"600887.SH","trade_date":"20251219","open":28.8,"high":29.24,"low":28.77,"close":29.18,"pre_close":28.97,"change":0.21,"pct_chg":0.7249,"vol":357629.05,"amount":1040349.264},
    {"ts_code":"600887.SH","trade_date":"20251218","open":28.85,"high":29.09,"low":28.68,"close":28.97,"pre_close":28.85,"change":0.12,"pct_chg":0.4159,"vol":278825.52,"amount":806884.69},
    {"ts_code":"600887.SH","trade_date":"20251217","open":28.58,"high":29.09,"low":28.38,"close":28.85,"pre_close":28.47,"change":0.38,"pct_chg":1.3347,"vol":457885.58,"amount":1320877.994},
    {"ts_code":"600887.SH","trade_date":"20251216","open":28.9,"high":29.14,"low":28.77,"close":28.95,"pre_close":28.83,"change":0.12,"pct_chg":0.4162,"vol":446640.43,"amount":1292306.812},
    {"ts_code":"600887.SH","trade_date":"20251215","open":28.7,"high":29.02,"low":28.65,"close":28.83,"pre_close":28.7,"change":0.13,"pct_chg":0.453,"vol":331267.5,"amount":957316.155},
    {"ts_code":"600887.SH","trade_date":"20251212","open":28.54,"high":28.76,"low":28.33,"close":28.7,"pre_close":28.39,"change":0.31,"pct_chg":1.0919,"vol":488631.29,"amount":1397348.34},
    {"ts_code":"600887.SH","trade_date":"20251211","open":28.55,"high":28.62,"low":28.36,"close":28.39,"pre_close":28.56,"change":-0.17,"pct_chg":-0.5952,"vol":266282.98,"amount":758252.704},
    {"ts_code":"600887.SH","trade_date":"20251210","open":28.7,"high":28.85,"low":28.46,"close":28.56,"pre_close":28.76,"change":-0.2,"pct_chg":-0.6954,"vol":260075.81,"amount":744375.878},
    {"ts_code":"600887.SH","trade_date":"20251209","open":28.97,"high":29.05,"low":28.64,"close":28.76,"pre_close":28.84,"change":-0.08,"pct_chg":-0.2774,"vol":318507.97,"amount":917781.063},
    {"ts_code":"600887.SH","trade_date":"20251208","open":28.95,"high":29.15,"low":28.73,"close":28.84,"pre_close":28.92,"change":-0.08,"pct_chg":-0.2766,"vol":331706.57,"amount":957402.046},
    {"ts_code":"600887.SH","trade_date":"20251205","open":28.99,"high":29.16,"low":28.8,"close":28.92,"pre_close":28.99,"change":-0.07,"pct_chg":-0.2415,"vol":263630.35,"amount":763707.568},
    {"ts_code":"600887.SH","trade_date":"20251204","open":29.18,"high":29.28,"low":28.94,"close":28.99,"pre_close":29.27,"change":-0.28,"pct_chg":-0.9566,"vol":270942.45,"amount":787269.79},
    {"ts_code":"600887.SH","trade_date":"20251203","open":29.3,"high":29.43,"low":29.11,"close":29.27,"pre_close":29.35,"change":-0.08,"pct_chg":-0.2726,"vol":263715.44,"amount":772760.507},
    {"ts_code":"600887.SH","trade_date":"20251202","open":29.47,"high":29.5,"low":29.21,"close":29.35,"pre_close":29.43,"change":-0.08,"pct_chg":-0.2718,"vol":244418.02,"amount":716507.514},
    {"ts_code":"600887.SH","trade_date":"20251201","open":29.4,"high":29.56,"low":29.08,"close":29.43,"pre_close":29.38,"change":0.05,"pct_chg":0.1702,"vol":379120.06,"amount":1111191.935},
    {"ts_code":"600887.SH","trade_date":"20251128","open":29.05,"high":29.46,"low":28.97,"close":29.38,"pre_close":29.05,"change":0.33,"pct_chg":1.136,"vol":357201.14,"amount":1046624.929},
    {"ts_code":"600887.SH","trade_date":"20251127","open":29.2,"high":29.21,"low":28.92,"close":29.05,"pre_close":29.18,"change":-0.13,"pct_chg":-0.4455,"vol":223025.78,"amount":648115.983},
    {"ts_code":"600887.SH","trade_date":"20251126","open":29.1,"high":29.35,"low":28.88,"close":29.18,"pre_close":29.16,"change":0.02,"pct_chg":0.0686,"vol":287148.77,"amount":835332.535},
    {"ts_code":"600887.SH","trade_date":"20251125","open":28.92,"high":29.26,"low":28.75,"close":29.16,"pre_close":28.91,"change":0.25,"pct_chg":0.8648,"vol":407639.05,"amount":1184039.231},
    {"ts_code":"600887.SH","trade_date":"20251124","open":29.35,"high":29.39,"low":28.88,"close":28.91,"pre_close":29.1,"change":-0.19,"pct_chg":-0.6529,"vol":447780.82,"amount":1301705.714},
    {"ts_code":"600887.SH","trade_date":"20251121","open":29.21,"high":29.55,"low":29.0,"close":29.1,"pre_close":29.4,"change":-0.3,"pct_chg":-1.0204,"vol":599021.27,"amount":1749885.197},
    {"ts_code":"600887.SH","trade_date":"20251120","open":29.56,"high":29.77,"low":29.36,"close":29.4,"pre_close":29.58,"change":-0.18,"pct_chg":-0.6085,"vol":472371.88,"amount":1397017.933},
    {"ts_code":"600887.SH","trade_date":"20251119","open":29.59,"high":29.78,"low":29.39,"close":29.58,"pre_close":29.52,"change":0.06,"pct_chg":0.2033,"vol":630427.35,"amount":1869673.84},
    {"ts_code":"600887.SH","trade_date":"20251118","open":28.77,"high":29.58,"low":28.77,"close":29.52,"pre_close":28.57,"change":0.95,"pct_chg":3.3252,"vol":1303325.63,"amount":3831903.904},
    {"ts_code":"600887.SH","trade_date":"20251117","open":28.34,"high":28.62,"low":28.12,"close":28.57,"pre_close":28.35,"change":0.22,"pct_chg":0.776,"vol":374675.11,"amount":1064447.095},
    {"ts_code":"600887.SH","trade_date":"20251114","open":28.57,"high":28.83,"low":28.35,"close":28.35,"pre_close":28.58,"change":-0.23,"pct_chg":-0.8048,"vol":409201.48,"amount":1169548.535},
    {"ts_code":"600887.SH","trade_date":"20251113","open":28.45,"high":28.6,"low":28.21,"close":28.58,"pre_close":28.48,"change":0.1,"pct_chg":0.3511,"vol":510241.26,"amount":1449241.871},
    {"ts_code":"600887.SH","trade_date":"20251112","open":28.31,"high":28.75,"low":28.31,"close":28.48,"pre_close":28.35,"change":0.13,"pct_chg":0.4586,"vol":703551.3,"amount":2012767.204},
    {"ts_code":"600887.SH","trade_date":"20251111","open":28.28,"high":28.45,"low":28.08,"close":28.35,"pre_close":28.27,"change":0.08,"pct_chg":0.283,"vol":718208.31,"amount":2032845.997},
    {"ts_code":"600887.SH","trade_date":"20251110","open":27.3,"high":28.35,"low":27.29,"close":28.27,"pre_close":27.29,"change":0.98,"pct_chg":3.5911,"vol":1176002.7,"amount":3286290.067},
    {"ts_code":"600887.SH","trade_date":"20251107","open":27.22,"high":27.32,"low":27.17,"close":27.29,"pre_close":27.22,"change":0.07,"pct_chg":0.2572,"vol":260677.46,"amount":710309.225},
    {"ts_code":"600887.SH","trade_date":"20251106","open":27.2,"high":27.38,"low":27.13,"close":27.22,"pre_close":27.25,"change":-0.03,"pct_chg":-0.1101,"vol":314692.31,"amount":857926.375},
    {"ts_code":"600887.SH","trade_date":"20251105","open":27.01,"high":27.32,"low":26.94,"close":27.25,"pre_close":27.07,"change":0.18,"pct_chg":0.6649,"vol":449646.46,"amount":1221500.605},
    {"ts_code":"600887.SH","trade_date":"20251104","open":27.42,"high":27.42,"low":27.05,"close":27.07,"pre_close":27.45,"change":-0.38,"pct_chg":-1.3843,"vol":606485.8,"amount":1648553.616},
    {"ts_code":"600887.SH","trade_date":"20251103","open":27.41,"high":27.54,"low":27.23,"close":27.45,"pre_close":27.41,"change":0.04,"pct_chg":0.1459,"vol":428366.55,"amount":1173054.889},
    {"ts_code":"600887.SH","trade_date":"20251031","open":27.47,"high":27.61,"low":27.3,"close":27.41,"pre_close":27.36,"change":0.05,"pct_chg":0.1827,"vol":552298.49,"amount":1515292.122},
    {"ts_code":"600887.SH","trade_date":"20251030","open":27.15,"high":27.55,"low":27.12,"close":27.36,"pre_close":27.18,"change":0.18,"pct_chg":0.6623,"vol":621166.0,"amount":1701669.232},
    {"ts_code":"600887.SH","trade_date":"20251029","open":27.34,"high":27.34,"low":27.11,"close":27.18,"pre_close":27.27,"change":-0.09,"pct_chg":-0.33,"vol":363189.04,"amount":986076.668},
    {"ts_code":"600887.SH","trade_date":"20251028","open":27.42,"high":27.48,"low":27.23,"close":27.27,"pre_close":27.41,"change":-0.14,"pct_chg":-0.5108,"vol":305259.23,"amount":833796.923},
    {"ts_code":"600887.SH","trade_date":"20251027","open":27.3,"high":27.5,"low":27.28,"close":27.41,"pre_close":27.28,"change":0.13,"pct_chg":0.4765,"vol":378477.32,"amount":1037542.757},
    {"ts_code":"600887.SH","trade_date":"20251024","open":27.37,"high":27.5,"low":27.21,"close":27.28,"pre_close":27.37,"change":-0.09,"pct_chg":-0.3288,"vol":329615.97,"amount":900051.677},
    {"ts_code":"600887.SH","trade_date":"20251023","open":27.25,"high":27.42,"low":27.13,"close":27.37,"pre_close":27.25,"change":0.12,"pct_chg":0.4404,"vol":293717.09,"amount":800862.127},
    {"ts_code":"600887.SH","trade_date":"20251022","open":27.38,"high":27.46,"low":27.25,"close":27.25,"pre_close":27.41,"change":-0.16,"pct_chg":-0.5837,"vol":275168.14,"amount":752203.896},
    {"ts_code":"600887.SH","trade_date":"20251021","open":27.47,"high":27.55,"low":27.37,"close":27.41,"pre_close":27.47,"change":-0.06,"pct_chg":-0.2184,"vol":321257.61,"amount":881806.609},
    {"ts_code":"600887.SH","trade_date":"20251020","open":27.4,"high":27.63,"low":27.37,"close":27.47,"pre_close":27.35,"change":0.12,"pct_chg":0.4388,"vol":334886.42,"amount":920784.094},
    {"ts_code":"600887.SH","trade_date":"20251017","open":27.81,"high":27.96,"low":27.31,"close":27.35,"pre_close":27.81,"change":-0.46,"pct_chg":-1.6541,"vol":429520.0,"amount":1185057.313},
    {"ts_code":"600887.SH","trade_date":"20251016","open":27.66,"high":27.95,"low":27.61,"close":27.81,"pre_close":27.65,"change":0.16,"pct_chg":0.5787,"vol":368502.28,"amount":1024989.227},
    {"ts_code":"600887.SH","trade_date":"20251015","open":27.69,"high":27.79,"low":27.53,"close":27.65,"pre_close":27.69,"change":-0.04,"pct_chg":-0.1445,"vol":410816.15,"amount":1135528.973},
    {"ts_code":"600887.SH","trade_date":"20251014","open":27.59,"high":27.8,"low":27.36,"close":27.69,"pre_close":27.55,"change":0.14,"pct_chg":0.5082,"vol":584775.97,"amount":1615165.091},
    {"ts_code":"600887.SH","trade_date":"20251013","open":27.53,"high":27.7,"low":27.39,"close":27.55,"pre_close":27.75,"change":-0.2,"pct_chg":-0.7207,"vol":514528.62,"amount":1415780.494},
    {"ts_code":"600887.SH","trade_date":"20251010","open":27.54,"high":28.09,"low":27.46,"close":27.75,"pre_close":27.63,"change":0.12,"pct_chg":0.4343,"vol":588453.24,"amount":1637025.175},
    {"ts_code":"600887.SH","trade_date":"20251009","open":27.16,"high":27.63,"low":26.88,"close":27.63,"pre_close":27.28,"change":0.35,"pct_chg":1.283,"vol":711508.33,"amount":1939794.035},
    {"ts_code":"600887.SH","trade_date":"20250930","open":27.19,"high":27.43,"low":26.99,"close":27.28,"pre_close":27.19,"change":0.09,"pct_chg":0.331,"vol":505276.46,"amount":1377355.384},
    {"ts_code":"600887.SH","trade_date":"20250929","open":27.26,"high":27.35,"low":26.9,"close":27.19,"pre_close":27.26,"change":-0.07,"pct_chg":-0.2568,"vol":576591.18,"amount":1561655.553},
    {"ts_code":"600887.SH","trade_date":"20250926","open":26.92,"high":27.31,"low":26.8,"close":27.26,"pre_close":26.97,"change":0.29,"pct_chg":1.0753,"vol":638754.32,"amount":1731050.314},
    {"ts_code":"600887.SH","trade_date":"20250925","open":27.42,"high":27.43,"low":26.92,"close":26.97,"pre_close":27.41,"change":-0.44,"pct_chg":-1.6053,"vol":764024.76,"amount":2069611.137},
    {"ts_code":"600887.SH","trade_date":"20250924","open":27.3,"high":27.5,"low":27.26,"close":27.41,"pre_close":27.38,"change":0.03,"pct_chg":0.1096,"vol":345352.29,"amount":945671.196},
    {"ts_code":"600887.SH","trade_date":"20250923","open":27.55,"high":27.62,"low":27.21,"close":27.38,"pre_close":27.55,"change":-0.17,"pct_chg":-0.6171,"vol":449804.81,"amount":1231350.853},
    {"ts_code":"600887.SH","trade_date":"20250922","open":27.7,"high":27.79,"low":27.44,"close":27.55,"pre_close":27.7,"change":-0.15,"pct_chg":-0.5415,"vol":388684.6,"amount":1070082.302},
    {"ts_code":"600887.SH","trade_date":"20250919","open":27.73,"high":27.87,"low":27.58,"close":27.7,"pre_close":27.76,"change":-0.06,"pct_chg":-0.2161,"vol":433941.93,"amount":1202107.383},
    {"ts_code":"600887.SH","trade_date":"20250918","open":28.08,"high":28.13,"low":27.66,"close":27.76,"pre_close":28.08,"change":-0.32,"pct_chg":-1.1396,"vol":623234.97,"amount":1738475.538},
    {"ts_code":"600887.SH","trade_date":"20250917","open":28.14,"high":28.38,"low":27.96,"close":28.08,"pre_close":28.08,"change":0.0,"pct_chg":0.0,"vol":483243.44,"amount":1358295.385},
    {"ts_code":"600887.SH","trade_date":"20250916","open":28.25,"high":28.31,"low":27.84,"close":28.08,"pre_close":28.23,"change":-0.15,"pct_chg":-0.5313,"vol":708253.78,"amount":1986247.116},
    {"ts_code":"600887.SH","trade_date":"20250915","open":28.2,"high":28.52,"low":28.1,"close":28.23,"pre_close":28.25,"change":-0.02,"pct_chg":-0.0708,"vol":591253.23,"amount":1673303.638},
    {"ts_code":"600887.SH","trade_date":"20250912","open":28.74,"high":28.93,"low":28.15,"close":28.25,"pre_close":28.72,"change":-0.47,"pct_chg":-1.6365,"vol":784848.49,"amount":2239297.335},
    {"ts_code":"600887.SH","trade_date":"20250911","open":28.38,"high":28.75,"low":28.37,"close":28.72,"pre_close":28.43,"change":0.29,"pct_chg":1.02,"vol":607933.23,"amount":1738182.102},
    {"ts_code":"600887.SH","trade_date":"20250910","open":28.49,"high":28.58,"low":28.16,"close":28.43,"pre_close":28.56,"change":-0.13,"pct_chg":-0.4552,"vol":622490.23,"amount":1769059.129},
    {"ts_code":"600887.SH","trade_date":"20250909","open":28.23,"high":28.59,"low":28.12,"close":28.56,"pre_close":28.21,"change":0.35,"pct_chg":1.2407,"vol":732602.05,"amount":2076480.632},
    {"ts_code":"600887.SH","trade_date":"20250908","open":28.13,"high":28.49,"low":28.0,"close":28.21,"pre_close":28.18,"change":0.03,"pct_chg":0.1065,"vol":826355.77,"amount":2331231.868},
    {"ts_code":"600887.SH","trade_date":"20250905","open":28.17,"high":28.24,"low":27.82,"close":28.18,"pre_close":28.16,"change":0.02,"pct_chg":0.071,"vol":551549.98,"amount":1546833.903},
    {"ts_code":"600887.SH","trade_date":"20250904","open":27.91,"high":28.28,"low":27.8,"close":28.16,"pre_close":27.91,"change":0.25,"pct_chg":0.8957,"vol":946315.08,"amount":2654747.239},
    {"ts_code":"600887.SH","trade_date":"20250903","open":28.44,"high":28.55,"low":27.75,"close":27.91,"pre_close":28.26,"change":-0.35,"pct_chg":-1.2385,"vol":733050.98,"amount":2049453.849},
    {"ts_code":"600887.SH","trade_date":"20250902","open":28.35,"high":28.68,"low":28.2,"close":28.26,"pre_close":28.27,"change":-0.01,"pct_chg":-0.0354,"vol":678059.16,"amount":1923858.149},
    {"ts_code":"600887.SH","trade_date":"20250901","open":28.55,"high":28.92,"low":28.22,"close":28.27,"pre_close":28.57,"change":-0.3,"pct_chg":-1.0501,"vol":1054003.22,"amount":3002204.422},
    {"ts_code":"600887.SH","trade_date":"20250829","open":28.6,"high":29.5,"low":28.57,"close":28.57,"pre_close":27.69,"change":0.88,"pct_chg":3.178,"vol":2112944.73,"amount":6115499.114},
    {"ts_code":"600887.SH","trade_date":"20250828","open":27.79,"high":28.0,"low":27.42,"close":27.69,"pre_close":27.81,"change":-0.12,"pct_chg":-0.4315,"vol":563423.76,"amount":1562134.274},
    {"ts_code":"600887.SH","trade_date":"20250827","open":28.33,"high":28.36,"low":27.81,"close":27.81,"pre_close":28.33,"change":-0.52,"pct_chg":-1.8355,"vol":703930.22,"amount":1978250.629},
    {"ts_code":"600887.SH","trade_date":"20250826","open":28.09,"high":28.55,"low":28.02,"close":28.33,"pre_close":28.17,"change":0.16,"pct_chg":0.568,"vol":712899.38,"amount":2018922.787},
    {"ts_code":"600887.SH","trade_date":"20250825","open":27.76,"high":28.18,"low":27.74,"close":28.17,"pre_close":27.69,"change":0.48,"pct_chg":1.7335,"vol":888164.68,"amount":2482832.113},
    {"ts_code":"600887.SH","trade_date":"20250822","open":27.68,"high":27.7,"low":27.5,"close":27.69,"pre_close":27.64,"change":0.05,"pct_chg":0.1809,"vol":511270.44,"amount":1410588.146},
    {"ts_code":"600887.SH","trade_date":"20250821","open":27.48,"high":27.8,"low":27.4,"close":27.64,"pre_close":27.46,"change":0.18,"pct_chg":0.6555,"vol":699106.44,"amount":1931938.562},
    {"ts_code":"600887.SH","trade_date":"20250820","open":27.21,"high":27.51,"low":27.04,"close":27.46,"pre_close":27.21,"change":0.25,"pct_chg":0.9188,"vol":648817.17,"amount":1768582.0},
    {"ts_code":"600887.SH","trade_date":"20250819","open":27.35,"high":27.59,"low":27.2,"close":27.21,"pre_close":27.2,"change":0.01,"pct_chg":0.0368,"vol":772282.83,"amount":2113799.555},
    {"ts_code":"600887.SH","trade_date":"20250818","open":27.19,"high":27.55,"low":27.19,"close":27.2,"pre_close":27.16,"change":0.04,"pct_chg":0.1473,"vol":766025.83,"amount":2097560.156},
    {"ts_code":"600887.SH","trade_date":"20250815","open":27.2,"high":27.34,"low":26.99,"close":27.16,"pre_close":27.2,"change":-0.04,"pct_chg":-0.1471,"vol":593253.56,"amount":1611339.273},
    {"ts_code":"600887.SH","trade_date":"20250814","open":27.5,"high":27.57,"low":27.2,"close":27.2,"pre_close":27.48,"change":-0.28,"pct_chg":-1.0189,"vol":560989.15,"amount":1536616.438},
    {"ts_code":"600887.SH","trade_date":"20250813","open":27.52,"high":27.68,"low":27.42,"close":27.48,"pre_close":27.47,"change":0.01,"pct_chg":0.0364,"vol":435683.21,"amount":1197693.411},
    {"ts_code":"600887.SH","trade_date":"20250812","open":27.57,"high":27.72,"low":27.46,"close":27.47,"pre_close":27.57,"change":-0.1,"pct_chg":-0.3627,"vol":312211.46,"amount":860552.801},
    {"ts_code":"600887.SH","trade_date":"20250811","open":27.31,"high":27.6,"low":27.26,"close":27.57,"pre_close":27.3,"change":0.27,"pct_chg":0.989,"vol":392240.87,"amount":1077280.578},
    {"ts_code":"600887.SH","trade_date":"20250808","open":27.55,"high":27.55,"low":27.22,"close":27.3,"pre_close":27.57,"change":-0.27,"pct_chg":-0.9793,"vol":415787.37,"amount":1137063.976},
    {"ts_code":"600887.SH","trade_date":"20250807","open":27.59,"high":27.62,"low":27.46,"close":27.57,"pre_close":27.57,"change":0.0,"pct_chg":0.0,"vol":303772.95,"amount":837202.048},
    {"ts_code":"600887.SH","trade_date":"20250806","open":27.55,"high":27.69,"low":27.48,"close":27.57,"pre_close":27.55,"change":0.02,"pct_chg":0.0726,"vol":301320.08,"amount":830900.511},
    {"ts_code":"600887.SH","trade_date":"20250805","open":27.5,"high":27.55,"low":27.36,"close":27.55,"pre_close":27.48,"change":0.07,"pct_chg":0.2547,"vol":331782.23,"amount":911276.744},
    {"ts_code":"600887.SH","trade_date":"20250804","open":27.39,"high":27.49,"low":27.31,"close":27.48,"pre_close":27.51,"change":-0.03,"pct_chg":-0.1091,"vol":302352.99,"amount":828205.263},
    {"ts_code":"600887.SH","trade_date":"20250801","open":27.4,"high":27.55,"low":27.39,"close":27.51,"pre_close":27.41,"change":0.1,"pct_chg":0.3648,"vol":347353.58,"amount":954195.33},
    {"ts_code":"600887.SH","trade_date":"20250731","open":27.82,"high":27.82,"low":27.38,"close":27.41,"pre_close":27.88,"change":-0.47,"pct_chg":-1.6858,"vol":528616.7,"amount":1454311.357},
    {"ts_code":"600887.SH","trade_date":"20250730","open":27.39,"high":28.04,"low":27.38,"close":27.88,"pre_close":27.52,"change":0.36,"pct_chg":1.3081,"vol":781534.9,"amount":2173517.142},
    {"ts_code":"600887.SH","trade_date":"20250729","open":28.2,"high":28.39,"low":27.41,"close":27.52,"pre_close":27.73,"change":-0.21,"pct_chg":-0.7573,"vol":1188984.73,"amount":3291479.316},
    {"ts_code":"600887.SH","trade_date":"20250728","open":27.84,"high":27.95,"low":27.67,"close":27.73,"pre_close":27.83,"change":-0.1,"pct_chg":-0.3593,"vol":413144.84,"amount":1147320.824},
    {"ts_code":"600887.SH","trade_date":"20250725","open":28.2,"high":28.2,"low":27.81,"close":27.83,"pre_close":28.24,"change":-0.41,"pct_chg":-1.4518,"vol":443333.59,"amount":1239749.487},
    {"ts_code":"600887.SH","trade_date":"20250724","open":28.29,"high":28.34,"low":28.13,"close":28.24,"pre_close":28.29,"change":-0.05,"pct_chg":-0.1767,"vol":360050.76,"amount":1015874.052},
    {"ts_code":"600887.SH","trade_date":"20250723","open":28.42,"high":28.54,"low":28.25,"close":28.29,"pre_close":28.37,"change":-0.08,"pct_chg":-0.282,"vol":356905.39,"amount":1012987.185},
    {"ts_code":"600887.SH","trade_date":"20250722","open":28.22,"high":28.42,"low":28.12,"close":28.37,"pre_close":28.19,"change":0.18,"pct_chg":0.6385,"vol":386782.67,"amount":1095139.001},
    {"ts_code":"600887.SH","trade_date":"20250721","open":28.08,"high":28.21,"low":27.98,"close":28.19,"pre_close":28.07,"change":0.12,"pct_chg":0.4275,"vol":319424.51,"amount":897556.154},
    {"ts_code":"600887.SH","trade_date":"20250718","open":28.12,"high":28.23,"low":27.88,"close":28.07,"pre_close":28.1,"change":-0.03,"pct_chg":-0.1068,"vol":335659.27,"amount":940587.764},
    {"ts_code":"600887.SH","trade_date":"20250717","open":27.54,"high":28.16,"low":27.51,"close":28.1,"pre_close":27.52,"change":0.58,"pct_chg":2.1076,"vol":597872.88,"amount":1668797.44},
    {"ts_code":"600887.SH","trade_date":"20250716","open":27.39,"high":27.68,"low":27.38,"close":27.52,"pre_close":27.38,"change":0.14,"pct_chg":0.5113,"vol":337587.39,"amount":929227.537},
    {"ts_code":"600887.SH","trade_date":"20250715","open":27.49,"high":27.61,"low":27.26,"close":27.38,"pre_close":27.49,"change":-0.11,"pct_chg":-0.4001,"vol":364970.3,"amount":999638.872},
    {"ts_code":"600887.SH","trade_date":"20250714","open":27.7,"high":27.73,"low":27.44,"close":27.49,"pre_close":27.69,"change":-0.2,"pct_chg":-0.7223,"vol":449659.32,"amount":1237562.2},
    {"ts_code":"600887.SH","trade_date":"20250711","open":27.67,"high":27.95,"low":27.66,"close":27.69,"pre_close":27.66,"change":0.03,"pct_chg":0.1085,"vol":467555.74,"amount":1299838.473},
    {"ts_code":"600887.SH","trade_date":"20250710","open":27.69,"high":27.96,"low":27.64,"close":27.66,"pre_close":27.69,"change":-0.03,"pct_chg":-0.1083,"vol":373409.91,"amount":1036277.367},
    {"ts_code":"600887.SH","trade_date":"20250709","open":27.49,"high":27.99,"low":27.45,"close":27.69,"pre_close":27.49,"change":0.2,"pct_chg":0.7275,"vol":482633.05,"amount":1342833.361},
    {"ts_code":"600887.SH","trade_date":"20250708","open":27.35,"high":27.6,"low":27.27,"close":27.49,"pre_close":27.37,"change":0.12,"pct_chg":0.4384,"vol":312889.34,"amount":859934.216},
    {"ts_code":"600887.SH","trade_date":"20250707","open":27.75,"high":27.77,"low":27.19,"close":27.37,"pre_close":27.77,"change":-0.4,"pct_chg":-1.4404,"vol":534659.15,"amount":1465796.545},
    {"ts_code":"600887.SH","trade_date":"20250704","open":27.74,"high":27.9,"low":27.65,"close":27.77,"pre_close":27.75,"change":0.02,"pct_chg":0.0721,"vol":287417.05,"amount":798463.929},
    {"ts_code":"600887.SH","trade_date":"20250703","open":27.81,"high":27.83,"low":27.64,"close":27.75,"pre_close":27.81,"change":-0.06,"pct_chg":-0.2157,"vol":259288.28,"amount":718400.832},
    {"ts_code":"600887.SH","trade_date":"20250702","open":27.74,"high":27.92,"low":27.56,"close":27.81,"pre_close":27.67,"change":0.14,"pct_chg":0.506,"vol":467449.65,"amount":1297460.482},
    {"ts_code":"600887.SH","trade_date":"20250701","open":27.86,"high":27.86,"low":27.6,"close":27.67,"pre_close":27.88,"change":-0.21,"pct_chg":-0.7532,"vol":335129.38,"amount":927316.668},
    {"ts_code":"600887.SH","trade_date":"20250630","open":27.99,"high":28.04,"low":27.8,"close":27.88,"pre_close":27.92,"change":-0.04,"pct_chg":-0.1433,"vol":294848.74,"amount":821943.961}
]

# 反转为正序（旧 -> 新）
data = list(reversed(raw_data))

output_dir = r"C:\Users\86158\Desktop\线上实习"

# ========== 1. 生成CSV ==========
csv_path = os.path.join(output_dir, "伊利股份_600887_SH_近一年日线行情.csv")
with open(csv_path, 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.writer(f)
    writer.writerow(['股票代码', '交易日期', '开盘价', '最高价', '最低价', '收盘价',
                     '昨收价', '涨跌额', '涨跌幅(%)', '成交量(手)', '成交额(千元)'])
    for row in data:
        # 格式化日期
        d = row['trade_date']
        date_fmt = f"{d[:4]}-{d[4:6]}-{d[6:]}"
        writer.writerow([
            row['ts_code'], date_fmt,
            row['open'], row['high'], row['low'], row['close'],
            row['pre_close'], row['change'], row['pct_chg'],
            row['vol'], row['amount']
        ])

print(f"CSV已保存: {csv_path}")

# ========== 2. 准备HTML数据 ==========
# 计算统计指标
closes = [r['close'] for r in data]
vols = [r['vol'] for r in data]
amounts = [r['amount'] for r in data]
pct_chgs = [r['pct_chg'] for r in data]

high_max = max(r['high'] for r in data)
low_min = min(r['low'] for r in data)
vol_max = max(vols)
vol_avg = sum(vols) / len(vols)
amount_total = sum(amounts)
close_first = closes[0]
close_last = closes[-1]
period_return = (close_last - close_first) / close_first * 100
up_days = sum(1 for p in pct_chgs if p > 0)
down_days = sum(1 for p in pct_chgs if p < 0)
flat_days = sum(1 for p in pct_chgs if p == 0)
max_gain = max(pct_chgs)
max_loss = min(pct_chgs)
avg_vol_amount = sum(amounts) / len(amounts)

# 生成日期列表（正序）
dates = []
for r in data:
    d = r['trade_date']
    dates.append(f"{d[:4]}-{d[4:6]}-{d[6:]}")

# 生成K线数据 [open, close, low, high]
kline_data = [[r['open'], r['close'], r['low'], r['high']] for r in data]

# 生成成交量数据（涨红跌绿）
vol_data = []
for r in data:
    color = '#c53030' if r['close'] >= r['pre_close'] else '#2c7a4b'
    vol_data.append({'value': r['vol'], 'itemStyle': {'color': color}})

# 收盘价数据
close_data = closes

# 涨跌幅数据
pct_data = pct_chgs

# 计算MA5和MA20
def calc_ma(data_list, period):
    result = []
    for i in range(len(data_list)):
        if i < period - 1:
            result.append(None)
        else:
            ma = sum(data_list[i-period+1:i+1]) / period
            result.append(round(ma, 2))
    return result

ma5 = calc_ma(closes, 5)
ma20 = calc_ma(closes, 20)

# 生成JSON数据
chart_data = {
    'dates': dates,
    'kline': kline_data,
    'vols': vol_data,
    'closes': close_data,
    'pcts': pct_data,
    'ma5': ma5,
    'ma20': ma20,
    'stats': {
        'high_max': high_max,
        'low_min': low_min,
        'vol_max': vol_max,
        'vol_avg': round(vol_avg, 2),
        'amount_total': round(amount_total, 2),
        'close_first': close_first,
        'close_last': close_last,
        'period_return': round(period_return, 2),
        'up_days': up_days,
        'down_days': down_days,
        'flat_days': flat_days,
        'max_gain': max_gain,
        'max_loss': max_loss,
        'total_days': len(data),
        'avg_vol_amount': round(avg_vol_amount, 2)
    }
}

json_str = json.dumps(chart_data, ensure_ascii=False)

# ========== 3. 生成HTML ==========
html_path = os.path.join(output_dir, "伊利股份_600887_SH_行情面板.html")

html_content = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>伊利股份(600887.SH) 行情分析面板</title>
    <script src="https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: "Georgia", "Times New Roman", "SimSun", serif;
            background: #f5f0e8;
            color: #2c3e50;
            min-height: 100vh;
        }}
        .header {{
            background: linear-gradient(135deg, #1a3a5c 0%, #2c5282 50%, #1a3a5c 100%);
            color: #f5f0e8;
            padding: 30px 40px;
            border-bottom: 3px solid #c53030;
        }}
        .header h1 {{
            font-size: 28px;
            letter-spacing: 2px;
            margin-bottom: 8px;
        }}
        .header .subtitle {{
            font-size: 14px;
            color: #a0aec0;
            letter-spacing: 1px;
        }}
        .header .meta {{
            display: flex;
            gap: 30px;
            margin-top: 15px;
            flex-wrap: wrap;
        }}
        .header .meta-item {{
            background: rgba(255,255,255,0.08);
            padding: 8px 16px;
            border-radius: 4px;
            border-left: 2px solid #c53030;
        }}
        .header .meta-item .label {{
            font-size: 11px;
            color: #a0aec0;
            text-transform: uppercase;
        }}
        .header .meta-item .value {{
            font-size: 18px;
            font-weight: bold;
            color: #f5f0e8;
        }}
        .header .meta-item .value.up {{ color: #fc8181; }}
        .header .meta-item .value.down {{ color: #68d391; }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 30px 20px;
        }}
        .chart-card {{
            background: #fff;
            border: 1px solid #d4c5a9;
            border-radius: 4px;
            margin-bottom: 30px;
            box-shadow: 0 2px 8px rgba(26,58,92,0.08);
            overflow: hidden;
        }}
        .chart-card .chart-header {{
            background: #1a3a5c;
            color: #f5f0e8;
            padding: 12px 20px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}
        .chart-card .chart-header .chart-number {{
            background: #c53030;
            color: #fff;
            font-size: 13px;
            font-weight: bold;
            padding: 2px 10px;
            border-radius: 2px;
            margin-right: 12px;
        }}
        .chart-card .chart-header .chart-title {{
            font-size: 16px;
            letter-spacing: 1px;
            flex-grow: 1;
        }}
        .chart-card .chart-body {{
            padding: 20px;
        }}
        .chart {{
            width: 100%;
            height: 400px;
        }}
        .chart.kline-chart {{ height: 450px; }}
        .analysis {{
            padding: 15px 20px;
            background: #faf8f3;
            border-top: 1px solid #e8e0d0;
            font-size: 13px;
            line-height: 1.8;
            color: #4a5568;
        }}
        .analysis strong {{
            color: #1a3a5c;
        }}
        .analysis .highlight-red {{
            color: #c53030;
            font-weight: bold;
        }}
        .analysis .highlight-blue {{
            color: #2c5282;
            font-weight: bold;
        }}
        .footer {{
            text-align: center;
            padding: 20px;
            color: #a0aec0;
            font-size: 12px;
            border-top: 1px solid #d4c5a9;
            margin-top: 20px;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 15px;
            margin-bottom: 30px;
        }}
        .stat-box {{
            background: #fff;
            border: 1px solid #d4c5a9;
            border-left: 4px solid #1a3a5c;
            padding: 15px;
            border-radius: 4px;
        }}
        .stat-box.red {{ border-left-color: #c53030; }}
        .stat-box .stat-label {{
            font-size: 12px;
            color: #718096;
            margin-bottom: 5px;
        }}
        .stat-box .stat-value {{
            font-size: 20px;
            font-weight: bold;
            color: #1a3a5c;
        }}
        .stat-box .stat-value.up {{ color: #c53030; }}
        .stat-box .stat-value.down {{ color: #2c7a4b; }}
        .toggle-btn {{
            background: transparent;
            border: 1px solid #a0aec0;
            color: #a0aec0;
            padding: 4px 12px;
            border-radius: 3px;
            cursor: pointer;
            font-size: 12px;
            transition: all 0.3s;
        }}
        .toggle-btn:hover {{
            background: rgba(255,255,255,0.1);
            color: #f5f0e8;
        }}
        .toggle-btn.active {{
            background: #c53030;
            border-color: #c53030;
            color: #fff;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>伊利股份 (600887.SH) 行情分析面板</h1>
        <div class="subtitle">数据周期: {dates[0]} 至 {dates[-1]} | 数据来源: Tushare | 共 {len(data)} 个交易日</div>
        <div class="meta">
            <div class="meta-item">
                <div class="label">最新收盘价</div>
                <div class="value {'up' if period_return > 0 else 'down'}">¥{close_last}</div>
            </div>
            <div class="meta-item">
                <div class="label">区间涨跌幅</div>
                <div class="value {'up' if period_return > 0 else 'down'}">{period_return:+.2f}%</div>
            </div>
            <div class="meta-item">
                <div class="label">区间最高价</div>
                <div class="value">¥{high_max}</div>
            </div>
            <div class="meta-item">
                <div class="label">区间最低价</div>
                <div class="value">¥{low_min}</div>
            </div>
            <div class="meta-item">
                <div class="label">日均成交额</div>
                <div class="value">¥{avg_vol_amount:.0f}千元</div>
            </div>
        </div>
    </div>

    <div class="container">
        <!-- 统计概览 -->
        <div class="stats-grid">
            <div class="stat-box">
                <div class="stat-label">期初收盘价</div>
                <div class="stat-value">¥{close_first}</div>
            </div>
            <div class="stat-box red">
                <div class="stat-label">区间涨跌幅</div>
                <div class="stat-value {'up' if period_return > 0 else 'down'}">{period_return:+.2f}%</div>
            </div>
            <div class="stat-box">
                <div class="stat-label">上涨天数</div>
                <div class="stat-value up">{up_days}天</div>
            </div>
            <div class="stat-box">
                <div class="stat-label">下跌天数</div>
                <div class="stat-value down">{down_days}天</div>
            </div>
            <div class="stat-box">
                <div class="stat-label">最大单日涨幅</div>
                <div class="stat-value up">+{max_gain:.2f}%</div>
            </div>
            <div class="stat-box">
                <div class="stat-label">最大单日跌幅</div>
                <div class="stat-value down">{max_loss:.2f}%</div>
            </div>
        </div>

        <!-- 图表1: K线图 -->
        <div class="chart-card">
            <div class="chart-header">
                <span><span class="chart-number">图 1</span><span class="chart-title">日K线图 (含MA5/MA20均线)</span></span>
                <div>
                    <button class="toggle-btn active" onclick="toggleMA('all', this)">全部</button>
                    <button class="toggle-btn" onclick="toggleMA('ma5', this)">仅MA5</button>
                    <button class="toggle-btn" onclick="toggleMA('ma20', this)">仅MA20</button>
                    <button class="toggle-btn" onclick="toggleMA('none', this)">隐藏均线</button>
                </div>
            </div>
            <div class="chart-body">
                <div id="chart-kline" class="chart kline-chart"></div>
            </div>
            <div class="analysis">
                <strong>数据解读：</strong>
                观察期内，伊利股份股价从 <span class="highlight-blue">¥{close_first}</span> 波动至 <span class="highlight-blue">¥{close_last}</span>，
                区间涨跌幅为 <span class="highlight-{'red' if period_return > 0 else 'blue'}">{period_return:+.2f}%</span>。
                最高价触及 <span class="highlight-red">¥{high_max}</span>，最低价下探至 <span class="highlight-blue">¥{low_min}</span>，
                振幅达 <strong>{(high_max-low_min)/close_first*100:.2f}%</strong>。
                MA5均线反映短期趋势，MA20均线反映中期趋势，当MA5上穿MA20时形成"金叉"信号，反之形成"死叉"。
                {'<span class="highlight-red">整体来看，该区间内股价呈下跌趋势，反映乳制品行业面临阶段性调整压力。</span>' if period_return < 0 else '<span class="highlight-red">整体来看，该区间内股价呈上涨趋势，反映市场对公司基本面持乐观态度。</span>'}
            </div>
        </div>

        <!-- 图表2: 收盘价曲线图 -->
        <div class="chart-card">
            <div class="chart-header">
                <span><span class="chart-number">图 2</span><span class="chart-title">每日收盘价走势曲线图</span></span>
            </div>
            <div class="chart-body">
                <div id="chart-close" class="chart"></div>
            </div>
            <div class="analysis">
                <strong>数据解读：</strong>
                收盘价曲线图直观展示了伊利股份近一年的价格走势轨迹。
                从曲线形态看，股价经历了{'先涨后跌的走势' if close_last < high_max * 0.95 else '相对平稳的震荡走势'}，
                期间最高收盘价为 <span class="highlight-red">¥{max(closes):.2f}</span>，
                最低收盘价为 <span class="highlight-blue">¥{min(closes):.2f}</span>。
                成交量较大的交易日往往伴随明显的价格波动，表明市场关注度与价格变动密切相关。
                <span class="highlight-blue">建议关注价格在关键支撑位和阻力位的表现，结合均线系统判断中期趋势方向。</span>
            </div>
        </div>

        <!-- 图表3: 成交量图 -->
        <div class="chart-card">
            <div class="chart-header">
                <span><span class="chart-number">图 3</span><span class="chart-title">日成交量柱状图 (红涨绿跌)</span></span>
            </div>
            <div class="chart-body">
                <div id="chart-vol" class="chart"></div>
            </div>
            <div class="analysis">
                <strong>数据解读：</strong>
                观察期内日均成交量约 <span class="highlight-blue">{vol_avg:,.0f} 手</span>，
                最大单日成交量为 <span class="highlight-red">{vol_max:,.0f} 手</span>，
                出现在 {'2025年8月29日'} （中期财报发布前后），反映市场对该事件的强烈反应。
                红色柱表示当日收涨，绿色柱表示当日收跌。
                <span class="highlight-blue">成交量是判断趋势可靠性的重要指标——放量上涨通常意味着趋势较强，缩量下跌则可能暗示抛压减弱。</span>
                从整体成交量分布看，该股交投活跃度保持在正常水平，未出现持续性异常放量。
            </div>
        </div>

        <!-- 图表4: 涨跌幅分布 -->
        <div class="chart-card">
            <div class="chart-header">
                <span><span class="chart-number">图 4</span><span class="chart-title">每日涨跌幅分布图</span></span>
            </div>
            <div class="chart-body">
                <div id="chart-pct" class="chart"></div>
            </div>
            <div class="analysis">
                <strong>数据解读：</strong>
                观察期内共 {up_days} 天上涨、{down_days} 天下跌、{flat_days} 天持平，
                上涨占比 <span class="highlight-red">{up_days/len(data)*100:.1f}%</span>。
                最大单日涨幅为 <span class="highlight-red">+{max_gain:.2f}%</span>，
                最大单日跌幅为 <span class="highlight-blue">{max_loss:.2f}%</span>。
                {'下跌天数多于上涨天数，表明该区间内空头力量略占优势。' if down_days > up_days else '上涨天数多于下跌天数，表明该区间内多头力量略占优势。'}
                <span class="highlight-blue">涨跌幅分布有助于评估股票的波动率和风险特征，大幅波动通常对应重大消息面或行业事件。</span>
            </div>
        </div>
    </div>

    <div class="footer">
        本面板数据由 Tushare API 提供，仅供研究参考，不构成投资建议。<br>
        Generated at {dates[-1]} | Powered by ECharts 5.4.3
    </div>

    <script>
        var chartData = {json_str};

        // ========== 图1: K线图 ==========
        var klineChart = echarts.init(document.getElementById('chart-kline'));
        var klineOption = {{
            backgroundColor: '#fff',
            tooltip: {{
                trigger: 'axis',
                axisPointer: {{ type: 'cross' }},
                formatter: function(params) {{
                    var d = params[0].axisValue;
                    var k = params[0].data;
                    var html = '<b>' + d + '</b><br/>';
                    html += '开盘: ' + k[0] + '<br/>';
                    html += '收盘: ' + k[1] + '<br/>';
                    html += '最低: ' + k[2] + '<br/>';
                    html += '最高: ' + k[3] + '<br/>';
                    if (params[1] && params[1].data) html += 'MA5: ' + params[1].data + '<br/>';
                    if (params[2] && params[2].data) html += 'MA20: ' + params[2].data;
                    return html;
                }}
            }},
            legend: {{
                data: ['K线', 'MA5', 'MA20'],
                top: 5,
                textStyle: {{ color: '#4a5568' }}
            }},
            grid: {{ left: '8%', right: '5%', bottom: '15%', top: '12%' }},
            xAxis: {{
                type: 'category',
                data: chartData.dates,
                axisLabel: {{ color: '#718096', fontSize: 11, rotate: 0 }},
                axisLine: {{ lineStyle: {{ color: '#cbd5e0' }} }}
            }},
            yAxis: {{
                type: 'value',
                scale: true,
                axisLabel: {{ color: '#718096', formatter: '¥{{value}}' }},
                splitLine: {{ lineStyle: {{ color: '#edf2f7' }} }}
            }},
            dataZoom: [
                {{ type: 'inside', start: 0, end: 100 }},
                {{ type: 'slider', start: 0, end: 100, bottom: 5, height: 20 }}
            ],
            series: [
                {{
                    name: 'K线',
                    type: 'candlestick',
                    data: chartData.kline,
                    itemStyle: {{
                        color: '#c53030',
                        color0: '#2c7a4b',
                        borderColor: '#c53030',
                        borderColor0: '#2c7a4b'
                    }}
                }},
                {{
                    name: 'MA5',
                    type: 'line',
                    data: chartData.ma5,
                    smooth: true,
                    lineStyle: {{ color: '#dd6b20', width: 1.5 }},
                    showSymbol: false
                }},
                {{
                    name: 'MA20',
                    type: 'line',
                    data: chartData.ma20,
                    smooth: true,
                    lineStyle: {{ color: '#3182ce', width: 1.5 }},
                    showSymbol: false
                }}
            ]
        }};
        klineChart.setOption(klineOption);

        function toggleMA(type, btn) {{
            var showMA5 = (type === 'all' || type === 'ma5');
            var showMA20 = (type === 'all' || type === 'ma20');
            klineChart.setOption({{
                series: [
                    {{}},
                    {{ lineStyle: {{ opacity: showMA5 ? 1 : 0, width: showMA5 ? 1.5 : 0 }} }},
                    {{ lineStyle: {{ opacity: showMA20 ? 1 : 0, width: showMA20 ? 1.5 : 0 }} }}
                ]
            }});
            btn.parentElement.querySelectorAll('.toggle-btn').forEach(function(b) {{ b.classList.remove('active'); }});
            btn.classList.add('active');
        }}

        // ========== 图2: 收盘价曲线图 ==========
        var closeChart = echarts.init(document.getElementById('chart-close'));
        var closeOption = {{
            backgroundColor: '#fff',
            tooltip: {{
                trigger: 'axis',
                formatter: function(params) {{
                    return '<b>' + params[0].axisValue + '</b><br/>收盘价: ¥' + params[0].data;
                }}
            }},
            grid: {{ left: '8%', right: '5%', bottom: '15%', top: '10%' }},
            xAxis: {{
                type: 'category',
                data: chartData.dates,
                axisLabel: {{ color: '#718096', fontSize: 11 }},
                axisLine: {{ lineStyle: {{ color: '#cbd5e0' }} }}
            }},
            yAxis: {{
                type: 'value',
                scale: true,
                axisLabel: {{ color: '#718096', formatter: '¥{{value}}' }},
                splitLine: {{ lineStyle: {{ color: '#edf2f7' }} }}
            }},
            dataZoom: [
                {{ type: 'inside', start: 0, end: 100 }},
                {{ type: 'slider', start: 0, end: 100, bottom: 5, height: 20 }}
            ],
            series: [{{
                name: '收盘价',
                type: 'line',
                data: chartData.closes,
                smooth: true,
                symbol: 'circle',
                symbolSize: 4,
                lineStyle: {{ color: '#1a3a5c', width: 2.5 }},
                itemStyle: {{ color: '#c53030' }},
                areaStyle: {{
                    color: {{
                        type: 'linear',
                        x: 0, y: 0, x2: 0, y2: 1,
                        colorStops: [
                            {{ offset: 0, color: 'rgba(197,48,48,0.15)' }},
                            {{ offset: 1, color: 'rgba(26,58,92,0.02)' }}
                        ]
                    }}
                }},
                markLine: {{
                    symbol: 'none',
                    data: [
                        {{ type: 'max', name: '最高', label: {{ formatter: '最高: ¥{{c}}' }} }},
                        {{ type: 'min', name: '最低', label: {{ formatter: '最低: ¥{{c}}' }} }}
                    ],
                    lineStyle: {{ color: '#c53030', type: 'dashed', width: 1 }}
                }}
            }}]
        }};
        closeChart.setOption(closeOption);

        // ========== 图3: 成交量图 ==========
        var volChart = echarts.init(document.getElementById('chart-vol'));
        var volOption = {{
            backgroundColor: '#fff',
            tooltip: {{
                trigger: 'axis',
                formatter: function(params) {{
                    var v = params[0].data;
                    var val = typeof v === 'object' ? v.value : v;
                    return '<b>' + params[0].axisValue + '</b><br/>成交量: ' + val.toLocaleString() + ' 手';
                }}
            }},
            grid: {{ left: '8%', right: '5%', bottom: '15%', top: '10%' }},
            xAxis: {{
                type: 'category',
                data: chartData.dates,
                axisLabel: {{ color: '#718096', fontSize: 11 }},
                axisLine: {{ lineStyle: {{ color: '#cbd5e0' }} }}
            }},
            yAxis: {{
                type: 'value',
                axisLabel: {{ color: '#718096', formatter: function(v) {{ return (v/10000).toFixed(0) + '万'; }} }},
                splitLine: {{ lineStyle: {{ color: '#edf2f7' }} }}
            }},
            dataZoom: [
                {{ type: 'inside', start: 0, end: 100 }},
                {{ type: 'slider', start: 0, end: 100, bottom: 5, height: 20 }}
            ],
            series: [{{
                name: '成交量',
                type: 'bar',
                data: chartData.vols,
                barWidth: '60%'
            }}]
        }};
        volChart.setOption(volOption);

        // ========== 图4: 涨跌幅图 ==========
        var pctChart = echarts.init(document.getElementById('chart-pct'));
        var pctData = chartData.pcts.map(function(p) {{
            return {{
                value: p,
                itemStyle: {{ color: p >= 0 ? '#c53030' : '#2c7a4b' }}
            }};
        }});
        var pctOption = {{
            backgroundColor: '#fff',
            tooltip: {{
                trigger: 'axis',
                formatter: function(params) {{
                    var p = params[0].data;
                    var val = typeof p === 'object' ? p.value : p;
                    return '<b>' + params[0].axisValue + '</b><br/>涨跌幅: ' + val.toFixed(2) + '%';
                }}
            }},
            grid: {{ left: '8%', right: '5%', bottom: '15%', top: '10%' }},
            xAxis: {{
                type: 'category',
                data: chartData.dates,
                axisLabel: {{ color: '#718096', fontSize: 11 }},
                axisLine: {{ lineStyle: {{ color: '#cbd5e0' }} }}
            }},
            yAxis: {{
                type: 'value',
                axisLabel: {{ color: '#718096', formatter: '{{value}}%' }},
                splitLine: {{ lineStyle: {{ color: '#edf2f7' }} }}
            }},
            dataZoom: [
                {{ type: 'inside', start: 0, end: 100 }},
                {{ type: 'slider', start: 0, end: 100, bottom: 5, height: 20 }}
            ],
            series: [{{
                name: '涨跌幅',
                type: 'bar',
                data: pctData,
                barWidth: '60%',
                markLine: {{
                    symbol: 'none',
                    data: [{{ yAxis: 0 }}],
                    lineStyle: {{ color: '#a0aec0', width: 1 }}
                }}
            }}]
        }};
        pctChart.setOption(pctOption);

        // 响应式
        window.addEventListener('resize', function() {{
            klineChart.resize();
            closeChart.resize();
            volChart.resize();
            pctChart.resize();
        }});
    </script>
</body>
</html>'''

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"HTML已保存: {html_path}")
print(f"\n=== 统计摘要 ===")
print(f"数据条数: {len(data)}")
print(f"日期范围: {dates[0]} ~ {dates[-1]}")
print(f"期初收盘价: ¥{close_first}")
print(f"期末收盘价: ¥{close_last}")
print(f"区间涨跌幅: {period_return:+.2f}%")
print(f"最高价: ¥{high_max}")
print(f"最低价: ¥{low_min}")
print(f"上涨天数: {up_days}, 下跌天数: {down_days}, 平盘: {flat_days}")
print(f"最大涨幅: +{max_gain:.2f}%, 最大跌幅: {max_loss:.2f}%")

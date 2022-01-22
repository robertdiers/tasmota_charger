#!/usr/bin/env python

import pymodbus
import configparser
import os
import psycopg2
from datetime import datetime
from pymodbus.client.sync import ModbusTcpClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.payload import BinaryPayloadBuilder
from urllib.request import urlopen

#read config
config = configparser.ConfigParser()

#-----------------------------------------
# Routine to read a float    
def ReadFloat(client,myadr_dec,unitid):
    r1=client.read_holding_registers(myadr_dec,2,unit=unitid)
    FloatRegister = BinaryPayloadDecoder.fromRegisters(r1.registers, byteorder=Endian.Big, wordorder=Endian.Little)
    result_FloatRegister =round(FloatRegister.decode_32bit_float(),2)
    return(result_FloatRegister)   
#----------------------------------------- 
# Routine to write float
def WriteFloat(client,myadr_dec,feed_in,unitid):
    builder = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Little)
    builder.add_32bit_float( feed_in )
    payload = builder.to_registers() 
    client.write_registers(myadr_dec, payload, unit=unitid)

# read status from Tasmota
def StatusTasmota(tasmotaip):
    if not tasmotaip:
        return 'DISABLED'
    try:
        statuslink = urlopen('http://'+tasmotaip+'/?m=1')
        return statuslink.read().decode('utf-8')
    except Exception as e:
        print (e)
        return 'ERROR'

# set status Tasmota
def SwitchTasmota(tasmotaip, status):
    print (tasmotaip+' '+status)
    try:
        if 'ON' in status and 'OFF' in StatusTasmota(tasmotaip):
            switchlink = urlopen('http://'+tasmotaip+'/?m=1&o=1')
            retval = switchlink.read().decode('utf-8')
            print(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ' ' + tasmotaip + ': ' + retval)
        if 'OFF' in status and 'ON' in StatusTasmota(tasmotaip):
            switchlink = urlopen('http://'+tasmotaip+'/?m=1&o=1')
            retval = switchlink.read().decode('utf-8')
            print(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ' ' + tasmotaip + ': ' + retval)
    except Exception as e:
        print (e)

# write metric to TimescaleDB
def WriteTimescaleDb(conn, table, value):
    if conn:
        # create a cursor
        cur = conn.cursor()   
        # execute a statement
        sql = 'insert into '+table+' (time, value) values (now(), %s)'
        cur.execute(sql, (value,))   
        # commit the changes to the database
        conn.commit()
        # close the communication with the PostgreSQL
        cur.close()

if __name__ == "__main__":  
    print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " START #####")
    try:
        #read config
        config.read('tasmotachargerdefaults.ini')
        config.read('tasmotacharger.ini')

        #read config and default values
        inverter_ip = config['KostalSection']['inverter_ip']
        inverter_port = config['KostalSection']['inverter_port']
        tasmota_charge_ip = config['TasmotaSection']['tasmota_charge_ip']
        tasmota_charge_start = config['TasmotaSection']['tasmota_charge_start']  
        tasmota_charge_end = config['TasmotaSection']['tasmota_charge_end']  
        timescaledb_ip = config['MetricSection']['timescaledb_ip']
        timescaledb_username = config['MetricSection']['timescaledb_username']
        timescaledb_password = config['MetricSection']['timescaledb_password']

        # override with environment variables
        if os.getenv('INVERTER_IP','None') != 'None':
            inverter_ip = os.getenv('INVERTER_IP')
            print ("using env: INVERTER_IP")
        if os.getenv('INVERTER_PORT','None') != 'None':
            inverter_port = os.getenv('INVERTER_PORT')
            print ("using env: INVERTER_PORT")
        if os.getenv('TASMOTA_CHARGE_IP','None') != 'None':
            tasmota_charge_ip = os.getenv('TASMOTA_CHARGE_IP')
            print ("using env: TASMOTA_CHARGE_IP")
        if os.getenv('TASMOTA_CHARGE_START','None') != 'None':
            tasmota_charge_start = os.getenv('TASMOTA_CHARGE_START')
            print ("using env: TASMOTA_CHARGE_START")
        if os.getenv('TASMOTA_CHARGE_END','None') != 'None':
            tasmota_charge_end = os.getenv('TASMOTA_CHARGE_END')
            print ("using env: TASMOTA_CHARGE_END")
        if os.getenv('TIMESCALEDB_IP','None') != 'None':
            timescaledb_ip = os.getenv('TIMESCALEDB_IP')
            print ("using env: TIMESCALEDB_IP")
        if os.getenv('TIMESCALEDB_USERNAME','None') != 'None':
            timescaledb_username = os.getenv('TIMESCALEDB_USERNAME')
            print ("using env: TIMESCALEDB_USERNAME")
        if os.getenv('TIMESCALEDB_PASSWORD','None') != 'None':
            timescaledb_password = os.getenv('TIMESCALEDB_PASSWORD')
            print ("using env: TIMESCALEDB_PASSWORD")

        print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " inverter_ip: ", inverter_ip)
        print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " inverter_port: ", inverter_port)
        print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " tasmota_charge_ip: ", tasmota_charge_ip)
        print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " tasmota_charge_start: ", tasmota_charge_start)
        print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " tasmota_charge_end: ", tasmota_charge_end)
        print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " timescaledb_ip: ", timescaledb_ip)
        print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " timescaledb_username: ", timescaledb_username)
        print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " timescaledb_password: ", timescaledb_password)
        
        #init Timescaledb if used
        if timescaledb_ip:
            conn = psycopg2.connect(
                host=timescaledb_ip,
                database="postgres",
                user=timescaledb_username,
                password=timescaledb_password)

        #connection Kostal
        inverterclient = ModbusTcpClient(inverter_ip,port=inverter_port)            
        inverterclient.connect()       
        
        #all additional invertes will decrease my home consumption, so it might be negative - this is fine
        consumptionbat = ReadFloat(inverterclient,106,71)
        #print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " consumption battery: ", consumptionbat)
        WriteTimescaleDb(conn, 'solar_kostal_consumption_battery', consumptionbat)
        consumptiongrid = ReadFloat(inverterclient,108,71)
        #print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " consumption grid: ", consumptiongrid)
        WriteTimescaleDb(conn, 'solar_kostal_consumption_grid', consumptiongrid)
        consumptionpv = ReadFloat(inverterclient,116,71)
        #print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " consumption pv: ", consumptionpv)
        WriteTimescaleDb(conn, 'solar_kostal_consumption_pv', consumptionpv)
        consumption_total = consumptionbat + consumptiongrid + consumptionpv
        print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " consumption: ", consumption_total)
        WriteTimescaleDb(conn, 'solar_kostal_consumption_total', consumption_total)
        
        #Kostal generation (by tracker/battery)
        dc1 = ReadFloat(inverterclient,260,71)
        #print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " dc1: ", dc1)
        WriteTimescaleDb(conn, 'solar_kostal_generation_dc1', dc1)
        dc2 = ReadFloat(inverterclient,270,71)
        #print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " dc2: ", dc2)
        WriteTimescaleDb(conn, 'solar_kostal_generation_dc2', dc2)
        dc3 = ReadFloat(inverterclient,280,71)
        #print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " dc3: ", dc3)
        WriteTimescaleDb(conn, 'solar_kostal_generation_dc3', dc3)
        generation = round(dc1+dc2+dc3,2)
        print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " generation: ", generation) 
        WriteTimescaleDb(conn, 'solar_kostal_generation_total', generation)
        
        #this is not exact, but enough for us
        surplus = round(generation - consumption_total,1)
        print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " surplus: ", surplus)
        WriteTimescaleDb(conn, 'solar_kostal_surplus', surplus)
        
        inverterclient.close()
        
        #charging
        chargestatus = StatusTasmota(tasmota_charge_ip)
        if 'ON' in chargestatus:
            print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " chargestatus: ", 'ON')
            WriteTimescaleDb(conn, 'solar_battery_chargestatus', 1)
        if 'OFF' in chargestatus:
            print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " chargestatus: ", 'OFF')
            WriteTimescaleDb(conn, 'solar_battery_chargestatus', 0)

        #we will always charge between 12:00 and 12:05 to ensure a kind of "battery protect"
        now = datetime.now()
        if now.hour == 12 and now.minute < 5:
            if 'OFF' in chargestatus:
                SwitchTasmota(tasmota_charge_ip, 'ON')
                print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " start charging battery protect: ", surplus)
                WriteTimescaleDb(conn, 'solar_battery_chargestatus', 1)
        else:
            if 'OFF' in chargestatus and surplus > int(tasmota_charge_start):
                SwitchTasmota(tasmota_charge_ip, 'ON')
                print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " start charging: ", surplus)
                WriteTimescaleDb(conn, 'solar_battery_chargestatus', 1)
            if 'ON' in chargestatus and surplus < int(tasmota_charge_end):
                SwitchTasmota(tasmota_charge_ip, 'OFF')
                print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " stop charging: ", surplus)
                WriteTimescaleDb(conn, 'solar_battery_chargestatus', 0)

        print (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " END #####")
        
    except Exception as ex:
        print ("ERROR :", ex) 
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')          

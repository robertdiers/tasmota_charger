#!/bin/bash
cd /app
#echo INVERTER_IP $INVERTER_IP
#echo INVERTER_PORT $INVERTER_PORT
#echo TASMOTA_CHARGE_IP $TASMOTA_CHARGE_IP
#echo TASMOTA_CHARGE_START $TASMOTA_CHARGE_START
#echo TASMOTA_CHARGE_END $TASMOTA_CHARGE_END
python3 tasmotacharger.py

#!/bin/bash
cd /app
#echo INVERTER_IP $INVERTER_IP
#echo INVERTER_PORT $INVERTER_PORT
#echo TASMOTA_CHARGE_IP $TASMOTA_CHARGE_IP
#echo TASMOTA_CHARGE_START $TASMOTA_CHARGE_START
#echo TASMOTA_CHARGE_END $TASMOTA_CHARGE_END
#echo TASMOTA_STAGE1_IP $TASMOTA_STAGE1_IP
#echo TASMOTA_STAGE1_START $TASMOTA_STAGE1_START
#echo TASMOTA_STAGE1_END $TASMOTA_STAGE1_END
#echo TASMOTA_STAGE2_IP $TASMOTA_STAGE2_IP
#echo TASMOTA_STAGE2_START $TASMOTA_STAGE2_START
#echo TASMOTA_STAGE2_END $TASMOTA_STAGE2_END
python3 tasmotabatmanager.py

# tasmota_charger
charge batteries based on solar generation

## TimescaleDB
CREATE  TABLE solar_kostal_consumption_battery ( 
	"time"               timestamptz  NOT NULL  ,
	"value"              double precision    
 );

SELECT create_hypertable('solar_kostal_consumption_battery', 'time');

CREATE  TABLE solar_kostal_consumption_grid ( 
	"time"               timestamptz  NOT NULL  ,
	"value"              double precision    
 );

SELECT create_hypertable('solar_kostal_consumption_grid', 'time');

CREATE  TABLE solar_kostal_consumption_pv ( 
	"time"               timestamptz  NOT NULL  ,
	"value"              double precision    
 );

SELECT create_hypertable('solar_kostal_consumption_pv', 'time');

CREATE  TABLE solar_kostal_consumption_total ( 
	"time"               timestamptz  NOT NULL  ,
	"value"              double precision    
 );

SELECT create_hypertable('solar_kostal_consumption_total', 'time');

CREATE  TABLE solar_kostal_generation_total ( 
	"time"               timestamptz  NOT NULL  ,
	"value"              double precision    
 );

SELECT create_hypertable('solar_kostal_generation_total', 'time');

CREATE  TABLE solar_kostal_generation_dc1 ( 
	"time"               timestamptz  NOT NULL  ,
	"value"              double precision    
 );

SELECT create_hypertable('solar_kostal_generation_dc1', 'time');

CREATE  TABLE solar_kostal_generation_dc2 ( 
	"time"               timestamptz  NOT NULL  ,
	"value"              double precision    
 );

SELECT create_hypertable('solar_kostal_generation_dc2', 'time');

CREATE  TABLE solar_kostal_generation_dc3 ( 
	"time"               timestamptz  NOT NULL  ,
	"value"              double precision    
 );
 
SELECT create_hypertable('solar_kostal_generation_dc3', 'time');

CREATE  TABLE solar_kostal_surplus ( 
	"time"               timestamptz  NOT NULL  ,
	"value"              double precision    
 );

SELECT create_hypertable('solar_kostal_surplus', 'time');

CREATE  TABLE solar_battery_chargestatus ( 
	"time"               timestamptz  NOT NULL  ,
	"value"              double precision    
 );
 
SELECT create_hypertable('solar_battery_chargestatus', 'time');
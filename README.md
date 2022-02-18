# tasmota_charger
charge batteries based on solar generation

## TimescaleDB
CREATE  TABLE solar_kostal_consumption_battery ( 
	"time"               timestamptz  NOT NULL  ,
	"value"              double precision    
 );

SELECT create_hypertable('solar_kostal_consumption_battery', 'time');

ALTER TABLE solar_kostal_consumption_battery SET (
 timescaledb.compress,
 timescaledb.compress_segmentby = 'time'
);

SELECT add_compression_policy('solar_kostal_consumption_battery', INTERVAL '1 days');

CREATE  TABLE solar_kostal_consumption_grid ( 
	"time"               timestamptz  NOT NULL  ,
	"value"              double precision    
 );

SELECT create_hypertable('solar_kostal_consumption_grid', 'time');

ALTER TABLE solar_kostal_consumption_grid SET (
 timescaledb.compress,
 timescaledb.compress_segmentby = 'time'
);

SELECT add_compression_policy('solar_kostal_consumption_grid', INTERVAL '1 days');

CREATE  TABLE solar_kostal_consumption_pv ( 
	"time"               timestamptz  NOT NULL  ,
	"value"              double precision    
 );

SELECT create_hypertable('solar_kostal_consumption_pv', 'time');

ALTER TABLE solar_kostal_consumption_pv SET (
 timescaledb.compress,
 timescaledb.compress_segmentby = 'time'
);

SELECT add_compression_policy('solar_kostal_consumption_pv', INTERVAL '1 days');

CREATE  TABLE solar_kostal_consumption_total ( 
	"time"               timestamptz  NOT NULL  ,
	"value"              double precision    
 );

SELECT create_hypertable('solar_kostal_consumption_total', 'time');

ALTER TABLE solar_kostal_consumption_total SET (
 timescaledb.compress,
 timescaledb.compress_segmentby = 'time'
);

SELECT add_compression_policy('solar_kostal_consumption_total', INTERVAL '1 days');

CREATE  TABLE solar_kostal_generation_total ( 
	"time"               timestamptz  NOT NULL  ,
	"value"              double precision    
 );

SELECT create_hypertable('solar_kostal_generation_total', 'time');

ALTER TABLE solar_kostal_generation_total SET (
 timescaledb.compress,
 timescaledb.compress_segmentby = 'time'
);

SELECT add_compression_policy('solar_kostal_generation_total', INTERVAL '1 days');

CREATE  TABLE solar_kostal_generation_dc1 ( 
	"time"               timestamptz  NOT NULL  ,
	"value"              double precision    
 );

SELECT create_hypertable('solar_kostal_generation_dc1', 'time');

ALTER TABLE solar_kostal_generation_dc1 SET (
 timescaledb.compress,
 timescaledb.compress_segmentby = 'time'
);

SELECT add_compression_policy('solar_kostal_generation_dc1', INTERVAL '1 days');

CREATE  TABLE solar_kostal_generation_dc2 ( 
	"time"               timestamptz  NOT NULL  ,
	"value"              double precision    
 );

SELECT create_hypertable('solar_kostal_generation_dc2', 'time');

ALTER TABLE solar_kostal_generation_dc2 SET (
 timescaledb.compress,
 timescaledb.compress_segmentby = 'time'
);

SELECT add_compression_policy('solar_kostal_generation_dc2', INTERVAL '1 days');

CREATE  TABLE solar_kostal_generation_dc3 ( 
	"time"               timestamptz  NOT NULL  ,
	"value"              double precision    
 );
 
SELECT create_hypertable('solar_kostal_generation_dc3', 'time');

ALTER TABLE solar_kostal_generation_dc3 SET (
 timescaledb.compress,
 timescaledb.compress_segmentby = 'time'
);

SELECT add_compression_policy('solar_kostal_generation_dc3', INTERVAL '1 days');

CREATE  TABLE solar_kostal_surplus ( 
	"time"               timestamptz  NOT NULL  ,
	"value"              double precision    
 );

SELECT create_hypertable('solar_kostal_surplus', 'time');

ALTER TABLE solar_kostal_surplus SET (
 timescaledb.compress,
 timescaledb.compress_segmentby = 'time'
);

SELECT add_compression_policy('solar_kostal_surplus', INTERVAL '1 days');

CREATE  TABLE solar_battery_chargestatus ( 
	"time"               timestamptz  NOT NULL  ,
	"value"              double precision    
 );
 
SELECT create_hypertable('solar_battery_chargestatus', 'time');

ALTER TABLE solar_battery_chargestatus SET (
 timescaledb.compress,
 timescaledb.compress_segmentby = 'time'
);

SELECT add_compression_policy('solar_battery_chargestatus', INTERVAL '1 days');

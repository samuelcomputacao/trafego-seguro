select gid,
ds_local_i,
ds_local_f,
vl_km_inic,
vl_km_fina,
vl_extensa,
ST_AsText(ST_pointn(geom,10)) as points,
geom
from rodovias_federais where sg_uf = 'PB' and vl_br = '104'and gid=1067

select  ST_PointN (
	  geom,
	  generate_series (1, ST_NPoints (geom))
   ),
   ST_NPoints (geom)
from rodovias_federais where gid='1069'

SELECT ST_distance(ST_GeomFromText('POINT(-35.8750504 -7.0215504 )',4326),
	 ST_GeomFromText('POINT(-35.8698295 -7.1053985)', 4326)) * 111.11 as km;
	 
SELECT ST_distance(ST_GeomFromText('POINT(-36.059419429999934 -6.721801859999971)',4326),
ST_GeomFromText('POINT(-35.795983329999956 -6.967585819999954)', 4326)) * 111.11 as km,
ST_GeomFromText('POINT(-36.059419429999934 -6.721801859999971)',4326),
ST_GeomFromText('POINT(-35.795983329999956 -6.967585819999954)', 4326)
;

SELECT ST_GeomFromText('POINT(-36.20386295999998 -6.432954979999977)', 4326);
	 
	 
select * from rodovias_federais
where vl_km_inic <= 50 and vl_km_fina >= 50 and vl_br = '104' and sg_uf = 'PB'

CREATE OR REPLACE FUNCTION calculate_km(km DECIMAL, uf VARCHAR(2), rodovia VARCHAR(3))
	RETURNS geometry AS $$
	DECLARE
      point_current geometry;
	  point_last geometry;
	  rec_trecho RECORD;
	  km_count DECIMAL DEFAULT 0;
	  flag_point INTEGER DEFAULT 0; 
	  cur_points CURSOR(p_gid integer) 
					FOR SELECT  ST_PointN (
							geom,
							generate_series (1, ST_NPoints (geom)))
						FROM rodovias_federais WHERE gid = p_gid;
   	BEGIN
		SELECT gid, vl_km_inic into rec_trecho
		FROM rodovias_federais
		WHERE vl_km_inic <= km AND vl_km_fina >= km AND vl_br = rodovia AND sg_uf = uf;
		
		Raise notice 'gid %', rec_trecho.gid;
		
		km_count = rec_trecho.vl_km_inic;
		
	    OPEN cur_points(rec_trecho.gid);

	    LOOP
			FETCH cur_points INTO point_current;
		  	EXIT WHEN NOT FOUND;
			
			IF flag_point=0 THEN
				point_last = point_current;
				flag_point = 1;
			END IF;
			
			IF km_count < km THEN
				km_count = km_count + (ST_Distance(point_current, point_last) * 111.11);
				point_last = point_current;
				Raise notice '% --> %', ST_AsText(point_current),km_count;
			END IF;
			
		END LOOP;
		
	   	CLOSE cur_points;

        RETURN point_last;
    END;
$$ LANGUAGE plpgsql;

select calculate_km(120,'PB','104')

		
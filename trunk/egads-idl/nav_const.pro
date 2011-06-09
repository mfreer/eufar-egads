;+
; NAME:
;   nav_const
;
; PURPOSE:
;   Additional consistency check & QA for .gps (no correction!)
;   
; CATEGORY:
;		
; CALLING SEQUENCE:
;   nav_const, fname, stat_lun=stat_lun, gps_err_array=gps_err_array, gps_data=gps_data
; 
; INPUTS:
;    fname => base-filename WITH .gps - suffix !
;
; OPTIONAL INPUTS:
;	
; KEYWORD PARAMETERS:
;
; OUTPUTS:
;   status file => template+'_status'
;
; OPTIONAL OUTPUTS:
;   if (KEYWORD_SET(gps_err_array)) => QC array
;       otime, lat, lon, alt, pit, rol, heading, track, speed, sat, dgps
;       Values: 0:OK    1:minor problem    2:major problem
;
;   if (KEYWORD_SET(gps_data))      => gps data as array
;       otime, lat, lon, alt, pit, rol, heading, track, speed, sat, dgps
; 
; COMMON BLOCKS:
;
; SIDE EFFECTS:
;
; RESTRICTIONS:
;
; PROCEDURE:
;   test & report the following:
;   - if data range is not plausible
;   - if change between steps > threshold: 
;     latlon, alt, pit, rol, heading, track, speed
;   - uncorrectable errors in:
;     time, latlon, alt, pit, rol, heading, track, speed, sat, dgps
;
; EXAMPLE:
;
; MODIFICATION HISTORY:
; 2006/05/10   Documentation finished by Martin Bachmann, DLR-DFD-UG  	
; 2011/01/03   Plausibility of data range (MB)
; 
; TODO: 
; 
; 
;-

pro nav_const, fname, stat_lun=stat_lun, gps_err_array=gps_err_array, gps_data=gps_data, extradatum=extradatum

  ; ---------------------------------------------
  ; consistency check for .gps
  ; 
  ; also includes GPS QC   if keyword_set: gps_err_array
  ; also pass all GPS data if keyword_set: gps_data

  filename = fname + '.gps'

  hymap_read_gps, filename=filename, uyear=uyear, umonth=umonth, uday=uday, uhour=uhour, umin=umin, usec=usec, $
     urest=urest, lat=lat, lon=lon, alt=alt, pit=pit, rol=rol, heading=heading, track=track, speed=speed, sat=sat, dgps=dgps

  orig_time = urest + usec + 60*umin + 60*60*uhour

    ; Set tolerance values:  
    latlon_thresh = 0.0001
    alt_thresh = 1.
    pit_thresh = 0.1
    rol_thresh = 0.1
    heading_thresh = 0.2
    track_thresh = 0.3
    speed_thresh = 0.1


   ; Set plausibility range 
   lat_pmax = 72  ; abs, in degree
   alt_pmax = 6000   ; in meter
   alt_pmin = 1000   ; in meter
   pit_pmax = 2.0     ; abs
   rol_pmax = 2.0     ; abs
   heading_pmax = 181 ; abs
   track_pmax =   361
   speed_pmax = 60
   speed_pmin = 80
   

  ; create the QC array
  ;
  ; otime, lat, lon, alt, pit, rol, heading, track, speed, sat, dgps
  ;
  ; Values: 0:OK    1:minor problem    2:major problem

  dummy = size(orig_time ,/dimensions)

  IF (KEYWORD_SET(gps_err_array)) THEN begin
    gps_err_array = bytarr(dummy(0)-1,11)
  end 

    if max(orig_time) EQ min(orig_time) then begin
      print, 'Still errors with Timestamp  - Manual check required!'
      IF (KEYWORD_SET(stat_lun)) THEN printf, stat_lun,'Still errors with Timestamp  - Manual check required!'
      IF (KEYWORD_SET(gps_err_array)) THEN gps_err_array(*,0)=2
    end

    if max(lat) EQ min(lat) then begin
      print, 'Still errors with Lat  - Manual check required!'
      IF (KEYWORD_SET(stat_lun)) THEN printf, stat_lun,'Still errors with Lat  - Manual check required!'
      IF (KEYWORD_SET(gps_err_array)) THEN gps_err_array(*,1)=2
    end
    dummy = where( max(lat) GE lat_pmax , count)
    if count GT 0 then begin
      print, 'WARNING - Lat values out of realitsic range  - Manual check required!'
      IF (KEYWORD_SET(stat_lun)) THEN printf, stat_lun, 'WARNING - Lat values out of realitsic range  - Manual check required!'
      IF (KEYWORD_SET(gps_err_array)) THEN gps_err_array(dummy,1)=2             
    end    
    
    if max(lon) EQ min(lon) then begin
      print, 'Still errors with Lon  - Manual check required!'
      IF (KEYWORD_SET(stat_lun)) THEN printf, stat_lun,'Still errors with Lon  - Manual check required!'
      IF (KEYWORD_SET(gps_err_array)) THEN gps_err_array(*,2)=2
    end
    
    if max(alt) EQ min(alt) then begin
      print, 'Still errors with Altitude  - Manual check required!'
      IF (KEYWORD_SET(stat_lun)) THEN printf, stat_lun,'Still errors with Altitude  - Manual check required!'
      IF (KEYWORD_SET(gps_err_array)) THEN gps_err_array(*,3)=2
    end    
    dummy = where(max(alt) GE alt_pmax, count)
    if count GT 0 then begin
      print, 'WARNING - Altitude values out of realitsic range  - Manual check required!'
      IF (KEYWORD_SET(stat_lun)) THEN printf, stat_lun, 'WARNING - Altitude values out of realitsic range  - Manual check required!'
      IF (KEYWORD_SET(gps_err_array)) THEN gps_err_array(dummy,3)=2             
    end    
    dummy = where( min(alt) LE alt_pmin , count)
    if count GT 0 then begin
      print, 'WARNING - Altitude values out of realitsic range  - Manual check required!'
      IF (KEYWORD_SET(stat_lun)) THEN printf, stat_lun, 'WARNING - Altitude values out of realitsic range  - Manual check required!'
      IF (KEYWORD_SET(gps_err_array)) THEN gps_err_array(dummy,3)=2             
    end    
    
    
    if max(pit) EQ min(pit) then begin
      print, 'Still errors with Pitch  - Manual check required!'
      IF (KEYWORD_SET(stat_lun)) THEN printf, stat_lun,'Still errors with Pitch - Manual check required!'
      IF (KEYWORD_SET(gps_err_array)) THEN gps_err_array(*,4)=2
    end
    dummy = where ( max(abs(pit)) GE pit_pmax , count)
    if count GT 0 then begin
      print, 'WARNING - Pitch values out of realitsic range  - Manual check required!'
      IF (KEYWORD_SET(stat_lun)) THEN printf, stat_lun, 'WARNING - Pitch values out of realitsic range  - Manual check required!'
      IF (KEYWORD_SET(gps_err_array)) THEN gps_err_array(dummy,4)=2             
    end      
    
    if max(rol) EQ min(rol) then begin
      print, 'Still errors with Roll  - Manual check required!'
      IF (KEYWORD_SET(stat_lun)) THEN printf, stat_lun,'Still errors with Roll - Manual check required!'
      IF (KEYWORD_SET(gps_err_array)) THEN gps_err_array(*,5)=2
    end
    dummy = where (max(abs(rol)) GE rol_pmax, count)
    if count GT 0 then begin
      print, 'WARNING - Roll values out of realitsic range  - Manual check required!'
      IF (KEYWORD_SET(stat_lun)) THEN printf, stat_lun, 'WARNING - Roll values out of realitsic range  - Manual check required!'
      IF (KEYWORD_SET(gps_err_array)) THEN gps_err_array(dummy,5)=2             
    end  
        
    if max(heading) EQ min(heading) then begin    
      print, 'Still errors with Heading  - Manual check required!'
      IF (KEYWORD_SET(stat_lun)) THEN printf, stat_lun,'Still errors with Heading - Manual check required!'
      IF (KEYWORD_SET(gps_err_array)) THEN gps_err_array(*,6)=2
    end
    dummy = where( max(abs(heading)) GE heading_pmax, count)
    if count GT 0 then begin
      print, 'WARNING - Heading values out of realitsic range  - Manual check required!'
      IF (KEYWORD_SET(stat_lun)) THEN printf, stat_lun, 'WARNING - Heading values out of realitsic range  - Manual check required!'
      IF (KEYWORD_SET(gps_err_array)) THEN gps_err_array(dummy,6)=2             
    end 
        
    
    if max(track) EQ min(track) then begin
      print, 'Still errors with TrueTrack  - Manual check required!'
      IF (KEYWORD_SET(stat_lun)) THEN printf, stat_lun,'Still errors with TrueTrack - Manual check required!'
      IF (KEYWORD_SET(gps_err_array)) THEN gps_err_array(*,7)=2
    end
    dummy = where (max(track) GE track_pmax, count)    
    if count GT 0 then begin    
      print, 'WARNING - TrueTrack values out of realitsic range  - Manual check required!'
      IF (KEYWORD_SET(stat_lun)) THEN printf, stat_lun, 'WARNING - TrueTrack values out of realitsic range  - Manual check required!'
      IF (KEYWORD_SET(gps_err_array)) THEN gps_err_array(dummy,7)=2             
    end     
    dummy = where (min(track) LT 0, count)    
    if count GT 0 then begin
      print, 'WARNING - TrueTrack values out of realitsic range  - Manual check required!'
      IF (KEYWORD_SET(stat_lun)) THEN printf, stat_lun, 'WARNING - TrueTrack values out of realitsic range  - Manual check required!'
      IF (KEYWORD_SET(gps_err_array)) THEN gps_err_array(dummy,7)=2             
    end     
    
    
    if max(speed) EQ min(speed) then begin
      print, 'Still errors with Speed  - Manual check required!'
      IF (KEYWORD_SET(stat_lun)) THEN printf, stat_lun,'Still errors with Speed - Manual check required!'
      IF (KEYWORD_SET(gps_err_array)) THEN gps_err_array(*,8)=2
    end 
    dummy = where (max(speed) GE speed_pmax, count)
    if count GT 0 then begin
      print, 'WARNING - Speed values out of realitsic range  - Manual check required!'
      IF (KEYWORD_SET(stat_lun)) THEN printf, stat_lun, 'WARNING - Speed values out of realitsic range  - Manual check required!'
      IF (KEYWORD_SET(gps_err_array)) THEN gps_err_array(dummy,8)=2             
    end     
    dummy = where (min(speed) LE speed_pmin, count)
    if count GT 0 then begin
      print, 'WARNING - Speed values out of realitsic range  - Manual check required!'
      IF (KEYWORD_SET(stat_lun)) THEN printf, stat_lun, 'WARNING - Speed values out of realitsic range  - Manual check required!'
      IF (KEYWORD_SET(gps_err_array)) THEN gps_err_array(dummy,8)=2             
    end     

    dummy = where(sat LE 3, count)
    if count GT 0 then begin
      print, 'Still errors with Sat  - Manual check required!'
      IF (KEYWORD_SET(stat_lun)) THEN printf, stat_lun,'Still errors with Sat - Manual check required!'
      IF (KEYWORD_SET(gps_err_array)) THEN gps_err_array(dummy,9)=2
    end 

    dummy = where(dgps NE 1, count)
    if count GT 0 then begin
      print, 'Still errors with DGPS  - Manual check required!'
      IF (KEYWORD_SET(stat_lun)) THEN printf, stat_lun,'Still errors with DGPS - Manual check required!'
      IF (KEYWORD_SET(gps_err_array)) THEN gps_err_array(dummy,10)=2
    end 

  ; ----------
  ; loop it...

  dummy = size(orig_time ,/dimensions)
  for i = 0, (dummy(0)-2) do begin

    if orig_time(i) GE orig_time(i+1) then begin 
      print, 'Still errors with UTC Time Signature - Manual check required! Line ', strtrim(i,2)
      IF (KEYWORD_SET(stat_lun)) THEN printf, stat_lun,'Still errors with UTC Time Signature - Manual check required! Line ', strtrim(i,2)
      IF (KEYWORD_SET(gps_err_array)) THEN gps_err_array(i,0)=1
    end
    if abs((lat(i)-lat(i+1))) GE latlon_thresh then begin 
      print, 'Still errors with Lat - Manual check required! Line ', strtrim(i,2)
      IF (KEYWORD_SET(stat_lun)) THEN printf, stat_lun,'Still errors with Lat - Manual check required! Line ', strtrim(i,2)
      IF (KEYWORD_SET(gps_err_array)) THEN gps_err_array(i,1)=1
    end
    if abs((lon(i)-lon(i+1))) GE latlon_thresh then begin
      print, 'Still errors with Lon - Manual check required! Line ', strtrim(i,2)
      IF (KEYWORD_SET(stat_lun)) THEN printf, stat_lun,'Still errors with Lon - Manual check required! Line ', strtrim(i,2)
      IF (KEYWORD_SET(gps_err_array)) THEN gps_err_array(i,2)=1
    end
    if abs((alt(i)-alt(i+1))) GE alt_thresh then begin
      print, 'Still errors with Altitude - Manual check required! Line ', strtrim(i,2)
      IF (KEYWORD_SET(stat_lun)) THEN printf, stat_lun,'Still errors with Altitude - Manual check required! Line ', strtrim(i,2)
      IF (KEYWORD_SET(gps_err_array)) THEN gps_err_array(i,3)=1
    end
    if abs((pit(i)-pit(i+1))) GE pit_thresh then begin
      print, 'Still errors with Pitch - Manual check required! Line ', strtrim(i,2)
      IF (KEYWORD_SET(stat_lun)) THEN printf, stat_lun,'Still errors with Pitch - Manual check required! Line ', strtrim(i,2)
      IF (KEYWORD_SET(gps_err_array)) THEN gps_err_array(i,4)=1
    end
    if abs((rol(i)-rol(i+1))) GE rol_thresh then begin
      print, 'Still errors with Roll - Manual check required! Line ', strtrim(i,2)
      IF (KEYWORD_SET(stat_lun)) THEN printf, stat_lun,'Still errors with Roll - Manual check required! Line ', strtrim(i,2)
      IF (KEYWORD_SET(gps_err_array)) THEN gps_err_array(i,5)=1
    end 

; ... since heading = +-180� => use absolute values
    if abs (abs(heading(i)) - abs(heading(i+1)) ) GE heading_thresh then begin
      print, 'Still errors with Heading - Manual check required! Line ', strtrim(i,2)
      IF (KEYWORD_SET(stat_lun)) THEN printf, stat_lun, 'Still errors with Heading - Manual check required! Line ', strtrim(i,2)
      IF (KEYWORD_SET(gps_err_array)) THEN gps_err_array(i,6)=1
    end

; ... since TrueTrack = 0...360� => catch errors
    if abs((track(i)-track(i+1))) GE track_thresh then begin
      if abs((track(i)-track(i+1))) LE 359.7 then begin
        print, 'Still errors with TrueTrack - Manual check required! Line ', strtrim(i,2)
        IF (KEYWORD_SET(stat_lun)) THEN printf, stat_lun,'Still errors with TrueTrack - Manual check required! Line ', strtrim(i,2)
        IF (KEYWORD_SET(gps_err_array)) THEN gps_err_array(i,7)=1
      end
    end

    if abs((speed(i)-speed(i+1))) GE speed_thresh then begin
      print, 'Still errors with Speed - Manual check required! Line ', strtrim(i,2)
      IF (KEYWORD_SET(stat_lun)) THEN printf, stat_lun,'Still errors with Speed - Manual check required! Line ', strtrim(i,2)
      IF (KEYWORD_SET(gps_err_array)) THEN gps_err_array(i,8)=1
    end
   
  end

  print, '.gps consistency check completed'
  IF (KEYWORD_SET(stat_lun)) THEN printf, stat_lun,'.gps consistency check completed'

if (KEYWORD_SET(gps_data)) THEN begin
   dummy = size(orig_time ,/dimensions)
   gps_data = dblarr(dummy(0),11)
   gps_data(*,0) = orig_time
   gps_data(*,1) = lat
   gps_data(*,2) = lon
   gps_data(*,3) = alt
   gps_data(*,4) = pit
   gps_data(*,5) = rol
   gps_data(*,6) = heading
   gps_data(*,7) = track
   gps_data(*,8) = speed
   gps_data(*,9) = sat
   gps_data(*,10)= dgps
end

if (KEYWORD_SET(extradatum)) then begin
   extradatum = intarr(3)
   extradatum(0) =  uyear(0)
   extradatum(1) = umonth(0)
   extradatum(2) =   uday(0)
end

end

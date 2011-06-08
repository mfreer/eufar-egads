pro test_gps

;+
; NAME:
; test_gps
;
; PURPOSE:
; tests nav file as produced with HyMap datasets for inconsistencies
;
; CATEGORY:
;
; CALLING SEQUENCE:
;
; INPUTS:
;
; OPTIONAL INPUTS:
;
; KEYWORD PARAMETERS:
;
; OUTPUTS:
;
; OPTIONAL OUTPUTS:
;
; COMMON BLOCKS:
;
; SIDE EFFECTS:
;
; RESTRICTIONS:
;
;
;
; PROCEDURE:
;
;
;
; EXAMPLE:
;
;
;
; MODIFICATION HISTORY:
;
;-

; 1. Find all gps files from the current directory downwards
SPAWN, 'find * -name *.gps', files, count=count;, /NOSHELL
data = strarr(7,count)

; For each and every file do:
for i=0, count-1 do begin
    counter=0
    warning=strarr(7)
    ; 2. Read GPS file
    hymap_read_gps, filen=files(i), uyear=uyear, umonth=umonth, uday=uday, uhour=uhour, umin=umin, usec=usec, urest=urest, lat=lat, lon=lon, alt=alt, pit=pit, rol=rol, heading=heading, track=track, speed=speed, sat=sat, dgps=dgps
    ; 3. Check heading
    headmean = mean(abs(heading))
    if headmean gt 180 then headmean = headmean-360

    if max(heading)-min(heading) gt 20 then begin
        if max(heading)-min(heading) gt 355 then begin
            absmean=mean(abs(heading))
            for j=0, n_elements(heading)-1 do begin
                if absmean - abs(heading(j)) gt 5 then begin
                
                    heading(j)=179.999
                endif 
            endfor
            warning(1) = 'changed some heading values!'
        endif else Warning(1) = 'The heading shows large differences'
        counter=counter+1
    endif
    
    ; 4. latitude
    latmean = mean(lat)
    latstabw = stdev(lat)
    if latstabw eq 0 then begin
        warning(2) = 'there are no changes in the latitude'
        counter=counter+1
    endif

    ; 5. longitude
    lonmean = mean(lon)
    lonstabw = stdev(lon)
    if lonstabw eq 0 then begin
        warning(3) = 'there are no changes in the longitude'
        counter = counter+1
    endif

    ; 6. roll
    rolmean=mean(rol)
    if max(rol) - min(rol) gt 5 then begin
        warning(4) = 'there are large changes in the roll'
        if mean(rol) gt 3 then begin
            warning(4) = 'the values of roll are large and there are large changes'
        endif
        counter=counter+1
    endif else if mean(rol) gt 3 then begin
        warning(4) = 'the values of roll are large'
        counter=counter +1
    endif

    ; 7. pitch
    pitmean = mean(pit)
    if max(pit) - min(pit) gt 5 then begin 
        warning(5) = 'there are large changes in the pitch'
        if mean(pit) gt 3 then begin
            warning(5) = 'the values of pitch are large and there are large changes'
            counter=counter + 1
        endif
    endif else if mean(pit) gt 3 then begin
        warning(5) = 'the values of pitch are large'
        counter=counter+1
    endif

    ; 8. altitude
    altmean = mean(alt)
   if max(alt) - min(alt) gt 50 then begin
       warning(6) = 'there are large changes in the altitude'
       counter=counter+1
   endif

   if min(alt) lt 1000 then begin
       warning(6) = 'the flight altitude seems to be too deep'
       counter=counter+1
   endif
   find = strpos(files(i),'/', /reverse_search)
   scene = strmid(files(i), find+1)
   if counter gt 0 then begin
       warning(0)=files(i)
       err_file = scene + '.war'
       openw, 1, err_file
       for l=0,6 do printf, 1, warning(l) 
       close, 1
       
   endif
   data(0,i)= scene
   data(1,i)= headmean
   data(2,i)= altmean
   data(3,i)= latmean
   data(4,i)= lonmean
   data(5,i)= uhour(0)
   data(6,i)= umin(0)
   
endfor
openw, 1, 'gps-data.txt'
printf, 1, 'scene, heading, altitude, latitude, longitude, time'
for k=0, count-1 do printf, 1, data(*,k)
close, 1


end

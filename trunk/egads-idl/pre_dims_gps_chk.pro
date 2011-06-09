;+
; NAME:
;   pre_dims_gps_chk
;
; PURPOSE:
;   Check and correct .gps - File
;   
; CATEGORY:
;		
; CALLING SEQUENCE:
;   pre_dims_gps_chk, fname = name_tmp, linenumb_hdr = linenumb_hdr, stat_lun=stat_lun
;
; INPUTS:
;    fname => base-filename WITH .gps - suffix !
;    linenumb_hdr => #Image-Lines according to .hdr
;
; OPTIONAL INPUTS:
;	
; KEYWORD PARAMETERS:
;
; OUTPUTS:
;   status file => template+'_status'
;
;   if applicable: 
;     corrected gps file
;     backup of original .gps => filename.gps_original
;
; OPTIONAL OUTPUTS:
;
; COMMON BLOCKS:
;
; SIDE EFFECTS:
;
; RESTRICTIONS:
;
; PROCEDURE:
;   test & correct the following
;   - point or colon - separator in .gps => error catched in hymap_read_gps.pro
;     corrected when re-writing the .gps-file anyway
;   - #lines in image  =  #lines in gps
;     if too many gps-lines: truncate lines at beginning (like Hyvista does)
;     if too few gps-lines:  adding extrapolated lines at end
;   - invalid start / end time: calculating average timestep & using last relieable line
;   - data gaps (indicated by identical time): interpolate info
;
; EXAMPLE:
;
; MODIFICATION HISTORY:
; 2006/05/10   Documentation finished by Martin Bachmann, DLR-DFD-UG  	
; 
; TODO: 
; 
; 
;-

pro pre_dims_gps_chk, fname = name_tmp, linenumb_hdr = linenumb_hdr, stat_lun=stat_lun

; -----------------------------------------
; read .gps file

gps_error = 0
gps_missing = 0
lines_to_trunc = -1
lines_to_add = -1

fname = name_tmp
; print, name_tmp


hymap_read_gps, filename=name_tmp, uyear=uyear, umonth=umonth, uday=uday, uhour=uhour, umin=umin, usec=usec, $
  urest=urest, lat=lat, lon=lon, alt=alt, pit=pit, rol=rol, heading=heading, track=track, speed=speed, sat=sat, dgps=dgps



; ---------------------------------------------
; point or colon - separator in .gps - File
; => error is already catched in the hymap_read_gps.pro
; no need to adjust this... but when re-writing the .gps-file
; anyway, separator is corrected, too (see in "double lines" below)




; ---------------------------------------------
; check if #lines in image  =  #lines in gps
; and fix it

; linenumb_hdr => enth�lt #lines aus dem header

linenumb_gps = size(uday ,/dimensions)
linenumb_gps = linenumb_gps(0)


if linenumb_hdr LT linenumb_gps then begin
    gps_error = 4
    print, 'Error - more GPS-lines than image lines. Truncating the .gps file'
    print, 'header: ',strtrim(linenumb_hdr,2), ' gps: ',strtrim(linenumb_gps,2)
    IF (KEYWORD_SET(stat_lun)) THEN printf, stat_lun,'Error - more GPS-lines than image lines. Truncating the .gps file'
    IF (KEYWORD_SET(stat_lun)) THEN printf, stat_lun,'header: ',strtrim(linenumb_hdr,2), ' gps: ',strtrim(linenumb_gps,2)

    lines_to_trunc = linenumb_gps - linenumb_hdr

    ; truncate when writing the file

end


if linenumb_hdr GT linenumb_gps then begin
  gps_error = 5
  gps_missing = 1
  print, 'Error - less GPS-lines than image lines. Dublicating last GPS info'
  IF (KEYWORD_SET(stat_lun)) THEN printf, stat_lun,'Error - less GPS-lines than image lines. Dublicating last GPS info'
  lines_to_add = linenumb_hdr - linenumb_gps

  ; add lines when writing the file

end 


; ---------------------------------------------
; invalid start time at beginning of .gps

orig_time = urest + usec + 60*umin + 60*60*uhour

   ; !!! recently compare line 0 with line 40
   ; !!! there are better ways to do this ;)

if orig_time(0) GT orig_time(40) then begin

  print, 'Correcting Error: incorrect GPS start time'
  IF (KEYWORD_SET(stat_lun)) THEN printf, stat_lun,'Correcting Error: incorrect GPS start time'

  gps_error = 1

  ; calculate mean timestep
  if orig_time(22) NE orig_time (23) then begin
     dummy = abs((orig_time(22)-orig_time(23))/2)
  end else begin
     if orig_time(42) NE orig_time (43) then begin
        dummy = abs((orig_time(42)-orig_time(43))/2)
     end else begin
        if orig_time(142) NE orig_time (143) then begin
          dummy = abs((orig_time(42)-orig_time(43))/2)
        end else begin
          print, 'Trouble: Tested for average time step and 3 samples lead to error. Can not continue. Is GPS-File messy?'
          ; retall ????????????
        end
     end
  end

  ; print, 'Timestep is ', dummy

  ; find the first correct line: (using MIN is intentially avoided!)
  first_correct = 1
  while orig_time(first_correct) EQ orig_time(first_correct-1) do first_correct = first_correct + 1

  ; print, 'First correct line: ', first_correct

  ; count backwards from last correct time using timestep in "dummy"
  for i = 0, first_correct-1 do begin
    orig_time(i) = orig_time(first_correct) - ((first_correct-i)*dummy)
    ; print, 'Line ', strtrim(i,2) , ' was ', strtrim(orig_time(i),2), ' now: ', strtrim(orig_time(i),2)
  end

  ;  copy the other info from that line which is  lat, lon, alt, pit, rol, heading, track, speed, sat, dgps
  lat(0:first_correct-1) = lat(first_correct)
  lon(0:first_correct-1) = lon(first_correct)
  alt(0:first_correct-1) = alt(first_correct)
  pit(0:first_correct-1) = pit(first_correct)
  rol(0:first_correct-1) = rol(first_correct)
  heading(0:first_correct-1) = heading(first_correct)
  track(0:first_correct-1) = track(first_correct)
  speed(0:first_correct-1) = speed(first_correct)
  sat(0:first_correct-1) = sat(first_correct)
  dgps(0:first_correct-1) = dgps(first_correct)

end


; ---------------------------------------------
; invalid start time at end of .gps

nline = size(orig_time ,/dimensions)
nline = nline(0)
nline = nline - 1


; compare last two lines

if orig_time(nline) EQ orig_time(nline-1) then begin

  print, 'Correcting Error: incorrect GPS end time'
  IF (KEYWORD_SET(stat_lun)) THEN printf, stat_lun,'Correcting Error: incorrect GPS end time'

  gps_error = 1

  ; calculate mean timestep
  if orig_time(22) NE orig_time (23) then begin
     dummy = abs((orig_time(22)-orig_time(23))/2)
  end else begin
     if orig_time(42) NE orig_time (43) then begin
        dummy = abs((orig_time(42)-orig_time(43))/2)
     end else begin
        if orig_time(142) NE orig_time (143) then begin
          dummy = abs((orig_time(42)-orig_time(43))/2)
        end else begin
          print, 'Trouble: Tested for average time step and 3 samples lead to error. Can not continue. Is GPS-File messy?'
          IF (KEYWORD_SET(stat_lun)) THEN printf, stat_lun,'Trouble: Tested for average time step and 3 samples lead to error. Can not continue. Is GPS-File messy?'
          ; retall ????????????
        end
     end
  end

  ; print, 'Timestep is ', dummy

  ; find the last correct line: (using MIN is intentially avoided!)
  last_correct = nline
  while orig_time(last_correct) EQ orig_time(last_correct-1) do last_correct = last_correct - 1
  last_correct = last_correct - 1

  ; print, 'last correct line: ', last_correct

  ; count forward from last correct time using timestep in "dummy"



  for i = (last_correct(0)+1), nline do begin
    orig_time(i) = orig_time(i-1) + dummy
  end

  ;  copy the other info from that line which is  lat, lon, alt, pit, rol, heading, track, speed, sat, dgps
  lat(last_correct:*) = lat(last_correct)
  lon(last_correct:*) = lon(last_correct)
  alt(last_correct:*) = alt(last_correct)
  pit(last_correct:*) = pit(last_correct)
  rol(last_correct:*) = rol(last_correct)
  heading(last_correct:*) = heading(last_correct)
  track(last_correct:*) = track(last_correct)
  speed(last_correct:*) = speed(last_correct)
  sat(last_correct:*) = sat(last_correct)
  dgps(last_correct:*) = dgps(last_correct)

end



; ---------------------------------------------
; double lines in .gps

dummy = size(orig_time ,/dimensions)
err_doppelt = intarr(2,100)
err_anzahl = -1
my_flag = 0



for i = 0, (dummy(0)-2) do begin
 if orig_time(i) EQ orig_time(i+1) then begin
   gps_error = 2

   if my_flag EQ 0 then begin
     err_anzahl = err_anzahl+1
     my_flag = 1
     err_doppelt(0,err_anzahl) = i
   end

 end else begin
   if my_flag EQ 1 then begin
     my_flag = 0
     err_doppelt(1,err_anzahl) = i
   end
 end

end




if gps_error EQ 2 then begin

 for i = 0, (err_anzahl) do begin 


   err_startrow = err_doppelt(0,i)
   err_endrow = err_doppelt(1,i)

    print, 'Correcting Error: dublicated info between lines ', strtrim(err_startrow,2) , ' and ', strtrim(err_endrow,2)
    IF (KEYWORD_SET(stat_lun)) THEN printf, stat_lun,'Correcting Error: dublicated info between lines ', strtrim(err_startrow,2) , ' and ', strtrim(err_endrow,2)
    ; print, 'Correcting the errors...' 

    ; number of points to interpolate:
    ; (endrow-startrow+1) are missing
    ; plus include one point left & right => 3
    err_numb = (err_endrow - err_startrow)+3

       ; initialisiere array mit var_typ & 2 feldern

       ; dummy[0] = my_arr(j,err_startrow-1)
       ; dummy[1] = my_arr(j,err_endrow+1)

       ; corrected = interpol (dummy, err_numb)
       ; my_arr(j,err_startrow-1:err_endrow+1) = corrected

  dummy = [0d,0d]
  dummy(0) = orig_time(err_startrow-1)
  dummy(1) = orig_time(err_endrow+1)
  corrected = interpol(dummy, err_numb)
  orig_time(err_startrow-1:err_endrow+1) = corrected

  dummy(0) = lat(err_startrow-1)
  dummy(1) = lat(err_endrow+1)
  corrected = interpol(dummy, err_numb)
  lat(err_startrow-1:err_endrow+1) = corrected

  dummy(0) = lon(err_startrow-1)
  dummy(1) = lon(err_endrow+1)
  corrected = interpol(dummy, err_numb)
  lon(err_startrow-1:err_endrow+1) = corrected

  dummy(0) = alt(err_startrow-1)
  dummy(1) = alt(err_endrow+1)
  corrected = interpol(dummy, err_numb)
  alt(err_startrow-1:err_endrow+1) = corrected

  dummy(0) = pit(err_startrow-1)
  dummy(1) =pit(err_endrow+1)
  corrected = interpol(dummy, err_numb)
  pit(err_startrow-1:err_endrow+1) = corrected

  dummy(0) = rol(err_startrow-1)
  dummy(1) = rol(err_endrow+1)
  corrected = interpol(dummy, err_numb)
  rol(err_startrow-1:err_endrow+1) = corrected

  dummy(0) = heading(err_startrow-1)
  dummy(1) = heading(err_endrow+1)
  corrected = interpol(dummy, err_numb)
  heading(err_startrow-1:err_endrow+1) = corrected

  dummy(0) = track(err_startrow-1)
  dummy(1) = track(err_endrow+1)
  corrected = interpol(dummy, err_numb)
  track(err_startrow-1:err_endrow+1) = corrected

  dummy(0) = speed(err_startrow-1)
  dummy(1) = speed(err_endrow+1)
  corrected = interpol(dummy, err_numb)
  speed(err_startrow-1:err_endrow+1) = corrected

;  ; ? does interpol make sense for SAT ?
;  dummy(0) = sat(err_startrow-1)
;  dummy(1) = sat(err_endrow+1)
;  corrected = interpol(dummy, err_numb)
;  sat(err_startrow-1:err_endrow+1) = corrected
;
;  ; ? does interpol make sense for DGPS ?
;  dummy(0) = dgps(err_startrow-1)
;  dummy(1) = dgps(err_endrow+1)
;  corrected = interpol(dummy, err_numb)
;  dgps(err_startrow-1:err_endrow+1) = corrected

 end
 ; des fuer_jeden_fehler

end
; des fuer_gps_error=2

; ---------------------------------------------------------
; in case of gps errors:
; rewrite the .gps file, this time with correct separator


if gps_error NE 0 then begin

   

   ; first backup the original file:
   dummy = fname
   dummy2 = dummy + '_original'
   SPAWN, 'cp ' + dummy + ' ' + dummy2
   print, 'Creating backup & Writing corrected .gps file: ', dummy
   IF (KEYWORD_SET(stat_lun)) THEN printf, stat_lun, 'Creating backup & Writing corrected .gps file: ', dummy

   line = ''
   OPENR, unit, dummy2, /GET_LUN
   openw, unit2, dummy, /get_lun

   ; keep the first header row
   READF, unit, line
   printf, unit2, line

   line_nr = 0
   WHILE NOT(EOF(unit)) DO BEGIN
     READF, unit, line

     if line_nr GE lines_to_trunc then begin
       line = strsubst(str=line, search=',', subst='.')
       sub1 = strmid(line, 0, strpos(line, '/'))
       sub2 = strmid(line, strpos(line, '/')+1, STRLEN(line)-strpos(line, '/'))  
       sub2_1 = STRMID(sub2, 0, 10)
       sub2_2 = STRMID(sub2, 11, STRLEN(sub2)-10)  
       restline = STRSPLIT(sub2_2, ' ', /extract) 

       ; orig_time is missing one tailing position, thus fill in a 0 and insert a /
       utc_format = string(orig_time)+'0/'
;       utc_format = string(orig_time(1))+'0/'


     ; Format:            zeile         utc_zeit    datum       vme               cmi

       ; if #lines is correct
       if lines_to_trunc EQ -1 then begin
         ttt = strtrim((line_nr+1),0) + ' ' + strtrim(utc_format(line_nr)) + sub2_1 + ' ' + restline(0) + ' ' + restline(1) + ' ' + strtrim(lat(line_nr)) $ 
            + ' ' + strtrim(lon(line_nr)) + ' ' + strtrim(alt(line_nr)) + ' ' + strtrim(pit(line_nr)) + ' ' + strtrim(rol(line_nr)) + ' ' + $
           strtrim(heading(line_nr)) + ' ' + strtrim(track(line_nr)) + ' ' + strtrim(speed(line_nr)) + ' ' + restline(10)+ ' '+ restline(11)

       ; if too much gps lines
       end else begin
         temp2 = (line_nr+1)-lines_to_trunc
         ttt = strtrim(temp2,0) + ' ' + strtrim(utc_format(line_nr)) + sub2_1 + ' ' + restline(0) + ' ' + restline(1) + ' ' + strtrim(lat(line_nr)) $ 
            + ' ' + strtrim(lon(line_nr)) + ' ' + strtrim(alt(line_nr)) + ' ' + strtrim(pit(line_nr)) + ' ' + strtrim(rol(line_nr)) + ' ' + $
           strtrim(heading(line_nr)) + ' ' + strtrim(track(line_nr)) + ' ' + strtrim(speed(line_nr)) + ' ' + restline(10)+ ' '+ restline(11)
       end

      printf, unit2, ttt

;     printf, unit2, (line_nr+1), ' ', utc_format(line_nr), sub2_1,' ', restline(0), ' ', restline(1), ' ', lat(line_nr), ' ', lon(line_nr), ' ',$
;        alt(line_nr), ' ', pit(line_nr), ' ', rol(line_nr), ' ', heading(line_nr), ' ', track(line_nr), ' ', speed(line_nr), ' ', $
;        restline(10), ' ', restline(11)


     end

     line_nr = line_nr +1
   ENDWHILE


   ; ------------------------
   ; if gps lines are missing: 
 

   if gps_missing EQ 1 then begin

     neu_line = line_nr
     neu_time = orig_time(line_nr-1)

     ; first go back to last valid line
     line_nr = line_nr -1

     ; calculate mean timestep
     if orig_time(22) NE orig_time (23) then begin
        dummyt = abs((orig_time(22)-orig_time(23))/2)
     end else begin
        if orig_time(42) NE orig_time (43) then begin
           dummyt = abs((orig_time(42)-orig_time(43))/2)
        end else begin
           if orig_time(142) NE orig_time (143) then begin
            dummyt = abs((orig_time(42)-orig_time(43))/2)
           end else begin
             print, 'Trouble: Tested for average time step and 3 samples lead to error. Can not continue. Is GPS-File messy?'
             ; retall ????????????
           end
        end
     end

    ; add new linenr & time & copy rest of last line
    for nnn = 0, (lines_to_add-1) do begin

       ; orig_time is missing one tailing position, thus fill in a 0 and insert a /

        neu_line = neu_line + 1
        neu_time = neu_time + dummyt
       
        utc_neu_time = string(neu_time)+'0/'

        ttt = strtrim((neu_line),0) + '     ' + strtrim(utc_neu_time,2) + sub2_1 + ' ' + restline(0) + ' ' + restline(1) + ' ' + strtrim(lat(line_nr)) $ 
            + ' ' + strtrim(lon(line_nr)) + ' ' + strtrim(alt(line_nr)) + ' ' + strtrim(pit(line_nr)) + ' ' + strtrim(rol(line_nr)) + ' ' + $
           strtrim(heading(line_nr)) + ' ' + strtrim(track(line_nr)) + ' ' + strtrim(speed(line_nr)) + ' ' + restline(10)+ ' '+ restline(11)
        printf, unit2, ttt
    end
   end



   FREE_LUN, unit
   FREE_LUN, unit2

   ; correct the fu__ing linebreak of the header  
    concat_lines, dummy, outfile=dummy

end


end

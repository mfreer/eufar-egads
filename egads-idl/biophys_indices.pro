pro biophys_indices, event

;+
; NAME:
;   biophys_indices
;
; PURPOSE:
;   calculation of biophysical indices for IMAGES
;  
; CATEGORY:
;  PhD Martin Bachmann
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
; PROCEDURE:
; 
; EXAMPLE:
;
; MODIFICATION HISTORY:
;   2009-01-26: prog & documentation finished (Martin Bachmann, DLR-DFD-US)
;
;-

; => fuer Bilder


; fuer SLBs:   biophys_indices_slb.pro



; siehe auch: red_edge_inf_2
; und resi_unmix_anal_2
; und spec_class_4



; --------------------------------------------------------------------------
; Inputs and Initialization:

IF (NOT(KEYWORD_SET(fid_img))) THEN begin
  ENVI_SELECT, fid=fid_img, /roi, file_type=envi_file_type('ENVI Standard'), pos=pos_img, dims=dims_img, /mask, m_fid=fid_mask ,m_pos=pos_mask ,TITLE='Reflectance Image File'
end

dum = WHERE(pos_img GT 0, count)

; stop criterion: no file selected
IF (fid_img[0] EQ -1) THEN BEGIN
    print, "ERROR: No File selected !"
    RETURN
ENDIF

; Find filename, wavelengths, and bandnames of Image
ENVI_FILE_QUERY, fid_img, wl=wavel_img, bnames=bnames, fname=fname, fwhm=fwhm_img
IF (wavel_img[0] EQ -1) THEN wavel_img = INDGEN(count)

; ensure Micrometers
if wavel_img(1) GT 10 then wavel_img = wavel_img / 1000


fid=fid_img
dims=dims_img
pos=pos_img
nbnds = N_ELEMENTS(pos)
nrows = dims[4]-dims[3]+1
ncols = dims[2]-dims[1]+1


; output files:
;rededge_pos = fltarr(ncols,nrows)
;bildraus_dgvi1 = fltarr(ncols,nrows)
;bildraus_dgvi2 = fltarr(ncols,nrows)
;bildraus_maxslope = fltarr(ncols,nrows)

ndvi = fltarr(ncols,nrows)
mcari = fltarr(ncols,nrows)
lci =  fltarr(ncols,nrows)
sr =   fltarr(ncols,nrows)
mnd =  fltarr(ncols,nrows)

	rvi = fltarr(ncols,nrows)
	gi = fltarr(ncols,nrows)

pri =  fltarr(ncols,nrows)
re_pos = fltarr(ncols,nrows)
re_pos_sav1 = fltarr(ncols,nrows)
re_pos_sav2 = fltarr(ncols,nrows)

dgvi1= fltarr(ncols,nrows)
dgvi2= fltarr(ncols,nrows)

ndni = fltarr(ncols,nrows)
ndli = fltarr(ncols,nrows)
cai  = fltarr(ncols,nrows)
ndwi = fltarr(ncols,nrows)
lwvi1= fltarr(ncols,nrows)
lwvi2= fltarr(ncols,nrows)
mirndwi = fltarr(ncols,nrows)
dwsi = fltarr(ncols,nrows)
; csi1 = fltarr(ncols,nrows)
csi2 = fltarr(ncols,nrows)
swirvi=fltarr(ncols,nrows)
swirli=fltarr(ncols,nrows)
swirsi=fltarr(ncols,nrows)


	clay_1 = fltarr(ncols,nrows)
	iron_1 = fltarr(ncols,nrows)


; -------------------------
; Create Savitzky-Golay-Filter-Kernel:

; sav_0 = SAVGOL(4,4,0,3)

sav_1 = SAVGOL(4,4,1,3)
sav_2 = SAVGOL(4,4,2,3)

; sav_3 = SAVGOL(4,4,3,4)
; sav_4 = SAVGOL(4,4,4,4)


; -------------------------
; search for features...
; difference between min & max of about 0.02

; dummy = where (((wavel_img GE 0.41) AND (wavel_img LE 0.43)), count)
; if count GE 1 then p_420  = MAX(dummy) else p_420 = -1

dummy = where (((wavel_img GE 0.44) AND (wavel_img LE 0.452)), count)
if count GE 1 then p_440  = MAX(dummy) else p_440 = -1

dummy = where (((wavel_img GE 0.52) AND (wavel_img LE 0.54)), count)
if count GE 1 then p_529  = MAX(dummy) else p_529 = -1

dummy = where (((wavel_img GE 0.53) AND (wavel_img LE 0.556)), count)
if count GE 1 then p_549  = MAX(dummy) else p_549 = -1

dummy = where (((wavel_img GE 0.55) AND (wavel_img LE 0.571)), count)
if count GE 1 then p_569  = MAX(dummy) else p_569 = -1

dummy = where (((wavel_img GE 0.66) AND (wavel_img LE 0.678)), count)
if count GE 1 then p_671  = MAX(dummy) else p_671 = -1

dummy = where (((wavel_img GE 0.67) AND (wavel_img LE 0.693)), count)
if count GE 1 then p_680  = MAX(dummy) else p_680 = -1

dummy = where (((wavel_img GE 0.69) AND (wavel_img LE 0.71)), count)
if count GE 1 then p_701  = MAX(dummy) else p_701 = -1

dummy = where (((wavel_img GE 0.706) AND (wavel_img LE 0.724)), count)
if count GE 1 then p_710  = MAX(dummy) else p_710 = -1

dummy = where (((wavel_img GE 0.73) AND (wavel_img LE 0.75)), count)
if count GE 1 then p_740  = MIN(dummy) else p_740 = -1

dummy = where (((wavel_img GE 0.75) AND (wavel_img LE 0.77)), count)
if count GE 1 then p_760  = MAX(dummy) else p_760 = -1

dummy = where (((wavel_img GE 0.77) AND (wavel_img LE 0.799)), count)
if count GE 1 then p_780  = MIN(dummy) else p_780 = -1

dummy = where (((wavel_img GE 0.79) AND (wavel_img LE 0.814)), count)
if count GE 1 then p_803  = MIN(dummy) else p_803 = -1

dummy = where (((wavel_img GE 0.84) AND (wavel_img LE 0.859)), count)
if count GE 1 then p_850  = MAX(dummy) else p_850 = -1

dummy = where (((wavel_img GE 0.85) AND (wavel_img LE 0.875)), count)
if count GE 1 then p_864  = MAX(dummy) else p_864 = -1

dummy = where (((wavel_img GE 0.911) AND (wavel_img LE 0.930)), count)
if count GE 1 then p_920  = MAX(dummy) else p_920 = -1

dummy = where (((wavel_img GE 0.970) AND (wavel_img LE 0.990)), count)
if count GE 1 then p_980  = MAX(dummy) else p_980 = -1

dummy = where (((wavel_img GE 1.080) AND (wavel_img LE 1.100)), count)
if count GE 1 then p_1090  = MAX(dummy) else p_1090 = -1

dummy = where (((wavel_img GE 1.190) AND (wavel_img LE 1.210)), count)
if count GE 1 then p_1200  = MAX(dummy) else p_1200 = -1

dummy = where (((wavel_img GE 1.24) AND (wavel_img LE 1.257)), count)
if count GE 1 then p_1245  = MIN(dummy) else p_1245 = -1

dummy = where (((wavel_img GE 1.5) AND (wavel_img LE 1.52)), count)
if count GE 1 then p_1510  = MIN(dummy) else p_1510 = -1

dummy = where (((wavel_img GE 1.645) AND (wavel_img LE 1.67)), count)
if count GE 1 then p_1659  = MAX(dummy) else p_1659 = -1

dummy = where (((wavel_img GE 1.67) AND (wavel_img LE 1.69)), count)
if count GE 1 then p_1680  = MIN(dummy) else p_1680 = -1

dummy = where (((wavel_img GE 1.74) AND (wavel_img LE 1.76)), count)
if count GE 1 then p_1754  = MIN(dummy) else p_1754 = -1



dummy = where (((wavel_img GE 2.007) AND (wavel_img LE 2.028)), count)
if count GE 1 then p_2015 = MIN(dummy) else p_2015 = -1

dummy = where (((wavel_img GE 2.08) AND (wavel_img LE 2.11)), count)
if count GE 1 then p_2090 = MIN(dummy) else p_2090 = -1

dummy = where (((wavel_img GE 2.098) AND (wavel_img LE 2.119)), count)
if count GE 1 then p_2106 = MIN(dummy) else p_2106 = -1

	dummy = where (((wavel_img GE 2.115) AND (wavel_img LE 2.137)), count)
	if count GE 1 then p_2136 = MAX(dummy) else p_2136 = -1

dummy = where (((wavel_img GE 2.15) AND (wavel_img LE 2.172)), count)
if count GE 1 then p_2161 = MIN(dummy) else p_2161 = -1

dummy = where (((wavel_img GE 2.187) AND (wavel_img LE 2.207)), count)
if count GE 1 then p_2195 = MIN(dummy) else p_2195 = -1

dummy = where (((wavel_img GE 2.20) AND (wavel_img LE 2.224)), count)
if count GE 1 then p_2210 = MIN(dummy) else p_2210 = -1

	dummy = where (((wavel_img GE 2.238) AND (wavel_img LE 2.26)), count)
	if count GE 1 then p_2240 = MIN(dummy) else p_2240 = -1



dummy = where (((wavel_img GE 2.27) AND (wavel_img LE 2.299)), count)
if count GE 1 then p_2280 = MIN(dummy) else p_2280 = -1


; -------------------------------------------
; main loop

FOR irow=dims[3], dims[4] DO BEGIN
  specvec = FLOAT(ENVI_GET_SLICE(fid=fid, pos=pos, line=irow, xs=dims[1], xe=dims[2], /bil))

  FOR icol = 0, ncols-1 DO BEGIN
    spec = reform( specvec(icol,*) )



; -------------------------


; NDVI 
; (864 - 671) / (864 + 671)
; ggf. als Maske > 0.5
ndvi(icol,irow) = (spec(p_864) - spec(p_671)) / (spec(p_864) + spec(p_671))


; Modified Chlorophyll absorption in Reflectance
; ((701 - 671) - 0.2* (701 - 549)) * (701 / 671)
mcari(icol,irow) = (spec(p_701) - spec(p_671)) - 0.2* (spec(p_701)-spec(p_549)) *(spec(p_701) / spec(p_671)) 


; LCI Leaf Chlorophyll Index = f(Chloro.content)
; LCI = (850 - 710) / (850 - 680)
lci(icol,irow) = (spec(p_850) - spec(p_710)) / (spec(p_850) + spec(p_710))


;  Chlorophyll-Index SR705 // linear regression
; (Sims et al RSENVI 2002)
; 750 / 705
if spec(p_701) NE 0 then sr(icol,irow) = (spec(p_760) / spec(p_701))


; Chlorophyll-Index mND704 // hyperbolic regression 
; (Sims et al RSENVI 2002)
; (750 - 705) / (750 + 705 - 2*445)
mnd(icol,irow) = (1. * spec(p_760) - spec(p_701)) / (spec(p_760) + spec(p_701) - (2*spec(p_440) ) )



; Photochemical reflectance PRI
; auch : Carotenoid / chlorophyll (Sims et al RSENVI 2002)
; (529 - 569) / (529 + 569)
pri(icol,irow) = (spec(p_529) - spec(p_569)) / (spec(p_529) + spec(p_569))



	; my Green Ratio
	; GP : RED : NIR
	; _1 = (870 / 670 ) => pot. Green
	; _2 = (549 / 670 ) => really Green

; RVI: Ratio vegetation index
; old: greeness_ration_1 = (870 / 670 ) => pot. Green
rvi(icol, irow) = spec(p_864) / spec(p_671)

; Greeness index
; old: greeness_ration_2 = (670/550) => really Green
gi(icol, irow) = spec(p_671) / spec(p_549)




; -------- RedEdge --------

; red edge infliction point method 1
; Re = (670 + 780) /2
; Re_position = 700 + 40 * (( Re - 700) / (740 - 700))


; re_pos = 700. + 40 * ( ( ( 0.5* (spec(p_671) + spec(p_780) ) - spec(p_701)) / (spec(p_749) - spec(p_700)) )
re_pos(icol,irow) = 700. + 40 * ( (  (0.5*(spec(p_671)+spec(p_780))) - spec(p_701))  / (spec(p_740) - spec(p_701))   )


		; TODO
		; red edge via SavGol
		; between 691 and 763


; Derivate Indices 
; DGVI als flaeche unter 1. und 2. ableitung (savgol mit polynom 3. ordnung)
; red edge position via max der 1. ableitung
;                   und nullstelle der 2. ableitung => DIES IST BESSER !!!!!

 dummy = convol (spec, sav_1,/edge_truncate)
 dgvi1(icol,irow) = total(abs (dummy(p_680:p_760)) )

 dummy = where (dummy(p_680:p_760) EQ max(dummy(p_680:p_760)) , count)

; noch baender vorher hinzuaddieren
  dummy = dummy + p_680

 if count EQ 1 then re_pos_sav1(icol,irow) = float(wavel_img(dummy))

 dummy = convol (spec, sav_2,/edge_truncate)
 dgvi2(icol,irow) = total(abs (dummy(p_680:p_760)) )

 ; fuer jedes band im bereich...
 for mypos = p_680, p_760-1 do begin
   if dummy(mypos) GE 0 AND dummy(mypos+1) LE 0 then begin
     re_pos_sav2(icol,irow) = float(wavel_img(mypos))
   end
   if dummy(mypos) LE 0 AND dummy(mypos+1) GE 0 then begin
     re_pos_sav2(icol,irow) = float(wavel_img(mypos))
   end
 end



; -------- Dry --------

; nach Serrano '02:
; for shrub vegetation:
; Normalized Difference Nitrogen Index 
; (NDNI = [log (1/R1510) - log (1/R1680)]/[log (1/R1510) + log (1/R1680)]) 

ndni(icol,irow) = (alog10 (1./spec(p_1510)) - alog10 (1/spec(p_1680))) / (alog10 (1/spec(p_1510)) + alog10 (1/spec(p_1680)))


; Normalized Difference Lignin Index 
; (NDLI = [log (1/R1754) - log (1/R1680)]/ [log (1/R1754) + log (1/R1680)]) 

ndli(icol,irow) = (alog10 (1./spec(p_1754)) - alog10 (1/spec(p_1680))) / (alog10 (1/spec(p_1754)) + alog10 (1/spec(p_1680)))

; CAI cellulose absorption index (CAI)
; calculated as: CAI = 0.5(R2.0 + R2.2)-R2.1; where R2.0, R2.1,

cai(icol,irow) = 0.5 * (spec(p_2015) + spec(p_2195)) - spec(p_2106)

; -------- Water --------

; NDWI
; (864 - 1245) / (864 + 1245)
ndwi(icol,irow) = (spec(p_864) - spec(p_1245)) / (spec(p_864) + spec(p_1245))

; Leaf Water Vegetation Index LWVI-1
; (1094 - 983) / (1094 + 983) 
lwvi1(icol, irow) = (spec(p_1090)-spec(p_980)) / (spec(p_1090)+spec(p_980))

; Leaf Water Vegetation Index LWVI-2
; (1094 - 1205) (1094 + 1205) 
lwvi2(icol, irow) = (spec(p_1090)-spec(p_1200)) / (spec(p_1090)+spec(p_1200))

; mIR-NDWI = (864.1 - 2161.6) / (864.1 + 2161.6)
mirndwi(icol,irow) = (spec(p_864) - spec(p_2161)) / (spec(p_864) + spec(p_2161))


; -------- Stress --------

; Disease Water Stress Index
; (803 + 549) / (1659 + 681)
dwsi(icol,irow) = (spec(p_803) + spec(p_549)) / (spec(p_1659) + spec(p_680))


	; RedEdge Vegetation Stress
	; ((712 + 752) / 2) - 732

	; carter stress 1
	; 695 / 420

; carter stress 2
; 695 / 760
csi2(icol,irow) = spec(p_701) / spec(p_760)


; -----------------------------------------------
; nach LOBELL '01:
; SWIR-Indices ~ Cover%
; Green: SWIRVI = 37,72(2210 - 2090) + 26.27(2280 - 2090) + 0.57
swirvi(icol,irow) = 37.72 * (spec(p_2210) - spec(p_2090) ) + 26.27 * (spec(p_2280) - spec(p_2090) ) + 0.57

; Litter: SWIRLI = 3,87(2210 - 2090) - 27,51 (2280 - 2090) - 0,20
swirli(icol,irow) = 3.87 * (spec(p_2210) - spec(p_2090) ) + 27.51 * (spec(p_2280) - spec(p_2090) ) - 0.2

; Soil: SWIRSI= -41.59 (2210-2090) + 1.24 (2280 - 2090) + 0,64
swirsi(icol,irow) = -41.59 * (spec(p_2210) - spec(p_2090) ) + 1.24 * (spec(p_2280) - spec(p_2090) ) + 0.64





; -----------------------------------------------
; 		SOIL

; clay ratio 
; via 0.5 * (sholder_left + sholder_right ) - clay_center
clay_1(icol,irow) = 0.5 * (spec(p_2136) + spec(p_2240)) - spec(p_2195)  


; iron ratio
; via + 
iron_1(icol,irow) = 0.5 * (spec(p_780) + spec(p_1245)) - spec(p_920)  



; -----------------------------------------------
; end of main loop
  end
  ; ende des for every pix
end
; ende des for every row

print, 'hier break'

;    fname_re=fname+'_rededge'
;    my_image_out, image=rededge_pos, o_file_name=fname_re

;    ENVI_ENTER_DATA, rededge_pos, bnames = 'RedEdge'
;    ENVI_ENTER_DATA, bildraus_dgvi1, bnames = 'DGVI 1'
;    ENVI_ENTER_DATA, bildraus_dgvi2, bnames = 'DGVI 2'
;    ENVI_ENTER_DATA, bildraus_maxslope, bnames = 'Slope at RedEdge Inflict.'
;    ENVI_ENTER_DATA, bildraus1, bnames = 'Der1'
;    ENVI_ENTER_DATA, bildraus2, bnames = 'Der2'
;    ENVI_ENTER_DATA, bildraus3, bnames = 'Der3'
;    ENVI_ENTER_DATA, bildraus_tmp, bnames = 'abs_der2'

ENVI_ENTER_DATA, ndvi, bnames = 'ndvi'
ENVI_ENTER_DATA, mcari, bnames = 'mcari'
ENVI_ENTER_DATA, lci , bnames = 'lci'
ENVI_ENTER_DATA, pri , bnames = 'pri'
ENVI_ENTER_DATA, sr , bnames = 'sr705_chloro'
ENVI_ENTER_DATA, mnd , bnames = 'mnd705_chloro'
ENVI_ENTER_DATA, re_pos , bnames = 'reip'
ENVI_ENTER_DATA, re_pos_sav1 , bnames = 'reip_1'
ENVI_ENTER_DATA, re_pos_sav2 , bnames = 'reip_2'

	ENVI_ENTER_DATA, rvi, bnames = 'rvi'
	ENVI_ENTER_DATA, gi, bnames = 'gi'

ENVI_ENTER_DATA, dgvi1 , bnames = 'dgvi1'
ENVI_ENTER_DATA, dgvi2 , bnames = 'dgvi2'


ENVI_ENTER_DATA, ndni , bnames = 'ndni'
ENVI_ENTER_DATA, ndli , bnames = 'ndli'
ENVI_ENTER_DATA, cai  , bnames = 'cai'
ENVI_ENTER_DATA, ndwi , bnames = 'ndwi'
ENVI_ENTER_DATA, lwvi1, bnames = 'lwvi1'
ENVI_ENTER_DATA, lwvi2, bnames = 'lwvi2'
ENVI_ENTER_DATA, mirndwi, bnames = 'ndwi_mir'
ENVI_ENTER_DATA, dwsi , bnames = 'dwsi5'
; ENVI_ENTER_DATA, csi1 = fltarr(ncols,nrows), bnames = '
ENVI_ENTER_DATA, csi2 , bnames = 'csi2'
ENVI_ENTER_DATA, swirvi , bnames = 'swir_vi'
ENVI_ENTER_DATA, swirli , bnames = 'swir_li'
ENVI_ENTER_DATA, swirsi , bnames = 'swir_si'

	ENVI_ENTER_DATA, clay_1, bnames = 'Clay 1'
	ENVI_ENTER_DATA, iron_1, bnames = 'Iron 1'
print, 'hier break'

end


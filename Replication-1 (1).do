log using session

use /Users/Yuvraj/Desktop/ECO375/Final_Project/Phase_4/anon_bo_threads.dta
merge m:1 anon_item_id using /Users/Yuvraj/Desktop/ECO375/Final_Project/Phase_4/anon_bo_lists_smaller.dta, keep(master match)

keep anon_item_id start_price_usd item_price decline_price accept_price ref_price1 store offr_price offr_type_id store bo_ck_yn anon_byr_id

drop if bo_ck_yn == 0
drop if offr_type_id != 0
drop if offr_price ==. | ref_price1 ==. | start_price_usd ==. 
save final.dta, replace


use final.dta

*asdoc sum offr_price ref_price1 start_price_usd store, detail
set seed 4568
sample 2000000, count
drop if bo_ck_yn != 1

* Variables Summary Statistics
sum offr_price ref_price1 start_price_usd store, detail


*Removing Outliers
drop if offr_price > 142.7115 + (4*484.5496)
drop if offr_price < 142.7115 - (4*484.5496)

drop if ref_price1 > 175.6249 + (4*543.5227)
drop if ref_price1 < 175.6249 - (4*543.5227)

drop if start_price_usd > 227.9197 + (4*3020.229)
drop if start_price_usd < 227.9197 - (4*3020.229)

asdoc sum offr_price ref_price1 start_price_usd store, detail
 

* Variables Scatter Plots
twoway scatter ref_price1 start_price_usd
graph export ref_price1&start_price_usd.jpg, replace


* Regressions
** Reg1
reg offr_price ref_price1 start_price_usd c.ref_price1#c.start_price_usd, robust
estimates store model1

**Ramsey test
estat ovtest

** Hypothesis test
asdoc test ref_price1-start_price_usd=0

**Residual plots
rvfplot
graph export resid&fitted.jpg, replace
rvpplot ref_price1
graph export resid&ref_price1.jpg, replace
rvpplot start_price_usd
graph export resid&start_price_usd.jpg, replace



** Reg2
reg offr_price ref_price1 start_price_usd c.ref_price1#c.start_price_usd if store==0, robust

estimates store model2

** Reg3
reg offr_price ref_price1 start_price_usd c.ref_price1#c.start_price_usd if store==1, robust
estimates store model3

etable, estimates(model1 model2 model3) showstars showstarsnote title("Table 1.Regression Results") export(mydoc.docx, replace) 


log close



## Overview
The BRFSS objective is to collect uniform, state-specific data on preventive health practices and risk behaviors that are linked to chronic diseases, injuries, and preventable infectious diseases that affect the adult population. Factors assessed by the BRFSS in 2015 include tobacco use, HIV/AIDS knowledge and prevention, exercise, immunization, health status, healthy days health-related quality of life, health care access, hypertension awareness, arthritis burden, chronic health conditions, alcohol consumption, fruits and vegetables, and seatbelt use.  The BRFSS was initiated in 1984, with 15 states collecting surveillance data on risk behaviors through monthly telephone interviews. Over time, the number of states participating in the survey increased, and by 2001, 50 states, the District of Columbia, Puerto Rico, Guam, and the US Virgin Islands were participating in the BRFSS.

### Data Availability
* SAS format data available from 1984 to 2015.
* Geospatial (Maps data) available for different levels of city/metro/county
** Filtered to include minimum number of respondents per geo region

### Questionairre Structure
* Core component used by all states
* Optional modules (25 modules in 2015)
* Rotated core questions included based on odd/even-numbered years
* State-added questions


### Weigthing Structure
* State-level stratum sample design
* Disproportionately sampled states are in the majority
* Design weights are calculated using the weight of each geographic stratum (_STRWT), the number of landline phones within a household (NUMPHON2), and the number of adults who use those phones (NUMADULT). For cellphone respondents, both NUMPHON2 and NUMADULT are set to 1. The formula for the design weight is: Design Weight = _STRWT * (1/NUMPHON2) * NUMADULT
* BRFSS calculates the stratum weight (_STRWT) using the following items:
** Number of available records (NRECSTR) and the number of records users select (NRECSEL) within each geographic strata and density strata.
** Geographic strata (GEOSTR), which may be the entire state or a geographic subset (e.g., counties, census tracts).
** Density strata (_DENSTR) indicating the density of the phone numbers for a given block of numbers as listed or not listed.
* In 2015, the inclusion of cellular telephone respondents who also have landline telephones in their household required an adjustment to the design weights to account for the overlapping sample frames

### Characteristic Issues
* Sampling through phone survey
** Previously restricted to landline
** Then stratified at household level (?)
** Finally using any primary phone number for eligible adults
* Changes in weighting methodology
** Most recent was 2011
** Further change in weighting due to inclusion of landlines in 2015
* Comparability/combine-ability of previous years is dubious
** Not clear if multi-year comparisons are using raw or weighted data
** How do they reconcile the different yearly weighting strategies?
* Direct collection vs contractor data collectors add additional variability


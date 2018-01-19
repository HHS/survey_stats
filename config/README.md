## BRFSS Dataset

### Behavioral Risk Factor Surveillance System

The BRFSS objective is to collect uniform, state-specific data on preventive health practices and risk behaviors that are linked to chronic diseases, injuries, and preventable infectious diseases that affect the adult population. Factors assessed by the BRFSS in 2015 include tobacco use, HIV/AIDS knowledge and prevention, exercise, immunization, health status, healthy days health-related quality of life, health care access, hypertension awareness, arthritis burden, chronic health conditions, alcohol consumption, fruits and vegetables, and seatbelt use. The BRFSS was initiated in 1984, with 15 states collecting surveillance data on risk behaviors through monthly telephone interviews. Over time, the number of states participating in the survey increased, and by 2001, 50 states, the District of Columbia, Puerto Rico, Guam, and the US Virgin Islands were participating in the BRFSS.

#### Data Availability
- SAS format data available from 1984 to 2015.
- Geospatial (Maps data) available for different levels of city/metro/county
- Filtered to include minimum number of respondents per geo region

#### Questionnaire Structure
- Core component used by all states
- Optional modules (25 modules in 2015)
- Rotated core questions included based on odd/even-numbered years
- State-added questions

#### Weighting Structure
- State-level stratum sample design
- Disproportionately sampled states are in the majority
- Design weights are calculated using the weight of each geographic stratum (_STRWT), the number of landline phones within a household (NUMPHON2), and the number of adults who use those phones (NUMADULT). For cellphone respondents, both NUMPHON2 and NUMADULT are set to 1. The formula for the design weight is: Design Weight = _STRWT * (1/NUMPHON2) * NUMADULT
- BRFSS calculates the stratum weight (_STRWT) using the following items:
    - Number of available records (NRECSTR) and the number of records users select (NRECSEL) within each geographic strata and density strata.
    - Geographic strata (GEOSTR), which may be the entire state or a geographic subset (e.g., counties, census tracts).
    - Density strata (_DENSTR) indicating the density of the phone numbers for a given block of numbers as listed or not listed.
- In 2015, the inclusion of cellular telephone respondents who also have landline telephones in their household required an adjustment to the design weights to account for the overlapping sample frames

### BRFSS Survey Statistics

The BRFSS dataset uses cluster sampling along strata defined by geographic regions, and telephone number blocks independently for each year of the survey. SInce we do not have a combined dataset across the relevant years of the BRFSS study, we redefine the effective strata to be a combination of survey year and the yearly strata. We find the following design variables in the BRFSS data sets:
1. **_psu**: the primary sampling unit for the given survey year, relabeled `psu` in our framework
2. **_ststr**:  the year specific stratum id, relabeled `strata` in our framework
3. **_llcpwt** or **_finalwt**:  the sampling weight for the given row, relabeled `weight` in our framework

Translating the stratified random sampling setup given for SUDAAN/SAS (STRWOR) and SPSS, we have the following survey design for the R `survey` package:
```
des = svydesign(id=~psu, strata=~year+strata,  weight=~weight, data=brfss_data)
```
and state-wise (recoded `sitecode`) and year-wise breakouts of a given response for a question are found using the `svyby` function as follows:
```
svyby(~I(addepev2=='yes'), ~year+sitecode, des, ci_xlogit, vartype=c('se','ci'), na.rm.by=T)
```
where those responding 'yes' to the addepev2 question are of interest here.

## PRAMS Data

###  Pregnancy Risk Assessment Monitoring System (PRAMS)

Developed in 1987, PRAMS collects state-specific, population-based data on maternal attitudes and experiences before, during, and shortly after pregnancy. PRAMS surveillance currently covers about 83% of all U.S. births. The PRAMS sample of women who have had a recent live birth is drawn from the state's birth certificate file. Each participating state samples between 1,300 and 3,400 women per year. Topics addressed in the PRAMS core questionnaire include barriers to and content of prenatal care, obstetric history, maternal use of alcohol and cigarettes, physical abuse, contraception, economic status, maternal stress, and early infant development and health status.

####  Data Summary
- 40 states/demographic regions (NY State excl NYC, NYC, South Dakota Tribal)
- ~26 participants/yr
- ~8.5 years avg lifetime participation, range 1-13
- ~9 regions participated in all 13 PRAMS surveys
- 250 outcome/response variables indexed by class and topic
- 17 control/breakout variables to stratify the population responses available for three survey periods:  
    - **PH5**: 2000–2003
    - **PH6**: 2004–2008
    - **PH7**: 2009–2011
- state data availability by year: https://www.cdc.gov/prams/pramstat/state-availability-year.html
- topic classes include 
    1. delivery, 
    2. demographics,
    3. family planning,
    4. flu,
    5. infant health,
    6. insurance/medicaid/services,
    7. maternal behaviour/health,
    8. maternal experiences, and 
    9. prenatal care


#### Data Availability
- low level weighted survey response data (this is what we used for YRBSS analysis) is not public
- non-CDC researchers must submit a study proposal detailing how the data will be used before gaining access
- PRAMS Data Portal provides all the precomputed response mean, SE, and CIs used for PRAMStat app
   - Datasets on PRAMS Data Portal: https://goo.gl/kOBC19
- Survey data for ph7 provided by PRAMS group at CDC
   - data are weighted to be comparable across states and years


### PRAMS Survey Statistics

The PRAMS dataset, unlike YRBS and BRFSS uses stratified random sampling rather than cluster sampling.  The strata in the PRAMS design are formulated as a combination of year and state specific stratum (some combination of adequacy of prenatal care factors, birth weight, and/or income/demographic factors), where the stratification methodology differs by state. This is captured in the post-processed survey variable SUD_NEST (relabeled as `strata` in our framework ), and given alongside other design variables, namely:
1. **wtanal**: the analysis weight for sample row concerned, relabelled `weight` in our framework
2. **totcnt**:  the total count for the specified subgroub/stratum, relabelled `fpc` in our framework
3. **samcnt**: the sample count for the specified subgroup/stratum, relabelled `sample_ct` in our framework, and
4. **cell**: the within state stratification variable for the given year

Translating the stratified random sampling setup given for SUDAAN/SAS (STRWOR) and SPSS, we have the following survey design for the R `survey` package:
```
des = svydesign(id=~1, strata=~strata,  fpc=~fpc, weight=~weight, data=prams_data)
```
and state-wise (recoded `sitecode`) and year-wise breakouts of a given response for a question are found using the `svyby` function as follows:
```
svyby(~I(cp_vitamin=='Yes'), ~year+sitecode, des, ci_xlogit, vartype=c('se','ci'), na.rm.by=T)
```
where those responding 'Yes' to the cp_vitamin question are of interest here.

* This SPSS syntax file reads ASCII format (text format) 2015 SADC data and creates a formatted 
and labeled SPSS data file that you can analyze in SPSS.
 
* Change the file location specifications from 'c:\sadc2015' to the location where you 
downloaded, unzipped, and stored the 2015 SADC ASCII data file before you run this syntax; 
Change the location specification in three places - in the 'data list' statement at the top 
of the syntax and in the 'save' and 'get' statements at the end of this syntax file.

* Change 'xxxxxxx' in the 'data list' statement and the 'save' and 'get' statements at the 
end of this syntax file to 'national', 'district', 'state_a_m', or 'state_n_z' depending on which 
file you are analyzing.   

DATA LIST FILE="C:\sadc2015\sadc_2015_xxxxxxx.dat"/
sitecode 1-5 (A) sitename 6-55 (A) sitetype 56-105 (A) sitetypenum 106-113
year 114-121 survyear 122-124 weight 125-134 stratum 135-142
PSU 143-150 record 151-158 age 159-161 sex 162-164 grade 165-167
race4 168-170 race7 171-173 stheight 174-181 stweight 182-189
bmi 190-197 bmipct 198-205 qnobese 206-208 qnowt 209-211 
q68 212-212 q67 213-213 sexid 214-221 sexid2 222-229 sexpart 230-237 sexpart2 238-245
q8 246-246 q9 247-247 q10 248-248
q11 249-249 q12 250-250 q13 251-251 
q14 252-252 q15 253-253 q16 254-254 
q17 255-255 q18 256-256 q19 257-257 
q20 258-258 q21 259-259 q22 260-260 
q23 261-261 q24 262-262 q25 263-263 
q26 264-264 q27 265-265 q28 266-266 
q29 267-267 q30 268-268 q31 269-269 
q32 270-270 q33 271-271 q34 272-272 
q35 273-273 q36 274-274 q37 275-275 
q38 276-276 q39 277-277 q40 278-278 
q41 279-279 q42 280-280 q43 281-281 
q44 282-282 q45 283-283 q46 284-284 
q47 285-285 q48 286-286 q49 287-287 
q50 288-288 q51 289-289 q52 290-290 
q53 291-291 q54 292-292 q55 293-293 
q56 294-294 q57 295-295 q58 296-296 
q59 297-297 q60 298-298 q61 299-299 
q62 300-300 q63 301-301 q64 302-302
q65 303-303 q66 304-304 q69 305-305
q70 306-306 q71 307-307 q72 308-308
q73 309-309 q74 310-310 q75 311-311
q76 312-312 q77 313-313 q78 314-314
q79 315-315 q80 316-316 q81 317-317
q82 318-318 q83 319-319 q84 320-320
q85 321-321 q86 322-322 q87 323-323
q88 324-324 q89 325-325
qn8 326-328 qn9 329-331 qn10 332-334
qn11 335-337 qn12 338-340 qn13 341-343 
qn14 344-346 qn15 347-349 qn16 350-352
qn17 353-355 qn18 356-358 qn19 359-361 
qn20 362-364 qn21 365-367 qn22 368-370 
qn23 371-373 qn24 374-376 qn25 377-379 
qn26 380-382 qn27 383-385 qn28 386-388 
qn29 389-391 qn30 392-394 qn31 395-397 
qn32 398-400 qn33 401-403 qn34 404-406 
qn35 407-409 qn36 410-412 qn37 413-415 
qn38 416-418 qn39 419-421 qn40 422-424
qn41 425-427 qn42 428-430 qn43 431-433 
qn44 434-436 qn45 437-439 qn46 440-442 
qn47 443-445 qn48 446-448 qn49 449-451 
qn50 452-454 qn51 455-457 qn52 458-460 
qn53 461-463 qn54 464-466 qn55 467-469 
qn56 470-472 qn57 473-475 qn58 476-478 
qn59 479-481 qn60 482-484 qn61 485-487 
qn62 488-490 qn63 491-493 qn64 494-496 
qn65 497-499 qn66 500-502 qn69 503-505 
qn70 506-508 qn71 509-511 qn72 512-514 
qn73 515-517 qn74 518-520 qn75 521-523 
qn76 524-526 qn77 527-529 qn78 530-532 
qn79 533-535 qn80 536-538 qn81 539-541 
qn82 542-544 qn83 545-547 qn84 548-550 
qn85 551-553 qn86 554-556 qn87 557-559 
qn88 560-562 qn89 563-565 
qnfrcig 566-568 qndaycig 569-571 qncigint 572-574
qntob2 575-577 qntob3 578-580 qntob4 581-583
qnnotob2 584-586 qnnotob3 587-589 qnnotob4 590-592
qniudimp 593-595 qnshparg 596-598 qnothhpl 599-601
qndualbc 602-604 qnbcnone 605-607 qnfr0 608-610
qnfr1 611-613 qnfr2 614-616 qnfr3 617-619
qnveg0 620-622 qnveg1 623-625 qnveg2 626-628
qnveg3 629-631 qnsoda1 632-634 qnsoda2 635-637
qnsoda3 638-640 qnmilk1 641-643 qnmilk2 644-646
qnmilk3 647-649 qnbk7day 650-652 qnpa0day 653-655
qnpa7day 656-658 qndlype 659-661
qhowmarijuana 662-662 qhallucdrug 663-663 qsunscreenuse 664-664
qindoortanning 665-665 qmusclestrength 666-666 qgenderexp 667-667 
qcelldriving 668-668 qbullyweight 669-669 qbullygay 670-670 
qtypealcohol 671-671 qcigschool 672-672 qchewtobschool 673-673 
qalcoholschool 674-674 qmarijuanaschool 675-675 qprescription30d 676-676
qcurrentcocaine 677-677 qcurrentasthma 678-678 qtaughtsexed 679-679 
qtaughtstd 680-680 qtaughtbc 681-681 qdietpop 682-682 
qcoffeetea 683-683 qsportsdrink 684-684 qenergydrink 685-685 
qsugardrink 686-686 qwater 687-687 qfastfood 688-688 
qfoodallergy 689-689 qsunburn 690-690 qconcentrating 691-691
qspeakenglish 692-692
qnhowmarijuana 693-695 qnhallucdrug 696-698 qnsunscreenuse 699-701
qnindoortanning 702-704 qnmusclestrength 705-707 qngenderexp 708-710
qncelldriving 711-713 qnbullyweight 714-716 qnbullygay 717-719
qntypealcohol 720-722 qncigschool 723-725 qnchewtobschool 726-728
qnalcoholschool 729-731 qnmarijuanaschool 732-734 qnprescription30d 735-737
qncurrentcocaine 738-740 qncurrentasthma 741-743 qntaughtsexed 744-746
qntaughtstd 747-749 qntaughtbc 750-752 qndietpop 753-755
qncoffeetea 756-758 qnsportsdrink 759-761 qnspdrk1 762-764
qnspdrk2 765-767 qnspdrk3 768-770 qnenergydrink 771-773
qnsugardrink 774-776 qnwater 777-779 qnwater1 780-782
qnwater2 783-785 qnwater3 786-788 qnfastfood 789-791
qnfoodallergy 792-794 qnsunburn 795-797 qnconcentrating 798-800
qnspeakenglish 801-803.
EXECUTE.
 
VARIABLE LABELS
sitecode "Site code"
sitename "Site name"
sitetype "Site type"
sitetypenum "1=District, 2=State, 3=National"
year "4-digit Year of survey"
survyear "1=1991...13=2015"
weight "Analysis weight"
stratum "Analysis stratum"
PSU "Analysis primary sampling unit"
record "Record ID"
age "1= <=12...7=18+ years old"
sex "1=Female, 2=Male"
grade "1=9th...4=12th grade"
race4 "4-level race variable"
race7 "7-level race variable"
stheight "Height in meters"
stweight "Weight in kilograms"
bmi "Body Mass Index"
bmipct "BMI percentile"
qnobese "Were Obese"
qnowt "Were Overweight"
q68 "Sexual identity"
q67 "Sex of sexual contacts"
sexid "Sexual identity"
sexid2 "Collapsed sexual identity"
sexpart "Sex of sex contact(s)"
sexpart2 "Collapsed sex of sex contact(s)"
q8 "Bicycle helmet use"
q9 "Seat belt use"
q10 "Riding with a drinking driver"
q11 "Drinking and driving"
q12 "Texting and driving"
q13 "Weapon carrying"
q14 "Gun carrying"
q15 "Weapon carrying at school"
q16 "Safety concerns at school"
q17 "Threatened at school"
q18 "Physical fighting"
q19 "Injurious physical fighting"
q20 "Physical fighting at school"
q21 "Ever been forced to have sexual intercourse"
q22 "Did date physically hurt them 12 mo"
q23 "Sexual dating violence"
q24 "Bullying at school"
q25 "Electronic bullying"
q26 "Sad or hopeless"
q27 "Considered suicide"
q28 "Made a suicide plan"
q29 "Attempted suicide"
q30 "Injurious suicide attempt"
q31 "Ever cigarette use"
q32 "Initiation of cigarette use"
q33 "Current cigarette use"
q34 "Smoked >10 cigarettes"
q35 "Cigarettes from store"
q36 "Smoking cessation"
q37 "Current smokeless tobacco use"
q38 "Current cigar use"
q39 "Electronic vapor product use"
q40 "Current electronic vapor product use"
q41 "Ever alcohol use"
q42 "Initiation of alcohol use"
q43 "Current alcohol use"
q44 "5 or more drinks in a row"
q45 "Largest number of drinks"
q46 "Source of alcohol"
q47 "Ever marijuana use"
q48 "Initiation of marijuana use"
q49 "Current marijuana use"
q50 "Ever cocaine use"
q51 "Ever inhalant use"
q52 "Ever heroin use"
q53 "Ever methamphetamine use"
q54 "Ever ecstasy use"
q55 "Ever synthetic marijuana use"
q56 "Ever steroid use"
q57 "Ever prescription drug use"
q58 "Illegal injected drug use"
q59 "Illegal drugs at school"
q60 "Ever sexual intercourse"
q61 "Sex before 13 years"
q62 "Multiple sex partners"
q63 "Current sexual activity"
q64 "Alcohol/drugs and sex"
q65 "Condom use"
q66 "Birth control pill use"
q69 "Perception of weight"
q70 "Weight loss"
q71 "Fruit juice drinking"
q72 "Fruit eating"
q73 "Salad eating"
q74 "Potato eating"
q75 "Carrot eating"
q76 "Other vegetable eating"
q77 "Soda drinking"
q78 "How many glass of milk 7 days"
q79 "Breakfast eating"
q80 "Physical activity >= 5 days"
q81 "Television watching"
q82 "Computer use"
q83 "PE attendance"
q84 "Sports team participation"
q85 "HIV testing"
q86 "Oral health care"
q87 "Asthma"
q88 "Hours of sleep on school night"
q89 "Grades in school"
qn8 "Rarely or never wore a bicycle helmet"
qn9 "Rarely or never wore a seat belt"
qn10 "Rode with a driver who had been drinking alcohol"
qn11 "Drove when drinking alcohol"
qn12 "Texted or e-mailed while driving a car or other vehicle"
qn13 "Carried a weapon"
qn14 "Carried a gun"
qn15 "Carried a weapon on school property"
qn16 "Did not go to school because they felt unsafe at school or on their way to or from school"
qn17 "Were threatened or injured with a weapon on school property"
qn18 "Were in a physical fight"
qn19 "Were injured in a physical fight"
qn20 "Were in a physical fight on school property"
qn21 "Were ever physically forced to have sexual intercourse"
qn22 "Experienced physical dating violence"
qn23 "Experienced sexual dating violence"
qn24 "Were bullied on school property"
qn25 "Were electronically bullied"
qn26 "Felt sad or hopeless"
qn27 "Seriously considered attempting suicide"
qn28 "Made a plan about how they would attempt suicide"
qn29 "Attempted suicide"
qn30 "Attempted suicide that resulted in an injury, poisoning, or overdose that had to be treated by a doctor or nurse"
qn31 "Ever tried cigarette smoking"
qn32 "Smoked a whole cigarette before age 13 years"
qn33 "Currently smoked cigarettes"
qn34 "Smoked more than 10 cigarettes per day"
qn35 "Usually obtained their own cigarettes by buying them in a store or gas station"
qn36 "Tried to quit smoking cigarettes"
qn37 "Currently used smokeless tobacco"
qn38 "Currently smoked cigars"
qn39 "Ever used electronic vapor products"
qn40 "Currently used electronic vapor products"
qn41 "Ever drank alcohol"
qn42 "Drank alcohol before age 13 years"
qn43 "Currently drank alcohol"
qn44 "Drank five or more drinks of alcohol in a row"
qn45 "Reported that the largest number of drinks they had in a row was 10 or more"
qn46 "Usually obtained the alcohol they drank by someone giving it to them"
qn47 "Ever used marijuana"
qn48 "Tried marijuana before age 13 years"
qn49 "Currently used marijuana"
qn50 "Ever used cocaine"
qn51 "Ever used inhalants"
qn52 "Ever used heroin"
qn53 "Ever used methamphetamines"
qn54 "Ever used ecstasy"
qn55 "Ever used synthetic marijuana"
qn56 "Ever took steroids without a doctor's prescription"
qn57 "Ever took prescription drugs without a doctor's prescription"
qn58 "Ever injected any illegal drug"
qn59 "Were offered, sold, or given an illegal drug on school property"
qn60 "Ever had sexual intercourse"
qn61 "Had sexual intercourse before age 13 years"
qn62 "Had sexual intercourse with four or more persons"
qn63 "Were currently sexually active"
qn64 "Drank alcohol or used drugs before last sexual intercourse"
qn65 "Used a condom"
qn66 "Used birth control pills"
qn69 "Described themselves as slightly or very overweight"
qn70 "Were trying to lose weight"
qn71 "Did not drink fruit juice"
qn72 "Did not eat fruit"
qn73 "Did not eat salad"
qn74 "Did not eat potatoes"
qn75 "Did not eat carrots"
qn76 "Did not eat other vegetables"
qn77 "Did not drink a can, bottle, or glass of soda or pop"
qn78 "Did not drink milk"
qn79 "Did not eat breakfast"
qn80 "Were physically active at least 60 minutes per day on 5 or more days"
qn81 "Watched television 3 or more hours per day"
qn82 "Played video or computer games or used a computer 3 or more hours per day"
qn83 "Attended physical education classes on 1 or more days"
qn84 "Played on at least one sports team"
qn85 "Were ever tested for HIV"
qn86 "Saw a dentist"
qn87 "Had ever been told by a doctor or nurse that they had asthma"
qn88 "Had 8 or more hours of sleep"
qn89 "Made mostly A's or B's in school"
qnfrcig "Currently frequently smoked cigarettes"
qndaycig "Currently smoked cigarettes daily"
qncigint "Usually obtained their own cigarettes by buying on the internet"
qntob2 "Currently smoked cigarettes or cigars"
qntob3 "Currently used cigarettes, cigars, or smokeless tobacco"
qntob4 "Currently used tobacco"
qnnotob2 "Did not currently smoke cigarettes or cigars"
qnnotob3 "Did not currently use cigarettes, cigars, or smokeless tobacco"
qnnotob4 "Did not currently use tobacco"
qniudimp "Used an IUD (e.g., Mirena or ParaGard) or implant (e.g., Implanon or Nexplanon)"
qnshparg "Used a shot (e.g., Depo-Provera), patch (e.g., OrthoEvra), or birth control ring (e.g., NuvaRing)"
qnothhpl "Used birth control pills; an IUD or implant; or a shot, patch, or birth control ring"
qndualbc "Used both a condom during and birth control pills; an IUD or implant; or a shot, patch, or birth control ring before last sexual intercourse"
qnbcnone "Did not use any method to prevent pregnancy"
qnfr0 "Did not eat fruit or drink 100% fruit juices"
qnfr1 "Ate fruit or drank 100% fruit juices one or more times per day"
qnfr2 "Ate fruit or drank 100% fruit juices two or more times per day"
qnfr3 "Ate fruit or drank 100% fruit juices three or more times per day"
qnveg0 "Did not eat vegetables"
qnveg1 "Ate vegetables one or more times per day"
qnveg2 "Ate vegetables two or more times per day"
qnveg3 "Ate vegetables three or more times per day"
qnsoda1 "Drank a can, bottle, or glass of soda or pop one or more times per day"
qnsoda2 "Drank a can, bottle, or glass of soda or pop two or more times per day"
qnsoda3 "Drank a can, bottle, or glass of soda or pop three or more times per day"
qnmilk1 "Drank one or more glasses per day of milk"
qnmilk2 "Drank two or more glasses per day of milk"
qnmilk3 "Drank three or more glasses per day of milk"
qnbk7day "Ate breakfast on all 7 days"
qnpa0day "Did not participate in at least 60 minutes of physical activity on at least 1 day"
qnpa7day "Were physically active at least 60 minutes per day on all 7 days"
qndlype "Attended physical education classes on all 5 days"
qhowmarijuana "Usual use of marijuana"
qhallucdrug "Ever used LSD"
qsunscreenuse "Sunscreen use outside"
qindoortanning "How many times indoor tanning"
qmusclestrength "Strengthen muscles past 7 days"
qgenderexp "How others would describe you"
qcelldriving "Did you talk on cell phone while driving"
qbullyweight "Ever been teased because of weight"
qbullygay "Ever been teased b/c labeled GLB"
qtypealcohol "What type of alcohol usually drink 30d"
qcigschool "Days use cigarettes school property 30 days"
qchewtobschool "Days use snuff school property 30 days"
qalcoholschool "How many days drink @ school 30 days"
qmarijuanaschool "How many times marijuana@school 30 days"
qprescription30d "Times take drug w/o prescription 30d"
qcurrentcocaine "How many times use cocaine 30 days"
qcurrentasthma "Do you still have asthma"
qtaughtsexed "Ever had sex education in school"
qtaughtstd "Ever been taught in school about STDs"
qtaughtbc "Ever been taught about BC methods in sch"
qdietpop "How many times diet soda past 7 days"
qcoffeetea "Times drink coffee or tea past 7 days"
qsportsdrink "How many times sports drink past 7 days"
qenergydrink "How many times energy drink past 7 days"
qsugardrink "Times sugar-sweetened beverage past 7d"
qwater "How many times plain water past 7 days"
qfastfood "Days 1+ meal/snack fast food past 7d"
qfoodallergy "Food allergies"
qsunburn "Sunburn"
qconcentrating "Difficulty concentrating"
qspeakenglish "How well speak English"
qnhowmarijuana "Usually used marijuana by smoking it in a joint, bong, pipe, or blunt"
qnhallucdrug "Used LSD 1+ times"
qnsunscreenuse "Mostly or always wear sunscreen"
qnindoortanning "Used 1+ times indoor tanning"
qnmusclestrength "Strengthened muscles 3+ of past 7 days"
qngenderexp "Equally feminine and masculine"
qncelldriving "Talked on cell phone driving 1+ past 30d"
qnbullyweight "Been teased b/c of weight past 12 mos"
qnbullygay "Been teased b/c labeled GLB past 12 mos"
qntypealcohol "Liquor type alcohol drank past 30 days"
qncigschool "Used cigarettes at school 1+ 30 days"
qnchewtobschool "Used snuff/dip at school 1+ 30 days"
qnalcoholschool "Had 1+ drinks at school 1+ 30 days"
qnmarijuanaschool "Used marijuana@school 1+ times 30 day"
qnprescription30d "Prescription drug 1+ times past 30 days"
qncurrentcocaine "Used cocaine 1+ times past 30 days"
qncurrentasthma "With current asthma"
qntaughtsexed "Had sex education in school ever"
qntaughtstd "Been taught in school about STDs ever"
qntaughtbc "Been taught in school about BC methods"
qndietpop "Drink 1+ times/day diet soda past 7d"
qncoffeetea "Drank 1+ times/day coffee/tea past 7d"
qnsportsdrink "Did not drink a can, bottle, or glass of a sports drink"
qnspdrk1 "Drank a can, bottle, or glass of a sports drink one or more times per day"
qnspdrk2 "Drank a can, bottle, or glass of a sports drink two or more times per day"
qnspdrk3 "Drank a can, bottle, or glass of a sports drink three or more times per day"
qnenergydrink "Drank 1+ times/day energy drink past 7d"
qnsugardrink "Drank 1+times/day sugar beverage past 7d"
qnwater "Did not drink a bottle or glass of plain water"
qnwater1 "Drank one or more glasses per day of water"
qnwater2 "Drank two or more glasses per day of water"
qnwater3 "Drank three or more glasses per day of water"
qnfastfood "Ate 1+ meal/snack fast food 3+ days"
qnfoodallergy "Have to avoid some foods because eating the food could cause an allergic reaction"
qnsunburn "Had a sunburn"
qnconcentrating "Have serious difficulty concentrating, remembering, or making decisions"
qnspeakenglish "Speak English well or very well".
 
VALUE LABELS
q8
1 "Did not ride a bicycle"
2 "Never wore a helmet"
3 "Rarely wore a helmet"
4 "Sometimes wore a helmet"
5 "Most of the time wore a helmet"
6 "Always wore a helmet"
/
q9
1 "Never"
2 "Rarely"
3 "Sometimes"
4 "Most of the time"
5 "Always"
/
q10
1 "0 times"
2 "1 time"
3 "2 or 3 times"
4 "4 or 5 times"
5 "6 or more times"
/
q11
1 "Did not drive"
2 "0 times"
3 "1 time"
4 "2 or 3 times"
5 "4 or 5 times"
6 "6 or more times"
/
q12
1 "Did not drive"
2 "0 days"
3 "1 or 2 days"
4 "3 to 5 days"
5 "6 to 9 days"
6 "10 to 19 days"
7 "20 to 29 days"
8 "All 30 days"
/
q13
1 "0 days"
2 "1 day"
3 "2 or 3 days"
4 "4 or 5 days"
5 "6 or more days"
/
q14
1 "0 days"
2 "1 day"
3 "2 or 3 days"
4 "4 or 5 days"
5 "6 or more days"
/
q15
1 "0 days"
2 "1 day"
3 "2 or 3 days"
4 "4 or 5 days"
5 "6 or more days"
/
q16
1 "0 days"
2 "1 day"
3 "2 or 3 days"
4 "4 or 5 days"
5 "6 or more days"
/
q17
1 "0 times"
2 "1 time"
3 "2 or 3 times"
4 "4 or 5 times"
5 "6 or 7 times"
6 "8 or 9 times"
7 "10 or 11 times"
8 "12 or more times"
/
q18
1 "0 times"
2 "1 time"
3 "2 or 3 times"
4 "4 or 5 times"
5 "6 or 7 times"
6 "8 or 9 times"
7 "10 or 11 times"
8 "12 or more times"
/
q19
1 "0 times"
2 "1 time"
3 "2 or 3 times"
4 "4 or 5 times"
5 "6 or more times"
/
q20
1 "0 times"
2 "1 time"
3 "2 or 3 times"
4 "4 or 5 times"
5 "6 or 7 times"
6 "8 or 9 times"
7 "10 or 11 times"
8 "12 or more times"
/
q21
1 "Yes"
2 "No"
/
q22
1 "Did not date"
2 "0 times"
3 "1 time"
4 "2 or 3 times"
5 "4 or 5 times"
6 "6 or more times"
/
q23
1 "Did not date"
2 "0 times"
3 "1 time"
4 "2 or 3 times"
5 "4 or 5 times"
6 "6 or more times"
/
q24
1 "Yes"
2 "No"
/
q25
1 "Yes"
2 "No"
/
q26
1 "Yes"
2 "No"
/
q27
1 "Yes"
2 "No"
/
q28
1 "Yes"
2 "No"
/
q29
1 "0 times"
2 "1 time"
3 "2 or 3 times"
4 "4 or 5 times"
5 "6 or more times"
/
q30
1 "Did not attempt suicide"
2 "Yes"
3 "No"
/
q31
1 "Yes"
2 "No"
/
q32
1 "Never smoked a cigarette"
2 "8 years old or younger"
3 "9 or 10 years old"
4 "11 or 12 years old"
5 "13 or 14 years old"
6 "15 or 16 years old"
7 "17 years old or older"
/
q33
1 "0 days"
2 "1 or 2 days"
3 "3 to 5 days"
4 "6 to 9 days"
5 "10 to 19 days"
6 "20 to 29 days"
7 "All 30 days"
/
q34
1 "Did not smoke cigarettes"
2 "Less than 1 cigarette"
3 "1 cigarette"
4 "2 to 5 cigarettes"
5 "6 to 10 cigarettes"
6 "11 to 20 cigarettes"
7 "More than 20 cigarettes"
/
q35
1 "Did not smoke cigarettes"
2 "Store or gas station"
3 "I got them on the Internet"
4 "Someone else bought them"
5 "Borrowed/bummed them"
6 "A person 18 or older gave me"
7 "Took them from store/family "
8 "Some other way"
/
q36
1 "Did not smoke in past 12 mos"
2 "Yes"
3 "No"
/
q37
1 "0 days"
2 "1 or 2 days"
3 "3 to 5 days"
4 "6 to 9 days"
5 "10 to 19 days"
6 "20 to 29 days"
7 "All 30 days"
/
q38
1 "0 days"
2 "1 or 2 days"
3 "3 to 5 days"
4 "6 to 9 days"
5 "10 to 19 days"
6 "20 to 29 days"
7 "All 30 days"
/
q39
1 "Yes"
2 "No"
/
q40
1 "0 days"
2 "1 or 2 days"
3 "3 to 5 days"
4 "6 to 9 days"
5 "10 to 19 days"
6 "20 to 29 days"
7 "All 30 days"
/
q41
1 "0 days"
2 "1 or 2 days"
3 "3 to 9 days"
4 "10 to 19 days"
5 "20 to 39 days"
6 "40 to 99 days"
7 "100 or more days"
/
q42
1 "Never drank alcohol"
2 "8 years old or younger"
3 "9 or 10 years old"
4 "11 or 12 years old"
5 "13 or 14 years old"
6 "15 or 16 years old"
7 "17 years old or older"
/
q43
1 "0 days"
2 "1 or 2 days"
3 "3 to 5 days"
4 "6 to 9 days"
5 "10 to 19 days"
6 "20 to 29 days"
7 "All 30 days"
/
q44
1 "0 days"
2 "1 day"
3 "2 days"
4 "3 to 5 days"
5 "6 to 9 days"
6 "10 to 19 days"
7 "20 or more days"
/
q45
1 "Did not drink in past 30 days"
2 "1 or 2 drinks"
3 "3 drinks"
4 "4 drinks"
5 "5 drinks"
6 "6 or 7 drinks"
7 "8 or 9 drinks"
8 "10 or more drinks"
/
q46
1 "Did not drink in past 30 days"
2 "Bought in store"
3 "Bought in restaurant"
4 "Bought at public event"
5 "I gave someone money to buy"
6 "Someone gave it to me"
7 "Took from store/family"
8 "Some other way"
/
q47
1 "0 times"
2 "1 or 2 times"
3 "3 to 9 times"
4 "10 to 19 times"
5 "20 to 39 times"
6 "40 to 99 times"
7 "100 or more times"
/
q48
1 "Never tried marijuana"
2 "8 years old or younger"
3 "9 or 10 years old"
4 "11 or 12 years old"
5 "13 or 14 years old"
6 "15 or 16 years old"
7 "17 years old or older"
/
q49
1 "0 times"
2 "1 or 2 times"
3 "3 to 9 times"
4 "10 to 19 times"
5 "20 to 39 times"
6 "40 or more times"
/
q50
1 "0 times"
2 "1 or 2 times"
3 "3 to 9 times"
4 "10 to 19 times"
5 "20 to 39 times"
6 "40 or more times"
/
q51
1 "0 times"
2 "1 or 2 times"
3 "3 to 9 times"
4 "10 to 19 times"
5 "20 to 39 times"
6 "40 or more times"
/
q52
1 "0 times"
2 "1 or 2 times"
3 "3 to 9 times"
4 "10 to 19 times"
5 "20 to 39 times"
6 "40 or more times"
/
q53
1 "0 times"
2 "1 or 2 times"
3 "3 to 9 times"
4 "10 to 19 times"
5 "20 to 39 times"
6 "40 or more times"
/
q54
1 "0 times"
2 "1 or 2 times"
3 "3 to 9 times"
4 "10 to 19 times"
5 "20 to 39 times"
6 "40 or more times"
/
q55
1 "0 times"
2 "1 or 2 times"
3 "3 to 9 times"
4 "10 to 19 times"
5 "20 to 39 times"
6 "40 or more times"
/
q56
1 "0 times"
2 "1 or 2 times"
3 "3 to 9 times"
4 "10 to 19 times"
5 "20 to 39 times"
6 "40 or more times"
/
q57
1 "0 times"
2 "1 or 2 times"
3 "3 to 9 times"
4 "10 to 19 times"
5 "20 to 39 times"
6 "40 or more times"
/
q58
1 "0 times"
2 "1 time"
3 "2 or more times"
/
q59
1 "Yes"
2 "No"
/
q60
1 "Yes"
2 "No"
/
q61
1 "Never had sex"
2 "11 years old or younger"
3 "12 years old"
4 "13 years old"
5 "14 years old"
6 "15 years old"
7 "16 years old"
8 "17 years old or older"
/
q62
1 "Never had sex"
2 "1 person"
3 "2 people"
4 "3 people"
5 "4 people"
6 "5 people"
7 "6 or more people"
/
q63
1 "Never had sex"
2 "None during past 3 months"
3 "1 person"
4 "2 people"
5 "3 people"
6 "4 people"
7 "5 people"
8 "6 or more people"
/
q64
1 "Never had sex"
2 "Yes"
3 "No"
/
q65
1 "Never had sex"
2 "Yes"
3 "No"
/
q66
1 "Never had sex"
2 "No method was used"
3 "Birth control pills"
4 "Condoms"
5 "IUD or implant"
6 "Shot/patch/birth control ring"
7 "Withdrawal/other method"
8 "Not sure"
/
q67
1 "Never had sexual contact"
2 "Females"
3 "Males"
4 "Females and males"
/
q68
1 "Heterosexual (straight)"
2 "Gay or lesbian"
3 "Bisexual"
4 "Not sure"
/
q69
1 "Very underweight"
2 "Slightly underweight"
3 "About the right weight"
4 "Slightly overweight"
5 "Very overweight"
/
q70
1 "Lose weight"
2 "Gain weight"
3 "Stay the same weight"
4 "Not trying to do anything"
/
q71
1 "Did not drink fruit juice"
2 "1 to 3 times"
3 "4 to 6 times"
4 "1 time per day"
5 "2 times per day"
6 "3 times per day"
7 "4 or more times per day"
/
q72
1 "Did not eat fruit"
2 "1 to 3 times"
3 "4 to 6 times"
4 "1 time per day"
5 "2 times per day"
6 "3 times per day"
7 "4 or more times per day"
/
q73
1 "Did not eat green salad"
2 "1 to 3 times"
3 "4 to 6 times"
4 "1 time per day"
5 "2 times per day"
6 "3 times per day"
7 "4 or more times per day"
/
q74
1 "Did not eat potatoes"
2 "1 to 3 times"
3 "4 to 6 times"
4 "1 time per day"
5 "2 times per day"
6 "3 times per day"
7 "4 or more times per day"
/
q75
1 "Did not eat carrots"
2 "1 to 3 times"
3 "4 to 6 times"
4 "1 time per day"
5 "2 times per day"
6 "3 times per day"
7 "4 or more times per day"
/
q76
1 "Did not eat other vegetables"
2 "1 to 3 times"
3 "4 to 6 times"
4 "1 time per day"
5 "2 times per day"
6 "3 times per day"
7 "4 or more times per day"
/
q77
1 "Did not drink soda or pop"
2 "1 to 3 times"
3 "4 to 6 times"
4 "1 time per day"
5 "2 times per day"
6 "3 times per day"
7 "4 or more times per day"
/
q78
1 "Did not drink milk"
2 "1 to 3 glasses"
3 "4 to 6 glasses"
4 "1 glass per day"
5 "2 glasses per day"
6 "3 glasses per day"
7 "4 or more glasses per day"
/
q79
1 "0 days"
2 "1 day"
3 "2 days"
4 "3 days"
5 "4 days"
6 "5 days"
7 "6 days"
8 "7 days"
/
q80
1 "0 days"
2 "1 day"
3 "2 days"
4 "3 days"
5 "4 days"
6 "5 days"
7 "6 days"
8 "7 days"
/
q81
1 "No TV on average school day"
2 "Less than 1 hour per day"
3 "1 hour per day"
4 "2 hours per day"
5 "3 hours per day"
6 "4 hours per day"
7 "5 or more hours per day"
/
q82
1 "No playing video/computer game"
2 "Less than 1 hour per day"
3 "1 hour per day"
4 "2 hours per day"
5 "3 hours per day"
6 "4 hours per day"
7 "5 or more hours per day"
/
q83
1 "0 days"
2 "1 day"
3 "2 days"
4 "3 days"
5 "4 days"
6 "5 days"
/
q84
1 "0 teams"
2 "1 team"
3 "2 teams"
4 "3 or more teams"
/
q85
1 "Yes"
2 "No"
3 "Not sure"
/
q86
1 "During the past 12 months"
2 "Between 12 and 24 months ago"
3 "More than 24 months ago"
4 "Never"
5 "Not sure"
/
q87
1 "Yes"
2 "No"
3 "Not sure"
/
q88
1 "4 or less hours"
2 "5 hours"
3 "6 hours"
4 "7 hours"
5 "8 hours"
6 "9 hours"
7 "10 or more hours"
/
q89
1 "Mostly A's"
2 "Mostly B's"
3 "Mostly C's"
4 "Mostly D's"
5 "Mostly F's"
6 "None of these grades"
7 "Not sure"
/
qhowmarijuana
1 "Did not use marijuana"
2 "Smoked it"
3 "Ate in food"
4 "Drank in tea or other drink"
5 "Vaporized"
6 "Some other way"
/
qhallucdrug
1 "0 times"
2 "1 or 2 times"
3 "3 to 9 times"
4 "10 to 19 times"
5 "20 to 39 times"
6 "40 or more times"
/
qsunscreenuse
1 "Never"
2 "Rarely"
3 "Sometimes"
4 "Most of the time"
5 "Always"
/
qindoortanning
1 "0 times"
2 "1 or 2 times"
3 "3 to 9 times"
4 "10 to 19 times"
5 "20 to 39 times"
6 "40 or more times"
/
qmusclestrength
1 "0 days"
2 "1 day"
3 "2 days"
4 "3 days"
5 "4 days"
6 "5 days"
7 "6 days"
8 "7 days"
/
qgenderexp
1 "Very feminine"
2 "Mostly feminine"
3 "Somewhat feminine"
4 "Equally feminine and masculine"
5 "Somewhat masculine"
6 "Mostly masculine"
7 "Very masculine"
/
qcelldriving
1 "I did not drive a car or other vehicle during the past 30 days"
2 "0 days"
3 "1 or 2 days"
4 "3 to 5 days"
5 "6 to 9 days"
6 "10 to 19 days"
7 "20 to 29 days"
8 "All 30 days"
/
qbullyweight
1 "Yes"
2 "No"
/
qbullygay
1 "Yes"
2 "No"
/
qtypealcohol
1 "I did not drink alcohol during the past 30 days"
2 "I do not have a usual type"
3 "Beer"
4 "Flavored malt beverages"
5 "Wine coolers"
6 "Wine"
7 "Liquor"
8 "Some other type"
/
qcigschool
1 "0 days"
2 "1 or 2 days"
3 "3 to 5 days"
4 "6 to 9 days"
5 "10 to 19 days"
6 "20 to 29 days"
7 "All 30 days"
/
qchewtobschool
1 "0 days"
2 "1 or 2 days"
3 "3 to 5 days"
4 "6 to 9 days"
5 "10 to 19 days"
6 "20 to 29 days"
7 "All 30 days"
/
qalcoholschool
1 "0 days"
2 "1 or 2 days"
3 "3 to 5 days"
4 "6 to 9 days"
5 "10 to 19 days"
6 "20 to 29 days"
7 "All 30 days"
/
qmarijuanaschool
1 "0 times"
2 "1 or 2 times"
3 "3 to 9 times"
4 "10 to 19 times"
5 "20 to 39 times"
6 "40 or more times"
/
qprescription30d
1 "0 times"
2 "1 or 2 times"
3 "3 to 9 times"
4 "10 to 19 times"
5 "20 to 39 times"
6 "40 or more times"
/
qcurrentcocaine
1 "0 times"
2 "1 or 2 times"
3 "3 to 9 times"
4 "10 to 19 times"
5 "20 to 39 times"
6 "40 or more times"
/
qcurrentasthma
1 "I have never had asthma"
2 "Yes"
3 "No"
4 "Not Sure"
/
qtaughtsexed
1 "Yes"
2 "No"
3 "Not sure"
/
qtaughtstd
1 "Yes"
2 "No"
3 "Not sure"
/
qtaughtbc
1 "Yes"
2 "No"
3 "Not sure"
/
qdietpop
1 "Did not drink diet soda or pop"
2 "1 to 3 times"
3 "4 to 6 times"
4 "1 time per day"
5 "2 times per day"
6 "3 times per day"
7 "4 or more times per day"
/
qcoffeetea
1 "Did not drink coffee or tes"
2 "1 to 3 times"
3 "4 to 6 times"
4 "1 time per day"
5 "2 times per day"
6 "3 times per day"
7 "4 or more times per day"
/
qsportsdrink
1 "Did not drink sports drink"
2 "1 to 3 times"
3 "4 to 6 times"
4 "1 time per day"
5 "2 times per day"
6 "3 times per day"
7 "4 or more times per day"
/
qenergydrink
1 "Did not drink energy drink"
2 "1 to 3 times"
3 "4 to 6 times"
4 "1 time per day"
5 "2 times per day"
6 "3 times per day"
7 "4 or more times per day"
/
qsugardrink
1 "Did not drink sugar drinks"
2 "1 to 3 times"
3 "4 to 6 times"
4 "1 time per day"
5 "2 times per day"
6 "3 times per day"
7 "4 or more times per day"
/
qwater
1 "Did not drink water"
2 "1 to 3 times"
3 "4 to 6 times"
4 "1 time per day"
5 "2 times per day"
6 "3 times per day"
7 "4 or more times per day"
/
qfastfood
1 "0 days"
2 "1 day"
3 "2 days"
4 "3 days"
5 "4 days"
6 "5 days"
7 "6 days"
8 "7 days"
/
qfoodallergy
1 "Yes"
2 "No"
3 "Not sure"
/
qsunburn
1 "0 times"
2 "1 time"
3 "2 times"
4 "3 times"
5 "4 times"
6 "5 or more times"
/
qconcentrating
1 "Yes"
2 "No"
/
qspeakenglish
1 "Very well"
2 "Well"
3 "Not well"
4 "Not at all"
/
sitecode
'AK' 'Alaska'
'AL' 'Alabama'
'AR' 'Arkansas'
'AZB' 'Arizona'
'CA' 'California'
'CT' 'Connecticut'
'DE' 'Delaware'
'FL' 'Florida'
'IA' 'Iowa'
'ID' 'Idaho'
'IL' 'Illinois'
'KS' 'Kansas'
'KY' 'Kentucky'
'LA' 'Louisiana'
'MD' 'Maryland'
'ME' 'Maine'
'MI' 'Michigan'
'MO' 'Missouri'
'MS' 'Mississippi'
'MT' 'Montana'
'NC' 'North Carolina'
'ND' 'North Dakota'
'NE' 'Nebraska'
'NH' 'New Hampshire'
'NJ' 'New Jersey'
'NM' 'New Mexico'
'NV' 'Nevada'
'NY' 'New York'
'OK' 'Oklahoma'
'RI' 'Rhode Island'
'SC' 'South Carolina'
'SD' 'South Dakota'
'TN' 'Tennessee'
'UT' 'Utah'
'VA' 'Virginia'
'WI' 'Wisconsin'
'WV' 'West Virginia'
'WY' 'Wyoming'
'XX' 'United States'
'FT' 'Broward County, FL'
'CH' 'Chicago, IL'
'CM' 'Charlotte-Mecklenburg County, NC'
'DA' 'Dallas, TX'
'DU' 'Duval County, FL'
'MM' 'Miami-Dade County, FL'
'NYC' 'New York City, NY'
'NYG' 'Borough of Bronx, NY'
'NYH' 'Borough of Brooklyn, NY'
'NYI' 'Borough of Manhattan, NY'
'NYJ' 'Borough of Queens, NY'
'NYK' 'Borough of Staten Island, NY'
'OL' 'Orange County, FL'
'SA' 'San Diego, CA'
'SB' 'San Bernardino, CA'
'SE' 'Seattle, WA'
/
age 
1 "12 years old or younger"
2 "13 years old"
3 "14 years old"
4 "15 years old"
5 "16 years old"
6 "17 years old"
7 "18 years old or older"
/
sex 
1 "Female"
2 "Male"
/
grade
1 "9th"
2 "10th"
3 "11th"
4 "12th"
/
race4
1 "White"
2 "Black or African American"
3 "Hispanic/Latino"
4 "All other races"
/
race7
1 "Am Indian / Alaska Native"
2 "Asian"
3 "Black or African American"
4 "Hispanic/Latino"
5 "Native Hawaiian/other PI"
6 "White"
7 "Multiple - Non-Hispanic"
/
sexid 		
1 "Heterosexual"
2 "Gay or Lesbian"
3 "Bisexual"
4 "Not Sure"
/
sexid2		
1 "Heterosexual"
2 "Sexual Minority"
3 "Unsure"
/
sexpart     
1 "Never had sex"
2 "Opposite sex only"
3 "Same sex only"
4 "Both Sexes"
/
sexpart2    
1 "Never had sex"
2 "Opposite sex only"
3 "Same sex only or both sexes"
/.

MISSING VALUES
sitecode ("     ") sitetypenum ("        ")
year ("        ") survyear ("   ") weight ("          ") stratum ("        ")
PSU ("        ") record ("        ") age ("   ") sex ("   ") grade ("   ")
race4 ("   ") race7 ("   ") stheight ("        ") stweight ("        ")
bmi ("        ") bmipct ("        ") qnobese ("   ") qnowt ("   ")
q68 (" ") q67 (" ") sexid ("        ") sexid2 ("        ")
sexpart ("        ") sexpart2 ("        ")
q8 (" ") q9 (" ") q10 (" ") q11 (" ") q12 (" ")
q13 (" ") q14 (" ") q15 (" ") q16 (" ") q17 (" ")
q18 (" ") q19 (" ") q20 (" ") q21 (" ") q22 (" ")
q23 (" ") q24 (" ") q25 (" ") q26 (" ") q27 (" ")
q28 (" ") q29 (" ") q30 (" ") q31 (" ") q32 (" ")
q33 (" ") q34 (" ") q35 (" ") q36 (" ") q37 (" ")
q38 (" ") q39 (" ") q40 (" ") q41 (" ") q42 (" ")
q43 (" ") q44 (" ") q45 (" ") q46 (" ") q47 (" ")
q48 (" ") q49 (" ") q50 (" ") q51 (" ") q52 (" ")
q53 (" ") q54 (" ") q55 (" ") q56 (" ") q57 (" ")
q58 (" ") q59 (" ") q60 (" ") q61 (" ") q62 (" ")
q63 (" ") q64 (" ") q65 (" ") q66 (" ") 
q69 (" ") q70 (" ") q71 (" ") q72 (" ")
q73 (" ") q74 (" ") q75 (" ") q76 (" ") q77 (" ")
q78 (" ") q79 (" ") q80 (" ") q81 (" ") q82 (" ")
q83 (" ") q84 (" ") q85 (" ") q86 (" ") q87 (" ")
q88 (" ") q89 (" ") 
qn8 ("   ")  qn9 ("   ") qn10 ("   ") qn11 ("   ") qn12 ("   ") 
qn13 ("   ") qn14 ("   ") qn15 ("   ") qn16 ("   ") qn17 ("   ") 
qn18 ("   ") qn19 ("   ") qn20 ("   ") qn21 ("   ") qn22 ("   ") 
qn23 ("   ") qn24 ("   ") qn25 ("   ") qn26 ("   ") qn27 ("   ") 
qn28 ("   ") qn29 ("   ") qn30 ("   ") qn31 ("   ") qn32 ("   ")
qn33 ("   ") qn34 ("   ") qn35 ("   ") qn36 ("   ") qn37 ("   ") 
qn38 ("   ") qn39 ("   ") qn40 ("   ") qn41 ("   ") qn42 ("   ") 
qn43 ("   ") qn44 ("   ") qn45 ("   ") qn46 ("   ") qn47 ("   ") 
qn48 ("   ") qn49 ("   ") qn50 ("   ") qn51 ("   ") qn52 ("   ") 
qn53 ("   ") qn54 ("   ") qn55 ("   ") qn56 ("   ") qn57 ("   ") 
qn58 ("   ") qn59 ("   ") qn60 ("   ") qn61 ("   ") qn62 ("   ")
qn63 ("   ") qn64 ("   ") qn65 ("   ") qn66 ("   ")
qn69 ("   ") qn70 ("   ") qn71 ("   ") qn72 ("   ")
qn73 ("   ") qn74 ("   ") qn75 ("   ") qn76 ("   ") qn77 ("   ") 
qn78 ("   ") qn79 ("   ") qn80 ("   ") qn81 ("   ") qn82 ("   ") 
qn83 ("   ") qn84 ("   ") qn85 ("   ") qn86 ("   ") qn87 ("   ") 
qn88 ("   ") qn89 ("   ")
qnfrcig ("   ") qndaycig ("   ") qncigint ("   ") 
qntob2 ("   ") qntob3 ("   ") qntob4 ("   ")
qnnotob2 ("   ") qnnotob3 ("   ") qnnotob4 ("   ")
qniudimp ("   ") qnshparg ("   ") qnothhpl ("   ")
qndualbc ("   ") qnbcnone ("   ") qnfr0 ("   ")
qnfr1 ("   ") qnfr2 ("   ") qnfr3 ("   ")
qnveg0 ("   ") qnveg1 ("   ") qnveg2 ("   ")
qnveg3 ("   ") qnsoda1 ("   ") qnsoda2 ("   ")
qnsoda3 ("   ") qnmilk1 ("   ") qnmilk2 ("   ")
qnmilk3 ("   ") qnbk7day ("   ") qnpa0day ("   ")
qnpa7day ("   ") qndlype ("   ")
qhowmarijuana (" ") qhallucdrug (" ") qsunscreenuse (" ")
qindoortanning (" ") qmusclestrength (" ") qgenderexp (" ")
qcelldriving (" ") qbullyweight (" ") qbullygay (" ")
qtypealcohol (" ") qcigschool (" ") qchewtobschool (" ")
qalcoholschool (" ") qmarijuanaschool (" ") qprescription30d (" ")
qcurrentcocaine (" ") qcurrentasthma (" ") qtaughtsexed (" ")
qtaughtstd (" ") qtaughtbc (" ") qdietpop (" ")
qcoffeetea (" ") qsportsdrink (" ") qenergydrink (" ")
qsugardrink (" ") qwater (" ") qfastfood (" ")
qfoodallergy (" ") qsunburn (" ") qconcentrating (" ")
qspeakenglish (" ")
qnhowmarijuana ("   ") qnhallucdrug ("   ") qnsunscreenuse ("   ")
qnindoortanning ("   ") qnmusclestrength ("   ") qngenderexp ("   ")
qncelldriving ("   ") qnbullyweight ("   ") qnbullygay ("   ")
qntypealcohol ("   ") qncigschool ("   ") qnchewtobschool ("   ")
qnalcoholschool ("   ") qnmarijuanaschool ("   ") qnprescription30d ("   ") 
qncurrentcocaine ("   ") qncurrentasthma ("   ") qntaughtsexed ("   ") 
qntaughtstd ("   ") qntaughtbc ("   ") qndietpop ("   ")
qncoffeetea ("   ") qnsportsdrink ("   ") qnspdrk1 ("   ")
qnspdrk2 ("   ") qnspdrk3 ("   ") qnenergydrink ("   ")
qnsugardrink ("   ") qnwater ("   ") qnwater1 ("   ")
qnwater2 ("   ") qnwater3 ("   ") qnfastfood ("   ")
qnfoodallergy ("   ") qnsunburn ("   ") qnconcentrating ("   ")
qnspeakenglish ("   ").

Formats stheight stweight (F5.2).

SAVE OUTFILE "C:\sadc2015\sadc2015_xxxxxxx.sav"/.
 
GET FILE="C:\sadc2015\sadc2015_xxxxxxx.sav"/.

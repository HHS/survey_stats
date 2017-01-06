* 
This SPSS syntax reads ASCII format (text format) 1999 YRBS data and creates a formatted 
and labeled SPSS data file that you can analyze in SPSS;

*
Change the file location specifications from "c:\yrbs1999" to the location where you have 
stored the SPSS syntax and the YRBS ASCII data file before you run this syntax;  
Change the location specification in three places - in the "data list" statement at the top 
of the syntax and in the "save" and "get" statements at the end of the syntax;.

DATA LIST FILE="c:\yrbs1999\yrbs1999.dat"/
Q1 1-1 (A) Q2 2-2 (A) Q3 3-3 (A)
Q4 4-4 (A) Q5 5-12 Q6 13-20
Q7 21-21 (A) Q8 22-22 (A) Q9 23-23 (A)
Q10 24-24 (A) Q11 25-25 (A) Q12 26-26 (A)
Q13 27-27 (A) Q14 28-28 (A) Q15 29-29 (A)
Q16 30-30 (A) Q17 31-31 (A) Q18 32-32 (A)
Q19 33-33 (A) Q20 34-34 (A) Q21 35-35 (A)
Q22 36-36 (A) Q23 37-37 (A) Q24 38-38 (A)
Q25 39-39 (A) Q26 40-40 (A) Q27 41-41 (A)
Q28 42-42 (A) Q29 43-43 (A) Q30 44-44 (A)
Q31 45-45 (A) Q32 46-46 (A) Q33 47-47 (A)
Q34 48-48 (A) Q35 49-49 (A) Q36 50-50 (A)
Q37 51-51 (A) Q38 52-52 (A) Q39 53-53 (A)
Q40 54-54 (A) Q41 55-55 (A) Q42 56-56 (A)
Q43 57-57 (A) Q44 58-58 (A) Q45 59-59 (A)
Q46 60-60 (A) Q47 61-61 (A) Q48 62-62 (A)
Q49 63-63 (A) Q50 64-64 (A) Q51 65-65 (A)
Q52 66-66 (A) Q53 67-67 (A) Q54 68-68 (A)
Q55 69-69 (A) Q56 70-70 (A) Q57 71-71 (A)
Q58 72-72 (A) Q59 73-73 (A) Q60 74-74 (A)
Q61 75-75 (A) Q62 76-76 (A) Q63 77-77 (A)
Q64 78-78 (A) Q65 79-79 (A) Q66 80-80 (A)
Q67 81-81 (A) Q68 82-82 (A) Q69 83-83 (A)
Q70 84-84 (A) Q71 85-85 (A) Q72 86-86 (A)
Q73 87-87 (A) Q74 88-88 (A) Q75 89-89 (A)
Q76 90-90 (A) Q77 91-91 (A) Q78 92-92 (A)
Q79 93-93 (A) Q80 94-94 (A) Q81 95-95 (A)
Q82 96-96 (A) Q83 97-97 (A)Q84 98-98 (A)
Q85 99-99 (A) Q86 100-100 (A) Q87 101-101 (A)
Q88 102-102 (A) Q89 103-103 (A) Q90 104-104 (A)
Q91 105-105 (A) Q92 106-106 (A)
WEIGHT 107-114 STRATUM 115-117 PSU 118-123
GREG 124-124 (A)
METROST 125-125 (A).
EXECUTE.

VARIABLE LABELS
Q1 "HOW OLD ARE YOU"
Q2 "WHAT IS YOUR SEX"
Q3 "IN WHAT GRADE ARE YOU"
Q4 "HOW DO YOU DESCRIBE YOURSELF"
Q5 "HEIGHT (IN METERS)"
Q6 "WEIGHT (IN KILOGRAMS)"
Q7 "HOW OFTEN WEAR HELMET RIDING MOTORCYCLE"
Q8 "HOW OFTEN WEAR HELMET RIDING BICYCLE"
Q9 "HOW OFTEN WEAR BELT WHEN RIDING IN A CAR"
Q10 "HOW OFTEN RIDE WITH DRINKING DRIVER"
Q11 "HOW MANY TIMES DRIVE WHILE DRINKING"
Q12 "HOW MANY DAYS IN PAST 30 CARRY WEAPON"
Q13 "HOW MANY DAYS IN PAST 30 CARRY GUN"
Q14 "HOW MANY DAYS CARRY WEAPON AT SCHOOL"
Q15 "HOW MANY DAYS NO SCHOOL BECAUSE UNSAFE"
Q16 "HOW MANY TIMES THREATENED/INJURED SCHOOL"
Q17 "HOW MANY TIMES IN PHYSICAL FIGHT"
Q18 "HOW MANY TIMES INJURED IN FIGHT"
Q19 "HOW MANY TIMES IN FIGHT AT SCHOOL"
Q20 "EVER HIT BY BOYFRIEND OR GIRLFRIEND"
Q21 "EVER BEEN FORCED TO HAVE SEX"
Q22 "EVER FELT SO SAD THAT STOPPED ACTIVITIES"
Q23 "HAVE YOU SERIOUSLY CONSIDERED SUICIDE"
Q24 "DID YOU MAKE A PLAN ABOUT SUICIDE"
Q25 "HOW MANY TIMES DID ATTEMPT SUICIDE"
Q26 "DID SUICIDE ATTEMPT RESULT IN INJURY"
Q27 "HAVE YOU EVER TRIED CIGARETTE SMOKING"
Q28 "AGE WHEN SMOKED FIRST CIGARETTE"
Q29 "HOW MANY DAYS DID YOU SMOKE CIGARETTES"
Q30 "HOW MANY CIGARETTES PER DAY"
Q31 "HOW DID YOU GET YOUR CIGARETTES"
Q32 "ASKED FOR PROOF OF AGE BUYING CIGARETTES"
Q33 "SMOKED CIGARETTES AT SCHOOL PAST 30 DAYS"
Q34 "HAVE EVER SMOKED CIGARETTES REGULARLY"
Q35 "HAVE YOU EVER TRIED TO QUIT SMOKING"
Q36 "DID YOU USE CHEWING TOBACCO OR SNUFF"
Q37 "USED CHEWING TOBACCO/SNUFF AT SCHOOL"
Q38 "SMOKE CIGARS DURING THE PAST 30 DAYS"
Q39 "DAYS HAD AT LEAST ONE DRINK OF ALCOHOL"
Q40 "AGE OF FIRST DRINK OF ALCOHOL"
Q41 "HOW MANY PAST 30 DAYS AT LEAST ONE DRINK"
Q42 "HOW MANY PAST 30 DAYS 5 OR MORE DRINKS"
Q43 "HOW MANY DAYS DRANK ALCOHOL AT SCHOOL"
Q44 "TIMES USED MARIJUANA DURING YOUR LIFE"
Q45 "HOW OLD WHEN FIRST TRIED MARIJUANA"
Q46 "HOW MANY TIMES PAST 30 DAYS MARIJUANA"
Q47 "HOW MANY TIMES USED MARIJUANA AT SCHOOL"
Q48 "HOW MANY TIMES IN LIFE USED COCAINE"
Q49 "HOW MANY TIMES PAST 30 DAYS USED COCAINE"
Q50 "HOW MANY TIMES IN LIFE SNIFFED GLUE"
Q51 "SNIFFED GLUE TO GET HIGH PAST 30 DAYS"
Q52 "HOW MANY TIMES IN LIFE USED HEROIN"
Q53 "HOW MANY TIMES USED METHAMPHETAMINES"
Q54 "HOW MANY TIMES IN LIFE USED STEROIDS"
Q55 "HOW MANY TIMES INJECTED ILLEGAL DRUG"
Q56 "ANYONE OFFERED YOU DRUGS AT SCHOOL"
Q57 "EVER HAD SEXUAL INTERCOURSE"
Q58 "AGE WHEN FIRST HAD SEXUAL INTERCOURSE"
Q59 "NUMBER OF SEX PARTNERS IN LIFE"
Q60 "NUMBER OF SEX PARTNERS IN PAST 3 MONTHS"
Q61 "USE ALCOHOL OR DRUGS BEFORE LAST SEX"
Q62 "USE CONDOM DURING LAST SEX"
Q63 "WHAT BIRTH CONTROL USED DURING LAST SEX"
Q64 "TIMES BEEN OR GOTTEN SOMEONE PREGNANT"
Q65 "HOW DO YOU DESCRIBE YOUR WEIGHT"
Q66 "WHICH ARE YOU TRYING TO DO ABOUT WEIGHT"
Q67 "DID YOU EXERCISE TO LOSE WEIGHT"
Q68 "ATE LESS FOOD TO LOSE WEIGHT"
Q69 "FASTED TO LOSE WEIGHT"
Q70 "DID YOU TAKE DIET PILLS TO LOSE WEIGHT"
Q71 "VOMITED OR TOOK LAXATIVES TO LOSE WEIGHT"
Q72 "HOW MANY TIMES DID YOU DRINK FRUIT JUICE"
Q73 "HOW MANY TIMES DID YOU EAT FRUIT"
Q74 "HOW MANY TIMES DID YOU EAT GREEN SALAD"
Q75 "HOW MANY TIMES DID YOU EAT POTATOES"
Q76 "HOW MANY TIMES DID YOU EAT CARROTS"
Q77 "TIMES ATE OTHER VEGETABLES"
Q78 "HOW MANY GLASSES OF MILK DID YOU DRINK"
Q79 "HOW MANY PAST 7 DAYS DO HARD EXERCISE"
Q80 "HOW MANY PAST 7 DAYS DO EASY EXERCISE"
Q81 "HOW MANY PAST 7 DAYS DO TONING EXERCISE"
Q82 "HOW MANY HOURS DO YOU WATCH TV"
Q83 "HOW MANY DAYS DO YOU GO TO PE CLASS"
Q84 "HOW MANY MINUTES EXERCISE IN PE CLASS"
Q85 "ON HOW MANY SPORTS TEAMS DID YOU PLAY"
Q86 "TIMES INJURED WHILE EXERCISING"
Q87 "BEEN TAUGHT ABOUT AIDS/HIV IN SCHOOL"
Q88 "WHICH BRAND USUALLY SMOKED"
Q89 "HOW LONG SINCE LAST CHECK-UP OR PHYSICAL"
Q90 "DISCUSSED STD/PREG PREV WITH DOCTOR"
Q91 "LAST TIME SAW A DENTIST"
Q92 "HOW OFTEN WEAR SUNBLOCK"
weight "Analysis weight"
stratum "Stratum"
psu "PSU"
GREG "Geographic Region"
METROST "Metropolitan Status".

VALUE LABELS
Q1
1 "12 years old or younger"
2 "13 years old"
3 "14 years old"
4 "15 years old"
5 "16 years old"
6 "17 years old"
7 "18 years old or older"
/
Q2
1 "Female"
2 "Male"
/
Q3
1 "9th grade"
2 "10th grade"
3 "11th grade"
4 "12th grade"
5 "Ungraded or other grade"
/
Q4
1 "Am Indian / Alaska Native"
2 "Asian"
3 "Black or African American"
4 "Hispanic or Latino"
5 "Native Hawaiian/other PI"
6 "White"
7 "Multiple - Hispanic"
8 "Multiple - Non-hispanic"
/
Q7
1 "Did not ride a motorcycle"
2 "Never"
3 "Rarely"
4 "Sometimes"
5 "Most of the time"
6 "Always"
/
Q8
1 "Did not ride a bicycle"
2 "Never"
3 "Rarely"
4 "Sometimes"
5 "Most of the time"
6 "Always"
/
Q9
1 "Never"
2 "Rarely"
3 "Sometimes"
4 "Most of the time"
5 "Always"
/
Q10
1 "0 times"
2 "1 time"
3 "2 or 3 times"
4 "4 or 5 times"
5 "6 or more times"
/
Q11
1 "0 times"
2 "1 time"
3 "2 or 3 times"
4 "4 or 5 times"
5 "6 or more times"
/
Q12
1 "0 days"
2 "1 day"
3 "2 or 3 days"
4 "4 or 5 days"
5 "6 or more days"
/
Q13
1 "0 days"
2 "1 day"
3 "2 or 3 days"
4 "4 or 5 days"
5 "6 or more days"
/
Q14
1 "0 days"
2 "1 day"
3 "2 or 3 days"
4 "4 or 5 days"
5 "6 or more days"
/
Q15
1 "0 days"
2 "1 day"
3 "2 or 3 days"
4 "4 or 5 days"
5 "6 or more days"
/
Q16
1 "0 times"
2 "1 time"
3 "2 or 3 times"
4 "4 or 5 times"
5 "6 or 7 times"
6 "8 or 9 times"
7 "10 or 11 times"
8 "12 or more times"
/
Q17
1 "0 times"
2 "1 time"
3 "2 or 3 times"
4 "4 or 5 times"
5 "6 or 7 times"
6 "8 or 9 times"
7 "10 or 11 times"
8 "12 or more times"
/
Q18
1 "0 times"
2 "1 time"
3 "2 or 3 times"
4 "4 or 5 times"
5 "6 or more times"
/
Q19
1 "0 times"
2 "1 time"
3 "2 or 3 times"
4 "4 or 5 times"
5 "6 or 7 times"
6 "8 or 9 times"
7 "10 or 11 times"
8 "12 or more times"
/
Q20
1 "Yes"
2 "No"
/
Q21
1 "Yes"
2 "No"
/
Q22
1 "Yes"
2 "No"
/
Q23
1 "Yes"
2 "No"
/
Q24
1 "Yes"
2 "No"
/
Q25
1 "0 times"
2 "1 time"
3 "2 or 3 times"
4 "4 or 5 times"
5 "6 or more times"
/
Q26
1 "Did not attempt suicide"
2 "Yes"
3 "No"
/
Q27
1 "Yes"
2 "No"
/
Q28
1 "Never smoked a cigarette"
2 "8 years old or younger"
3 "9 or 10 years old"
4 "11 or 12 years old"
5 "13 or 14 years old"
6 "15 or 16 years old"
7 "17 years old or older"
/
Q29
1 "0 days"
2 "1 or 2 days"
3 "3 to 5 days"
4 "6 to 9 days"
5 "10 to 19 days"
6 "20 to 29 days"
7 "All 30 days"
/
Q30
1 "Did not smoke"
2 "Less than 1 per day"
3 "1 cigarette per day"
4 "2 to 5 cigarettes per day"
5 "6 to 10 cigarettes per day"
6 "11 to 20 cigarettes per day"
7 "More than 20 per day"
/
Q31
1 "Did not smoke cigarettes"
2 "Store"
3 "Vending machine"
4 "Someone else bought them"
5 "Borrowed them"
6 "Stole them"
7 "Some other way"
/
Q32
1 "Did not buy cigarettes"
2 "Yes"
3 "No"
/
Q33
1 "0 days"
2 "1 or 2 days"
3 "3 to 5 days"
4 "6 to 9 days"
5 "10 to 19 days"
6 "20 to 29 days"
7 "All 30 days"
/
Q34
1 "Yes"
2 "No"
/
Q35
1 "Yes"
2 "No"
/
Q36
1 "0 days"
2 "1 or 2 days"
3 "3 to 5 days"
4 "6 to 9 days"
5 "10 to 19 days"
6 "20 to 29 days"
7 "All 30 days"
/
Q37
1 "0 days"
2 "1 or 2 days"
3 "3 to 5 days"
4 "6 to 9 days"
5 "10 to 19 days"
6 "20 to 29 days"
7 "All 30 days"
/
Q38
1 "0 days"
2 "1 or 2 days"
3 "3 to 5 days"
4 "6 to 9 days"
5 "10 to 19 days"
6 "20 to 29 days"
7 "All 30 days"
/
Q39
1 "0 days"
2 "1 or 2 days"
3 "3 to 9 days"
4 "10 to 19 days"
5 "20 to 39 days"
6 "40 to 99 days"
7 "100 or more days"
/
Q40
1 "Never drank alcohol"
2 "8 years old or younger"
3 "9 or 10 years old"
4 "11 or 12 years old"
5 "13 or 14 years old"
6 "15 or 16 years old"
7 "17 years old or older"
/
Q41
1 "0 days"
2 "1 or 2 days"
3 "3 to 5 days"
4 "6 to 9 days"
5 "10 to 19 days"
6 "20 to 29 days"
7 "All 30 days"
/
Q42
1 "0 days"
2 "1 day"
3 "2 days"
4 "3 to 5 days"
5 "6 to 9 days"
6 "10 to 19 days"
7 "20 or more days"
/
Q43
1 "0 days"
2 "1 or 2 days"
3 "3 to 5 days"
4 "6 to 9 days"
5 "10 to 19 days"
6 "20 to 29 days"
7 "All 30 days"
/
Q44
1 "0 times"
2 "1 or 2 times"
3 "3 to 9 times"
4 "10 to 19 times"
5 "20 to 39 times"
6 "40 to 99 times"
7 "100 or more times"
/
Q45
1 "Never tried marijuana"
2 "8 years old or younger"
3 "9 or 10 years old"
4 "11 or 12 years old"
5 "13 or 14 years old"
6 "15 or 16 years old"
7 "17 years old or older"
/
Q46
1 "0 times"
2 "1 or 2 times"
3 "3 to 9 times"
4 "10 to 19 times"
5 "20 to 39 times"
6 "40 or more times"
/
Q47
1 "0 times"
2 "1 or 2 times"
3 "3 to 9 times"
4 "10 to 19 times"
5 "20 to 39 times"
6 "40 or more times"
/
Q48
1 "0 times"
2 "1 or 2 times"
3 "3 to 9 times"
4 "10 to 19 times"
5 "20 to 39 times"
6 "40 or more times"
/
Q49
1 "0 times"
2 "1 or 2 times"
3 "3 to 9 times"
4 "10 to 19 times"
5 "20 to 39 times"
6 "40 or more times"
/
Q50
1 "0 times"
2 "1 or 2 times"
3 "3 to 9 times"
4 "10 to 19 times"
5 "20 to 39 times"
6 "40 or more times"
/
Q51
1 "0 times"
2 "1 or 2 times"
3 "3 to 9 times"
4 "10 to 19 times"
5 "20 to 39 times"
6 "40 or more times"
/
Q52
1 "0 times"
2 "1 or 2 times"
3 "3 to 9 times"
4 "10 to 19 times"
5 "20 to 39 times"
6 "40 or more times"
/
Q53
1 "0 times"
2 "1 or 2 times"
3 "3 to 9 times"
4 "10 to 19 times"
5 "20 to 39 times"
6 "40 or more times"
/
Q54
1 "0 times"
2 "1 or 2 times"
3 "3 to 9 times"
4 "10 to 19 times"
5 "20 to 39 times"
6 "40 or more times"
/
Q55
1 "0 times"
2 "1 time"
3 "2 or more times"
/
Q56
1 "Yes"
2 "No"
/
Q57
1 "Yes"
2 "No"
/
Q58
1 "Never had sexual intercourse"
2 "11 years old or younger"
3 "12 years old"
4 "13 years old"
5 "14 years old"
6 "15 years old"
7 "16 years old"
8 "17 years old or older"
/
Q59
1 "Never had sexual intercourse"
2 "1 person"
3 "2 people"
4 "3 people"
5 "4 people"
6 "5 people"
7 "6 or more people"
/
Q60
1 "Never had sexual intercourse"
2 "None during past 3 months"
3 "1 person"
4 "2 people"
5 "3 people"
6 "4 people"
7 "5 people"
8 "6 or more people"
/
Q61
1 "Never had sexual intercourse"
2 "Yes"
3 "No"
/
Q62
1 "Never had sexual intercourse"
2 "Yes"
3 "No"
/
Q63
1 "Never had sexual intercourse"
2 "No method was used"
3 "Birth control pills"
4 "Condoms"
5 "Depo-Provera"
6 "Withdrawal"
7 "Some other method"
8 "Not sure"
/
Q64
1 "0 times"
2 "1 time"
3 "2 or more times"
4 "Not sure"
/
Q65
1 "Very underweight"
2 "Slightly underweight"
3 "About the right weight"
4 "Slightly overweight"
5 "Very overweight"
/
Q66
1 "Lose weight"
2 "Gain weight"
3 "Stay the same weight"
4 "Not trying to do anything"
/
Q67
1 "Yes"
2 "No"
/
Q68
1 "Yes"
2 "No"
/
Q69
1 "Yes"
2 "No"
/
Q70
1 "Yes"
2 "No"
/
Q71
1 "Yes"
2 "No"
/
Q72
1 "Not during the past 7 days"
2 "1 to 3 times past 7 days"
3 "4 to 6 times past 7 days"
4 "1 time per day"
5 "2 times per day"
6 "3 times per day"
7 "4 or more times per day"
/
Q73
1 "Not during the past 7 days"
2 "1 to 3 times past 7 days"
3 "4 to 6 times past 7 days"
4 "1 time per day"
5 "2 times per day"
6 "3 times per day"
7 "4 or more times per day"
/
Q74
1 "Not during the past 7 days"
2 "1 to 3 times past 7 days"
3 "4 to 6 times past 7 days"
4 "1 time per day"
5 "2 times per day"
6 "3 times per day"
7 "4 or more times per day"
/
Q75
1 "Not during the past 7 days"
2 "1 to 3 times past 7 days"
3 "4 to 6 times past 7 days"
4 "1 time per day"
5 "2 times per day"
6 "3 times per day"
7 "4 or more times per day"
/
Q76
1 "Not during the past 7 days"
2 "1 to 3 times past 7 days"
3 "4 to 6 times past 7 days"
4 "1 time per day"
5 "2 times per day"
6 "3 times per day"
7 "4 or more times per day"
/
Q77
1 "Not during the past 7 days"
2 "1 to 3 times past 7 days"
3 "4 to 6 times past 7 days"
4 "1 time per day"
5 "2 times per day"
6 "3 times per day"
7 "4 or more times per day"
/
Q78
1 "Not during the past 7 days"
2 "1 to 3 glasses past 7 days"
3 "4 to 6 glasses past 7 days"
4 "1 glass per day"
5 "2 glasses per day"
6 "3 glasses per day"
7 "4 or more glasses per day"
/
Q79
1 "0 days"
2 "1 day"
3 "2 days"
4 "3 days"
5 "4 days"
6 "5 days"
7 "6 days"
8 "7 days"
/
Q80
1 "0 days"
2 "1 day"
3 "2 days"
4 "3 days"
5 "4 days"
6 "5 days"
7 "6 days"
8 "7 days"
/
Q81
1 "0 days"
2 "1 day"
3 "2 days"
4 "3 days"
5 "4 days"
6 "5 days"
7 "6 days"
8 "7 days"
/
Q82
1 "No TV on average school day"
2 "Less than 1 hour per day"
3 "1 hour per day"
4 "2 hours per day"
5 "3 hours per day"
6 "4 hours per day"
7 "5 or more hours per day"
/
Q83
1 "0 days"
2 "1 day"
3 "2 days"
4 "3 days"
5 "4 days"
6 "5 days"
/
Q84
1 "Do not take PE"
2 "Less than 10 minutes"
3 "10 to 20 minutes"
4 "21 to 30 minutes"
5 "More than 30 minutes"
/
Q85
1 "0 teams"
2 "1 team"
3 "2 teams"
4 "3 or more teams"
/
Q86
1 "0 times"
2 "1 time"
3 "2 times"
4 "3 times"
5 "4 times"
6 "5 or more times"
/
Q87
1 "Yes"
2 "No"
3 "Not sure"
/
Q88
1 "Did not smoke past 30 days"
2 "Do not have a usual brand"
3 "Camel"
4 "Marlboro"
5 "Newport"
6 "Virginia Slims"
7 "GPC, Basic, or Doral"
8 "Some other brand"
/
Q89
1 "During the past 12 months"
2 "Between 12 and 24 months"
3 "More than 24 months ago"
4 "Never"
5 "Not sure"
/
Q90
1 "Yes"
2 "No"
3 "Not sure"
/
Q91
1 "During the past 12 months"
2 "Between 12 and 24 months"
3 "More than 24 months ago"
4 "Never"
5 "Not sure"
/
Q92
1 "Never"
2 "Rarely"
3 "Sometimes"
4 "Most of the time"
5 "Always"
/
GREG
1 "Northeast"
2 "Midwest"
3 "South"
4 "West"
/
METROST
1 "Urban"
2 "Suburban"
3 "Metropolitan"
/.

MISSING VALUES
Q1 (" ")
Q2 (" ") Q3 (" ") Q4 (" ")
Q5 ("     ") Q6 ("     ") Q7 (" ")
Q8 (" ") Q9 (" ") Q10 (" ")
Q11 (" ") Q12 (" ") Q13 (" ")
Q14 (" ") Q15 (" ") Q16 (" ")
Q17 (" ") Q18 (" ") Q19 (" ")
Q20 (" ") Q21 (" ") Q22 (" ")
Q23 (" ") Q24 (" ") Q25 (" ")
Q26 (" ") Q27 (" ") Q28 (" ")
Q29 (" ") Q30 (" ") Q31 (" ")
Q32 (" ") Q33 (" ") Q34 (" ")
Q35 (" ") Q36 (" ") Q37 (" ")
Q38 (" ") Q39 (" ") Q40 (" ")
Q41 (" ") Q42 (" ") Q43 (" ")
Q44 (" ") Q45 (" ") Q46 (" ")
Q47 (" ") Q48 (" ") Q49 (" ")
Q50 (" ") Q51 (" ") Q52 (" ")
Q53 (" ") Q54 (" ") Q55 (" ")
Q56 (" ") Q57 (" ") Q58 (" ")
Q59 (" ") Q60 (" ") Q61 (" ")
Q62 (" ") Q63 (" ") Q64 (" ")
Q65 (" ") Q66 (" ") Q67 (" ")
Q68 (" ") Q69 (" ") Q70 (" ")
Q71 (" ") Q72 (" ") Q73 (" ")
Q74 (" ") Q75 (" ") Q76 (" ")
Q77 (" ") Q78 (" ") Q79 (" ")
Q80 (" ") Q81 (" ") Q82 (" ")
Q83 (" ") Q84 (" ") Q85 (" ")
Q86 (" ") Q87 (" ") Q88 (" ")
Q89 (" ") Q90 (" ") Q91 (" ")
Q92 (" ") 
weight ("        ")
stratum ("   ")
psu ("      ")
greg (" ") metrost (" ").

Formats q5 q6 (F5.2) weight (F8.4).

EXECUTE.

SAVE OUTFILE='c:\yrbs1999\yrbs1999.sav'
/COMPRESSED.
EXECUTE.

GET FILE='c:\yrbs1999\yrbs1999.sav'.
EXECUTE.






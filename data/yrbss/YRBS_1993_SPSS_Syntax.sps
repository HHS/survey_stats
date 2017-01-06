* 
This SPSS syntax reads ASCII format (text format) 1993 YRBS data and creates a formatted 
and labeled SPSS data file that you can analyze in SPSS;

*
Change the file location specifications from "c:\yrbs1993" to the location where you have 
stored the SPSS syntax and the YRBS ASCII data file before you run this syntax;  
Change the location specification in three places - in the "data list" statement at the top 
of the syntax and in the "save" and "get" statements at the end of the syntax;.

DATA LIST FILE="c:\yrbs1993\yrbs1993.dat"/
Q1 1-1 (A) Q2 2-2 (A) Q3 3-3 (A) Q4 4-4 (A)
Q5 5-5 (A) Q6 6-6 (A) Q7 7-7 (A) Q8 8-8 (A)
Q9 9-9 (A) Q10 10-10 (A) Q11 11-11 (A)
Q12 12-12 (A) Q13 13-13 (A) Q14 14-14 (A) 
Q15 15-15 (A) Q16 16-16 (A) Q17 17-17 (A)
Q18 18-18 (A) Q19 19-19 (A) Q20 20-20 (A)
Q21 21-21 (A) Q22 22-22 (A) Q23 23-23 (A)
Q24 24-24 (A) Q25 25-25 (A) Q26 26-26 (A)
Q27 27-27 (A) Q28 28-28 (A) Q29 29-29 (A)
Q30 30-30 (A) Q31 31-31 (A) Q32 32-32 (A)
Q33 33-33 (A) Q34 34-34 (A) Q35 35-35 (A)
Q36 36-36 (A) Q37 37-37 (A) Q38 38-38 (A)
Q39 39-39 (A) Q40 40-40 (A) Q41 41-41 (A)
Q42 42-42 (A) Q43 43-43 (A) Q44 44-44 (A)
Q45 45-45 (A) Q46 46-46 (A) Q47 47-47 (A)
Q48 48-48 (A) Q49 49-49 (A) Q50 50-50 (A)
Q51 51-51 (A) Q52 52-52 (A) Q53 53-53 (A)
Q54 54-54 (A) Q55 55-55 (A) Q56 56-56 (A)
Q57 57-57 (A) Q58 58-58 (A) Q59 59-59 (A)
Q60 60-60 (A) Q61 61-61 (A) Q62 62-62 (A)
Q63 63-63 (A) Q64 64-64 (A) Q65 65-65 (A)
Q66 66-66 (A) Q67 67-67 (A) Q68 68-68 (A)
Q69 69-69 (A) Q70 70-70 (A) Q71 71-71 (A)
Q72 72-72 (A) Q73 73-73 (A) Q74 74-74 (A)
Q75 75-75 (A) Q76 76-76 (A) Q77 77-77 (A) 
Q78 78-78 (A) Q79 79-79 (A) Q80 80-80 (A) 
Q81 81-81 (A) Q82 82-82 (A) Q83 83-83 (A) 
Q84 84-84 (A) Q85 85-85 (A) Q86 86-86 (A) 
Q87 87-87 (A)
weight 88-97 psu 98-102 stratum 103-107 
GREG 108-108 (A).
EXECUTE.

VARIABLE LABELS
Q1 "HOW OLD ARE YOU"
Q2 "WHAT IS YOUR SEX"
Q3 "IN WHAT GRADE ARE YOU"
Q4 "HOW DO YOU DESCRIBE YOURSELF"
Q5 "WHAT KIND OF STUDENT ARE YOU"
Q6 "HOW OFTEN WEAR SEAT BELT WITH SOMEONE"
Q7 "HOW MANY TIMES RIDE MOTORCYCLE"
Q8 "HOW OFTEN WEAR HELMET RIDING MOTORCYCLE"
Q9 "HOW OFTEN RIDE BICYCLE"
Q10 "HOW OFTEN WEAR HELMET RIDING BICYCLE"
Q11 "HOW OFTEN RIDE WITH DRINKING DRIVER"
Q12 "HOW MANY TIMES DRIVE WHILE DRINKING"
Q13 "HOW MANY TIMES CARRY WEAPON"
Q14 "HOW MANY DAYS IN PAST 30 CARRY GUN"
Q15 "HOW MANY DAYS CARRY WEAPON AT SCHOOL"
Q16 "HOW MANY DAYS NO SCHOOL BECAUSE UNSAFE"
Q17 "HOW MANY TIMES THREATENED/INJURED SCHOOL"
Q18 "HOW MANY TIMES PROPERTY STOLEN AT SCHOOL"
Q19 "HOW MANY TIMES IN PHYSICAL FIGHT"
Q20 "WITH WHOM DID YOU FIGHT IN LAST FIGHT"
Q21 "HOW MANY TIMES INJURED IN FIGHT"
Q22 "HOW MANY TIMES IN FIGHT AT SCHOOL"
Q23 "HOW MANY TIMES SWIM WITH SUPERVISION"
Q24 "HAVE YOU SERIOUSLY CONSIDERED SUICIDE"
Q25 "DID YOU MAKE A PLAN ABOUT SUICIDE"
Q26 "HOW MANY TIMES DID ATTEMPT SUICIDE"
Q27 "DID SUICIDE ATTEMPT RESULT IN INJURY"
Q28 "HAVE YOU EVER TRIED CIGARETTE SMOKING"
Q29 "AGE WHEN SMOKED FIRST CIGARETTE"
Q30 "EVER SMOKED CIGARETTES REGULARLY"
Q31 "AGE WHEN STARTED SMOKING REGULARLY"
Q32 "HOW MANY DAYS DID YOU SMOKE CIGARETTES"
Q33 "HOW MANY CIGARETTES PER DAY"
Q34 "HOW MANY DAYS SMOKE CIGARETTES AT SCHOOL"
Q35 "TRY TO QUIT SMOKING LAST 6 MONTHS"
Q36 "DID YOU USE CHEWING TOBACCO OR SNUFF"
Q37 "USE CHEWING TOBACCO/SNUFF AT SCHOOL"
Q38 "AGE OF FIRST DRINK OF ALCOHOL"
Q39 "HOW MANY DAYS IN LIFE AT LEAST ONE DRINK"
Q40 "HOW MANY PAST 30 DAYS AT LEAST ONE DRINK"
Q41 "HOW MANY PAST 30 DAYS 5 OR MORE DRINKS"
Q42 "HOW MANY DAYS DRINK ALCOHOL AT SCHOOL"
Q43 "HOW OLD WHEN FIRST TRIED MARIJUANA"
Q44 "HOW MANY TIMES IN LIFE USED MARIJUANA"
Q45 "HOW MANY TIMES PAST 30 DAYS MARIJUANA"
Q46 "HOW MANY TIMES USE MARIJUANA AT SCHOOL"
Q47 "HOW OLD WHEN FIRST TRIED COCAINE"
Q48 "HOW MANY TIMES IN LIFE USED COCAINE"
Q49 "HOW MANY TIMES PAST 30 DAYS USE COCAINE"
Q50 "HOW MANY TIMES IN LIFE CRACK/FREEBASE"
Q51 "HOW MANY TIMES IN LIFE USE ILLEGAL DRUGS"
Q52 "HOW MANY TIMES IN LIFE USED STEROIDS"
Q53 "EVER IN LIFE INJECTED ILLEGAL DRUG"
Q54 "ANYONE OFFERED YOU DRUGS AT SCHOOL"
Q55 "EVER TAUGHT ABOUT AIDS/HIV IN SCHOOL"
Q56 "EVER TALKED ABOUT AIDS WITH PARENTS"
Q57 "EVER HAD SEXUAL INTERCOURSE"
Q58 "AGE WHEN FIRST HAD SEXUAL INTERCOURSE"
Q59 "NUMBER OF SEX PARTNERS IN LIFE"
Q60 "NUMBER OF SEX PARTNERS IN PAST 3 MONTHS"
Q61 "USE ALCOHOL OR DRUGS BEFORE LAST SEX"
Q62 "USE CONDOM DURING LAST SEX"
Q63 "WHAT BIRTH CONTROL USED DURING LAST SEX"
Q64 "HOW MANY BEEN/GOTTEN SOMEONE PREGNANT"
Q65 "EVER BEEN TOLD THAT YOU HAVE A STD"
Q66 "HOW DO YOU THINK OF YOURSELF"
Q67 "WHICH ARE YOU TRYING TO DO"
Q68 "WHICH DID YOU DO TO LOSE WEIGHT"
Q69 "WHICH DID YOU DO TO LOSE WEIGHT"
Q70 "YESTERDAY DID YOU EAT FRUIT"
Q71 "YESTERDAY DID YOU DRINK FRUIT JUICE"
Q72 "YESTERDAY DID YOU EAT GREEN SALAD"
Q73 "YESTERDAY DID YOU EAT COOKED VEGETABLES"
Q74 "YESTERDAY DID YOU EAT HAMBURGER"
Q75 "YESTERDAY DID YOU EAT FRENCH FRIES"
Q76 "YESTERDAY DID YOU EAT COOKIES"
Q77 "HOW MANY PAST 7 DAYS DO HARD EXERCISE"
Q78 "HOW MANY PAST 7 DAYS DO STRETCHING"
Q79 "HOW MANY PAST 7 DAYS DO TONING EXERCISE"
Q80 "HOW MANY DAYS BIKE/WALK FOR 30 MINUTES"
Q81 "HOW MANY DAYS DO YOU GO TO PE CLASS"
Q82 "HOW MANY MINUTES EXERCISE IN PE CLASS"
Q83 "ON HOW MANY TEAMS AT SCHOOL"
Q84 "ON HOW MANY TEAMS OUTSIDE SCHOOL"
Q85 "HOW MANY CLASS PERIODS TAUGHT ABOUT AIDS"
Q86 "HOW FAR IN SCHOOL DID YOU MOTHER GO"
Q87 "HOW FAR IN SCHOOL DID YOUR FATHER GO"
weight "Analysis weight"
stratum "Stratum"
psu "PSU"
GREG "Geographic Region".

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
5 "Ungraded or other"
/
Q4
1 "White - not Hispanic"
2 "Black - not Hispanic"
3 "Hispanic"
4 "Asian or Pacific Islander"
5 "Native American or Alaskan"
6 "Other"
/
Q5
1 "One of the best"
2 "Far above the middle"
3 "A little above the middle"
4 "In the middle"
5 "A little below the middle"
6 "Far below the middle"
7 "Near the bottom"
/
Q6
1 "Never"
2 "Rarely"
3 "Sometimes"
4 "Most of the time"
5 "Always"
/
Q7
1 "0 times"
2 "1 to 10 times"
3 "11 to 20 times"
4 "21 to 39 times"
5 "40 or more times"
/
Q8
1 "Did not ride a motorcycle"
2 "Never"
3 "Rarely"
4 "Sometimes"
5 "Most of the time"
6 "Always"
/
Q9
1 "0 times"
2 "1 to 10 times"
3 "11 to 20 times"
4 "21 to 39 times"
5 "40 or more times"
/
Q10
1 "Did not ride a bicycle"
2 "Never"
3 "Rarely"
4 "Sometimes"
5 "Most of the time"
6 "Always"
/
Q11
1 "0 times"
2 "1 time"
3 "2 or 3 times"
4 "4 or 5 times"
5 "6 or more times"
/
Q12
1 "0 times"
2 "1 time"
3 "2 or 3 times"
4 "4 or 5 times"
5 "6 or more times"
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
1 "0 days"
2 "1 day"
3 "2 or 3 days"
4 "4 or 5 days"
5 "6 or more days"
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
5 "6 or 7 times"
6 "8 or 9 times"
7 "10 or 11 times"
8 "12 or more times"
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
1 "Have never been in a fight"
2 "Total stranger"
3 "Friend or someone I know"
4 "Boyfriend, girlfriend, date"
5 "Family member"
6 "Someone not listed above"
7 "More than one of the above"
/
Q21
1 "0 times"
2 "1 time"
3 "2 or 3 times"
4 "4 or 5 times"
5 "6 or more times"
/
Q22
1 "0 times"
2 "1 time"
3 "2 or 3 times"
4 "4 or 5 times"
5 "6 or 7 times"
6 "8 or 9 times"
7 "10 or 11 times"
8 "12 or more times"
/
Q23
1 "Did not go swimming"
2 "Never"
3 "Rarely"
4 "Sometimes"
5 "Most of the time"
6 "Always"
/
Q24
1 "Yes"
2 "No"
/
Q25
1 "Yes"
2 "No"
/
Q26
1 "0 times"
2 "1 time"
3 "2 or 3 times"
4 "4 or 5 times"
5 "6 or more times"
/
Q27
1 "Did not attempt suicide"
2 "Yes"
3 "No"
/
Q28
1 "Yes"
2 "No"
/
Q29
1 "Never smoked a cigarette"
2 "Less than 9 years old"
3 "9 or 10 years old"
4 "11 or 12 years old"
5 "13 or 14 years old"
6 "15 or 16 years old"
7 "17 or more years old"
/
Q30
1 "Yes"
2 "No"
/
Q31
1 "Never smoked regularly"
2 "Less than 9 years old"
3 "9 or 10 years old"
4 "11 or 12 years old"
5 "13 or 14 years old"
6 "15 or 16 years old"
7 "17 or more years old"
/
Q32
1 "0 days"
2 "1 or 2 days"
3 "3 to 5 days"
4 "6 to 9 days"
5 "10 to 19 days"
6 "20 to 29 days"
7 "All 30 days"
/
Q33
1 "Did not smoke"
2 "Less than 1 per day"
3 "1 per day"
4 "2 to 5 per day"
5 "6 to 10 per day"
6 "11 to 20 per day"
7 "More than 20 per day"
/
Q34
1 "0 days"
2 "1 or 2 days"
3 "3 to 5 days"
4 "6 to 9 days"
5 "10 to 19 days"
6 "20 to 29 days"
7 "All 30 days"
/
Q35
1 "Did not smoke"
2 "Yes"
3 "No"
/
Q36
1 "No"
2 "Yes, chewing tobacco only"
3 "Yes, snuff only"
4 "Yes, both tobacco and snuff"
/
Q37
1 "No"
2 "Yes, chewing tobacco only"
3 "Yes, snuff only"
4 "Yes, both tobacco and snuff"
/
Q38
1 "Never drank alcohol"
2 "Less than 9 years old"
3 "9 or 10 years old"
4 "11 or 12 years old"
5 "13 or 14 years old"
6 "15 or 16 years old"
7 "17 or more years old"
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
1 "0 days"
2 "1 or 2 days"
3 "3 to 5 days"
4 "6 to 9 days"
5 "10 to 19 days"
6 "20 to 29 days"
7 "All 30 days"
/
Q41
1 "0 days"
2 "1 day"
3 "2 days"
4 "3 to 5 days"
5 "6 to 9 days"
6 "10 to 19 days"
7 "20 or more days"
/
Q42
1 "0 days"
2 "1 or 2 days"
3 "3 to 5 days"
4 "6 to 9 days"
5 "10 to 19 days"
6 "20 to 29 days"
7 "All 30 days"
/
Q43
1 "Never tried marijuana"
2 "Less than 9 years old"
3 "9 or 10 years old"
4 "11 or 12 years old"
5 "13 or 14 years old"
6 "15 or 16 years old"
7 "17 or more years old"
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
1 "0 times"
2 "1 or 2 times"
3 "3 to 9 times"
4 "10 to 19 times"
5 "20 to 39 times"
6 "40 or more times"
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
1 "Never tried cocaine"
2 "Less than 9 years old"
3 "9 or 10 years old"
4 "11 or 12 years old"
5 "13 or 14 years old"
6 "15 or 16 years old"
7 "17 or more years old"
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
1 "Yes"
2 "No"
/
Q54
1 "Yes"
2 "No"
/
Q55
1 "Yes"
2 "No"
3 "Not sure"
/
Q56
1 "Yes"
2 "No"
3 "Not sure"
/
Q57
1 "Yes"
2 "No"
/
Q58
1 "Never had sexual intercourse"
2 "Less than 12 years old"
3 "12 years old"
4 "13 years old"
5 "14 years old"
6 "15 years old"
7 "16 years old"
8 "17 or more years old"
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
5 "Withdrawal"
6 "Some other method"
7 "Not sure"
/
Q64
1 "0 times"
2 "1 time"
3 "2 or more times"
4 "Not sure"
/
Q65
1 "Yes"
2 "No"
/
Q66
1 "Very underweight"
2 "Slightly underweight"
3 "About the right weight"
4 "Slightly overweight"
5 "Very overweight"
/
Q67
1 "Lose weight"
2 "Gain weight"
3 "Stay the same weight"
4 "Not trying to do anything"
/
Q68
1 "Did not do anything"
2 "Dieted"
3 "Exercised"
4 "Exercised and dieted"
5 "Other method"
/
Q69
1 "Did not do anything"
2 "Made myself vomit"
3 "Took diet pills"
4 "Vomiting and diet pills"
5 "Other method"
/
Q70
1 "No"
2 "Yes, once only"
3 "Yes, twice or more"
/
Q71
1 "No"
2 "Yes, once only"
3 "Yes, twice or more"
/
Q72
1 "No"
2 "Yes, once only"
3 "Yes, twice or more"
/
Q73
1 "No"
2 "Yes, once only"
3 "Yes, twice or more"
/
Q74
1 "No"
2 "Yes, once only"
3 "Yes, twice or more"
/
Q75
1 "No"
2 "Yes, once only"
3 "Yes, twice or more"
/
Q76
1 "No"
2 "Yes, once only"
3 "Yes, twice or more"
/
Q77
1 "0 days"
2 "1 day"
3 "2 days"
4 "3 days"
5 "4 days"
6 "5 days"
7 "6 days"
8 "7 days"
/
Q78
1 "0 days"
2 "1 day"
3 "2 days"
4 "3 days"
5 "4 days"
6 "5 days"
7 "6 days"
8 "7 days"
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
/
Q82
1 "Do not take PE"
2 "Less than 10 minutes"
3 "10 to 20 minutes"
4 "21 to 30 minutes"
5 "More than 30 minutes"
/
Q83
1 "0 teams"
2 "1 team"
3 "2 teams"
4 "3 or more teams"
/
Q84
1 "0 teams"
2 "1 team"
3 "2 teams"
4 "3 or more teams"
/
Q85
1 "0 periods"
2 "1 to 2 periods"
3 "3 to 5 periods"
4 "6 to 10 periods"
5 "11 or more periods"
6 "Not sure"
/
Q86
1 "Did not finish high school"
2 "Graduated from high school"
3 "Some after high school"
4 "Graduated from college"
5 "Not sure"
/
Q87
1 "Did not finish high school"
2 "Graduated from high school"
3 "Some after high school"
4 "Graduated from college"
5 "Not sure"
/
GREG
1 "Northeast"
2 "Midwest"
3 "South"
4 "West"
/
.

MISSING VALUES
Q1 (" ") Q2 (" ") Q3 (" ") Q4 (" ")
Q5 (" ") Q6 (" ") Q7 (" ")
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
Q86 (" ") Q87 (" ")
weight ("        ")
psu ("     ")
stratum ("    ")
greg (" ").

Formats weight (F10.8) .

EXECUTE.

SAVE OUTFILE='c:\yrbs1993\yrbs1993.sav'
/COMPRESSED.
EXECUTE.

GET FILE='c:\yrbs1993\yrbs1993.sav'.
EXECUTE.








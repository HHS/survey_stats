* 
This SPSS syntax reads ASCII format (text format) 1995 YRBS data and creates a formatted 
and labeled SPSS data file that you can analyze in SPSS;

*
Change the file location specifications from "c:\yrbs1995" to the location where you have 
stored the SPSS syntax and the YRBS ASCII data file before you run this syntax;  
Change the location specification in three places - in the "data list" statement at the top 
of the syntax and in the "save" and "get" statements at the end of the syntax;.

DATA LIST FILE="c:\yrbs1995\yrbs1995.dat"/
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
Q87 87-87 (A) Q88 88-88 (A)
WEIGHT 89-100 PSU 101-105 STRATUM 106-110
GREG 111-111 (A).
EXECUTE.

VARIABLE LABELS
Q1 "HOW OLD ARE YOU"
Q2 "WHAT IS YOUR SEX"
Q3 "IN WHAT GRADE ARE YOU"
Q4 "HOW DO YOU DESCRIBE YOURSELF"
Q5 "HOW OFTEN WEAR SEAT BELT WITH SOMEONE"
Q6 "HOW MANY TIMES RIDE MOTORCYCLE"
Q7 "HOW OFTEN WEAR HELMET RIDING MOTORCYCLE"
Q8 "HOW OFTEN RIDE BICYCLE"
Q9 "HOW OFTEN WEAR HELMET RIDING BICYCLE"
Q10 "HOW OFTEN RIDE WITH DRINKING DRIVER"
Q11 "HOW MANY TIMES DRIVE WHILE DRINKING"
Q12 "HOW MANY DAYS IN PAST 30 CARRY WEAPON"
Q13 "HOW MANY DAYS IN PAST 30 CARRY GUN"
Q14 "HOW MANY DAYS CARRY WEAPON AT SCHOOL"
Q15 "HOW MANY DAYS NO SCHOOL BECAUSE UNSAFE"
Q16 "HOW MANY TIMES THREATENED/INJURED SCHOOL"
Q17 "HOW MANY TIMES PROPERTY STOLEN AT SCHOOL"
Q18 "HOW MANY TIMES IN PHYSICAL FIGHT"
Q19 "HOW MANY TIMES INJURED IN FIGHT"
Q20 "HOW MANY TIMES IN FIGHT AT SCHOOL"
Q21 "WITH WHOM DID YOU FIGHT IN LAST FIGHT"
Q22 "HAVE YOU SERIOUSLY CONSIDERED SUICIDE"
Q23 "DID YOU MAKE A PLAN ABOUT SUICIDE"
Q24 "HOW MANY TIMES DID ATTEMPT SUICIDE"
Q25 "DID SUICIDE ATTEMPT RESULT IN INJURY"
Q26 "HAVE YOU EVER TRIED CIGARETTE SMOKING"
Q27 "AGE WHEN SMOKED FIRST CIGARETTE"
Q28 "HOW MANY DAYS DID YOU SMOKE CIGARETTES"
Q29 "HOW MANY CIGARETTES PER DAY"
Q30 "HOW DID YOU GET YOUR CIGARETTES"
Q31 "ASKED FOR PROOF OF AGE BUYING CIGARETTES"
Q32 "HOW MANY DAYS SMOKE CIGARETTES AT SCHOOL"
Q33 "HAVE YOU TRIED TO QUIT SMOKING"
Q34 "DID YOU USE CHEWING TOBACCO OR SNUFF"
Q35 "USE CHEWING TOBACCO/SNUFF AT SCHOOL"
Q36 "AGE OF FIRST DRINK OF ALCOHOL"
Q37 "HOW MANY DAYS IN LIFE AT LEAST ONE DRINK"
Q38 "HOW MANY PAST 30 DAYS AT LEAST ONE DRINK"
Q39 "HOW MANY PAST 30 DAYS 5 OR MORE DRINKS"
Q40 "HOW MANY DAYS DRINK ALCOHOL AT SCHOOL"
Q41 "HOW OLD WHEN FIRST TRIED MARIJUANA"
Q42 "HOW MANY TIMES IN LIFE USED MARIJUANA"
Q43 "HOW MANY TIMES PAST 30 DAYS MARIJUANA"
Q44 "HOW MANY TIMES USE MARIJUANA AT SCHOOL"
Q45 "HOW OLD WHEN FIRST TRIED COCAINE"
Q46 "HOW MANY TIMES IN LIFE USED COCAINE"
Q47 "HOW MANY TIMES PAST 30 DAYS USE COCAINE"
Q48 "HOW MANY TIMES IN LIFE CRACK/FREEBASE"
Q49 "HOW MANY TIMES HAVE YOU SNIFFED GLUE"
Q50 "HOW MANY TIMES IN LIFE USED STEROIDS"
Q51 "HOW MANY TIMES IN LIFE USE ILLEGAL DRUGS"
Q52 "HOW MANY TIMES INJECTED ILLEGAL DRUG"
Q53 "ANYONE OFFERED YOU DRUGS AT SCHOOL"
Q54 "EVER TAUGHT ABOUT AIDS/HIV IN SCHOOL"
Q55 "EVER TALKED ABOUT AIDS WITH PARENTS"
Q56 "EVER HAD SEXUAL INTERCOURSE"
Q57 "AGE WHEN FIRST HAD SEXUAL INTERCOURSE"
Q58 "NUMBER OF SEX PARTNERS IN LIFE"
Q59 "NUMBER OF SEX PARTNERS IN PAST 3 MONTHS"
Q60 "USE ALCOHOL OR DRUGS BEFORE LAST SEX"
Q61 "USE CONDOM DURING LAST SEX"
Q62 "WHAT BIRTH CONTROL USED DURING LAST SEX"
Q63 "HOW MANY BEEN/GOTTEN SOMEONE PREGNANT"
Q64 "HOW DO YOU DESCRIBE YOUR WEIGHT"
Q65 "WHICH ARE YOU TRYING TO DO ABOUT WEIGHT"
Q66 "DID YOU DIET TO LOSE WEIGHT"
Q67 "DID YOU EXERCISE TO LOSE WEIGHT"
Q68 "DID YOU VOMIT TO LOSE WEIGHT"
Q69 "DID YOU TAKE DIET PILLS TO LOSE WEIGHT"
Q70 "HOW MANY TIMES DID YOU EAT FRUIT"
Q71 "HOW MANY TIMES DID YOU DRINK FRUIT JUICE"
Q72 "HOW MANY TIMES DID YOU EAT GREEN SALAD"
Q73 "HOW MANY TIMES EAT COOKED VEGETABLES"
Q74 "HOW MANY TIMES DID YOU EAT HAMBURGER"
Q75 "HOW MANY TIMES DID YOU EAT FRENCH FRIES"
Q76 "HOW MANY TIMES DID YOU EAT COOKIES"
Q77 "HOW MANY PAST 7 DAYS DO HARD EXERCISE"
Q78 "HOW MANY PAST 7 DAYS DO STRETCHING"
Q79 "HOW MANY PAST 7 DAYS DO TONING EXERCISE"
Q80 "HOW MANY DAYS BIKE/WALK FOR 30 MINUTES"
Q81 "HOW MANY DAYS DO YOU GO TO PE CLASS"
Q82 "HOW MANY MINUTES EXERCISE IN PE CLASS"
Q83 "ON HOW MANY TEAMS AT SCHOOL"
Q84 "ON HOW MANY TEAMS OUTSIDE SCHOOL"
Q85 "EVER SMOKED CIGARETTES REGULARLY"
Q86 "HOW OLD WHEN STARTED SMOKING REGULARLY"
Q87 "HOW MUCH EDUCATION DOES MOTHER HAVE"
Q88 "HOW MUCH EDUCATION DOES FATHER HAVE"
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
3 "Hispanic or Latino"
4 "Asian or Pacific Islander"
5 "Native American or Alaskan"
6 "Other"
/
Q5
1 "Never"
2 "Rarely"
3 "Sometimes"
4 "Most of the time"
5 "Always"
/
Q6
1 "0 times"
2 "1 to 10 times"
3 "11 to 20 times"
4 "21 to 39 times"
5 "40 or more times"
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
1 "0 times"
2 "1 to 10 times"
3 "11 to 20 times"
4 "21 to 39 times"
5 "40 or more times"
/
Q9
1 "Did not ride a bicycle"
2 "Never"
3 "Rarely"
4 "Sometimes"
5 "Most of the time"
6 "Always"
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
5 "6 or more times"
/
Q20
1 "0 times"
2 "1 time"
3 "2 or 3 times"
4 "4 or 5 times"
5 "6 or 7 times"
6 "8 or 9 times"
7 "10 or 11 times"
8 "12 or more times"
/
Q21
1 "Have never been in a fight"
2 "Total stranger"
3 "Friend or someone I know"
4 "Boyfriend, girlfriend, date"
5 "Family member"
6 "Someone not listed above"
7 "More than one of the above"
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
1 "0 times"
2 "1 time"
3 "2 or 3 times"
4 "4 or 5 times"
5 "6 or more times"
/
Q25
1 "Did not attempt suicide"
2 "Yes"
3 "No"
/
Q26
1 "Yes"
2 "No"
/
Q27
1 "Never smoked a cigarette"
2 "8 years old or younger"
3 "9 or 10 years old"
4 "11 or 12 years old"
5 "13 or 14 years old"
6 "15 or 16 years old"
7 "17 or more years old"
/
Q28
1 "0 days"
2 "1 or 2 days"
3 "3 to 5 days"
4 "6 to 9 days"
5 "10 to 19 days"
6 "20 to 29 days"
7 "All 30 days"
/
Q29
1 "Did not smoke"
2 "Less than 1 per day"
3 "1 per day"
4 "2 to 5 per day"
5 "6 to 10 per day"
6 "11 to 20 per day"
7 "More than 20 per day"
/
Q30
1 "Did not smoke cigarettes"
2 "Store"
3 "Vending machine"
4 "Someone else bought them"
5 "Borrowed them"
6 "Stole them"
7 "Some other way"
/
Q31
1 "Did not smoke cigarettes"
2 "Did not buy cigarettes"
3 "Yes"
4 "No"
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
1 "Yes"
2 "No"
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
1 "0 days"
2 "1 or 2 days"
3 "3 to 5 days"
4 "6 to 9 days"
5 "10 to 19 days"
6 "20 to 29 days"
7 "All 30 days"
/
Q36
1 "Never drank alcohol"
2 "8 years old or younger"
3 "9 or 10 years old"
4 "11 or 12 years old"
5 "13 or 14 years old"
6 "15 or 16 years old"
7 "17 or more years old"
/
Q37
1 "0 days"
2 "1 or 2 days"
3 "3 to 9 days"
4 "10 to 19 days"
5 "20 to 39 days"
6 "40 to 99 days"
7 "100 or more days"
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
2 "1 day"
3 "2 days"
4 "3 to 5 days"
5 "6 to 9 days"
6 "10 to 19 days"
7 "20 or more days"
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
1 "Never tried marijuana"
2 "8 years old or younger"
3 "9 or 10 years old"
4 "11 or 12 years old"
5 "13 or 14 years old"
6 "15 or 16 years old"
7 "17 or more years old"
/
Q42
1 "0 times"
2 "1 or 2 times"
3 "3 to 9 times"
4 "10 to 19 times"
5 "20 to 39 times"
6 "40 to 99 times"
7 "100 or more times"
/
Q43
1 "0 times"
2 "1 or 2 times"
3 "3 to 9 times"
4 "10 to 19 times"
5 "20 to 39 times"
6 "40 or more times"
/
Q44
1 "0 times"
2 "1 or 2 times"
3 "3 to 9 times"
4 "10 to 19 times"
5 "20 to 39 times"
6 "40 or more times"
/
Q45
1 "Never tried cocaine"
2 "8 years old or younger"
3 "9 or 10 years old"
4 "11 or 12 years old"
5 "13 or 14 years old"
6 "15 or 16 years old"
7 "17 or more years old"
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
2 "1  or 2  times"
3 "3  to 9  times"
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
2 "1 time"
3 "2 or more times"
/
Q53
1 "Yes"
2 "No"
/
Q54
1 "Yes"
2 "No"
3 "Not sure"
/
Q55
1 "Yes"
2 "No"
3 "Not sure"
/
Q56
1 "Yes"
2 "No"
/
Q57
1 "Never had sexual intercourse"
2 "11 years old or younger"
3 "12 years old"
4 "13 years old"
5 "14 years old"
6 "15 years old"
7 "16 years old"
8 "17 years old or older"
/
Q58
1 "Never had sexual intercourse"
2 "1 person"
3 "2 people"
4 "3 people"
5 "4 people"
6 "5 people"
7 "6 or more people"
/
Q59
1 "Never had sexual intercourse"
2 "None during past 3 months"
3 "1 person"
4 "2 people"
5 "3 people"
6 "4 people"
7 "5 people"
8 "6 or more people"
/
Q60
1 "Never had sexual intercourse"
2 "Yes"
3 "No"
/
Q61
1 "Never had sexual intercourse"
2 "Yes"
3 "No"
/
Q62
1 "Never had sexual intercourse"
2 "No method was used"
3 "Birth control pills"
4 "Condoms"
5 "Withdrawal"
6 "Some other method"
7 "Not sure"
/
Q63
1 "0 times"
2 "1 time"
3 "2 or more times"
4 "Not sure"
/
Q64
1 "Very underweight"
2 "Slightly underweight"
3 "About the right weight"
4 "Slightly overweight"
5 "Very overweight"
/
Q65
1 "Lose weight"
2 "Gain weight"
3 "Stay the same weight"
4 "Not trying to do anything"
/
Q66
1 "Yes"
2 "No"
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
1 "0 times"
2 "1 time"
3 "2 times"
4 "3 or more times"
/
Q71
1 "0 times"
2 "1 time"
3 "2 times"
4 "3 or more times"
/
Q72
1 "0 times"
2 "1 time"
3 "2 times"
4 "3 or more times"
/
Q73
1 "0 times"
2 "1 time"
3 "2 times"
4 "3 or more times"
/
Q74
1 "0 times"
2 "1 time"
3 "2 times"
4 "3 or more times"
/
Q75
1 "0 times"
2 "1 time"
3 "2 times"
4 "3 or more times"
/
Q76
1 "0 times"
2 "1 time"
3 "2 times"
4 "3 or more times"
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
1 "Yes"
2 "No"
/
Q86
1 "Never smoked regularly"
2 "8 years old or younger"
3 "9 or 10 years old"
4 "11 or 12 years old"
5 "13 or 14 years old"
6 "15 or 16 years old"
7 "17 years old or older"
/
Q87
1 "Did not finish high school"
2 "Graduated from high school"
3 "Had some college"
4 "Graduated from college"
5 "Not sure"
/
Q88
1 "Did not finish high school"
2 "Graduated from high school"
3 "Had some college"
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
Q86 (" ") Q87 (" ") Q88 (" ")
weight ("            ")
psu ("     ")
stratum ("   ")
greg (" ").

Formats weight (F12.10) .

EXECUTE.

SAVE OUTFILE='c:\yrbs1995\yrbs1995.sav'
/COMPRESSED.
EXECUTE.

GET FILE='c:\yrbs1995\yrbs1995.sav'.
EXECUTE.



* 
This SPSS syntax reads ASCII format (text format) 2001 YRBS data and creates a formatted 
and labeled SPSS data file that you can analyze in SPSS;

*
Change the file location specifications from "c:\yrbs2001" to the location where you have 
stored the SPSS syntax and the YRBS ASCII data file before you run this syntax;  
Change the location specification in three places - in the "data list" statement at the top 
of the syntax and in the "save" and "get" statements at the end of the syntax;.

DATA LIST FILE="c:\yrbs2001\yrbs2001.dat"/
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
Q82 96-96 (A) Q83 97-97 (A) Q84 98-98 (A)
Q85 99-99 (A) Q86 100-100 (A) Q87 101-101 (A)
Q88 102-102 (A) Q89 103-103 (A) Q90 104-104 (A)
Q91 105-105 (A) Q92 106-106 (A) Q93 107-107 (A)
Q94 108-108 (A) Q95 109-109 (A)
WEIGHT 110-117 PSU 118-123 STRATUM 124-126
GREG 127-127 (A) METROST 128-128 (A).
EXECUTE.

VARIABLE LABELS
Q1 "How old are you"
Q2 "What is your sex"
Q3 "In what grade are you"
Q4 "How do you describe yourself"
Q5 "How tall are you"
Q6 "How much do you weigh"
Q7 "How were your grades past 12 months"
Q8 "How often wear motorcycle helmet"
Q9 "How often wear bicycle helmet"
Q10 "How often wear seat belt"
Q11 "How often ride w/drinking driver 30 days"
Q12 "How often drive while drinking 30 days"
Q13 "Carried weapon 30 days"
Q14 "Carried gun 30 days"
Q15 "Carried weapon at school  30 days"
Q16 "How many days feel unsafe@school 30 days"
Q17 "How  many times threatened@school 12 mos"
Q18 "How many times in fight 12 mos"
Q19 "How many times injured in fight 12 mos"
Q20 "How many times in fight @ school  12 mos"
Q21 "Did  boyfriend/girlfriend hit/slap 12 mo"
Q22 "Have you been forced to have sex"
Q23 "Ever feel sad or hopeless 12 mos"
Q24 "Ever considered suicide 12 mos"
Q25 "Ever make suicide plan 12 mos"
Q26 "Ever attempt suicide 12 mos"
Q27 "Ever injured from suicide attempt 12 mos"
Q28 "Ever smoked"
Q29 "How old when first smoked"
Q30 "How many days smoked 30 days"
Q31 "How many cigarettes/day 30 days"
Q32 "How did you get cigarettes past 30 days"
Q33 "Show age proof buying cigarettes 30 days"
Q34 "How many days smoke @ school 30 days"
Q35 "Have you ever smoked daily"
Q36 "Tried to quit smoking past 12 months"
Q37 "How many days use snuff past 30 days"
Q38 "Days use snuff school property 30 days"
Q39 "How many days smoke cigars 30 days"
Q40 "How many days drink alcohol"
Q41 "How old when first drank alcohol"
Q42 "How many days drink alcohol 30 days"
Q43 "How many days have 5+ drinks 30 days"
Q44 "How many days drink @ school 30 days"
Q45 "How many times smoke marijuana"
Q46 "How old when first tried marijuana"
Q47 "How many times use marijuana 30 days"
Q48 "How many times marijuana@school 30 days"
Q49 "How many times use cocaine"
Q50 "How many times use cocaine 30 days"
Q51 "How many times sniffed glue"
Q52 "How many times sniffed glue 30 days"
Q53 "How many times used heroin"
Q54 "How many times used methamphetamines"
Q55 "How many times used steroids"
Q56 "How many times injected drugs"
Q57 "Offered drugs @ school 12 mos"
Q58 "Ever had sex"
Q59 "How old at first sex"
Q60 "How many sex partners"
Q61 "How many sex partners 3 mos"
Q62 "Did you use alcohol/drugs @ last sex"
Q63 "Did you use condom @ last sex"
Q64 "What birth control @ last sex"
Q65 "Ever been/gotten someone pregnant"
Q66 "How do you describe your weight"
Q67 "What are you trying to do about weight"
Q68 "Did you exercise to lose weight 30 days"
Q69 "Did you eat less to lose weight 30 days"
Q70 "Did you fast to lose weight 30 days"
Q71 "Did you take pill to lose weight 30 days"
Q72 "Did you vomit to lose weight 30 days"
Q73 "How many times fruit juice 7 days"
Q74 "How many times fruit 7 days"
Q75 "How many time green salad 7 days"
Q76 "How many times potatoes 7 days"
Q77 "How many times carrots 7 days"
Q78 "How many times other vegetables 7 days"
Q79 "How many glass of milk 7 days"
Q80 "Did you do vigorous exercise 7 days"
Q81 "Did you do moderate exercise 7 days"
Q82 "Did you do toning exercise 7 days"
Q83 "How many hours watch TV"
Q84 "How many days go to PE class"
Q85 "How many minutes exercise in PE class"
Q86 "On how many sports team 12 mos"
Q87 "Ever taught about AIDS/HIV @ school"
Q88 "Seatbelt while driving"
Q89 "No usual brand"
Q90 "Ecstacy one or more time"
Q91 "Ever used LSD"
Q92 "Injured while playing sports"
Q93 "When was the last check-up when not sick"
Q94 "Dentist in last year"
Q95 "How often wear sunscreen on sunny day"
weight "Analysis weight"
stratum "Stratum"
psu "PSU"
greg "Geographic Region"
metrost "Metropolitan Status".
 
 
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
1 "Mostly A's"
2 "Mostly B's"
3 "Mostly C's"
4 "Mostly D's"
5 "Mostly F's"
6 "None of these grades"
7 "Not sure"
/
Q8
1 "Did not ride a motorcycle"
2 "Never wore a helmet"
3 "Rarely wore a helmet"
4 "Sometimes wore a helmet"
5 "Most of the time wore a helmet"
6 "Always wore a helmet"
/
Q9
1 "Did not ride a bicycle"
2 "Never wore a helmet"
3 "Rarely wore a helmet"
4 "Sometimes wore a helmet"
5 "Most of the time wore a helmet"
6 "Always wore a helmet"
/
Q10
1 "Never"
2 "Rarely"
3 "Sometimes"
4 "Most of the time"
5 "Always"
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
2 "8 years old or younger"
3 "9 or 10 years old"
4 "11 or 12 years old"
5 "13 or 14 years old"
6 "15 or 16 years old"
7 "17 years old or older"
/
Q30
1 "0 days"
2 "1 or 2 days"
3 "3 to 5 days"
4 "6 to 9 days"
5 "10 to 19 days"
6 "20 to 29 days"
7 "All 30 days"
/
Q31
1 "Did not smoke cigarettes"
2 "Less than 1 cigarette"
3 "1 cigarette"
4 "2 to 5 cigarettes"
5 "6 to 10 cigarettes"
6 "11 to 20 cigarettes"
7 "More than 20 cigarettes"
/
Q32
1 "Did not smoke cigarettes"
2 "Store or gas station"
3 "Vending machine"
4 "Someone else bought them"
5 "Borrowed/bummed them"
6 "A person 18 or older"
7 "Took them from store/family "
8 "Some other way"
/
Q33
1 "Did not buy cigarettes"
2 "Yes"
3 "No"
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
1 "Yes"
2 "No"
/
Q36
1 "Did not smoke in past 12 mos."
2 "Yes"
3 "No"
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
3 "3 to 5 days"
4 "6 to 9 days"
5 "10 to 19 days"
6 "20 to 29 days"
7 "All 30 days"
/
Q40
1 "0 days"
2 "1 or 2 days"
3 "3 to 9 days"
4 "10 to 19 days"
5 "20 to 39 days"
6 "40 to 99 days"
7 "100 or more days"
/
Q41
1 "Never drank alcohol"
2 "8 years old or younger"
3 "9 or 10 years old"
4 "11 or 12 years old"
5 "13 or 14 years old"
6 "15 or 16 years old"
7 "17 years old or older"
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
1 "0 days"
2 "1 day"
3 "2 days"
4 "3 to 5 days"
5 "6 to 9 days"
6 "10 to 19 days"
7 "20 or more days"
/
Q44
1 "0 days"
2 "1 or 2 days"
3 "3 to 5 days"
4 "6 to 9 days"
5 "10 to 19 days"
6 "20 to 29 days"
7 "All 30 days"
/
Q45
1 "0 times"
2 "1 or 2 times"
3 "3 to 9 times"
4 "10 to 19 times"
5 "20 to 39 times"
6 "40 to 99 times"
7 "100 or more times"
/
Q46
1 "Never tried marijuana"
2 "8 years old or younger"
3 "9 or 10 years old"
4 "11 or 12 years old"
5 "13 or 14 years old"
6 "15 or 16 years old"
7 "17 years old or older"
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
2 "1 or 2 times"
3 "3 to 9 times"
4 "10 to 19 times"
5 "20 to 39 times"
6 "40 or more times"
/
Q56
1 "0 times"
2 "1 time"
3 "2 or more times"
/
Q57
1 "Yes"
2 "No"
/
Q58
1 "Yes"
2 "No"
/
Q59
1 "Never had sex"
2 "11 years old or younger"
3 "12 years old"
4 "13 years old"
5 "14 years old"
6 "15 years old"
7 "16 years old"
8 "17 years old or older"
/
Q60
1 "Never had sex"
2 "1 person"
3 "2 people"
4 "3 people"
5 "4 people"
6 "5 people"
7 "6 or more people"
/
Q61
1 "Never had sex"
2 "None during past 3 months"
3 "1 person"
4 "2 people"
5 "3 people"
6 "4 people"
7 "5 people"
8 "6 or more people"
/
Q62
1 "Never had sex"
2 "Yes"
3 "No"
/
Q63
1 "Never had sex"
2 "Yes"
3 "No"
/
Q64
1 "Never had sex"
2 "No method was used"
3 "Birth control pills"
4 "Condoms"
5 "Depo-Provera"
6 "Withdrawal"
7 "Some other method"
8 "Not sure"
/
Q65
1 "0 times"
2 "1 time"
3 "2 or more times"
4 "Not sure"
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
1 "Yes"
2 "No"
/
Q73
1 "Did not drink fruit juice"
2 "1 to 3 times"
3 "4 to 6 times"
4 "1 time per day"
5 "2 times per day"
6 "3 times per day"
7 "4 or more times per day"
/
Q74
1 "Did not eat fruit"
2 "1 to 3 times"
3 "4 to 6 times"
4 "1 time per day"
5 "2 times per day"
6 "3 times per day"
7 "4 or more times per day"
/
Q75
1 "Did not eat green salad"
2 "1 to 3 times"
3 "4 to 6 times"
4 "1 time per day"
5 "2 times per day"
6 "3 times per day"
7 "4 or more times per day"
/
Q76
1 "Did not eat potatoes"
2 "1 to 3 times"
3 "4 to 6 times"
4 "1 time per day"
5 "2 times per day"
6 "3 times per day"
7 "4 or more times per day"
/
Q77
1 "Did not eat carrots"
2 "1 to 3 times"
3 "4 to 6 times"
4 "1 time per day"
5 "2 times per day"
6 "3 times per day"
7 "4 or more times per day"
/
Q78
1 "Did not eat other vegetables "
2 "1 to 3 times"
3 "4 to 6 times"
4 "1 time per day"
5 "2 times per day"
6 "3 times per day"
7 "4 or more times per day"
/
Q79
1 "Did not drink milk"
2 "1 to 3 glasses past 7 days"
3 "4 to 6 glasses past 7 days"
4 "1 glass per day"
5 "2 glasses per day"
6 "3 glasses per day"
7 "4 or more glasses per day"
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
1 "0 days"
2 "1 day"
3 "2 days"
4 "3 days"
5 "4 days"
6 "5 days"
7 "6 days"
8 "7 days"
/
Q83
1 "No TV on average school day"
2 "Less than 1 hour per day"
3 "1 hour per day"
4 "2 hours per day"
5 "3 hours per day"
6 "4 hours per day"
7 "5 or more hours per day"
/
Q84
1 "0 days"
2 "1 day"
3 "2 days"
4 "3 days"
5 "4 days"
6 "5 days"
/
Q85
1 "Do not take PE"
2 "Less than 10 minutes"
3 "10 to 20 minutes"
4 "21 to 30 minutes"
5 "31 to 40 minutes"
6 "41 to 50 minutes"
7 "51 to 60 minutes"
8 "More than 60 minutes"
/
Q86
1 "0 teams"
2 "1 team"
3 "2 teams"
4 "3 or more teams"
/
Q87
1 "Yes"
2 "No"
3 "Not sure"
/
Q88
1 "I do not drive a car"
2 "Never wear seatbelt"
3 "Rarely wear a seatbelt"
4 "Sometimes wear a seatbelt"
5 "Most of the time wear"
6 "Always wear a seatbelt"
/
Q89
1 "Did not smoke cigarettes"
2 "Do not have a usual brand"
3 "Camel"
4 "Marlboro"
5 "Newport"
6 "Virginia Slims"
7 "GPC, Basic, or Doral"
8 "Some other brand"
/
Q90
1 "0 times"
2 "1 or 2 times"
3 "3 to 9 times"
4 "10 to 19 times"
5 "20 to 39 times"
6 "40 or more times"
/
Q91
1 "0 times"
2 "1 or 2 times"
3 "3 to 9 times"
4 "10 to 19 times"
5 "20 to 39 times"
6 "40 or more times"
/
Q92
1 "No exercise in past 30 days"
2 "Yes"
3 "No"
/
Q93
1 "During the past 12 months"
2 "Between 12 and 24 months ago"
3 "More than 24 months ago"
4 "Never"
5 "Not sure"
/
Q94
1 "During the past 12 months"
2 "Between 12 and 24 months ago"
3 "More than 24 months ago"
4 "Never"
5 "Not sure"
/
Q95
1 "Never"
2 "Rarely"
3 "Sometimes"
4 "Most of the time"
5 "Always"
/
GREG
1 "Northeast"
2 "Midwest"
3 "Sout"
4 "West"
/
METROST
'0'="Unknown"
1 "Urban"
2 "Suburban"
3 "Rural"
/.

MISSING VALUES
Q1 (" ")
Q2 (" ") Q3 (" ") Q4 (" ")
Q5 ("        ") Q6 ("        ") Q7 (" ")
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
Q92 (" ") Q93 (" ") Q94 (" ")
Q95 (" ") 
weight ("        ")
psu ("      ")
stratum ("   ")
greg (" ")
metrost (" ").

Formats q5 q6 (F8.2) weight (F8.4) .

EXECUTE.

SAVE OUTFILE='c:\yrbs2001\yrbs2001.sav'
/COMPRESSED.
EXECUTE.

GET FILE='c:\yrbs2001\yrbs2001.sav'.
EXECUTE.

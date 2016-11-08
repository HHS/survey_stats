*
This SPSS syntax reads ASCII format (text format) 2015 YRBS data and creates a formatted 
and labeled SPSS data file that you can analyze in SPSS;
 
*
Change the file location specifications from "c:\yrbs2015" to the location where you have 
stored the SPSS syntax and the YRBS ASCII data file before you run this syntax;
Change the location specification in three places - in the "data list" statement at the top 
of the syntax and in the "save" and "get" statements at the end of the syntax;.
DATA LIST FILE="C:\yrbs2015\yrbs2015.dat"/
Q1 17-17  
Q2 18-18  Q3 19-19  Q4 20-20  
Q5 21-28 (A) Q6 29-32  Q7 33-38  
Q8 39-39  Q9 40-40  Q10 41-41  
Q11 42-42  Q12 43-43  Q13 44-44  
Q14 45-45  Q15 46-46  Q16 47-47  
Q17 48-48  Q18 49-49  Q19 50-50  
Q20 51-51  Q21 52-52  Q22 53-53  
Q23 54-54  Q24 55-55  Q25 56-56  
Q26 57-57  Q27 58-58  Q28 59-59  
Q29 60-60  Q30 61-61  Q31 62-62  
Q32 63-63  Q33 64-64  Q34 65-65  
Q35 66-66  Q36 67-67  Q37 68-68  
Q38 69-69  Q39 70-70  Q40 71-71  
Q41 72-72  Q42 73-73  Q43 74-74  
Q44 75-75  Q45 76-76  Q46 77-77  
Q47 78-78  Q48 79-79  Q49 80-80  
Q50 81-81  Q51 82-82  Q52 83-83  
Q53 84-84  Q54 85-85  Q55 86-86  
Q56 87-87  Q57 88-88  Q58 89-89  
Q59 90-90  Q60 91-91  Q61 92-92  
Q62 93-93  Q63 94-94  Q64 95-95  
Q65 96-96  Q66 97-97  Q67 98-98  
Q68 99-99  Q69 100-100  Q70 101-101  
Q71 102-102  Q72 103-103  Q73 104-104  
Q74 105-105  Q75 106-106  Q76 107-107  
Q77 108-108  Q78 109-109  Q79 110-110  
Q80 111-111  Q81 112-112  Q82 113-113  
Q83 114-114  Q84 115-115  Q85 116-116  
Q86 117-117  Q87 118-118  Q88 119-119  
Q89 120-120  Q90 121-121  Q91 122-122  
Q92 123-123  Q93 124-124  Q94 125-125  
Q95 126-126  Q96 127-127  Q97 128-128  
Q98 129-129  Q99 130-130  QN8 185-185  
QN9 186-186  QN10 187-187  QN11 188-188  
QN12 189-189  QN13 190-190  QN14 191-191  
QN15 192-192  QN16 193-193  QN17 194-194  
QN18 195-195  QN19 196-196  QN20 197-197  
QN21 198-198  QN22 199-199  QN23 200-200  
QN24 201-201  QN25 202-202  QN26 203-203  
QN27 204-204  QN28 205-205  QN29 206-206  
QN30 207-207  QN31 208-208  QN32 209-209  
QN33 210-210  QN34 211-211  QN35 212-212  
QN36 213-213  QN37 214-214  QN38 215-215  
QN39 216-216  QN40 217-217  QN41 218-218  
QN42 219-219  QN43 220-220  QN44 221-221  
QN45 222-222  QN46 223-223  QN47 224-224  
QN48 225-225  QN49 226-226  QN50 227-227  
QN51 228-228  QN52 229-229  QN53 230-230  
QN54 231-231  QN55 232-232  QN56 233-233  
QN57 234-234  QN58 235-235  QN59 236-236  
QN60 237-237  QN61 238-238  QN62 239-239  
QN63 240-240  QN64 241-241  QN65 242-242  
QN66 243-243  QN67 244-244  QN68 245-245  
QN69 246-246  QN70 247-247  QN71 248-248  
QN72 249-249  QN73 250-250  QN74 251-251  
QN75 252-252  QN76 253-253  QN77 254-254  
QN78 255-255  QN79 256-256  QN80 257-257  
QN81 258-258  QN82 259-259  QN83 260-260  
QN84 261-261  QN85 262-262  QN86 263-263  
QN87 264-264  QN88 265-265  QN89 266-266  
QN90 267-267  QN91 268-268  QN92 269-269  
QN93 270-270  QN94 271-271  QN95 272-272  
QN96 273-273  QN97 274-274  QN98 275-275  
QN99 276-276  site 1-3 (A) 
qnfrcig 350-350  qndaycig 351-351  
qncigint 352-352  qntob4 353-353  qntob3 354-354  
qntob2 355-355  qnnotob4 356-356  qnnotob3 357-357  
qnnotob2 358-358  qniudimp 359-359  qnshparg 360-360  
qnothhpl 361-361  qndualbc 362-362  qnbcnone 363-363  
qnfr0 364-364  qnfr1 365-365  qnfr2 366-366  
qnfr3 367-367  qnveg0 368-368  qnveg1 369-369  
qnveg2 370-370  qnveg3 371-371  qnsoda1 372-372  
qnsoda2 373-373  qnsoda3 374-374  qnmilk1 375-375  
qnmilk2 376-376  qnmilk3 377-377  qnbk7day 378-378  
qnpa0day 379-379  qnpa7day 380-380  qndlype 381-381  
qnspdrk1 382-382  qnspdrk2 383-383  qnspdrk3 384-384  
qnwater1 385-385  qnwater2 386-386  qnwater3 387-387  
qnobese 388-388  qnowt 389-389  weight 390-399  
stratum 400-402  psu 403-408  bmipct 409-413  
raceeth 414-415  q6orig 416-418  q7orig 419-421.
EXECUTE.
 
VARIABLE LABELS
Q1 "How old are you"
Q2 "What is your sex"
Q3 "In what grade are you"
Q4 "Are you Hispanic/Latino"
Q5 "What is your race"
Q6 "How tall are you"
Q7 "How much do you weigh"
Q8 "Bicycle helmet use"
Q9 "Seat belt use"
Q10 "Riding with a drinking driver"
Q11 "Drinking and driving"
Q12 "Texting and driving"
Q13 "Weapon carrying"
Q14 "Gun carrying"
Q15 "Weapon carrying at school"
Q16 "Safety concerns at school"
Q17 "Threatened at school"
Q18 "Physical fighting"
Q19 "Injurious physical fighting"
Q20 "Physical fighting at school"
Q21 "Forced sexual intercourse"
Q22 "Physical dating violence"
Q23 "Sexual dating violence"
Q24 "Bullying at school"
Q25 "Electronic bullying"
Q26 "Sad or hopeless"
Q27 "Considered suicide"
Q28 "Made a suicide plan"
Q29 "Attempted suicide"
Q30 "Injurious suicide attempt"
Q31 "Ever cigarette use"
Q32 "Initiation of cigarette use"
Q33 "Current cigarette use"
Q34 "Smoked >10 cigarettes"
Q35 "Cigarettes from store"
Q36 "Smoking cessation"
Q37 "Current smokeless tobacco use"
Q38 "Current cigar use"
Q39 "Electronic vapor product use"
Q40 "Current electronic vapor product use"
Q41 "Ever alcohol use"
Q42 "Initiation of alcohol use"
Q43 "Current alcohol use"
Q44 "5 or more drinks in a row"
Q45 "Largest number of drinks"
Q46 "Source of alcohol"
Q47 "Ever marijuana use"
Q48 "Initiation of marijuana use"
Q49 "Current marijuana use"
Q50 "Ever cocaine use"
Q51 "Ever inhalant use"
Q52 "Ever heroin use"
Q53 "Ever methamphetamine use"
Q54 "Ever ecstasy use"
Q55 "Ever synthetic marijuana use"
Q56 "Ever steroid use"
Q57 "Ever prescription drug use"
Q58 "Illegal injected drug use"
Q59 "Illegal drugs at school"
Q60 "Ever sexual intercourse"
Q61 "Sex before 13 years"
Q62 "Multiple sex partners"
Q63 "Current sexual activity"
Q64 "Alcohol/drugs and sex"
Q65 "Condom use"
Q66 "Birth control pill use"
Q67 "Sex of sexual contacts"
Q68 "Sexual identity"
Q69 "Perception of weight"
Q70 "Weight loss"
Q71 "Fruit juice drinking"
Q72 "Fruit eating"
Q73 "Salad eating"
Q74 "Potato eating"
Q75 "Carrot eating"
Q76 "Other vegetable eating"
Q77 "Soda drinking"
Q78 "How many glass of milk 7 days"
Q79 "Breakfast eating"
Q80 "Physical activity >= 5 days"
Q81 "Television watching"
Q82 "Computer use"
Q83 "PE attendance"
Q84 "Sports team participation"
Q85 "HIV testing"
Q86 "Oral health care"
Q87 "Asthma"
Q88 "Hours of sleep on school night"
Q89 "Grades in school"
Q90 "Usual use of marijuana"
Q91 "Ever used LSD"
Q92 "Sports drinks"
Q93 "Plain water"
Q94 "Food allergies"
Q95 "Muscle strengthening"
Q96 "Indoor tanning"
Q97 "Sunburn"
Q98 "Difficulty concentrating"
Q99 "How well speak English"
QN8 "Rarely or never wore a bicycle helmet"
QN9 "Rarely or never wore a seat belt"
QN10 "Rode with a driver who had been drinking alcohol"
QN11 "Drove when drinking alcohol"
QN12 "Texted or e-mailed while driving a car or other vehicle"
QN13 "Carried a weapon"
QN14 "Carried a gun"
QN15 "Carried a weapon on school property"
QN16 "Did not go to school because they felt unsafe at school or on their way to or from school"
QN17 "Were threatened or injured with a weapon on school property"
QN18 "Were in a physical fight"
QN19 "Were injured in a physical fight"
QN20 "Were in a physical fight on school property"
QN21 "Were ever physically forced to have sexual intercourse"
QN22 "Experienced physical dating violence"
QN23 "Experienced sexual dating violence"
QN24 "Were bullied on school property"
QN25 "Were electronically bullied"
QN26 "Felt sad or hopeless"
QN27 "Seriously considered attempting suicide"
QN28 "Made a plan about how they would attempt suicide"
QN29 "Attempted suicide"
QN30 "Attempted suicide that resulted in an injury, poisoning, or overdose that had to be treated by a doctor or nurse"
QN31 "Ever tried cigarette smoking"
QN32 "Smoked a whole cigarette before age 13 years"
QN33 "Currently smoked cigarettes"
QN34 "Smoked more than 10 cigarettes per day"
QN35 "Usually obtained their own cigarettes by buying them in a store or gas station"
QN36 "Tried to quit smoking cigarettes"
QN37 "Currently used smokeless tobacco"
QN38 "Currently smoked cigars"
QN39 "Ever used electronic vapor products"
QN40 "Currently used electronic vapor products"
QN41 "Ever drank alcohol"
QN42 "Drank alcohol before age 13 years"
QN43 "Currently drank alcohol"
QN44 "Drank five or more drinks of alcohol in a row"
QN45 "Reported that the largest number of drinks they had in a row was 10 or more"
QN46 "Usually obtained the alcohol they drank by someone giving it to them"
QN47 "Ever used marijuana"
QN48 "Tried marijuana before age 13 years"
QN49 "Currently used marijuana"
QN50 "Ever used cocaine"
QN51 "Ever used inhalants"
QN52 "Ever used heroin"
QN53 "Ever used methamphetamines"
QN54 "Ever used ecstasy"
QN55 "Ever used synthetic marijuana"
QN56 "Ever took steroids without a doctor's prescription"
QN57 "Ever took prescription drugs without a doctor's prescription"
QN58 "Ever injected any illegal drug"
QN59 "Were offered, sold, or given an illegal drug on school property"
QN60 "Ever had sexual intercourse"
QN61 "Had sexual intercourse before age 13 years"
QN62 "Had sexual intercourse with four or more persons"
QN63 "Were currently sexually active"
QN64 "Drank alcohol or used drugs before last sexual intercourse"
QN65 "Used a condom"
QN66 "Used birth control pills"
QN67 "Had sexual contact with females, males, or females and males"
QN68 "Described themselves as gay or lesbian or bisexual"
QN69 "Described themselves as slightly or very overweight"
QN70 "Were trying to lose weight"
QN71 "Did not drink fruit juice"
QN72 "Did not eat fruit"
QN73 "Did not eat salad"
QN74 "Did not eat potatoes"
QN75 "Did not eat carrots"
QN76 "Did not eat other vegetables"
QN77 "Did not drink a can, bottle, or glass of soda or pop"
QN78 "Did not drink milk"
QN79 "Did not eat breakfast"
QN80 "Were physically active at least 60 minutes per day on 5 or more days"
QN81 "Watched television 3 or more hours per day"
QN82 "Played video or computer games or used a computer 3 or more hours per day"
QN83 "Attended physical education classes on 1 or more days"
QN84 "Played on at least one sports team"
QN85 "Were ever tested for HIV"
QN86 "Saw a dentist"
QN87 "Had ever been told by a doctor or nurse that they had asthma"
QN88 "Had 8 or more hours of sleep"
QN89 "Made mostly A's or B's in school"
QN90 "usually used marijuana by smoking it in a joint, bong, pipe, or blunt"
QN91 "used hallucinogenic drugs"
QN92 "did not drink a can, bottle, or glass of a sports drink"
QN93 "Did not drink a bottle or glass of plain water"
QN94 "have to avoid some foods because eating the food could cause an allergic reaction"
QN95 "did exercises to strengthen or tone their muscles"
QN96 "used an indoor tanning device"
QN97 "had a sunburn"
QN98 "have serious difficulty concentrating, remembering, or making decisions"
QN99 "speak English well or very well"
site "Site Code"
qnfrcig "Currently frequently smoked cigarettes"
qndaycig "Currently smoked cigarettes daily"
qncigint "Usually obtained their own cigarettes by buying on the internet"
qntob4 "Currently used tobacco"
qntob3 "Currently used cigarettes, cigars, or smokeless tobacco"
qntob2 "Currently smoked cigarettes or cigars"
qnnotob4 "Did not currently use tobacco"
qnnotob3 "Did not currently use cigarettes, cigars, or smokeless tobacco"
qnnotob2 "Did not currently smoke cigarettes or cigars"
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
qnspdrk1 "Drank a can, bottle, or glass of a sports drink one or more times per day"
qnspdrk2 "Drank a can, bottle, or glass of a sports drink two or more times per day"
qnspdrk3 "Drank a can, bottle, or glass of a sports drink three or more times per day"
qnwater1 "Drank one or more glasses per day of water"
qnwater2 "Drank two or more glasses per day of water"
qnwater3 "Drank three or more glasses per day of water"
qnobese "Were Obese"
qnowt "Were Overweight"
weight "Weight"
stratum "Stratum"
psu "Primary Sampling Unit"
bmipct "Body Mass Index Percentage"
raceeth "Race/Ethnicity"
q6orig "Original value of Q6"
q7orig "Original value of Q7".
 
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
1 "Yes"
2 "No"
/
Q8
1 "Did not ride a bicycle"
2 "Never wore a helmet"
3 "Rarely wore a helmet"
4 "Sometimes wore a helmet"
5 "Most of the time wore a helmet"
6 "Always wore a helmet"
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
1 "Did not drive"
2 "0 times"
3 "1 time"
4 "2 or 3 times"
5 "4 or 5 times"
6 "6 or more times"
/
Q12
1 "Did not drive"
2 "0 days"
3 "1 or 2 days"
4 "3 to 5 days"
5 "6 to 9 days"
6 "10 to 19 days"
7 "20 to 29 days"
8 "All 30 days"
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
1 "Did not date"
2 "0 times"
3 "1 time"
4 "2 or 3 times"
5 "4 or 5 times"
6 "6 or more times"
/
Q23
1 "Did not date"
2 "0 times"
3 "1 time"
4 "2 or 3 times"
5 "4 or 5 times"
6 "6 or more times"
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
1 "Yes"
2 "No"
/
Q27
1 "Yes"
2 "No"
/
Q28
1 "Yes"
2 "No"
/
Q29
1 "0 times"
2 "1 time"
3 "2 or 3 times"
4 "4 or 5 times"
5 "6 or more times"
/
Q30
1 "Did not attempt suicide"
2 "Yes"
3 "No"
/
Q31
1 "Yes"
2 "No"
/
Q32
1 "Never smoked a cigarette"
2 "8 years old or younger"
3 "9 or 10 years old"
4 "11 or 12 years old"
5 "13 or 14 years old"
6 "15 or 16 years old"
7 "17 years old or older"
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
1 "Did not smoke cigarettes"
2 "Less than 1 cigarette"
3 "1 cigarette"
4 "2 to 5 cigarettes"
5 "6 to 10 cigarettes"
6 "11 to 20 cigarettes"
7 "More than 20 cigarettes"
/
Q35
1 "Did not smoke cigarettes"
2 "Store or gas station"
3 "I got them on the Internet"
4 "Someone else bought them"
5 "Borrowed/bummed them"
6 "A person 18 or older gave me"
7 "Took them from store/family "
8 "Some other way"
/
Q36
1 "Did not smoke in past 12 mos"
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
1 "Yes"
2 "No"
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
2 "1 or 2 days"
3 "3 to 9 days"
4 "10 to 19 days"
5 "20 to 39 days"
6 "40 to 99 days"
7 "100 or more days"
/
Q42
1 "Never drank alcohol"
2 "8 years old or younger"
3 "9 or 10 years old"
4 "11 or 12 years old"
5 "13 or 14 years old"
6 "15 or 16 years old"
7 "17 years old or older"
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
1 "0 days"
2 "1 day"
3 "2 days"
4 "3 to 5 days"
5 "6 to 9 days"
6 "10 to 19 days"
7 "20 or more days"
/
Q45
1 "Did not drink in past 30 days"
2 "1 or 2 drinks"
3 "3 drinks"
4 "4 drinks"
5 "5 drinks"
6 "6 or 7 drinks"
7 "8 or 9 drinks"
8 "10 or more drinks"
/
Q46
1 "Did not drink in past 30 days"
2 "Bought in store"
3 "Bought in restaurant"
4 "Bought at public event"
5 "I gave someone money to buy"
6 "Someone gave it to me"
7 "Took from store/family"
8 "Some other way"
/
Q47
1 "0 times"
2 "1 or 2 times"
3 "3 to 9 times"
4 "10 to 19 times"
5 "20 to 39 times"
6 "40 to 99 times"
7 "100 or more times"
/
Q48
1 "Never tried marijuana"
2 "8 years old or younger"
3 "9 or 10 years old"
4 "11 or 12 years old"
5 "13 or 14 years old"
6 "15 or 16 years old"
7 "17 years old or older"
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
2 "1 or 2 times"
3 "3 to 9 times"
4 "10 to 19 times"
5 "20 to 39 times"
6 "40 or more times"
/
Q57
1 "0 times"
2 "1 or 2 times"
3 "3 to 9 times"
4 "10 to 19 times"
5 "20 to 39 times"
6 "40 or more times"
/
Q58
1 "0 times"
2 "1 time"
3 "2 or more times"
/
Q59
1 "Yes"
2 "No"
/
Q60
1 "Yes"
2 "No"
/
Q61
1 "Never had sex"
2 "11 years old or younger"
3 "12 years old"
4 "13 years old"
5 "14 years old"
6 "15 years old"
7 "16 years old"
8 "17 years old or older"
/
Q62
1 "Never had sex"
2 "1 person"
3 "2 people"
4 "3 people"
5 "4 people"
6 "5 people"
7 "6 or more people"
/
Q63
1 "Never had sex"
2 "None during past 3 months"
3 "1 person"
4 "2 people"
5 "3 people"
6 "4 people"
7 "5 people"
8 "6 or more people"
/
Q64
1 "Never had sex"
2 "Yes"
3 "No"
/
Q65
1 "Never had sex"
2 "Yes"
3 "No"
/
Q66
1 "Never had sex"
2 "No method was used"
3 "Birth control pills"
4 "Condoms"
5 "IUD or implant"
6 "Shot/patch/birth control ring"
7 "Withdrawal/other method"
8 "Not sure"
/
Q67
1 "Never had sexual contact"
2 "Females"
3 "Males"
4 "Females and males"
/
Q68
1 "Heterosexual (straight)"
2 "Gay or lesbian"
3 "Bisexual"
4 "Not sure"
/
Q69
1 "Very underweight"
2 "Slightly underweight"
3 "About the right weight"
4 "Slightly overweight"
5 "Very overweight"
/
Q70
1 "Lose weight"
2 "Gain weight"
3 "Stay the same weight"
4 "Not trying to do anything"
/
Q71
1 "Did not drink fruit juice"
2 "1 to 3 times"
3 "4 to 6 times"
4 "1 time per day"
5 "2 times per day"
6 "3 times per day"
7 "4 or more times per day"
/
Q72
1 "Did not eat fruit"
2 "1 to 3 times"
3 "4 to 6 times"
4 "1 time per day"
5 "2 times per day"
6 "3 times per day"
7 "4 or more times per day"
/
Q73
1 "Did not eat green salad"
2 "1 to 3 times"
3 "4 to 6 times"
4 "1 time per day"
5 "2 times per day"
6 "3 times per day"
7 "4 or more times per day"
/
Q74
1 "Did not eat potatoes"
2 "1 to 3 times"
3 "4 to 6 times"
4 "1 time per day"
5 "2 times per day"
6 "3 times per day"
7 "4 or more times per day"
/
Q75
1 "Did not eat carrots"
2 "1 to 3 times"
3 "4 to 6 times"
4 "1 time per day"
5 "2 times per day"
6 "3 times per day"
7 "4 or more times per day"
/
Q76
1 "Did not eat other vegetables"
2 "1 to 3 times"
3 "4 to 6 times"
4 "1 time per day"
5 "2 times per day"
6 "3 times per day"
7 "4 or more times per day"
/
Q77
1 "Did not drink soda or pop"
2 "1 to 3 times"
3 "4 to 6 times"
4 "1 time per day"
5 "2 times per day"
6 "3 times per day"
7 "4 or more times per day"
/
Q78
1 "Did not drink milk"
2 "1 to 3 glasses"
3 "4 to 6 glasses"
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
1 "No TV on average school day"
2 "Less than 1 hour per day"
3 "1 hour per day"
4 "2 hours per day"
5 "3 hours per day"
6 "4 hours per day"
7 "5 or more hours per day"
/
Q82
1 "No playing video/computer game"
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
1 "0 teams"
2 "1 team"
3 "2 teams"
4 "3 or more teams"
/
Q85
1 "Yes"
2 "No"
3 "Not sure"
/
Q86
1 "During the past 12 months"
2 "Between 12 and 24 months ago"
3 "More than 24 months ago"
4 "Never"
5 "Not sure"
/
Q87
1 "Yes"
2 "No"
3 "Not sure"
/
Q88
1 "4 or less hours"
2 "5 hours"
3 "6 hours"
4 "7 hours"
5 "8 hours"
6 "9 hours"
7 "10 or more hours"
/
Q89
1 "Mostly A's"
2 "Mostly B's"
3 "Mostly C's"
4 "Mostly D's"
5 "Mostly F's"
6 "None of these grades"
7 "Not sure"
/
Q90
1 "Did not use marijuana "
2 "Smoked it"
3 "Ate in food"
4 "Drank in tea or other drink"
5 "Vaporized"
6 "Some other way"
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
1 "I did not drink"
2 "1 to 3 times"
3 "4 to 6 times"
4 "1 time per day"
5 "2 times per day"
6 "3 times per day"
7 "4 or more times per day"
/
Q93
1 "Did not drink water"
2 "1 to 3 times"
3 "4 to 6 times"
4 "1 time per day"
5 "2 times per day"
6 "3 times per day"
7 "4 or more times per day"
/
Q94
1 "Yes"
2 "No"
3 "Not sure"
/
Q95
1 "0 days"
2 "1 day"
3 "2 days"
4 "3 days"
5 "4 days"
6 "5 days"
7 "6 days"
8 "7 days"
/
Q96
1 "0 times"
2 "1 or 2 times"
3 "3 to 9 times"
4 "10 to 19 times"
5 "20 to 39 times"
6 "40 or more times"
/
Q97
1 "0 times"
2 "1 time"
3 "2 times"
4 "3 times"
5 "4 times"
6 "5 or more times"
/
Q98
1 "Yes"
2 "No"
/
Q99
1 "Very well"
2 "Well"
3 "Not well"
4 "Not at all"
/
RACEETH
1 "Am Indian / Alaska Native"
2 "Asian"
3 "Black or African American"
4 "Native Hawaiian/other PI"
5 "White"
6 "Hispanic / Latino"
7 "Multiple - Hispanic"
8 "Multiple - Non-Hispanic"
/.

MISSING VALUES
Q1 (" ") 
Q2 (" ") Q3 (" ") Q4 (" ") 
Q5 ("        ") Q6 ("    ") Q7 ("      ") 
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
Q95 (" ") Q96 (" ") Q97 (" ") 
Q98 (" ") Q99 (" ") QN8 (" ") 
QN9 (" ") QN10 (" ") QN11 (" ") 
QN12 (" ") QN13 (" ") QN14 (" ") 
QN15 (" ") QN16 (" ") QN17 (" ") 
QN18 (" ") QN19 (" ") QN20 (" ") 
QN21 (" ") QN22 (" ") QN23 (" ") 
QN24 (" ") QN25 (" ") QN26 (" ") 
QN27 (" ") QN28 (" ") QN29 (" ") 
QN30 (" ") QN31 (" ") QN32 (" ") 
QN33 (" ") QN34 (" ") QN35 (" ") 
QN36 (" ") QN37 (" ") QN38 (" ") 
QN39 (" ") QN40 (" ") QN41 (" ") 
QN42 (" ") QN43 (" ") QN44 (" ") 
QN45 (" ") QN46 (" ") QN47 (" ") 
QN48 (" ") QN49 (" ") QN50 (" ") 
QN51 (" ") QN52 (" ") QN53 (" ") 
QN54 (" ") QN55 (" ") QN56 (" ") 
QN57 (" ") QN58 (" ") QN59 (" ") 
QN60 (" ") QN61 (" ") QN62 (" ") 
QN63 (" ") QN64 (" ") QN65 (" ") 
QN66 (" ") QN67 (" ") QN68 (" ") 
QN69 (" ") QN70 (" ") QN71 (" ") 
QN72 (" ") QN73 (" ") QN74 (" ") 
QN75 (" ") QN76 (" ") QN77 (" ") 
QN78 (" ") QN79 (" ") QN80 (" ") 
QN81 (" ") QN82 (" ") QN83 (" ") 
QN84 (" ") QN85 (" ") QN86 (" ") 
QN87 (" ") QN88 (" ") QN89 (" ") 
QN90 (" ") QN91 (" ") QN92 (" ") 
QN93 (" ") QN94 (" ") QN95 (" ") 
QN96 (" ") QN97 (" ") QN98 (" ") 
QN99 (" ") site ("   ") 
qnfrcig (" ") qndaycig (" ") 
qncigint (" ") qntob4 (" ") qntob3 (" ") 
qntob2 (" ") qnnotob4 (" ") qnnotob3 (" ") 
qnnotob2 (" ") qniudimp (" ") qnshparg (" ") 
qnothhpl (" ") qndualbc (" ") qnbcnone (" ") 
qnfr0 (" ") qnfr1 (" ") qnfr2 (" ") 
qnfr3 (" ") qnveg0 (" ") qnveg1 (" ") 
qnveg2 (" ") qnveg3 (" ") qnsoda1 (" ") 
qnsoda2 (" ") qnsoda3 (" ") qnmilk1 (" ") 
qnmilk2 (" ") qnmilk3 (" ") qnbk7day (" ") 
qnpa0day (" ") qnpa7day (" ") qndlype (" ") 
qnspdrk1 (" ") qnspdrk2 (" ") qnspdrk3 (" ") 
qnwater1 (" ") qnwater2 (" ") qnwater3 (" ") 
qnobese (" ") qnowt (" ") weight ("          ") 
stratum ("   ") psu ("      ") bmipct ("     ") 
raceeth ("  ") q6orig ("   ") q7orig ("   ") .

Formats q6 q7 (F5.2) .
EXECUTE.
SAVE OUTFILE="C:\yrbs2015\yrbs2015.sav"/
/COMPRESSED.
EXECUTE.
 
GET FILE "C:\yrbs2015\yrbs2015.sav".

*** Do file public goods uncertainty paper 

*** LEGEND************************************************************************************************************************************************************************************

/*
 20 tokens= 1 USD 
 treatment: 1=baseline; 2=thin private; 3=thin public; 6=thick private; 7=thick public 
 round_number: goes from 1 to 32 and is the number of the round, in sequence
 period: is a number, from 1 to 4, that identifies the period within each experimental session 
 experim_session_number: is a unique identifier for each experimental session (day) 

 groupefficiency_rate: the MPCR for a given period
 playersignal: the signal received by the player (clearly in baseline it coincides with MPCR) 
*** playertreatment: 1=base VCM ; 2= Thin Private; 3= Thin Public; 6
*** Order: 1=0.25, 0.55,0.95, variable;   2=0.95,0.55,0.25, variable
***Playeramb_choiceX_urn: 0=uncertain urn; 1= certain  (so roughly speaking, the lower the sum, the more ambiguity seeking they are) 
** round_indiv_payoff (formerly "playerpotential_payoff"): variable for round earnings for each individual) 
** group_tot_contribution_round (formerly "grouptotal_contribution"): variable for round total contributions to the group account
**Group id :(there should be 4 in each period) : playersub_group_id (it is unique within a session but not across sessions so you need to create a new variables that is this var times the session number) 
** group_number: is a number that identifies, within each experimental session, who is with who in each period. This is unique across sessions, but needs to be checked each time a session is added. Each group should contain exactly 32 observations (8 rounds X 4 players) 
*** payoff of each subject in each round: playerpotential_payoff (is in TOKENS) 
*** Grouptotalcontribution is tot number of tokens in a round 
*** groupindividual_share: group total contribution X MPCR (for each round) 
participantname : is the unique individual id. 


20 tokens= 1 USD 
treatment: 1=baseline; 2=thin U private; 3=thin U public; 6=thick U private; 7=thick U public 
round_number: goes from 1 to 32 and is the number of the round, in sequence



* Environmental Uncertainty do-file (December 5 2016) 

*/

use "/Users/josephseidel/uchicago_pgg/data/merge/out/master.dta"

// JOE: Changed practice -> training
/* dropping practice rounds */
drop if subsessionapp_label=="training" 

/* renaming session number*/
rename participantcode subject_id

/*Generating sessions */
/* 	Rather than generating dummy variables you can just prefix i. infront
	of categorical variables
*/

generate experim_session_number=. 
replace experim_session_number=1 if sessioncode=="3syq0vf6"
replace experim_session_number=2 if sessioncode=="b1n8pl1s"
replace experim_session_number=3 if sessioncode=="cmdsil8r"
replace experim_session_number=4 if sessioncode=="lz1xgvv5"

// JOE: period is built into data as subsessiongame_number
/*generating period variable / 
generate period=. 
replace period=1 if round_number>=1 & round_number<=8
replace period=2 if round_number>8 & round_number<=16
replace period=3 if round_number>16 & round_number<=24
replace period=4 if round_number>24 
*/  


//	JOE: order is built into data as subessionmpcr_oder,
/*Dummy for the order in which MPCRs are experienced. Order: 1=0.25, 0.55,0.95, variable;   2=0.95,0.55,0.25, variable
gen order=. 
replace order=1 if experim_session_number==1
replace order=1 if experim_session_number==2
replace order=1 if experim_session_number==3
replace order=2 if experim_session_number==4
replace order=2 if experim_session_number==5
replace order=1 if experim_session_number==6
replace order=2 if experim_session_number==7
replace order=2 if experim_session_number==8
replace order=1 if experim_session_number==9
replace order=2 if experim_session_number==10
*/

//	JOE: 'order' is a stata keyword and shouldn't be used
//	as a variable name. renaming to mpcr_order
rename subsessionmpcr_order mpcr_order

*gender variable
gen female=(playerq_gender=="Female") 

*renaming age 
rename playerq_age age

// JOE: Changed how group_number is generated
*generating group numbers 
egen group_number = group(groupid_in_subsession sessioncode subsessiongame_number) 

** IMPORTANT NOTE: In the new program the playersub_group_id variable is defined by period and not over all session, so we will need to generate group using playersub_group_id+ session number + period_number

** check groups are correct (each one should have exactly 32 observations: if not, that means that the rule for creating the groups needs to change)
duplicates report group_number

//JOE: Changed playerpotential_payoff to playerround_points
***renaming playerpotential_payoff (is in the individual round payoff in TOKENS) 
rename playerround_points round_indiv_payoff

**renaming Grouptotalcontribution (total contribution of a group in a given round) 
rename grouptotal_contribution group_tot_contribution_round

//	JOE: playertreatment is now subsessiontreatment and takes values 1-5 and detailed in the readme.
//	suggest to remove lines 108-111
/*assigning correct treatments ( wide private treatment equal to 6 and wide public equal to 7)
replace playertreatment=6 if experim_session_number==6
replace playertreatment=6 if experim_session_number==7
replace playertreatment=7 if experim_session_number==9
replace playertreatment=7 if experim_session_number==10
*/

* Renaming treatment variable
rename subsessiontreatment treatment

//  JOE: changing to reflect that playertreatment takes values 1-5
*generating dummies for treatments
gen baseline=(treatment==1)
gen treatment2=(treatment==2)
gen treatment3=(treatment==3)
gen treatment4=(treatment==4)
gen treatment5=(treatment==5)


//	JOE: VVV is a bad comment.  Doesn't tell me anything
// 	that the actual command doesn't.  Also, ommiting this step
// 	to see why(if) it's neccessary.
/*encoding participant session 
encode participantsession, generate(participantsession2)
*/

//	JOE: lines 138-148 should no longer be neccessary
// 	with inclusion of subsessionvariable_mpcr_game in 
// 	'new' version of data

/** generating variable identifying whether a period has a CONSTANT or VARIABLE MPCR  
gen variable_mpcr_period=0
replace variable_mpcr_period=1 if experim_session_number==1 & period==4 
replace variable_mpcr_period=1 if experim_session_number==2 & period==4 
replace variable_mpcr_period=1 if experim_session_number==3 & period==4 
replace variable_mpcr_period=1 if experim_session_number==4 & period==4 
replace variable_mpcr_period=1 if experim_session_number==5 & period==4 
replace variable_mpcr_period=1 if experim_session_number==6 & period==4 
replace variable_mpcr_period=1 if experim_session_number==7 & period==4 
replace variable_mpcr_period=1 if experim_session_number==8 & period==4 
replace variable_mpcr_period=1 if experim_session_number==9 & period==4 
replace variable_mpcr_period=1 if experim_session_number==10 & period==4
*/

//  JOE: the mpcr dummy variables can be defined baed on subsessionfixed_mpcr_game
gen period_mpcr_constant_0_25=0
replace period_mpcr_constant_0_25=1 if subsessionfixed_mpcr_game==1

gen period_mpcr_constant_0_55=0
replace period_mpcr_constant_0_55=1 if subsessionfixed_mpcr_game==2

gen period_mpcr_constant_0_95=0
replace period_mpcr_constant_0_95=1 if subsessionfixed_mpcr_game==3

//	JOE:  subsessionfixed_mpcr_game is constant_mpcr_level in 'new' 
//	version of the data
rename subsessionfixed_mpcr_game constant_mpcr_level


//  JOE: period is new included in 'new' version of data
//  as subsessiongame_number
*gen dummy for period
gen period1=(subsessiongame_number==1)
gen period2=(subsessiongame_number==2) 
gen period3=(subsessiongame_number==3) 
gen period4=(subsessiongame_number==4) 


//  JOE: updating to reflect new code
*dummy for public signals treatments
gen public_signal=(treatment==3|treatment==5)

*dummy for private signal
gen private_signal=(treatment==2|treatment==4)

//  JOE: replacing period with subsessiongame_number
*** generating round average contribution 
by subsessiongame_number group_number subsessionround_number experim_session_number, sort: egen mean_round_contribution=mean(playercontribution)


//	JOE: lines 190-198 can be ommited.
//  subsessiongame_round is round_compressing_periods
/** generating a variable that sorts on round number but "hides" the fact that orders may come from different periods
generate round_compressing_periods=. 
replace round_compressing_periods=1 if round_number==1 | round_number==9 | round_number==17 | round_number==25
replace round_compressing_periods=2 if round_number==2 | round_number==10 | round_number==18 | round_number==26
replace round_compressing_periods=3 if round_number==3 | round_number==11 | round_number==19 | round_number==27
replace round_compressing_periods=4 if round_number==4 | round_number==12 | round_number==20 | round_number==28
replace round_compressing_periods=5 if round_number==5 | round_number==13 | round_number==21 | round_number==29
replace round_compressing_periods=6 if round_number==6 | round_number==14 | round_number==22 | round_number==30
replace round_compressing_periods=7 if round_number==7 | round_number==15 | round_number==23 | round_number==31
replace round_compressing_periods=8 if round_number==8 | round_number==16 | round_number==24 | round_number==32
*/

//	JOE: replaced  treatment conditionals to values 1-5
* generating mean round contributions for each treatment 
gen mean_round_contribution_t1=.
replace mean_round_contribution_t1= mean_round_contribution if treatment ==1
gen mean_round_contribution_t2=.
replace mean_round_contribution_t2= mean_round_contribution if treatment ==2
gen mean_round_contribution_t3=.
replace mean_round_contribution_t3= mean_round_contribution if treatment ==3
gen mean_round_contribution_t6=.
replace mean_round_contribution_t6= mean_round_contribution if treatment ==4
gen mean_round_contribution_t7=.
replace mean_round_contribution_t7= mean_round_contribution if treatment ==5

*generating dummies for biased signals
gen signal_above_true=(playersignal>groupefficiency_rate)
gen signal_equal_true=(playersignal==groupefficiency_rate)
gen signal_below_true=(playersignal<groupefficiency_rate)
gen signal_bias=0 if signal_equal_true==1
replace signal_bias=-1 if signal_below_true==1
replace signal_bias=1 if signal_above_true==1

** generating contribution var for each private signal (both thin and thick and baseline) 
gen contribution_w_signal_below= playercontribution if signal_below_true==1
gen contribution_w_signal_equal= playercontribution if signal_equal_true==1
gen contribution_w_signal_above= playercontribution if signal_above_true==1

** generating contribution var for each private signal (private only) 
gen contrib_w_priv_signal_below= playercontribution if signal_below_true==1 & private_signal==1
gen contrib_w_priv_signal_equal= playercontribution if signal_equal_true==1 & private_signal==1
gen contrib_w_priv_signal_above= playercontribution if signal_above_true==1 & private_signal==1

** generating contribution var for each private signal (public only) 
gen contrib_w_pub_signal_below= playercontribution if signal_below_true==1 & public_signal==1
gen contrib_w_pub_signal_equal= playercontribution if signal_equal_true==1 & public_signal==1
gen contrib_w_pub_signal_above= playercontribution if signal_above_true==1 & public_signal==1

** Dummies for how biased signals are 
gen signal_1_above_true=(playersignal==groupefficiency_rate+0.1)
gen signal_2_above_true=(playersignal==groupefficiency_rate+0.2) 
gen signal_1_below_true=(playersignal==groupefficiency_rate-0.1)
gen signal_2_below_true=(playersignal==groupefficiency_rate-0.2)

*dummy for signal bias intensity
gen signal_bias_intensity=-2 if signal_2_below_true==1
replace signal_bias_intensity=-1 if signal_1_below_true==1
replace signal_bias_intensity=0 if signal_bias==0
replace signal_bias_intensity=1 if signal_1_above_true==1
replace signal_bias_intensity=2 if signal_2_above_true==2

//	JOE: period->subsessiongame_number
* generating dummy for whether signal is fully revealing in thin public
by group_number subsessiongame_number subsessionround_number experim_session_number, sort: egen sum_above_signals_thin=sum(signal_above_true)
by group_number subsessiongame_number subsessionround_number experim_session_number, sort: egen sum_below_signals_thin=sum(signal_below_true)
by group_number subsessiongame_number subsessionround_number experim_session_number, sort: egen sum_equal_signals_thin=sum(signal_equal_true)
gen pub_thin_signal_fully_rev=(treatment==3 & sum_above_signals_thin>0 & sum_below_signals_thin>0) 

*generating dummy for how informative public thin signals are
gen possible_values_pub_thin=3 if treatment==3 & sum_equal_signals_thin==4 & sum_above_signals_thin==0 & sum_below_signals_thin==0
replace possible_values_pub_thin =3 if treatment==3 & sum_equal_signals_thin==0 & sum_above_signals_thin==4 & sum_below_signals_thin==0
replace possible_values_pub_thin =3 if treatment==3 & sum_equal_signals_thin==0 & sum_above_signals_thin==0 & sum_below_signals_thin==4
replace possible_values_pub_thin=2 if treatment==3 & sum_above_signals_thin>0 & sum_below_signals_thin==0 & sum_above_signals_thin<4
replace possible_values_pub_thin=2 if treatment==3 & sum_above_signals_thin==0 & sum_below_signals_thin>0 & sum_below_signals_thin<4
replace possible_values_pub_thin=1 if treatment==3 & sum_above_signals_thin>0 & sum_below_signals_thin>0
rename possible_values_pub_thin n_possible_thetas_thin_pub_t3

//JOE: period->subsessiongame_number
* generating dummy for whether signal is fully revealing in thick public
by group_number subsessiongame_number subsessionround_number experim_session_number, sort: egen sum_2_signals_above=sum(signal_2_above_true)
by group_number subsessiongame_number subsessionround_number experim_session_number, sort: egen sum_1_signals_above=sum(signal_1_above_true)
by group_number subsessiongame_number subsessionround_number experim_session_number, sort: egen sum_2_signals_below=sum(signal_2_below_true)
by group_number subsessiongame_number subsessionround_number experim_session_number, sort: egen sum_1_signals_below=sum(signal_1_below_true)
by group_number subsessiongame_number subsessionround_number experim_session_number, sort: egen sum_signals_equal=sum(signal_equal_true)
gen pub_thick_signal_fully_rev=(treatment==5 & sum_2_signals_above>0 & sum_2_signals_below>0) 


//JOE: period->subsessiongame_number round_number->subsessionround_number
*generating dummy for signal informativeness in thick public
generate playersignal_times_100=playersignal*100
foreach x in 5 15 25 35 45 55 65 75 85 95 105 115 125 {
	generate thick_admissible_`x'=1 if `x'-20 <= playersignal_times_100 & playersignal_times_100 <= `x'+20
	replace thick_admissible_`x'=0 if `x'-20 > playersignal_times_100 | playersignal_times_100 > `x'+20

}
by group_number subsessiongame_number subsessionround_number experim_session_number, sort: egen sum_t7_admiss5=sum (thick_admissible_5)
by group_number subsessiongame_number subsessionround_number experim_session_number, sort: egen sum_t7_admiss15=sum (thick_admissible_15)
by group_number subsessiongame_number subsessionround_number experim_session_number, sort: egen sum_t7_admiss25=sum (thick_admissible_25)
by group_number subsessiongame_number subsessionround_number experim_session_number, sort: egen sum_t7_admiss35=sum (thick_admissible_35)
by group_number subsessiongame_number subsessionround_number experim_session_number, sort: egen sum_t7_admiss45=sum (thick_admissible_45)
by group_number subsessiongame_number subsessionround_number experim_session_number, sort: egen sum_t7_admiss55=sum (thick_admissible_55)
by group_number subsessiongame_number subsessionround_number experim_session_number, sort: egen sum_t7_admiss65=sum (thick_admissible_65)
by group_number subsessiongame_number subsessionround_number experim_session_number, sort: egen sum_t7_admiss75=sum (thick_admissible_75)
by group_number subsessiongame_number subsessionround_number experim_session_number, sort: egen sum_t7_admiss85=sum (thick_admissible_85)
by group_number subsessiongame_number subsessionround_number experim_session_number, sort: egen sum_t7_admiss95=sum (thick_admissible_95)
by group_number subsessiongame_number subsessionround_number experim_session_number, sort: egen sum_t7_admiss105=sum (thick_admissible_105)
by group_number subsessiongame_number subsessionround_number experim_session_number, sort: egen sum_t7_admiss115=sum (thick_admissible_115)
by group_number subsessiongame_number subsessionround_number experim_session_number, sort: egen sum_t7_admiss125=sum (thick_admissible_125)
egen temp_group=group(group_number subsessiongame_number subsessionround_number experim_session_number)
 gen possible_t7_5=(sum_t7_admiss5==4) 
 gen possible_t7_15=(sum_t7_admiss15==4) 
 gen possible_t7_25=(sum_t7_admiss25==4) 
 gen possible_t7_35=(sum_t7_admiss35==4) 
 gen possible_t7_45=(sum_t7_admiss45==4) 
 gen possible_t7_55=(sum_t7_admiss55==4) 
 gen possible_t7_65=(sum_t7_admiss65==4) 
 gen possible_t7_75=(sum_t7_admiss75==4) 
 gen possible_t7_85=(sum_t7_admiss85==4) 
 gen possible_t7_95=(sum_t7_admiss95==4) 
 gen possible_t7_105=(sum_t7_admiss105==4) 
 gen possible_t7_115=(sum_t7_admiss115==4) 
 gen possible_t7_125=(sum_t7_admiss125==4) 
gen n_possible_thetas_thick_pub_t7=possible_t7_5 + possible_t7_15 + possible_t7_25 + possible_t7_35 + possible_t7_45 + possible_t7_55 + possible_t7_65 + possible_t7_75 + possible_t7_85 + possible_t7_95 + possible_t7_105 + possible_t7_115 + possible_t7_125


//	JOE: round_number->subsessionround_number
** other people with signals above below 

by group_number subsessionround_number, sort: egen sum_sig_above_in_group=sum(signal_above_true) 
gen sum_other_members_above_signals= sum_sig_above_in_group - signal_above_true

by group_number subsessionround_number, sort: egen sum_sig_equal_in_group=sum(signal_equal_true) 
gen sum_other_members_equal_signals= sum_sig_equal_in_group - signal_equal_true
	
by group_number subsessionround_number, sort: egen sum_sig_below_in_group=sum(signal_below_true) 
gen sum_other_members_below_signals= sum_sig_below_in_group - signal_below_true	

gen at_least_1oth_above_signal=(sum_other_members_above_signals>0)
gen at_least_1oth_below_signal=(sum_other_members_below_signals>0)

*generating dummy for whether public signals are fully revealing (both T3 and T7) 
gen pub_signal_fully_info=(n_possible_thetas_thick_pub_t7 ==1 | n_possible_thetas_thin_pub_t3==1) 

gen fully_informative=(n_possible_thetas_thick_pub_t7 ==1 | n_possible_thetas_thin_pub_t3==1 | treatment==1)
*generating dummy for upward and downward biases
gen upward_bias=(playersignal>groupefficiency_rate)
gen downward_bias=(playersignal<groupefficiency_rate)

*generating sum of upward and downward biases in groups 
by group_number, sort: egen sum_upward_biases=sum(upward_bias) 
by group_number, sort: egen sum_downward_biases=sum(downward_bias) 

*** generating variables for ambiguity 
gen sum_ambiguity= playeramb_choice1_urn +playeramb_choice2_urn + playeramb_choice2_urn + playeramb_choice3_urn+playeramb_choice4_urn +playeramb_choice5_urn+playeramb_choice6_urn+playeramb_choice7_urn+playeramb_choice8_urn+playeramb_choice9_urn+playeramb_choice10_urn

** gen variable for splitting
gen splitting=0
replace splitting=1 if playercontribution>0 & playercontribution<10

//	JOE: period->subsessiongame_number
*gen individual payoffs per-period
encode subject_id, generate(subject_id2)
by subsessiongame_number subject_id2, sort: egen period_payoff_tokens= sum(round_indiv_payoff)
gen period_payoff_us_dollars= period_payoff_tokens/20

** strong free riders: participants that give less than 1/3 of their endowment
gen strong_free_rider=0 
replace strong_free_rider=1 if playercontribution<=3

*gen dummy for uncertainty 
gen uncertainty=(treatment!=1) 

* generating variable for number of possible thetas 
gen number_possible_thetas= n_possible_thetas_thick_pub_t7 if treatment==5
replace number_possible_thetas=1 if treatment==1 
replace number_possible_thetas= n_possible_thetas_thin_pub_t3 if treatment==3 

**gen dummy for only one possible theta
gen one_possible_theta=(number_possible_thetas==1) 


//	JOE: variable_mpcr_period -> subsessionvariable_mpcr_game
* generating variable for type of mpcr 
gen mpcr_type=1 if constant_mpcr_level==1
replace mpcr_type=2 if constant_mpcr_level==2
replace mpcr_type=3 if constant_mpcr_level==3 
replace mpcr_type=4 if subsessionvariable_mpcr_game==1

*gen n thetas squared
gen number_possible_thetas_sq=(number_possible_thetas)^2


************************************
************************************
************************************
************************************
************************************

********************************************************************************
****Table 1 ********************************************************************
********************************************************************************

// JOE: added preserve
preserve

//	JOE: round_compressing_periods -> subsessiongame_round
//	player_treatment -> treatment
collapse (mean) meancontribution=playercontribution (sd) sdcontribution=playercontribution (count) n= playercontribution, by( subsessiongame_round treatment constant_mpcr_level) 

gen hicontribution = meancontribution + (sdcontribution / sqrt(n))
gen lowcontribution = meancontribution - (sdcontribution / sqrt(n))


//	JOE:  round_compressing_periods -> subsessiongame_round
//	replace values in playertreatment condition to 1-5
//	playertreatment was renamed to treatment... but both variables
//	are still being referenced in the do file.   The original do file sent 
// 	by Luigi does run with the data he sent.   I am going to replace
// 	playertreamtment -> treatment
gen collapse_round_times_treatmt=  subsessiongame_round if treatment==1
replace collapse_round_times_treatmt=  subsessiongame_round+9 if treatment==2
replace collapse_round_times_treatmt=  subsessiongame_round+18 if treatment==3
replace collapse_round_times_treatmt=  subsessiongame_round+27 if treatment==4
replace collapse_round_times_treatmt=  subsessiongame_round+36 if treatment==5

gen meancontrib_percent=meancontribution*10

//	JOE: round_compressing_periods -> subessiongame_round
la var treatment "Treatment" 
la def treatment 1 "Baseline_VCM" 2 "Private_thin" 3 "Public_thin" 6 "Private_Thick" 7 "Public_thick"
la val treatment treatment
la var subsessiongame_round "Round" 
tabout treatment subsessiongame_round using sum_contrib_025.csv if constant_mpcr_level==1, cell(mean meancontrib_percent) f(1c) sum replace
tabout treatment subsessiongame_round using sum_contrib_055.csv if constant_mpcr_level==2, cell(mean meancontrib_percent) f(1c) sum replace
tabout treatment subsessiongame_round using sum_contrib_095.csv if constant_mpcr_level==3, cell(mean meancontrib_percent) f(1c) sum replace

********************************************************************************
****************************************** Footnote 11********************
********************************************************************************
//	JOE: added restore
restore

//	JOE: order->mpcr_order throughout Footnone 11 section
//	variable_mpcr_period->subsessionvariable_mpcr_game
** are contributions comparable by order? 
by constant_mpcr_level,sort: ttest playercontribution if treatment==1, by(mpcr_order)
ksmirnov playercontribution if treatment==1 & constant_mpcr_level==1, by(mpcr_order) 
ksmirnov playercontribution if treatment==1 & constant_mpcr_level==2, by(mpcr_order) 
ksmirnov playercontribution if treatment==1 & constant_mpcr_level==3, by(mpcr_order) 
ksmirnov playercontribution if treatment==1 & subsessionvariable_mpcr_game==1, by(mpcr_order) 


//	JOE: round_compressing_periods -> subsessiongame_round
** private thin
by constant_mpcr_level,sort: ttest playercontribution if treatment==2, by(mpcr_order)
graph bar (mean) playercontribution if treatment==2, over(subsessiongame_round) over(mpcr_order) by(constant_mpcr_level)
ksmirnov playercontribution if treatment==2 & constant_mpcr_level==1, by(mpcr_order) 
ksmirnov playercontribution if treatment==2 & constant_mpcr_level==2, by(mpcr_order) 
ksmirnov playercontribution if treatment==2 & constant_mpcr_level==3, by(mpcr_order) 
ksmirnov playercontribution if treatment==2 & subsessionvariable_mpcr_game==1, by(mpcr_order) 

//	JOE: round_compressing_periods -> subsessiongame_round
** public thin 
by constant_mpcr_level,sort: ttest playercontribution if treatment==3, by(mpcr_order)
graph bar (mean) playercontribution if treatment==3, over(subsessiongame_round) over(mpcr_order) by(constant_mpcr_level)
ksmirnov playercontribution if treatment==3 & constant_mpcr_level==1, by(mpcr_order) 
ksmirnov playercontribution if treatment==3 & constant_mpcr_level==2, by(mpcr_order) 
ksmirnov playercontribution if treatment==3 & constant_mpcr_level==3, by(mpcr_order) 
ksmirnov playercontribution if treatment==3 & subsessionvariable_mpcr_game==1, by(mpcr_order) 

//	JOE: round_compressing_periods -> subsessiongame_round
** private thick
by constant_mpcr_level,sort: ttest playercontribution if treatment==4, by(mpcr_order)
graph bar (mean) playercontribution if treatment==4, over(subsessiongame_round) over(mpcr_order) by(constant_mpcr_level)
ksmirnov playercontribution if treatment==4 & constant_mpcr_level==1, by(mpcr_order) 
ksmirnov playercontribution if treatment==4 & constant_mpcr_level==2, by(mpcr_order) 
ksmirnov playercontribution if treatment==4 & constant_mpcr_level==3, by(mpcr_order) 
ksmirnov playercontribution if treatment==4 & subsessionvariable_mpcr_game==1, by(mpcr_order) 

//	JOE: round_compressing_periods -> subsessiongame_round
** public thick
by constant_mpcr_level,sort: ttest playercontribution if treatment==5, by(mpcr_order)
graph bar (mean) playercontribution if treatment==5, over(subsessiongame_round) over(mpcr_order) by(constant_mpcr_level)
ksmirnov playercontribution if treatment==5 & constant_mpcr_level==1, by(mpcr_order) 
ksmirnov playercontribution if treatment==5 & constant_mpcr_level==2, by(mpcr_order) 
ksmirnov playercontribution if treatment==5 & constant_mpcr_level==3, by(mpcr_order) 
ksmirnov playercontribution if treatment==5 & subsessionvariable_mpcr_game==1, by(mpcr_order)

********************************************************************************
*** Table 1 : comparisons of average contributions across treatments **********
********************************************************************************

* baseline Vs. Private thin
** overall difference in contributions bw baseline and private thin
ttest playercontribution if treatment!=3 & treatment!=4 & treatment!=5, by(treatment) 
ranksum playercontribution if treatment!=3 & treatment!=4 & treatment!=5, by(treatment)
** average differences by period 
by constant_mpcr_level, sort: ttest playercontribution if treatment!=3 & treatment!=4 & treatment!=5, by(treatment)
by constant_mpcr_level, sort: ranksum playercontribution if treatment!=3 & treatment!=4 & treatment!=5, by(treatment)


* Baseline vs private thick 
* overall difference in contributions bw baseline and private thin
ttest playercontribution if treatment!=2 & treatment!=4 & treatment!=5, by(treatment) 
ranksum playercontribution if treatment!=2 & treatment!=4 & treatment!=5, by(treatment)
** for each MPCR, overall do baseline and private thick differ? 
by constant_mpcr_level, sort: ttest playercontribution if treatment!=2 & treatment!=4 & treatment!=5, by(treatment) 
by constant_mpcr_level, sort: ranksum playercontribution if treatment!=2 & treatment!=4 & treatment!=5, by(treatment) 

* Baseline vs public thin 
* overall difference in contributions bw baseline and public thin
ttest playercontribution if treatment!=2 & treatment!=3 & treatment!=5, by(treatment) 
ranksum playercontribution if treatment!=2 & treatment!=3 & treatment!=5, by(treatment)
** for each MPCR, overall do baseline and  public thin differ? 
by constant_mpcr_level, sort: ttest playercontribution if treatment!=2 & treatment!=3 & treatment!=5, by(treatment) 
by constant_mpcr_level, sort: ranksum playercontribution if treatment!=2 & treatment!=3 & treatment!=5, by(treatment) 

* Baseline vs public thick 
* overall difference in contributions bw baseline and public thin
ttest playercontribution if treatment!=2 & treatment!=3 & treatment!=4, by(treatment) 
ranksum playercontribution if treatment!=2 & treatment!=3 & treatment!=4, by(treatment)
** for each MPCR, overall do baseline and  public thin differ? 
by constant_mpcr_level, sort: ttest playercontribution if treatment!=2 & treatment!=3 & treatment!=4, by(treatment) 
by constant_mpcr_level, sort: ranksum playercontribution if treatment!=2 & treatment!=3 & treatment!=4, by(treatment) 


***************************************************************************
** Page 11: are first and last round contributions different? *************
***************************************************************************
//	JOE: round_compressing_periods -> subsessiongame_round
*baseline
by constant_mpcr_level,sort: ranksum playercontribution if treatment==1 & subsessiongame_round!=2 & subsessiongame_round!=3 & subsessiongame_round!=4 & subsessiongame_round!=5 & subsessiongame_round!=6 & subsessiongame_round!=7, by(subsessiongame_round)
*private thin
by constant_mpcr_level,sort: ranksum playercontribution if treatment==2 & subsessiongame_round!=2 & subsessiongame_round!=3 & subsessiongame_round!=4 & subsessiongame_round!=5 & subsessiongame_round!=6 & subsessiongame_round!=7, by(subsessiongame_round)

*private thick
by constant_mpcr_level,sort: ranksum playercontribution if treatment==3 & subsessiongame_round!=2 & subsessiongame_round!=3 & subsessiongame_round!=4 & subsessiongame_round!=5 & subsessiongame_round!=6 & subsessiongame_round!=7, by(subsessiongame_round)

*public thin
by constant_mpcr_level,sort: ranksum playercontribution if treatment==4 & subsessiongame_round!=2 & subsessiongame_round!=3 & subsessiongame_round!=4 & subsessiongame_round!=5 & subsessiongame_round!=6 & subsessiongame_round!=7, by(subsessiongame_round)

*public thick
by constant_mpcr_level,sort: ranksum playercontribution if treatment==5 & subsessiongame_round!=2 & subsessiongame_round!=3 & subsessiongame_round!=4 & subsessiongame_round!=5 & subsessiongame_round!=6 & subsessiongame_round!=7, by(subsessiongame_round)


***************************************************************************
** Figure 1: contributions by type of signal  
***************************************************************************


//	JOE: signal_type was missing, so I generated it.
gen signal_type = .
replace signal_type = -1 if playersignal < groupefficiency_rate
replace signal_type = 1 if playersignal > groupefficiency_rate
replace signal_type = 0 if playersignal == groupefficiency_rate

//	JOE: added preserve
preserve
collapse (mean) meancontribution=playercontribution (sd) sdcontribution=playercontribution (count) n= playercontribution, by( subsessiongame_round treatment constant_mpcr_level signal_type) 

gen meancontrib_percent=meancontribution*10

gen base_contrib_perc= meancontrib_percent if treatment==1 
gen thin_priv_below_contr_perc= meancontrib_percent if treatment==2 & signal_type==-1
gen thin_priv_eq_contr_perc= meancontrib_percent if treatment==2 & signal_type==0
gen thin_priv_above_contr_perc= meancontrib_percent if treatment==2 & signal_type==1


twoway (connected meancontrib_percent subsessiongame_round if treatment==1, sort  mcolor(dknavy) msymbol(circle) lcolor(dknavy)) (connected meancontrib_percent subsessiongame_round if treatment==2 & signal_type==-1, sort  mcolor(red) msymbol(triangle) lcolor(red)) (connected meancontrib_percent subsessiongame_round if treatment==2 & signal_type==0, sort  mcolor(green) msymbol(triangle) lcolor(green)) (connected meancontrib_percent subsessiongame_round if treatment==2 & signal_type==1, sort  mcolor(purple) msymbol(triangle) lcolor(purple)), by(constant_mpcr_level) legend(label(1 "Baseline VCM") label (2 " Thin signal below true MPCR") label(3 "Thin signal equal true MPCR") label(4 "Thin signal above true MPCR"))
twoway (connected meancontrib_percent subsessiongame_round if treatment==1, sort  mcolor(dknavy) msymbol(circle) lcolor(dknavy)) (connected meancontrib_percent subsessiongame_round if treatment==4 & signal_type==-1, sort  mcolor(red) msymbol(triangle) lcolor(red)) (connected meancontrib_percent subsessiongame_round if treatment==4 & signal_type==0, sort  mcolor(green) msymbol(triangle) lcolor(green)) (connected meancontrib_percent subsessiongame_round if treatment==4 & signal_type==1, sort  mcolor(purple) msymbol(triangle) lcolor(purple)), by(constant_mpcr_level) legend(label(1 "Baseline VCM") label (2 " Thick signal below true MPCR") label(3 "Thick signal equal true MPCR") label(4 "Thick signal above true MPCR"))

//	JOE: added restore
restore

*********************************************************************
*** ***********************Regressions  *****************************
*********************************************************************

* declaring panel 
//	JOE: round_number->subessionround_number
xtset subject_id2 subsessionround_number
*previous round var
//	JOE: round_number->subsessionround_number
by subject_id2, sort: gen previous_round = subsessionround_number[_n-1]
*generating constant
gen costante=1
* ***generating per-period individual avgs 
//	JOE: period->subessiongame_number
//	JOE: round_compressing_periods->subsessiongame_round
by subject_id2 subsessiongame_number, sort: egen avg_period_contribution=mean(playercontribution)
gen avg_period_contribution_base= avg_period_contribution if treatment==1
** generating individuallagged variables 
by subject_id2, sort: gen lag1_contribution = playercontribution[_n-1]
by subject_id2, sort: gen lag2_contribution = playercontribution[_n-2]
gen lag1_group_tot_contrib_round= group_tot_contribution_round[_n-1]
gen group_tot_contr_perc_round= (group_tot_contribution_round*100)/40
gen l1_group_tot_contr_perc_round= (lag1_group_tot_contrib_round)*100/40
by subject_id2, sort: gen lag1_indiv_payoff=round_indiv_payoff[_n-1]
replace lag1_indiv_payoff=. if subsessiongame_round==1
by subject_id2, sort: gen lag2_indiv_payoff=round_indiv_payoff[_n-2]
replace lag2_indiv_payoff=. if subsessiongame_round==1
by subject_id2, sort: gen lag3_indiv_payoff=round_indiv_payoff[_n-3]
replace lag3_indiv_payoff=. if subsessiongame_round==1
* generating variables for other peoples' behavior 
gen other_members_contribution_round= group_tot_contribution_round - playercontribution
gen l1_other_members_contrib_round= other_members_contribution_round[_n-1]
replace l1_other_members_contrib_round=. if subsessiongame_round==1
gen avg_other_members_contr_round= other_members_contribution_round/3 
*gen lag of others' behavior
gen lag1_others_contrib_round= other_members_contribution_round[_n-1]
replace lag1_others_contrib_round=. if subsessiongame_round==1 
gen lag1_avg_others_contrib_round= avg_other_members_contr_round[_n-1]
replace lag1_avg_others_contrib_round=. if subsessiongame_round==1
*generating dummies for whether others are observing free riding compared to previous periods (in regressions we can probably simply interact other contributions with rounds?) 
gen declining_others_avg_contrib=(lag1_avg_others_contrib_round> avg_other_members_contr_round) 
*gen up and low bound for tobit 
gen left_censor=0
gen right_censor=10



 ***************************************************************************
* table 2: Comparing baseline and public signals treatments contributions
***************************************************************************

//	JOE: Generate decsion group dummies
tab group_number, generate(dgroup)

//	JOE:
//	round_compressing_periods->subsessiongame_round
//	period->subsessiongame_number
//	order->mpcr_order
xttobit playercontribution public_signal  subsessiongame_round subsessiongame_number mpcr_order  groupefficiency_rate dgroup* if treatment!=2 & treatment!=6 & one_possible_theta==1, ll(0) ul(10)  
outreg2 using "C:\Users\BFI-Team\Desktop\luigi\Delegation - lab with john\data\all data\atlanta\table_final\table2_aug17", replace
reghdfe playercontribution public_signal  subsessiongame_round subsessiongame_number mpcr_order  groupefficiency_rate if treatment!=2 & treatment!=6 & one_possible_theta==1, vce(cluster group_number subject_id2) absorb(costante)
outreg2 using "C:\Users\BFI-Team\Desktop\luigi\Delegation - lab with john\data\all data\atlanta\table_final\table2_aug17"
xttobit playercontribution public_signal  subsessiongame_round subsessiongame_number mpcr_order  groupefficiency_rate number_possible_thetas number_possible_thetas_sq one_possible_theta  c.groupefficiency_rate#c.number_possible_thetas c.groupefficiency_rate#c.subsessiongame_round c.subsessiongame_round#c.number_possible_thetas c.groupefficiency_rate#c.subsessiongame_round#c.number_possible_thetas dgroup*  if treatment!=2 & treatment!=6 , ll(0) ul(10) 
outreg2 using "C:\Users\BFI-Team\Desktop\luigi\Delegation - lab with john\data\all data\atlanta\table_final\table2_aug17"
reghdfe playercontribution public_signal  subsessiongame_round subsessiongame_number mpcr_order  groupefficiency_rate number_possible_thetas number_possible_thetas_sq one_possible_theta  c.groupefficiency_rate#c.number_possible_thetas c.groupefficiency_rate#c.subsessiongame_round c.subsessiongame_round#c.number_possible_thetas c.groupefficiency_rate#c.subsessiongame_round#c.number_possible_thetas  if treatment!=2 & treatment!=6 , vce(cluster group_number subject_id2) absorb(group_number subject_id2)
outreg2 using "C:\Users\BFI-Team\Desktop\luigi\Delegation - lab with john\data\all data\atlanta\table_final\table2_aug17", see tex excel

***************************************************************************
** Table 3: Effect of uncertainty on contributions over time and between levels of MPCR
***************************************************************************

//	JOE:
//	round_number->subessionround_number
//	order->mpcr_order
//	period->subsessiongame_number
xttobit playercontribution mpcr_type subsessionround_number playersignal groupefficiency_rate  uncertainty  c.groupefficiency_rate#c.playersignal c.uncertainty#c.subsessionround_number  l1_other_members_contrib_round c.l1_other_members_contrib_round#c.uncertainty mpcr_order subsessiongame_number at_least_1oth_above_signal at_least_1oth_below_signal  dgroup* if treatment!=3 & treatment!=7 , ll(0) ul(10) 
outreg2 using "C:\Users\BFI-Team\Desktop\luigi\Delegation - lab with john\data\all data\atlanta\table_final\table3_aug19", replace
reghdfe playercontribution mpcr_type subsessionround_number playersignal groupefficiency_rate  uncertainty  c.groupefficiency_rate#c.playersignal c.uncertainty#c.subsessionround_number  l1_other_members_contrib_round c.l1_other_members_contrib_round#c.uncertainty mpcr_order subsessiongame_number at_least_1oth_above_signal at_least_1oth_below_signal  if treatment!=3 & treatment!=7 , vce(cluster group_number subject_id2) absorb(group_number subject_id2 ) 
outreg2 using "C:\Users\BFI-Team\Desktop\luigi\Delegation - lab with john\data\all data\atlanta\table_final\table3_aug19", see tex excel

***************************************************************************
** Table 4: Effect of uncertainty on contributions within levels of MPCR θ
***************************************************************************

//	JOE:
//	round_number->subsessionround_number
//	variable_mpcr_period->subsessionvariable_mpcr_game
//	order->mpcr_order
xttobit playercontribution subsessionround_number  groupefficiency_rate mpcr_type signal_above_true signal_below_true playersignal   period_mpcr_constant_0_55 period_mpcr_constant_0_95 subsessionvariable_mpcr_game   c.period_mpcr_constant_0_55#c.signal_above_true  c.period_mpcr_constant_0_55#c.signal_below_true  c.period_mpcr_constant_0_95#c.signal_above_true c.period_mpcr_constant_0_95#c.signal_below_true c.subsessionvariable_mpcr_game#c.signal_above_true c.subsessionvariable_mpcr_game#c.signal_below_true mpcr_order sum_other_members_above_signals sum_other_members_below_signals lag1_others_contrib_round c.lag1_others_contrib_round#c.uncertainty   dgroup* if   public_signal ==0, ll(0) ul(10)
outreg2 using "C:\Users\BFI-Team\Desktop\luigi\Delegation - lab with john\data\all data\atlanta\table_final\table4_aug17", replace
reghdfe playercontribution subsessionround_number  groupefficiency_rate mpcr_type signal_above_true signal_below_true playersignal   period_mpcr_constant_0_55 period_mpcr_constant_0_95 subsessionvariable_mpcr_game   c.period_mpcr_constant_0_55#c.signal_above_true  c.period_mpcr_constant_0_55#c.signal_below_true  c.period_mpcr_constant_0_95#c.signal_above_true c.period_mpcr_constant_0_95#c.signal_below_true c.subsessionvariable_mpcr_game#c.signal_above_true c.subsessionvariable_mpcr_game#c.signal_below_true mpcr_order sum_other_members_above_signals sum_other_members_below_signals lag1_others_contrib_round c.lag1_others_contrib_round#c.uncertainty   if   public_signal ==0, vce(cluster group_number subject_id2 ) absorb(group_number subject_id2  )
outreg2 using "C:\Users\BFI-Team\Desktop\luigi\Delegation - lab with john\data\all data\atlanta\table_final\table4_aug17", see tex excel


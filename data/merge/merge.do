
clear
*** Unfortunately, Stata does not have a convienient way to deal with the
*** / vs \ on Mac/Unix vs Windows.  The code below is written for the former.
*** if using on Windows you will need to change / to \ throughout the .do file
cd "~/uchicago_pgg/data/merge"

***Set the sessions to be merged together here.  These can be found in Session.code from the ***
***raw data exported from your appication.***
local sessions "3syq0vf6 cmdsil8r lz1xgvv5 b1n8pl1s 2cd4524j 3aq6dyc3 07q8q19s 63a59oes 99onw02o ptorykjm ut43ysr8 xaqzbf9p" 

// **NOTE** the files must follow a directory hiearchy of
//  <dir>/out
//  <dir>/temp
//  <dir>/3syq0vf6
//		<file>3syq0vf6_risk.csv
//		<file>3syq0vf6_training.csv
//		<file>3syq0vf6_pg.csv
//		<file>3syq0vf6_survey.csv
//  <dir>/cmdsil8r
//		<file>cmdsil8r_risk.csv
//		<file>cmdsil8r_training.csv
//		<file>cmdsil8r_pg.csv
//		<file>cmdsil8r_survey.csv
//  <dir>/lz1xgvv5
//		<file>lz1xgvv5_risk.csv
//		<file>lz1xgvv5_training.csv
//		<file>lz1xgvv5_pg.csv
//		<file>lz1xgvv5_survey.csv
//	<dir>/b1n8pl1s
//		<file>b1n8pl1s_risk.csv
//		<file>b1n8pl1s_training.csv
//		<file>b1n8pl1s_pg.csv
//		<file>b1n8pl1s_survey.csv		
//  <file>merge.do

local stype "pg training risk survey"

//insheet csv and drop variables that aren't needed
foreach session of local sessions {
    foreach t of local stype {
        insheet using "`session'/`session'_`t'.csv", comma names double
        drop if sessioncode != "`session'"
        drop participantid_in_session participant_is_bot participant_index_in_pages	///
            participant_max_page_index participant_current_app_name ///
            participant_current_page_name participantip_address ///
            participantexclude_from_data_ana participantvisited ///
            participantmturk_worker_id participantmturk_assignment_id ///
            participant_round_number sessionmturk_hitid sessionmturk_hitgroupid
        save "temp/`session'_`t'.dta", replace
        clear
    }
}

// Stack practice and actual public_goods game rounds on top of eachother
foreach session of local sessions {
    use "temp/`session'_training"
    merge m:m participantcode subsessionapp_label sessioncode ///
        using "temp/`session'_pg"
        tostring participantlabel, replace
        drop _merge
        save "temp/`session'_master.dta", replace
        clear
}

//merge risk and survey data master files
foreach session of local sessions {
    use "temp/`session'_master"
    merge m:1 participantcode sessioncode using "temp/`session'_risk", force
    save "temp/`session'_master.dta", replace
    drop _merge
    merge m:1 participantcode sessioncode using "temp/`session'_survey", force
    drop _merge
    tostring playerq_gpa, replace
    tostring sessiontime_started, replace
    save "temp/`session'_master.dta", replace
    clear
}

//stack master files to one file
foreach session of local sessions {
    display "`session'"
    append using "temp/`session'_master"
}

save "out/master.dta", replace
outsheet using "out/master.csv", comma names replace
recast str244 playerq_comments, force
recast str244 playerq_decision, force
saveold "out/master12.dta", version(12) replace
outsheet using "out/master12.csv", comma names replace

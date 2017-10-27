
### Import and Prep ###

peJSS = haven::read_sas("pe_jss2_toseth_10162017.sas7bdat")

peSet2 = haven::read_sas("pe_set2_toseth_10162017.sas7bdat")

peDid = haven::read_sas("pe_did_toseth_10162017.sas7bdat")

library(quantreg); library(dplyr)


peSet2$NewFund = ifelse(peSet2$fundlife < 15, 1, 0)

peSet2$MoreExperience = ifelse(peSet2$experience > 1, 1, 0)

peSet2$LargeFund = ifelse(peSet2$fund_size > 199, 0, 1)

peSet2$Venture = ifelse(peSet2$Strategy2 == 2, 1, 0)


mod1Set2 = rq(NAV_abs_err_scaled ~ 
               post*SmallFund + 
               post*MoreExperience + 
               post*S_P_500_Qtrly_Return + 
               post*S_P_500_Qtrly_Return_l3 + 
               post*Fourthqtr + as.factor(firmyr), 
             data = peSet2, method = "sfn", tau = .5)

mod1Set2Sum = summary(mod1Set2, se = "boot", R = 200, cluster = peSet2$Coded_fund_id)

#write.csv(mod1Set2Sum$coefficients, "data/working/mod1Set2Sum.csv", row.names = FALSE)
write.csv(mod1Set2Sum$coefficients, file = "data/working/mod1Set2Sum.csv", 
          row.names = c("intercept", "post", "SmallFund", 
                        "MoreExperience", "S_P_500_Qtrly_Return", 
                        "S_P_500_Qtrly_Return_l3", "Fourthqtr", 
                        "firmyr.1", "firmyr.2", "firmyr.3", "firmyr.4", 
                        "firmyr.5", "firmyr.6", "firmyr.7", "firmyr.8", "firmyr.9",
                        "firmyr.10", "post:SmallFund", 
                        "post:MoreExperience", "post:S_P_500_Qtrly_Return", 
                        "post:S_P_500_Qtrly_Return_l3", "post:Fourthqtr"))


mod1Set2Null = rq(NAV_abs_err_scaled ~ 1, tau = .5, data = peSet2, 
                 method = "sfn")

mod1Set2R1 = 1 - mod1Set2$rho / mod1Set2Null$rho

mod2Set2 = rq(NAV_abs_err_scaled ~ 
                post*Venture + 
                post*S_P_500_Qtrly_Return + 
                post*S_P_500_Qtrly_Return_l3 + 
                post*Fourthqtr + as.factor(firmyr), 
              data = peSet2, method = "sfn", tau = .5)
mod2Set2Sum = summary(mod2Set2, se = "boot", R = 200, cluster = peSet2$Coded_fund_id)

write.csv(mod2Set2Sum$coefficients, "data/working/mod2Set2Sum.csv", 
          row.names = c("intercept", "post", "Venture", 
                        "S_P_500_Qtrly_Return", 
                        "S_P_500_Qtrly_Return_l3", "Fourthqtr", 
                        "firmyr.1", "firmyr.2", "firmyr.3", "firmyr.4", 
                        "firmyr.5", "firmyr.6", "firmyr.7", "firmyr.8", "firmyr.9",
                        "firmyr.10", "post:Venture", 
                        "post:S_P_500_Qtrly_Return", 
                        "post:S_P_500_Qtrly_Return_l3", "post:Fourthqtr"))

mod2Set2Null = rq(NAV_abs_err_scaled ~ 1, tau = .5, data = peSet2, 
                  method = "sfn")

mod2Set2R1 = 1 - mod2Set2$rho / mod2Set2Null$rho

mod3Set2 = rq(NAV_err_scaled ~ 
                post*S_P_500_Qtrly_Return + 
                post*S_P_500_Qtrly_Return_l3 + 
                post*Fourthqtr + as.factor(firmyr), 
              data = peSet2, method = "sfn", tau = .5)
mod3Set2Sum = summary(mod3Set2, se = "boot", R = 200, cluster = peSet2$Coded_fund_id)

write.csv(mod3Set2Sum$coefficients, "data/working/mod3Set2Sum.csv", 
          row.names = c("intercept", "post", 
                        "S_P_500_Qtrly_Return", 
                        "S_P_500_Qtrly_Return_l3", "Fourthqtr", 
                        "firmyr.1", "firmyr.2", "firmyr.3", "firmyr.4", 
                        "firmyr.5", "firmyr.6", "firmyr.7", "firmyr.8", "firmyr.9",
                        "firmyr.10", 
                        "post:S_P_500_Qtrly_Return", 
                        "post:S_P_500_Qtrly_Return_l3", "post:Fourthqtr"))

mod3Set2Null = rq(NAV_err_scaled ~ 1, tau = .5, data = peSet2, 
                  method = "sfn")

mod3Set2R1 = 1 - mod3Set2$rho / mod3Set2Null$rho

mod4Set2 = rq(NAV_err_scaled ~ 
                post*SmallFund +
                post*MoreExperience +
                post*S_P_500_Qtrly_Return + 
                post*S_P_500_Qtrly_Return_l3 + 
                post*Fourthqtr + as.factor(firmyr), 
              data = peSet2, method = "sfn", tau = .5)
mod4Set2Sum = summary(mod4Set2, se = "boot", R = 200, cluster = peSet2$Coded_fund_id)

write.csv(mod4Set2Sum$coefficients, "data/working/mod4Set2Sum.csv", 
          row.names = c("intercept", "post", "SmallFund", "MoreExperience",
                        "S_P_500_Qtrly_Return", 
                        "S_P_500_Qtrly_Return_l3", "Fourthqtr", 
                        "firmyr.1", "firmyr.2", "firmyr.3", "firmyr.4", 
                        "firmyr.5", "firmyr.6", "firmyr.7", "firmyr.8", "firmyr.9",
                        "firmyr.10", "post:SmallFund", "post:MoreExperience",
                        "post:S_P_500_Qtrly_Return", 
                        "post:S_P_500_Qtrly_Return_l3", "post:Fourthqtr"))

mod4Set2Null = rq(NAV_err_scaled ~ 1, tau = .5, data = peSet2, 
                  method = "sfn")

mod4Set2R1 = 1 - mod4Set2$rho / mod4Set2Null$rho

mod5Set2 = rq(NAV_err_scaled ~ 
                post*Venture +
                post*S_P_500_Qtrly_Return + 
                post*S_P_500_Qtrly_Return_l3 + 
                post*Fourthqtr + as.factor(firmyr), 
              data = peSet2, method = "sfn", tau = .5)
mod5Set2Sum = summary(mod5Set2, se = "boot", R = 200, cluster = peSet2$Coded_fund_id)

write.csv(mod5Set2Sum$coefficients, "data/working/mod5Set2Sum.csv", 
          row.names = c("intercept", "post", "Venture",
                        "S_P_500_Qtrly_Return", 
                        "S_P_500_Qtrly_Return_l3", "Fourthqtr", 
                        "firmyr.1", "firmyr.2", "firmyr.3", "firmyr.4", 
                        "firmyr.5", "firmyr.6", "firmyr.7", "firmyr.8", "firmyr.9",
                        "firmyr.10", "post:Venture",
                        "post:S_P_500_Qtrly_Return", 
                        "post:S_P_500_Qtrly_Return_l3", "post:Fourthqtr"))

mod5Set2Null = rq(NAV_err_scaled ~ 1, tau = .5, data = peSet2, 
                  method = "sfn")

mod5Set2R1 = 1 - mod5Set2$rho / mod5Set2Null$rho

# No Nav_change_scale. Used NAV_change instead
mod6Set2 = rq(NAV_change ~ 
                post*Contribution_scale +
                post*Distribution_scale +
                post*S_P_500_Qtrly_Return + 
                post*S_P_500_Qtrly_Return_l3 + 
                post*Fourthqtr + as.factor(firmyr), 
              data = peSet2, method = "sfn", tau = .5)
mod6Set2Sum = summary(mod6Set2, se = "boot", R = 200, cluster = peSet2$Coded_fund_id)

write.csv(mod6Set2Sum$coefficients, "data/working/mod6Set2Sum.csv", 
          row.names = c("intercept", "post", "Contribution_scale",
                        "Distribution_scale","S_P_500_Qtrly_Return", 
                        "S_P_500_Qtrly_Return_l3", "Fourthqtr", 
                        "firmyr.1", "firmyr.2", "firmyr.3", "firmyr.4", 
                        "firmyr.5", "firmyr.6", "firmyr.7", "firmyr.8", "firmyr.9",
                        "firmyr.10", "post:Contribution_scale","post:Distribution_scale",
                        "post:S_P_500_Qtrly_Return", 
                        "post:S_P_500_Qtrly_Return_l3", "post:Fourthqtr"))
mod6Set2Null = rq(NAV_change ~ 1, tau = .5, data = peSet2, 
                  method = "sfn")

mod6Set2R1 = 1 - mod6Set2$rho / mod6Set2Null$rho

modDid = rq(NAV_abs_err_scaled ~ 
              post*TREATMENT +
              post*S_P_500_Qtrly_Return + 
              post*S_P_500_Qtrly_Return_l3 + 
              post*Fourthqtr + as.factor(firmyr), 
            data = peDid, method = "sfn", tau = .5)
modDidSum = summary(modDid, se = "boot", R = 200, cluster = peDid$Coded_fund_id)

write.csv(modDidSum$coefficients, "data/working/modDidSum.csv", 
          row.names = c("intercept", "post", "TREATMENT",
                        "S_P_500_Qtrly_Return", 
                        "S_P_500_Qtrly_Return_l3", "Fourthqtr", 
                        "firmyr.1", "firmyr.2", "firmyr.3", "firmyr.4", 
                        "firmyr.5", "firmyr.6", "firmyr.7", "firmyr.8", "firmyr.9",
                        "firmyr.10", "post:TREATMENT",
                        "post:S_P_500_Qtrly_Return", 
                        "post:S_P_500_Qtrly_Return_l3", "post:Fourthqtr"))
modDidNull = rq(NAV_abs_err_scaled ~ 1, tau = .5, data = peDid, 
                  method = "sfn")

modDidR1 = 1 - modDid$rho / modDidNull$rho

# No Nav_change_scale. Used NAV_change instead
modJSS = rq(NAV_change ~ 
              post*Contribution_scale +
              post*Distribution_scale +
              post*S_P_500_Qtrly_Return + 
              post*S_P_500_Qtrly_Return_l3 + 
              post*Fourthqtr + as.factor(firmyr), 
            data = peJSS, method = "sfn", tau = .5)
modJSSSum = summary(modJSS, se = "boot", R = 200, cluster = peJSS$Coded_fund_id)

write.csv(modJSSSum$coefficients, "data/working/modJSSSum.csv", 
          row.names = c("intercept", "post", "Contribution_scale",
                        "Distribution_scale", "S_P_500_Qtrly_Return", 
                        "S_P_500_Qtrly_Return_l3", "Fourthqtr", 
                        "firmyr.1", "firmyr.2", "firmyr.3", "firmyr.4", 
                        "firmyr.5", "firmyr.6", "firmyr.7", "firmyr.8", "firmyr.9",
                        "firmyr.10", "post:Contribution_scale",
                        "post:Distribution_scale", "post:S_P_500_Qtrly_Return", 
                        "post:S_P_500_Qtrly_Return_l3", "post:Fourthqtr"))
modJSSNull = rq(NAV_change ~ 1, tau = .5, data = peJSS, 
                method = "sfn")

modJSSR1 = 1 - modJSS$rho / modJSSNull$rho


objsKeep = ls()[grep('.*R1$', ls())]
objsKeep

rm(list=ls()[ !ls() %in% objsKeep ])  

#
save.image('R1.RData')

r1DataFrame = data.frame(mod1Set2R1 = mod1Set2R1, 
                         mod2Set2R1 = mod2Set2R1,
                         mod3Set2R1 = mod3Set2R1, 
                         mod4Set2R1 = mod4Set2R1, 
                         mod5Set2R1 = mod5Set2R1,
                         mod6Set2R1 = mod6Set2R1, 
                         modDidR1 = modDidR1, 
                         modJSSR1 = modJSSR1)

r1DataFrame = as.data.frame(t(r1DataFrame))

names(r1DataFrame) = "R1"

write.csv(r1DataFrame, "data/working/modelR1.csv")



###########################################################
# My models above, Seth's previous code is below
###########################################################



modAJSS = rq(NAV_change_scale ~ Contribution_scale + 
               Distribution_scale + 
               S_P_500_Qtrly_Return +
               S_P_500_Qtrly_Return_l3 + 
               Fourthqtr + as.factor(firmyr), 
             data = peJSS, method = "sfn", tau = .5)

modAJSSSum = summary(modAJSS, se = "boot", R = 200, cluster = peJSS$Coded_fund_id)

write.csv(modAJSSSum$coefficients, "data/working/modAJSSSum.csv", row.names = FALSE)

modAJSSNull = rq(NAV_change_scale ~ 1, tau = .5, data = peJSS, 
              method = "sfn")

modAJSSR1 = 1 - modAJSS$rho / modAJSSNull$rho

modBJSS = rq(NAV_change_scale_dem ~ 
            Contribution_scale_dem + 
            Distribution_scale_dem + 
            S_P_500_Qtrly_Return_dem + 
            S_P_500_Qtrly_Return_l3_dem + 
            Fourthqtr + as.factor(firmyr), 
          data = peJSS, method = "sfn", tau = .5)

modBJSSSum = summary(modBJSS, se = "boot", R = 200, cluster = peJSS$Coded_fund_id)


write.csv(modBJSSSum$coefficients, file = "data/working/modBJSSSum.csv", 
          row.names = c("intercept","Contribution_scale_dem",
                        "Distribution_scale_dem", "S_P_500_Qtrly_Return_dem", 
                        "S_P_500_Qtrly_Return_l3_dem", "Fourthqtr", 
                        "firmyr.1", "firmyr.2", "firmyr.3", "firmyr.4", 
                        "firmyr.5", "firmyr.6", "firmyr.7", "firmyr.8", "firmyr.9",
                        "firmyr.10"))


modBJSSNull = rq(NAV_change_scale_dem ~ 1, tau = .5, data = peJSS, 
              method = "sfn")

modBJSSR1 = 1 - modBJSS$rho / modBJSSNull$rho

modCJSS = rq(NAV_change_scale_dem ~ 
            post*Contribution_scale_dem + 
            post*Distribution_scale_dem + 
            post*S_P_500_Qtrly_Return_dem + 
            post*S_P_500_Qtrly_Return_l3_dem + 
            post*Fourthqtr + as.factor(firmyr), 
          data = peJSS, method = "sfn", tau = .5)

modCJSSSum = summary(modCJSS, se = "boot", R = 200, cluster = peJSS$Coded_fund_id)


write.csv(modCJSSSum$coefficients, file = "data/working/modCJSSSum.csv", 
          row.names = c("intercept", "post", "Contribution_scale_dem", 
                        "Distribution_scale_dem", "S_P_500_Qtrly_Return_dem", 
                        "S_P_500_Qtrly_Return_l3_dem", "Fourthqtr", "firmyr.-1", 
                        "firmyr.0", "firmyr.1", "firmyr.2", "firmyr.3", "firmyr.4", 
                        "firmyr.5", "firmyr.6", "firmyr.7", "firmyr.8", "firmyr.9",
                        "firmyr.10", "post:Contribution_scale_dem", 
                        "post:Distribution_scale_dem", "post:S_P_500_Qtrly_Return_dem", 
                        "post:S_P_500_Qtrly_Return_l3_dem", "post:Fourthqtr"))



modCJSSNull = rq(NAV_change_scale_dem ~ 1, tau = .5, data = peJSS, 
              method = "sfn")

modCJSSR1 = 1 - modCJSS$rho / modCJSSNull$rho


modDJSS = rq(NAV_change_scale_dem ~ 
            post*Contribution_scale_dem + 
            post*Distribution_scale_dem + 
            Distribution_scale_dem*post*NewFund +
            Distribution_scale_dem*post*LargeFund +
            Distribution_scale_dem*post*MoreExperience +
            post*S_P_500_Qtrly_Return_dem + 
            post*S_P_500_Qtrly_Return_l3_dem + 
            post*Fourthqtr + as.factor(firmyr), data = peJSS, method = "sfn", 
            tau = .5, control = c(tmpmax = 1000))

modDJSSSum = summary(modDJSS, se = "boot", R = 200, cluster = peJSS$Coded_fund_id)

write.csv(modDJSSSum$coefficients, file = "data/working/modDJSSSum.csv", 
          row.names = c("intercept", "post", "Contribution_scale_dem", 
                        "Distribution_scale_dem", "NewFund", "LargeFund", 
                        "MoreExperience", "S_P_500_Qtrly_Return_dem", 
                        "S_P_500_Qtrly_Return_l3_dem", "Fourthqtr", "firmyr.-1", 
                        "firmyr.0", "firmyr.1", "firmyr.2", "firmyr.3", "firmyr.4", 
                        "firmyr.5", "firmyr.6", "firmyr.7", "firmyr.8", "firmyr.9",
                        "firmyr.10", "post:Contribution_scale_dem", 
                        "post:Distribution_scale_dem", "Distribution_scale_dem:NewFund", 
                        "post:NewFund", "Distribution_scale_dem:LargeFund", 
                        "post:LargeFund", "Distribution_scale_dem:MoreExperience", 
                        "post:MoreExperience", "post:S_P_500_Qtrly_Return_dem", 
                        "post:S_P_500_Qtrly_Return_l3_dem", "post:Fourthqtr", 
                        "post:Distribution_scale_dem:NewFund", 
                        "post:Distribution_scale_dem:LargeFund", 
                        "post:Distribution_scale_dem:MoreExperience"))


modDJSSNull = rq(NAV_change_scale_dem ~ 1, tau = .5, data = peJSS, 
              method = "sfn")

modDJSSR1 = 1 - modDJSS$rho / modDJSSNull$rho


modEJSS = rq(NAV_change_scale_dem ~ 
            post*Contribution_scale_dem + 
            post*Distribution_scale_dem + 
            Distribution_scale_dem*post*Venture +
            post*S_P_500_Qtrly_Return_dem + 
            post*S_P_500_Qtrly_Return_l3_dem + 
            post*Fourthqtr + as.factor(firmyr), data = peJSS, method = "sfn", tau = .5)

modEJSSSum = summary(modEJSS, se = "boot", R = 200, cluster = peJSS$Coded_fund_id)

write.csv(modEJSSSum$coefficients, file = "data/working/modEJSSSum.csv", 
          row.names = c("intercept", "post", "Contribution_scale_dem", 
                        "Distribution_scale_dem", "Venture", "S_P_500_Qtrly_Return_dem", 
                        "S_P_500_Qtrly_Return_l3_dem", "Fourthqtr", "firmyr.-1", 
                        "firmyr.0", "firmyr.1", "firmyr.2", "firmyr.3", "firmyr.4", 
                        "firmyr.5", "firmyr.6", "firmyr.7", "firmyr.8", "firmyr.9",
                        "firmyr.10", "post:Contribution_scale_dem", 
                        "post:Distribution_scale_dem", "Distribution_scale_dem:Venture", 
                        "post:Venture", "post:S_P_500_Qtrly_Return_dem",
                        "post:S_P_500_Qtrly_Return_l3_dem", "post:Fourthqtr", 
                        "post:Distribution_scale_dem:Venture"))


modEJSSNull = rq(NAV_change_scale_dem ~ 1, tau = .5, data = peJSS, 
              method = "fn")

modEJSSR1 = 1 - modEJSS$rho / modEJSSNull$rho


modASet2 = rq(NAV_err_scaled ~ 
            post*S_P_500_Qtrly_Return + 
            post*S_P_500_Qtrly_Return_l3 +
            post*Fourthqtr +
            as.factor(firmyr) + as.factor(Coded_fund_id),
          data = peSet2, method = "fn", tau = .5)

modASet2Sum = summary(modASet2, se = "boot", R = 200, cluster = peSet2$Coded_fund_id)

write.csv(modASet2Sum$coefficients, file = "data/working/modASet2Sum.csv")


modASet2Null = rq(NAV_err_scaled ~ 1, tau = .5, data = peSet2, 
              method = "fn")

modASet2R1 = 1 - modASet2$rho / modASet2Null$rho


modBSet2 = rq(NAV_err_scaled ~ 
            post*S_P_500_Qtrly_Return + 
            post*S_P_500_Qtrly_Return_l3 +
            post*Contribution_scale + 
            post*Distribution_scale + 
            post*Fourthqtr + 
            as.factor(firmyr) + as.factor(Coded_fund_id), 
          data = peSet2, method = "fn", tau = .5)

modBSet2Sum = summary(modBSet2, se = "boot", R = 200, cluster = peSet2$Coded_fund_id)

write.csv(modBSet2Sum$coefficients, file = "data/working/modBSet2Sum.csv")


modBSet2Null = rq(NAV_err_scaled ~ 1, tau = .5, data = peSet2, 
              method = "fn")

modBSet2R1 = 1 - modBSet2$rho / modBSet2Null$rho


modCSet2 = rq(NAV_abs_err_scaled ~ 
            post*S_P_500_Qtrly_Return + 
            post*S_P_500_Qtrly_Return_l3 +
            post*Fourthqtr + 
            as.factor(firmyr) + as.factor(Coded_fund_id), 
          data = peSet2, method = "fn", tau = .5)

modCSet2Sum = summary(modCSet2, se = "boot", R = 200, cluster = peSet2$Coded_fund_id)

write.csv(modCSet2Sum$coefficients, file = "data/working/modCSet2Sum.csv")

modCSet2Null = rq(NAV_abs_err_scaled ~ 1, tau = .5, data = peSet2, 
              method = "fn")

modCSet2R1 = 1 - modCSet2$rho / modCSet2Null$rho


modDSet2 = rq(NAV_abs_err_scaled ~ 
            post*S_P_500_Qtrly_Return + 
            post*S_P_500_Qtrly_Return_l3 + 
            post*Contribution_scale + 
            post*Distribution_scale + 
            post*Fourthqtr + 
            as.factor(firmyr) + as.factor(Coded_fund_id), 
          data = peSet2, method = "fn", tau = .5)

modDSet2Sum = summary(modDSet2, se = "boot", R = 200, cluster = peSet2$Coded_fund_id)

write.csv(modDSet2Sum$coefficients, file = "data/working/modDSet2Sum.csv")

modDSet2Null = rq(NAV_abs_err_scaled ~ 1, tau = .5, data = peSet2, 
              method = "fn")

modDSet2R1 = 1 - modDSet2$rho / modDSet2Null$rho


modESet2 = rq(NAV_err_scaled ~ 
            post*LargeFund +
            post*MoreExperience +
            post*NewFund +
            post*S_P_500_Qtrly_Return + 
            post*S_P_500_Qtrly_Return_l3 + 
            post*Fourthqtr + 
            as.factor(firmyr) + as.factor(Coded_fund_id), 
          data = peSet2, method = "sfn", tau = .5)

modESet2Sum = summary(modESet2, se = "boot", R = 200, cluster = peSet2$Coded_fund_id) # Clustering has singular matrix

write.csv(modESet2Sum$coefficients, file = "data/working/modESet2Sum.csv")

modESet2Null = rq(NAV_err_scaled ~ 1, tau = .5, data = peSet2, 
              method = "fn")

modESet2R1 = 1 - modESet2$rho / modESet2Null$rho


modFSet2 = rq(NAV_abs_err_scaled ~ 
            post*LargeFund +
            post*MoreExperience +
            post*NewFund +
            post*S_P_500_Qtrly_Return + 
            post*S_P_500_Qtrly_Return_l3 + 
            post*Fourthqtr + 
            as.factor(firmyr) + as.factor(Coded_fund_id), 
          data = peSet2, method = "sfn", tau = .5)

modFSet2Sum = summary(modFSet2, se = "boot", R = 200)

write.csv(modFSet2Sum$coefficients, file = "data/working/modFSet2Sum.csv")

modFSet2Null = rq(NAV_abs_err_scaled ~ 1, tau = .5, data = peSet2, 
              method = "sfn")

modFSet2R1 = 1 - modFSet2$rho / modFSet2Null$rho


modGSet2 = rq(NAV_err_scaled ~ 
            post*Venture +
            post*S_P_500_Qtrly_Return + 
            post*S_P_500_Qtrly_Return_l3 + 
            post*Fourthqtr + 
            as.factor(firmyr) + as.factor(Coded_fund_id), 
          data = peSet2, method = "sfn", tau = .5)

modGSet2Sum = summary(modGSet2, se = "boot", R = 200)

write.csv(modGSet2Sum$coefficients, file = "data/working/modGSet2Sum.csv")


modGSet2Null = rq(NAV_err_scaled ~ 1, tau = .5, data = peSet2, 
              method = "fn")

modGSet2R1 = 1 - modGSet2$rho / modGSet2Null$rho


modHSet2 = rq(NAV_abs_err_scaled ~ 
            post*Venture +
            post*S_P_500_Qtrly_Return + 
            post*S_P_500_Qtrly_Return_l3 + 
            post*Fourthqtr + 
            as.factor(firmyr) + as.factor(Coded_fund_id), 
          data = peSet2, method = "sfn", tau = .5)

modHSet2Sum = summary(modHSet2, se = "boot", R = 200)

write.csv(modHSet2Sum$coefficients, file = "data/working/modHSet2Sum.csv")

modHSet2Null = rq(NAV_abs_err_scaled ~ 1, tau = .5, data = peSet2, 
              method = "sfn")

modHSet2R1 = 1 - modHSet2$rho / modHSet2Null$rho

objsKeep = ls()[grep('.*R1$', ls())]
objsKeep

rm(list=ls()[ !ls() %in% objsKeep ])  

#
save.image('R1.RData')

r1DataFrame = data.frame(mod1Set2R1 = mod1Set2R1, 
                         mod2Set2R1 = mod2Set2R1,
                         mod3Set2R1 = mod3Set2R1, 
                         mod4Set2R1 = mod4Set2R1, 
                         mod5Set2R1 = mod5Set2R1,
                         mod6Set2R1 = mod6Set2R1, 
                         modDidR1 = modDidR1, 
                         modJSSR1 = modJSSR1)

r1DataFrame = as.data.frame(t(r1DataFrame))

names(r1DataFrame) = "R1"

write.csv(r1DataFrame, "data/working/modelR1.csv")





peSet2 = haven::read_sas("data/original/pe_set2_toseth_12012016.sas7bdat")

peSet2$NewFund = ifelse(peSet2$fundlife < 15, 1, 0)

peSet2$MoreExperience = ifelse(peSet2$experience > 1, 1, 0)

peSet2$LargeFund = ifelse(peSet2$fund_size > 199, 0, 1)

peSet2$Venture = ifelse(peSet2$Strategy2 == 2, 1, 0)



mod1 = rq(NAV_abs_err_scaled_dem ~ 
                post*SmallFund +
                post*MoreExperience +
                post*NewFund +
                post*S_P_500_Qtrly_Return_dem + 
                post*S_P_500_Qtrly_Return_l3_dem + 
                post*Fourthqtr + 
                as.factor(firmyr), 
              data = peSet2, tau = .5)

mod1Sum = summary(mod1, se = "boot", R = 200, cluster = peSet2$Coded_fund_id)

write.csv(mod1Sum$coefficients, file = "data/working/mod1Sum.csv")

mod1Null = rq(NAV_abs_err_scaled_dem ~ 1, tau = .5, data = peSet2)

mod1R1 = 1 - mod1$rho / mod1Null$rho



mod2 = rq(NAV_abs_err_scaled_dem ~ 
            post*Venture +
            post*S_P_500_Qtrly_Return_dem + 
            post*S_P_500_Qtrly_Return_l3_dem + 
            post*Fourthqtr + 
            as.factor(firmyr), 
          data = peSet2, tau = .5)

mod2Sum = summary(mod2, se = "boot", R = 200, cluster = peSet2$Coded_fund_id)

write.csv(mod2Sum$coefficients, file = "data/working/mod2Sum.csv")

mod2Null = rq(NAV_abs_err_scaled_dem ~ 1, tau = .5, data = peSet2)

mod2R1 = 1 - mod2$rho / mod2Null$rho

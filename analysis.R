require(survey)
require(feather)

svyciprop_yrbs = function(formula, design, method="xlogit", level=0.95,
                          df=degf(design), ...) {
  svyciprop(formula, design, method, level, df, na.rm=TRUE, ...)
}

svybyci_yrbs = function(formula, by, des, fn, ...){
  svyby(formula, by, des, fn, keep_var=TRUE, method='xlogit',
        vartype=c('se','ci'), na.rm.by=TRUE, na.rm.all=TRUE, multicore=TRUE)
}


fetch_stats_by = function(vars, qn, des){
  qn_f = as.formula(paste('~',qn))
  stats = svybyci_yrbs(qn_f, lvl_f, des, svyciprop_yrbs)
  print(stats)
  counts = svyby( qn_f, lvl_f, des, unwtd_count, na.rm=TRUE, na.rm.by=TRUE,
                  na.rm.all=TRUE, multicore=TRUE)
  res = merge(stats, counts)
  print(res)
  res = subset(res, select= -c('se'))
  print(res)
  res$level = len(vars)
  res$q = qn
  return(res)
}

#read in pre-parsed survey data
rdf = feather('cache/yrbs.combined.feather')

#setup the survey design
yrbsdes = svydesign(id=~psu, weight=~weight, strata=~stratum, data=rdf, nest=TRUE)

#variables to breakout reponses by: sex x grade x race7 x year
vars = c('sex','grade','race7','year')

#boolean questions of interest are columns with names starting with 'qn'
qn_list = colnames(rdf)[grep('^qn', colnames(rdf))]

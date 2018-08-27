import rpy2.robjects as robjects

svyciprop_xlogit = robjects.r('''
function(formula, design, method='xlogit', level = 0.95, df=degf(design), ...) {
    svyciprop(formula, design, method, level, df, na.rm=TRUE, ...)
}''')

svybyci_xlogit = robjects.r('''
function( formula, by, des, fn, ...) {
    svyby(formula, by, des, fn, keep.var=TRUE, method='xlogit',
          vartype=c('se','ci'), na.rm.by=TRUE, na.rm.all=TRUE, 
          multicore=FALSE, drop.empty.groups=FALSE)
}''')

svyby_nodrop = robjects.r('''
function( formula, by, des, fn, ...) {
    svyby(formula, by, des, fn, keep.var=TRUE,
          na.rm.by=TRUE, na.rm.all=TRUE, 
          multicore=FALSE, drop.empty.groups=FALSE)
}''')

filter_survey_var = robjects.r('''
function(des, k, vals){
    des$variables[[k]] %in% vals
}
''')

rm_nan_survey_var = robjects.r('''
function(des, k){
    !is.na(des$variables[[k]])
}
''')

tobool = robjects.r('''
function(col) {
    as.logical( 2 - col)
} ''')

classof = robjects.r('''
function(v) {
    class(v)
} ''')

factor_summary = robjects.r('''
function(v) {
    summary(as.factor(v))
}''')

subset_des_wexpr = robjects.r('''
function(des,expr) {
    subset( des,
            eval(parse(text=expr)))
}''')

fix_lonely_psus = robjects.r('''
function(){
    options(survey.lonely.psu="average")
}
''')

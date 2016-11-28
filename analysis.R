require(survey)

svymean_rmna = function(x, design, na.rm=TRUE, deff=FALSE, ...) {
  svymean(x, design, na.rm, deff, ...)
}

svyciprop_yrbs = function(formula, design, method="xlogit", level=0.95,
                          df=degf(design), ...) {
  svyciprop(formula, design, method, level, df, na.rm=TRUE, ...)

}
svytotal_yrbs = function(x, design, na.rm=TRUE, deff=FALSE, ...) {
  svytotal(x, design, na.rm=FALSE, deff=FALSE,...)
}

hmu = svyby(~I(qn8==1) + I(qn60==1) + I(qn52==1), ~q2, yrbsdes, svymean_rmna, keep_var=True, method="xlogit")

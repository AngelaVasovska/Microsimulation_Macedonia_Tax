"""
app1.py illustrates use of TPRU-India taxcalc release 2.0.0
USAGE: python app1.py > app1.res
CHECK: Use your favorite Windows diff utility to confirm that app1.res is
       the same as the app1.out file that is in the repository.
"""
from taxcalc import *

# create Records object containing pit.csv and pit_weights.csv input data
recs = Records()

# create GSTRecords object containing gst.csv and gst_weights.csv input data
grecs = GSTRecords()

assert isinstance(grecs, GSTRecords)
assert grecs.data_year == 2017
assert grecs.current_year == 2017

# create CorpRecords object containing cit.csv and cit_weights.csv input data
crecs = CorpRecords()

assert isinstance(crecs, CorpRecords)
assert crecs.data_year == 2017
assert crecs.current_year == 2017

# create Policy object containing current-law policy
pol = Policy()

# specify Calculator object for current-law policy
calc1 = Calculator(policy=pol, records=recs, gstrecords=grecs,
                   corprecords=crecs, verbose=False)
calc1.calc_all()

# specify Calculator object for reform in JSON file
reform = Calculator.read_json_param_objects('app1_reform.json', None)
pol.implement_reform(reform['policy'])
calc2 = Calculator(policy=pol, records=recs, gstrecords=grecs,
                   corprecords=crecs, verbose=False)
calc2.calc_all()

# compare aggregate results from two calculators
weighted_tax1 = calc1.weighted_total('pitax')
weighted_tax2 = calc2.weighted_total('pitax')
total_weights = calc1.total_weight()
print(f'Tax 1 {weighted_tax1 * 1e-6:,.2f}')
print(f'Tax 2 {weighted_tax2 * 1e-6:,.2f}')
print(f'Total weight {total_weights * 1e-6:,.2f}')

dump_vars = ['ID_No','Salaries','GTI','TTI', 'pitax','post_tax_income']
dumpdf = calc1.dataframe(dump_vars)
dumpdf= dumpdf.sort_values(by=['Salaries'])
dumpdf.to_csv('app0-dump_macedonia.csv',
              index=False, float_format='%.0f')


gini_pre_tax = calc1.gini(['GTI'])
print(gini_pre_tax)

gini_post_tax = calc1.gini(['post_tax_income'])
print(gini_post_tax)

gini_post_tax_reform = calc2.gini(['post_tax_income'])
print(gini_post_tax_reform)











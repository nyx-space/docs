TypeError: 'builtins.TimeSeries' object is not subscriptable

In [22]: ref_tai_s = Epoch('1970-01-01 00:00:00 UTC').as_tai_duration()

In [23]: ref_tai_dur = Epoch('1970-01-01 00:00:00 UTC').as_tai_duration()

In [24]: e_prime = Epoch('1970-01-01 00:00:00 UTC') + Unit.Day * 30.0

In [25]: e_prime
Out[25]: 1970-01-31T00:00:00 UTC

In [26]: e_prime.as_tai_duration() - ref_tai_dur
Out[26]: 30 days

In [27]: (e_prime.as_tai_duration() - ref_tai_dur).in_seconds()
Out[27]: 2592000.0

In [28]: (e_prime.as_utc_duration() - ref_tai_dur).in_seconds()
Out[28]: 2592000.0

In [29]: (e_prime.as_tt_duration() - ref_tai_dur).in_seconds()
Out[29]: 2592032.184

In [30]: (e_prime.as_et_duration() - ref_tai_dur).in_seconds()
Out[30]: -3153124767.8152266

In [31]: (e_prime.as_et_duration_since_j1900() - ref_tai_dur).in_seconds()
Out[31]: 2592032.184773294

In [32]: (e_prime.as_tdb_duration_since_j1900() - ref_tai_dur).in_seconds()
Out[32]: 2592032.184782055

In [33]: 

ts = TimeSeries(Epoch('1970-01-01 00:00:00 UTC'), Epoch('2023-01-01 00:00:00 UTC'), Unit.Day * 30.0, True)

data = []

 for epoch in ts:
    ...:     delta_duration = epoch.as_tai_duration() - ref_tai_dur
    ...:     delta_utc = epoch.as_utc_duration() - epoch.as_tai_duration()
    ...:     delta_tt = epoch.as_tt_duration() - epoch.as_tai_duration()
    ...:     delta_tdb = epoch.as_tdb_duration_since_j1900() - epoch.as_tai_duration()
    ...:     delta_et = epoch.as_et_duration_since_j1900() - epoch.as_tai_duration()
    ...:     # Build the pandas series
    ...:     data.append([str(epoch), delta_tt.in_seconds(), delta_et.in_seconds(), delta_tdb.in_seconds(), delta_utc.in_seconds()])

import plotly.express as px

df['UTC Datetime'] = pd.to_datetime(df['UTC Epoch'])

px.line(df, x='UTC Datetime', y=['\\Delta TT (s)', '\\Delta ET (s)']).show()

columns=["UTC Epoch", "\\Delta TT (s)", "\\Delta ET (s)", "\\Delta TDB (s)", "\\Delta UTC (s)"]

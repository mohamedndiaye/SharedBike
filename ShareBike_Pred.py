# In[]:
def fill_in_missing_dates(df, date_col_name = 'date', date_order = 'asc', fill_value = 0, days_back = 15):
    df.set_index(date_col_name,drop=True,inplace=True)
    df.index = pd.DatetimeIndex(df.index)
    d = datetime.now().date()
    d2 = d - timedelta(days = days_back)
    idx = pd.date_range(d2, d, freq = 'D')
    df = df.reindex(idx,fill_value=fill_value)
    df[date_col_name] = pd.DatetimeIndex(df.index)
    return df

daily = datacopy.resample('D').sum()
import scipy.sparse as sp
imp = Imputer(missing_values=0, strategy='mean', axis=0)
daily['count'] = imp.fit_transform(daily['count'].values.reshape(-1,1))
daily.rolling(30, center=True).sum().plot(style=[':', '--', '-'])
plt.ylabel('mean hourly count');


by_time = datacopy.groupby(datacopy.index.time).mean()
hourly_ticks = 1 * 60 * 60 * np.arange(24)
by_time.plot(xticks=hourly_ticks, style=[':', '--', '-']);

by_weekday = datacopy.groupby(datacopy.index.dayofweek).mean()
by_weekday.index = ['Mon', 'Tues', 'Wed', 'Thurs', 'Fri', 'Sat', 'Sun']
by_weekday.plot(style=[':', '--', '-']);

traindata['hour'] = traindata.datetime.apply([lambda st: time.strptime(st, '%Y-%m-%d %H:%M:%S')[3]])
datacopy = traindata[['datetime', 'hour' 'count']]
weekday_coef = dict(zip(by_time.loc['Weekend']['hour'].astype(int),
                   StandardScaler().fit_transform(by_time.loc['Weekday']['count'].values.reshape(-1,1))))
weekend_coef = dict(zip(by_time.loc['Weekend']['hour'].astype(int),
                   StandardScaler().fit_transform(by_time.loc['Weekend']['count'].values.reshape(-1,1))))

def conv_peakhour(df, weekday_coef, weekend_coef):
  by_time.loc['Weekday'].nlargest(5,columns=['count'])
  buf = []
  for row in df.itertuples():
    cur_hour = row.Index.hour
    isweekend = 'Weekday' if row.Index.dayofweek < 5 else 'Weekend'
    if isweekend == 'Weekday':
      cur_coef = float(weekday_coef.get(cur_hour))
    else:
      cur_coef = float(weekend_coef.get(cur_hour))
    buf.append(cur_coef)
  df['hour_coef'] = buf
  return df
#For use with Neware battery cycles
#To change to a different cycler modifiy the appropiate labels in 'usecols', line 11

import pandas as pd
import numpy as np


input_filename = input('What is your filname? (include .csv extension)')

#reads your CSV file
df = pd.read_csv(input_filename, usecols=['Cycle','Status', 'Voltage(V)', 'CapaCity(mAh)']) 

#filters data for microvoltages that are either higher or lower than previous data, useful for differential plots
def filter(df):
  temp = df['Voltage(V)'][0]
  for index, item in df['Voltage(V)'].iteritems():
    if df['Status'][index] == 'CC_DChg':
      if item > temp or item == temp:
        df['Voltage(V)'][index] = np.nan
      else:
        temp = item
    elif df['Status'][index] == 'CC_Chg':
      if item < temp or item == temp:
        df['Voltage(V)'][index] = np.nan
      else:
        temp = item
  return df

desire_filtering =input('Would you like to apply filter for differential plotting?')

if desire_filtering:
    df = filter(df)[df['Voltage(V)'].notna()]

#tranposes the voltage and capacity values for every cycle's charge and discharge to facilitate input into plotting software
def transpose(df):
  for i in range(1, df['Cycle'].iloc[-1].astype(int) + 1):
    df['{} D_Voltage(V)'.format(i)] = df[(df['Status'] == 'CC_DChg') & (df['Cycle'] == i)]['Voltage(V)']
    df['{} D_Capacity(mAh)'.format(i)] = df[(df['Status'] == 'CC_DChg') & (df['Cycle'] == i)]['CapaCity(mAh)']
    df['{} C_Voltage(V)'.format(i)] = df[(df['Status'] == 'CC_Chg') & (df['Cycle'] == i)]['Voltage(V)']
    df['{} C_Capacity(mAh)'.format(i)] = df[(df['Status'] == 'CC_Chg') & (df['Cycle'] == i)]['CapaCity(mAh)']
  return df

df = transpose(df).apply(lambda x: x.dropna().reset_index(drop = True))

output_filename = input('What would you like your new file to be called? (include .csv extension)')

#writes output file to working directory
df.to_csv(output_filename, index = False)

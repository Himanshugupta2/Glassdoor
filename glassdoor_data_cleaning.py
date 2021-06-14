import pandas as pd
#import numpy as np
#missing_values = ["n/a","na",np.nan]

#importing datset
dataset = "C:/Users/HIMANSHU GUPTA/Data analysis folder/glassdoor_data_analysis/glassdoor_dataset.csv"
glassdoor_dataset = pd.read_csv(dataset)

#copying data into df dataframe.
df = glassdoor_dataset.copy()

# checking info of datset
#df.info()

# checking shape of dataset
#df.shape

# finding unique values in each column.
#df.apply(lambda x: len(x.unique()))

# counting values of each category
def value_count_by_category(x,y):
    for i in y:
        print("value of this category:",i)
        print(x[i].value_counts())

#selected_column =['job_state']
#value_count_by_category(df,selected_column)

##################################cleaning####################################
  
######## droping columns

# droping unmamed:0, job description column.
column_drop = ['Unnamed: 0','Job Description']
df = df[df.drop(column_drop,axis = 1,inplace = True)]

# droping  -1 value in rating column.
df = df[df['Rating'] != -1]

# making new company column and drop company name column.
df['Company'] = df.apply(lambda x: x['Company Name'] if x['Rating'] <0 else x['Company Name'][:-3], axis = 1)

# droping company name column.
df = df[df.drop(['Company Name'], axis = 1,inplace = True)]

####### ownership column

# doing spliting in ownership column
df['Type of ownership'] = df['Type of ownership'].apply(lambda x: x.replace('Company -',''))
df['Type of ownership'] = df['Type of ownership'].apply(lambda x: x.strip())
#df['Type of ownership'] = df['Type of ownership'].replace(to_replace = ['Unknown'], value = [np.nan])

###### size column

# replacing values in size column.
#df['Size'] = df['Size'].astype('str')
df['Size'] = df['Size'].apply(lambda x: x.replace('+',''))
df['Size'] = df['Size'].apply(lambda x: x.replace('employees',''))
df['Size'] = df['Size'].apply(lambda x: x.replace('to','-'))
#df['SIZE'] = df['SIZE'].replace(to_replace = ['Unknown'], value = [np.nan])

####### revenue column

# replacing values in revenue column.
#df['REVENUE'] = df['REVENUE'].replace(to_replace = ['Unknown / Non-Applicable'], value = [np.nan])
#df['REVENUE'] = df['REVENUE'].apply(lambda x: x.replace('Unknown / Non-Applicable','nan'))
#df['Revenue'] = df['Revenue'].astype('str')
df['Revenue'] = df['Revenue'].apply(lambda x: x.replace('$',''))
df['Revenue'] = df['Revenue'].apply(lambda x: x.replace('+',''))
df['Revenue'] = df['Revenue'].apply(lambda x: x.replace('to','-'))
df['Revenue'] = df['Revenue'].apply(lambda x: x.replace('Less than',''))
df['Revenue'] = df['Revenue'].apply(lambda x: x.split('(')[0])
#df = df.replace({'Revenue':'Unknown / Non-Applicable'},np.nan)
#df['Revenue'] = df['Revenue'].astype('str')
df['Revenue'] = df['Revenue'].apply(lambda x: x.strip())

# finding nan values.
'''
df.info()
df1 = df.copy()
df1 = df1.replace(to_replace = ['-1'],value = [np.nan])
df1['Founded'] = df1['Founded'].replace(to_replace = [-1],value = [np.nan])
df1.isna().sum()
'''
######## salary estimate

# Removing (Glassdoor est.) from the values
salary = df['Salary Estimate'].apply(lambda x:x.split('(')[0])
# Removing 'k' , '$' sign from the values.
salary_sign_remove = salary.apply(lambda x: x.replace('K','').replace('$',''))
# checking empty value.
# df1 = df['min_salary'].copy()
# df2 = df1.loc[df1 == '']
# replacing -1 value witb another value.
salary_sign_remove = salary_sign_remove.replace(to_replace = ['-1'],value = ['55-101'])
# returns the list containing all the salaries present on the right hand side
df['min_salary'] = salary_sign_remove.apply(lambda x: x.split('-')[0])
df['min_salary'] = df['min_salary'].astype('int')
# returns the list containing all the salaries present on the left hand side 
df['max_salary'] = salary_sign_remove.apply(lambda x: x.split('-')[1])   
df['max_salary'] = df['max_salary'].astype('int') 
# we want to predict the salary of a particular person
# So now this becomes our dependent varible
df['avg_salary'] = (df.min_salary + df.max_salary)/2                                                                    

########### location

# taking all shortterm values.
# So we are splitting on the comma(,) 
# so now this returns a list of all the states where the job openings are present
df['job_state'] = df['Location'].apply(lambda x: x.split(',')[1])
df['job_state'] = df['job_state'].apply(lambda x: x.strip())

# comparing location and headquarters.
# This returns the list of states where the job openings are located in the headquarters
# we want to compare the rows so that's why we put axis=1
# If the job openings present in the headquarters then we get a 1 or else a 0
df['same_state'] = df.apply(lambda x: 1 if x.Location == x.Headquarters else 0,axis = 1)

######## founded

# calculating current age of company.
# To find the age of the company we can subtract the year founded from the present year. 
# if -1 is present then leave it
df['age'] = df.Founded.apply(lambda x: 1 if x<0 else 2021-x)

# copying df data into df1 variable.
df1 = df.copy()

drop_column = ['Salary Estimate','Founded']
df1 = df1[df1.drop(drop_column,inplace = True, axis = 1)]

###### duplicate values dropping.

# duplicate values removing
# therefore there is no duplicate values are there. 
#df2 = df1.loc[df1.duplicated(keep = False),:].sort_values(by = 'Job Title')
#df1 = df1.loc[df1.drop_duplicates(inplace = True),:]

# making new csv file.
df1.to_csv(r'C:/Users/HIMANSHU GUPTA/Data analysis folder/glassdoor_data_analysis/glassdoor_cleaned_dataset.csv',index=False)


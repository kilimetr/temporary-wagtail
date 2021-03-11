 
import pandas as pd
import numpy as np
 
 
xlsx = pd.ExcelFile(r"C:\Users\dominc\OneDrive - kochind.com\Desktop\SALES\SALES_Poland.xlsx")
extended = pd.read_excel(xlsx, "EXTENDED")
# Grouped jobs su unikatne kombinacie vlastnika jobu, job id a kontaktnych detailov
grouped_jobs = extended.groupby(['customer_id', 'job_id', 'contact_details'], as_index=False).count()
grouped_jobs = grouped_jobs[['customer_id', 'job_id', 'contact_details']]
# Teraz najdeme kombinacie vlastnika a job id, ktore maju viac kontaktnych detailov
grouped_jobs['count_col'] = 1
job_duplicity = grouped_jobs.groupby(['customer_id', 'job_id'], as_index=False).sum()
print(job_duplicity[job_duplicity['count_col] == 1])

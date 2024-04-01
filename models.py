import pandas as pd
import openpyxl
from fuzzywuzzy import fuzz,process
def read_file(file_path):
    dfs = []
    if file_path.endswith('.csv'):
        # Read CSV file
        df = pd.read_csv(file_path)
        dfs.append(df)
    elif file_path.endswith(('.xls', '.xlsx')):
        # Read Excel file
        xls = pd.ExcelFile(file_path)
        for sheet_name in xls.sheet_names:
            page = xls.parse(sheet_name)
            dfs.append(page)
    else:
        # Unsupported file format
        raise ValueError("Unsupported file format. Please provide a CSV, XLS, or XLSX file.")

    # Concatenate all dataframes
    merged_df = pd.concat(dfs, ignore_index=True)
    return merged_df




# Print the filtered matches

def search(threshold,table,search_text):
  matches =table['Site_ID'].apply(lambda x: process.extractOne(search_text, [x]))
  output = table[matches.apply(lambda x: x[1] >= int(threshold))]
  output=table[threshold<table['Site_ID'].apply(lambda x: fuzz.ratio(x.strip().lower(),search_text))]
  return output



class file_get():
  def __init__(self,file_path) -> None:
    self.data_frame=file_get.read_file(file_path)
  def search_on_text(self,text,threshold):
    text=text.strip().lower()
    self.matches =self.data_frame['Site_ID'].apply(lambda x: process.extractOne(text, [x.strip().lower()])[1])
    self.output=self.data_frame[threshold<=self.matches]    
    return self.output
  def change_threshold(self,threshold):
    self.output=self.data_frame[self.matches>=threshold]    
    return self.output
  @staticmethod
  def read_file(file_path):
      dfs = []
      if file_path.endswith('.csv'):
          # Read CSV file
          df = pd.read_csv(file_path)
          dfs.append(df)
      elif file_path.endswith(('.xls', '.xlsx')):
          # Read Excel file
          xls = pd.ExcelFile(file_path)
          for sheet_name in xls.sheet_names:
              page = xls.parse(sheet_name)
              dfs.append(page)
      else:
          # Unsupported file format
          raise ValueError("Unsupported file format. Please provide a CSV, XLS, or XLSX file.")

      # Concatenate all dataframes
      merged_df = pd.concat(dfs, ignore_index=True)
      return merged_df
  def export_file(self,path):
    self.output.to_csv(path ,index=False)
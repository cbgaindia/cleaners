
# coding: utf-8
import pandas as pd
import argparse
import re
import math

class FileCleaner(object):
	def cleanfile(self, input_filename):
		df = pd.read_excel(input_filename)

		#Fix Headers
		headers = df.iloc[0]
		df = df[2:]
		df = df.rename(columns = headers)

		#Drop Nan column 
		df = df.drop(df.columns[0], axis=1)

		#Reset Indexing
		df.reset_index(drop=True)

		#Find non state particulars.
		temp_lt=[]
		for index, row in df.iterrows():
		    if re.match("[A-Z]",row["States"]) and row["States"] != "All States":
		        temp_lt.append(index)
		        
		#Remove extra content. Sub categories mentions etc.
		df= df.drop(temp_lt)

		#Remove the indexing of states.
		for index, row in df.iterrows():
		    df["States"][index] = df['States'][index].split(".")[-1]

		#Replace unicode character ( – ) for missing values to ( ... )
		df=df.replace(to_replace=u"–", value="...")

		#Write cleaned dataframe to file
		df.to_csv(str(input_filename.split(".")[0] + ".csv"), sep=",", encoding='utf-8', index=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Clean given CSV File")
    parser.add_argument("input_file", help="Input CSV file")
    args = parser.parse_args()
    obj = FileCleaner()
    if not args.input_file : 
        print("Input a valid filepath")
    else:
        obj.cleanfile(args.input_file) 
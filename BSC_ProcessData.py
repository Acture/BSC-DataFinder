
import pandas as pd
file = input("File: ")
df = pd.read_csv(file)
df.columns = ["Digits","Symbol","Balance","Address"]
df["Balance"] = df["Balance"].apply(lambda x: x.zfill(30)[:-18]+"."+x.zfill(30)[-18:] )
df["Balance"] = pd.to_numeric(df["Balance"])
df = df.reindex(columns= ["Address","Symbol","Balance","Digits"])
df.drop("Digits", axis =1, inplace = True)
df.to_csv("{f}_formatted.csv".format(f=file.split()[0]),encoding='utf-8',index=False)
print(df)

#f_test.csv_1.csv
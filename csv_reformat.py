import pandas as pd
"Name-File-Vote-Truth"
df=pd.read_csv("user_votes.csv")

new_df=df.copy()


user_key_dict={}
counter=0

for user in df["Name"].unique():
    user_key_dict[user]=counter
    counter+=1

df["id"]=df["Name"].apply(lambda x: user_key_dict.get(x))
df["type"]=df["File"].apply(lambda x: "audio" if x[-1] == 3 else "video")
df["correct"]=(df["Vote"]==df["Truth"]).apply(lambda x: int(x))

final_df=df.groupby("id", "type", "Truth")["correct"].mean().reset_index()

final_df.to_csv("final_df.csv")

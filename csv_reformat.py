import pandas as pd
#"Name-File-Vote-Truth"
df=pd.read_csv("user_votes.csv")

new_df=df.copy()


user_key_dict={}
counter=1

for user in df["Name"].unique():
    user_key_dict[user]=counter
    counter+=1

df["id"]=df["Name"].apply(lambda x: user_key_dict.get(x))
df["type"]=df["File"].apply(lambda x: "audio" if x[-1] == '3' else "video")
df["accuracy"]=(df["Vote"]==df["Truth"]).apply(lambda x: int(x))
df["truth"]=df["Truth"]
accuracy_df=df.groupby(by=["id", "type", "truth"])["accuracy"].mean().reset_index()
accuracy_df.to_csv("accuracy_df.csv")

rt_df=df[["type", "truth", "RT"]]
rt_df.to_csv("rt_df.csv")

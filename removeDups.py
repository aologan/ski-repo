#convert dictionary to lowercase values
# then removes any items tahat aren't found in the resors dictionary and csv path

def remove_duplicates(csv_path, resort_dict):
    import pandas as pd

    # Read the CSV file
    df = pd.read_csv(csv_path)

    # Lowercase the column name and the resort dictionary values
    df['name'] = df['name'].str.lower()  # Lowercase the column name
    resort_dict = {k.lower(): v for k, v in resort_dict.items()}  # Lowercase the resort dictionary keys

    # Filter the DataFrame based on the keywords in resort_dict
    filtered_df = df[df['name'].isin(resort_dict)]  # Replace 'column_name' with the actual column to filter

    # Write the filtered DataFrame back to the CSV
    filtered_df.to_csv(csv_path, index=False)
    return filtered_df

csv_path = 'coloResorts.csv'
resort_dict = {
    "A basin": "39.6426,-105.8719",
    "aspen mountain": "39.1867,-106.8186",
    "beaver creek": "39.6042,-106.5165",
    "breckenridge": "39.4817,-106.0384",
    "copper mountain": "39.5022,-106.1500",
    "crested butte": "38.8998,-106.9650",
    "eldora mountain": "39.9372,-105.5829",
    "keystone": "39.6062,-105.9437",
    "loveland ski area": "39.6800,-105.8974",
    "monarch mountain": "38.5128,-106.3316",
    "powderhorn mountain resort": "39.0690,-108.1503",
    "purgatory resort": "37.6297,-107.8140",
    "silverton mountain": "37.8851,-107.6659",
    "steamboat": "40.4850,-106.8317",
    "telluride": "37.9375,-107.8123",
    "vail": "39.6403,-106.3742",
    "winter park": "39.8917,-105.7631",
    "wolf creek": "37.4720,-106.7934"
}
    
print(remove_duplicates(csv_path, resort_dict))
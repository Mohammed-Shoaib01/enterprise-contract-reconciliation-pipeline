def resolve_ultimate_parent(row):
    if row.get('GreatGrandparent_Account_Name') != 'N/A':
        return row['GreatGrandparent_Account_Name']
    if row.get('Grandparent_Account_Name') != 'N/A':
        return row['Grandparent_Account_Name']
    if row.get('Parent_Account_Name') != 'N/A':
        return row['Parent_Account_Name']
    return row['Account_Name']
import pandas as pd
import os
from datetime import datetime

# --- CONFIGURATION ---
# Anonymized threshold for "Expiring Soon" (e.g., end of next fiscal year)
EXPIRATION_THRESHOLD = pd.to_datetime('2027-08-31')
TODAY = pd.to_datetime('today').normalize()

# Anonymized Regional Manager Mapping
# Replace real names with generic placeholders for GitHub
MANAGER_MAPPING = {
    'West': 'Manager_A',
    'Southeast': 'Manager_B',
    'MidAtlantic': 'Manager_C',
    'Northeast': 'Manager_D',
    'Southwest': 'Manager_E',
    'Central(Midwest)': 'Manager_F',
    'International': 'Manager_G'
}

# --- 1. THE EXCLUSION SIEVE (ACCOUNT-FIRST LOGIC) ---

# Step A: Identify All Active Accounts
# An account is "Active" if ANY of its contracts end after the threshold
active_mask = df_master['Sub_End_Date__c'] > EXPIRATION_THRESHOLD
active_accounts = set(df_master[active_mask]['Prioritized_Account_Name'])

# Step B: Identify "Expiring Soon" Accounts
# Must NOT be in the Active set, and must have a contract ending before the threshold
expiring_mask = (df_master['Sub_End_Date__c'] <= EXPIRATION_THRESHOLD) & \
                (df_master['Sub_End_Date__c'] >= TODAY)
# Filter out accounts already flagged as Active
expiring_soon_accounts = set(df_master[expiring_mask]['Prioritized_Account_Name']) - active_accounts

# Step C: Identify "Truly Expired" Accounts
# Must NOT be in Active or Expiring, and all contracts ended before today
expired_mask = df_master['Sub_End_Date__c'] < TODAY
truly_expired_accounts = (set(df_master[expired_mask]['Prioritized_Account_Name']) 
                          - active_accounts 
                          - expiring_soon_accounts)

# --- 2. CONTACT PROCESSING & ENRICHMENT ---

def process_contact_lists(df, account_list):
    """
    Filters the master dataframe for specific accounts and merges 
    Primary Contacts and Contract Signers into a clean stakeholder list.
    """
    filtered_df = df[df['Prioritized_Account_Name'].isin(account_list)].copy()
    
    # Identify Stakeholders (Anonymized field names)
    # Using .melt to unpivot contact columns into a single 'Contact' column
    contact_cols = ['Primary_Contact__c', 'School_Contract_Signer__c', 'Follow_Up_Contact__c']
    valid_cols = [c for c in contact_cols if c in filtered_df.columns]
    
    stakeholder_df = filtered_df.melt(
        id_vars=['Prioritized_Account_Name', 'Region', 'Type_of_Business'],
        value_vars=valid_cols,
        value_name='Stakeholder_Name'
    ).dropna(subset=['Stakeholder_Name'])
    
    return stakeholder_df.drop_duplicates()

# Generate the three distinct dataframes
df_active = process_contact_lists(df_master, active_accounts)
df_expiring = process_contact_lists(df_master, expiring_soon_accounts)
df_expired = process_contact_lists(df_master, truly_expired_accounts)

# --- 3. REGIONAL DISTRIBUTION & EXPORT ---

def export_manager_files(df, bucket_name):
    """
    Splits a dataframe by region and saves a CSV for each Manager.
    """
    for region, manager_alias in MANAGER_MAPPING.items():
        region_data = df[df['Region'] == region]
        
        if not region_data.empty:
            filename = f"{manager_alias}_{bucket_name}_{datetime.now().strftime('%Y%m%d')}.csv"
            # In a real GitHub repo, you might save to a 'dist/' folder
            path = os.path.join('output', bucket_name, filename)
            
            os.makedirs(os.path.dirname(path), exist_ok=True)
            region_data.to_csv(path, index=False)
            print(f"Generated: {path}")

# Execute Export
export_manager_files(df_active, 'ACTIVE')
export_manager_files(df_expiring, 'EXPIRING_SOON')
export_manager_files(df_expired, 'TRULY_EXPIRED')

# --- 4. CLOUD INTEGRATION (GOOGLE DRIVE) ---

def upload_to_cloud(local_path, folder_id):
    """
    Placeholder for Google Drive API Upload logic.
    Anonymized for GitHub.
    """
    print(f"Simulating upload of {local_path} to Google Drive Folder: {folder_id}")
    # Actual implementation would use:
    # service.files().create(body=file_metadata, media_body=media, fields='id').execute()

# Example Folder IDs (Anonymized)
DRIVE_FOLDERS = {
    'ACTIVE': 'folder_id_alpha_123',
    'EXPIRING_SOON': 'folder_id_beta_456',
    'TRULY_EXPIRED': 'folder_id_gamma_789'
}

print("Workflow Complete. All regional files categorized and prepared for distribution.")
# Enterprise Contract Reconciliation & Hierarchical Account Mapping

This project provides an automated ETL pipeline for extracting, normalizing, and categorizing enterprise contract data across a **6-year historical lookback**. By resolving complex Salesforce account hierarchies and applying a priority-based "Exclusion Sieve," the system generates high-integrity marketing lists for regional distribution.

---

## 🏗️ System Architecture & Logic Flow
The following diagrams illustrate the automated logic, data flow, and structural models used in this pipeline.

### 1. Functional Process Flow
This chart illustrates the end-to-end technical journey from raw Salesforce extraction to automated regional delivery.

```mermaid
graph TD
    %% Source Extraction
    subgraph "1. Data Acquisition & Schema Mapping"
    A1[(Salesforce CRM)] -- "Product Line 1" --> B1[Dataset 1]
    A2[(Salesforce CRM)] -- "Product Line 2" --> B2[Dataset 2]
    B1 & B2 --> C[<b>Standardized Master Data</b><br/>6-Year Lookback]
    end

    %% The Technical Solve
    subgraph "2. Hierarchy & Account Consolidation"
    C --> D[<b>Ultimate Parent Rollup</b><br/>Great-Grandparent Resolution]
    D --> E[<b>Account Key Generation</b><br/>Consolidate all sub-contracts]
    end

    %% The Core Exclusion Logic
    subgraph "3. The Account-First Exclusion Sieve"
    E --> F{Priority 1:<br/>Account Active?}
    F -- "Yes" --> G[<b>Bucket: ACTIVE</b>]
    G --> H[Flag Account as 'Processed']

    F -- "No / Not Processed" --> I{Priority 2:<br/>Expiring Soon?}
    I -- "Yes" --> J[<b>Bucket: EXPIRING SOON</b>]
    J --> K[Flag Account as 'Processed']

    I -- "No / Not Processed" --> L{Priority 3:<br/>Truly Expired?}
    L -- "Yes" --> M[<b>Bucket: TRULY EXPIRED</b>]
    end

    %% Final Output
    subgraph "4. Contact Enrichment & Distribution"
    H & K & M --> N[<b>Contact Pull</b><br/>Primary + Signer Merge]
    N --> O[<b>Deduplication</b><br/>Unique Contact x Unique Bucket]
    O --> P[Region-based <br>Manager-Specific CSVs]
    P --> Q[(Google Drive Upload)]
    end

    %% Styling
    style G fill:#dfd,stroke:#28a745,stroke-width:2px
    style J fill:#fff9c4,stroke:#fbc02d,stroke-width:2px
    style M fill:#ffebee,stroke:#d32f2f,stroke-width:2px
    style F fill:#e1f5fe,stroke:#01579b
    style I fill:#e1f5fe,stroke:#01579b
```

### 2. Data Volume Flow (Sankey)
Visualizing how the master pool resolves into non-overlapping stakeholder pools.

```mermaid
sankey-beta

%% Nodes and Flow: Source, Target, Value
Salesforce_Master_Pool, Hierarchy_Engine, 1800
Hierarchy_Engine, ACTIVE_Bucket, 450
Hierarchy_Engine, EXPIRING_SOON_Bucket, 150
Hierarchy_Engine, TRULY_EXPIRED_Bucket, 1200
```

### 3. Class Hierarchy & Data Model (PlantUML)
Detailed mapping of the relationship traversal from child contracts to the Ultimate Parent level.

![Account Hierarchy UML](https://www.plantuml.com/plantuml/png/TOv1YzH048Nl_IkUSnmOPVUuZ67NC4P1CAok5zr3cLIIOYlTeRko6iJ_RYUEiY1Ukk5zhzvxryaesZogIm_Y9ueqOY3VVejYnXuTQU8dRABcWNh-O8io8ZVct5d2hWnn2f6CyKOuKco6POSV3lXSHIOxL347vnZsXjLxZ-FnJat6zQJUzA809LJLUlJKVikz17-_mPNLVrB6YVoowVMgbuDeY_TT9mtZPjFBYt_0gz_WqlrqpWTZHEa7G-XoCwxmBlJIO9fL4reo-kBlQbY03PAW_CZgN7c1mw50dUsdxvD4RlCORv4QS-Nb_rczeSfLsx_LxVStZSaZ_pNXTPXz-so_TqwvPzywuDXbY2PeY2zpO77BQLQxEhvOzG8dRxa77OsY2upwFfTIMhFBZsy_dN8MKCUytLl2xZnh1nv9DC42D2oaIFFN9ArG54xFNQu-3xZEppoUF_q5)

---

## 🚀 The Core Challenge: Hierarchy Fragmentation
In large-scale CRM environments, contracts often exist at various subsidiary levels. A "Child Account" may appear expired, while the "Ultimate Parent" remains active. 
* **The Risk:** Sending re-acquisition offers to active corporate clients ("False Churn").
* **The Solution:** A recursive hierarchy rollup that identifies the relationship status at the highest corporate level before bucket assignment.

## 🛠️ Key Technical Achievements

### 1. Recursive Hierarchy Resolution
To ensure data integrity, the pipeline traverses four levels of the Salesforce account object hierarchy (`Account.Parent.Parent.Parent.Name`). This allows the script to consolidate all transactional history under a single **Ultimate Parent** ID, ensuring the categorization reflects the total business relationship rather than a single siloed contract.

### 2. The "Account-First" Exclusion Engine
Unlike simple row-filtering, this logic treats the **Account** as the primary unit of measure.
* If an account holds *any* active contract, the account key is locked into the **Active** bucket.
* This "processed" flag prevents the account from appearing in lower-priority pools (Expiring or Expired), protecting the brand's professional image.

### 3. Automated Stakeholder Enrichment
The engine dynamically extracts and merges contacts from multiple roles:
* **Primary Contacts:** Operational stakeholders and follow-up leads.
* **Contract Signers:** Key decision-makers and financial signatories.
* **Deduplication:** A custom merging strategy ensures that unique individuals are contacted only once.

## 💻 Tech Stack
* **Python:** Core data processing and exclusion logic.
* **Pandas:** High-performance data manipulation and cross-object merging.
* **Simple-Salesforce:** SOQL query execution and CRM API integration.
* **Google Drive API:** Automated delivery and regional file categorization.

---

## 📈 Impact
By moving from manual list-pulling to an automated Python pipeline, the project reduced data preparation time by ~90% and eliminated the risk of brand-damaging "false churn" communications to top-tier enterprise clients.

# Predicting Hospital Readmission Risk



Hospitals face financial penalties when patients are readmitted within 30 days for the same condition, making it critical to identify high-risk patients early. This project leverages **Microsoft Fabric** to integrate patient bio data, visitation history, lab results, and admission cost, and applies a machine learning model to predict 30-day readmission risk.

## Prerequisite

- Azure account
- Fabrics setup. For the free trial follow [this](https://www.youtube.com/watch?v=RHV7jZqc_tE)
- Microsoft tenant/ work email.
- [Medalllion lakehouse architecture](https://learn.microsoft.com/en-us/azure/databricks/lakehouse/medallion)

- Pyspark
- scikit-learn, MLflow


## Data Overview

The project uses a synthetic dataset to simulate a typical hospital scenario. Patient info is stored in an **Azure SQL Database**, visitation data and admission cost details are stored as flat files in **ADLS Gen2**, and lab results are stored in a **Fabric workspace**. All data is accessed from these sources and ingested into a Fabric lakehouse for further processing.

## Data Pipeline Overview

This architecture follows the medallion approach to prepare data for machine learning within Fabric. Data from different sources are landed into the Bronze layer in their raw states. In the Silver layer, the data is cleaned and refined by filtering to inpatient events and joining with patients, labs, and cost tables. The Gold layer is then used to derive a 30-day readmission flag, which serves as the target variable for modeling. From there, notebooks are used to train models on the Gold dataset, with multiple experiments tracked and compared using MLflow. The best-performing model is saved in the Model Registry, where it is versioned and governed. Once registered, the model is used for batch predictions, allowing consistent scoring of new data that supports analytics and decision-making.

![alt text](/images/pipeline-overview.png)

## Data Ingestion

Patients → Pulled from Azure SQL DB using data pipeline → landed raw in **Bronze**.

Encounters & Costs → Flat files in **ADLS Gen2**, accessed via Fabric shortcut → landed in Bronze.

Lab Results → From another **Fabric workspace**, accessed via shortcut → landed in Bronze.

All data is ingested as-is into the Bronze layer before cleaning and integration in Silver.

## Data Transformation

**Silver Layer (Cleaning & Integration)**

- Patients, Encounters, Costs, and Labs joined on PatientID / AdmissionID.

- Standardized schemas (data types, column names).

- Derived fields like LengthOfStayDays.

- Filtered to inpatient encounters only.

- Missing values handled (e.g., funding type → "Unknown").

[Transform to Silver Notebook](https://github.com/adekolaolat/fabric-hospital-readmission-risk-ml/blob/main/notebooks/Transform%20to%20Silver.ipynb)

**Gold Layer (derive features for ML)**

- Split BloodPressure into SystolicBP / DiastolicBP.

Derived features:

- Past admissions.
- Average past length of stay.
- Added Readmission flag (30 days) as the target variable.

Combined clinical + demographic + cost data into a single Delta table ready for training.
[Tranform to Gold](https://github.com/adekolaolat/fabric-hospital-readmission-risk-ml/blob/main/notebooks/Transform%20to%20Gold.ipynb)
## Machine Learning Workflow

1. **Data Preparation**

Load the  gold table with patient demographics, encounters, labs, and costs.

2. **Feature Engineering**

Categorical features (`Gender, ChronicCondition, Procedure, Diagnosis, Specialty, FundingType, Department`) encoded with OneHotEncoder.

Numeric features (`Age`, `ClaimAmount`, `InNetwork`, `GlucoseLevel`, `Cholesterol`, `BMI`, `SystolicBP`, `DiastolicBP`, etc.) kept as is.

Combined using ColumnTransformer.

3. **Model Training**

Trained and evaluated multiple classifiers:

- **Logistic Regression**

- **Random Forest Classifier**

- **XGBoost Classifier**

Target: `ReadmittedWithin30Days` flag.



4. **Experiment Tracking with MLflow**

- Logged parameters (features, classifier type) and metrics (accuracy).

- Stored models and artifacts for reproducibility.

- Compared performance across classifiers (Logistic Regression vs Random Forest vs XGBoost) and **registered the best model** in **Fabric**.

[Training Notebook](https://github.com/adekolaolat/fabric-hospital-readmission-risk-ml/blob/main/notebooks/Training_notebook.ipynb)

1. **Output**

Generated a reproducible, MLflow-tracked model to predict 30-day hospital readmission risk.

Workflow supports batch scoring on new admissions data in Fabric.

## Hospital Readmission Risk Scoring

- **Input:** ML-ready gold dataset `hosp_training_data` with patient, lab, and encounter features.  
- **Model:** MLflow-trained `reAdmissionRisk-model` (version 1).  
- **Process:** Apply model using `MLFlowTransformer` to generate predictions.  
- **Output:** Add `AdmissionRisk` column (`Low Risk` / `High Risk`) and save as `predicted_table` in Gold Lakehouse.  
- **Purpose:** Enable batch scoring for hospital readmission risk in Fabric.

[Scoring Notebook](https://github.com/adekolaolat/fabric-hospital-readmission-risk-ml/blob/main/notebooks/Predict_Admission_Risk%20Notebook.ipynb)

## Outcome
 
This project has leveraged Fabric's capabilities for handling ML workloads to develop a predictive model that identifies patients at risk of 30-day hospital readmission. By integrating patients, visitation history, lab results, and cost of admission data, the model can predict patients' risk of being readmitted. The workflow utilized Fabric for tracking experiments during training and deploying the model for batch  which achieved an accuracy of 90%.




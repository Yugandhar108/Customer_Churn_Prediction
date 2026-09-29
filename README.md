# Leo Telecom Customer Churn Prediction

A phased Jupyter-based project to inspect customer data, explore churn patterns, train churn classifiers with TensorFlow/Keras, and translate model findings into retention recommendations.

## Current status

- **Phase 1: Environment setup and data loading**: implemented in `notebooks/phase_1_data_loading.ipynb`.
- **Phase 2: Pandas filtering and subgroup extraction**: implemented and exercised on the 205-row synthetic demo dataset.
- **Phase 3: Churn and internet-service visualizations**: implemented and exercised on the 205-row synthetic demo dataset.
- **Phase 4: Baseline, dropout, and multi-feature models**: all three models trained for 150 epochs on the synthetic demo dataset.
- **Phase 5: Evaluation, comparison, and recommendations**: comparison workflow executed on synthetic demo results; real findings await the full approved dataset.

Each phase will be reviewed before the next phase begins.

## Project layout

```text
Customer_Churn_Prediction/
|-- Input/                         # Supplied project brief, PDF, and data dictionary
|-- data/
|   `-- raw/                       # Demo/customer_churn.csv; replace with approved source data
|-- notebooks/
|   `-- phase_1_data_loading.ipynb # Phase 1 data loading and inspection notebook
|-- scripts/
|   `-- generate_synthetic_demo_data.py # Rebuild 200 synthetic rows for pipeline testing
|-- README.md
|-- Wiki.html
`-- requirements.txt
```

## Prerequisites

- Python 3.10 or later. TensorFlow availability depends on the Python version and operating system; use a TensorFlow-supported Python version if installation fails.
- VS Code with the Python extension, or JupyterLab.
- The complete approved customer dataset for meaningful evaluation. The CSV currently present is a synthetic demo, not the source dataset.

## Setup

From this project folder, create and activate a virtual environment, then install dependencies:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

On macOS/Linux, activate with `source .venv/bin/activate` instead.

Copy the dataset to:

```text
data/raw/customer_churn.csv
```

The current `customer_churn.csv` contains 205 rows: the five screenshot rows plus 200 generated demo rows. Some fields hidden in the screenshot were assumed. Synthetic churn labels are deliberately associated with generated tenure ranges so the model-fitting path can be exercised. The resulting metrics are not representative and must not be used for business conclusions.

To recreate the deterministic demo extension while preserving the original five rows, run:
The generator replaces its existing `SYNTH-` rows on rerun, so it does not keep appending duplicates. Replace the demo CSV with the full approved dataset before real model evaluation.

Open `notebooks/phase_1_data_loading.ipynb` in VS Code or JupyterLab and run its cells from top to bottom. The notebook reports the expected location if the CSV is missing and does not generate data automatically. The separate demo generator creates synthetic rows only when explicitly run; do not use its output for business conclusions.

## Phase 1 data checks

The workflow loads the CSV with Pandas, checks for columns needed by the planned tasks, prints the shape and sample rows, reports dtypes and missing values, and converts `TotalCharges` to numeric. Blank and invalid `TotalCharges` entries are reported separately.

Required columns: `gender`, `SeniorCitizen`, `InternetService`, `PaymentMethod`, `tenure`, `MonthlyCharges`, `TotalCharges`, and `Churn`.

The supplied data dictionary also describes `customerID` and additional service/account fields. `Churn` is documented as binary (`1`/`0`); Phase 4 also accepts `No`/`Yes` and maps them to `0`/`1`. Treat `customerID` as an identifier, not a predictive feature.

## Phase 4 model workflow

The notebook creates one reproducible stratified 80/20 split shared by all three models and standardizes features using training data only. It trains the `tenure` baseline, `tenure` with dropout rates 0.3 and 0.2, and a model using `tenure`, `MonthlyCharges`, and `TotalCharges`. Each uses 12- and 8-unit ReLU dense layers, a sigmoid output, Adam, binary cross-entropy, and 150 epochs. Outputs include test confusion matrices and training-accuracy plots. Training is skipped if the data cannot support the stratified split.

## Phase 5 evaluation workflow

When Phase 4 has results for all three models, the notebook compares shared-test-set accuracy, churn precision, churn recall, and F1. It reports accuracy changes for dropout and the additional features and identifies the highest-recall model as a candidate for further validation. On the synthetic demo data these outputs verify the pipeline only; actual recommendations require training and evaluation on the full approved dataset.

## Source material
For functional and technical guidance, FAQs, and troubleshooting, see [Wiki.html](Wiki.html).

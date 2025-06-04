# CPT Soil Classification Example

This project demonstrates a small machine learning pipeline to classify soil types from Cone Penetration Test (CPT) data. It is intended to run locally from VS Code or any terminal.

## Setup

1. Install **Python 3.9** or later.
2. Clone this repository and open the folder in VS Code.
3. Create a virtual environment and install the dependencies:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
pip install -r requirements.txt
```

## Workflow

1. **Generate data** *(optional)*

   ```bash
   python src/generate_data.py
   ```

   This creates `data/raw/generated_cpt_data.csv` with synthetic CPT profiles. If `data/raw/generated_cpt_data.csv` already exists, the preprocessing step will reuse it.

2. **Preprocess**

   ```bash
   python src/preprocess.py
   ```

   The script reads `report.docx` and `excel.xlsx` from `C:\Users\ismai\OneDrive - The University of Manchester\Desktop\Summer`.
   It generates an expanded CPT table with 0.01&nbsp;m depth increments and saves engineered features to `data/processed/cpt_features.csv`.

3. **Train model**

   ```bash
   python src/train.py
   ```

   A Random Forest classifier is trained and stored in `model_outputs/`.

### Full local workflow

1. Place `report.docx` and `excel.xlsx` in the path above.
2. Run `python src/preprocess.py` to build the dataset and feature file.
3. Run `python src/train.py` to fit the classifier.

All steps can be executed inside the VS Code terminal without internet access once the dependencies are installed.

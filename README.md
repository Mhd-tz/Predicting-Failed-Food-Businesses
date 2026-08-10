# Predicting Failed Food Businesses

IAT 461 final project, Summer 2026  
Student: Mahdi Taziki (301373483)  
Client: Jason Salonga, Greater Vancouver Food Bank

The goal of this project is to predict which Vancouver food businesses are more likely to fail, so the
Greater Vancouver Food Bank can decide which businesses may need support. The planned final output is a
list ranked by predicted risk.

## Status

This is the August 9 checkpoint submission.

- [`notebooks/01_EDA.ipynb`](notebooks/01_EDA.ipynb) is finished. It covers data quality, the target
  variable, a data leakage check, and the feature plan, with its progress report as Section 12.
- [`notebooks/02_Modeling.ipynb`](notebooks/02_Modeling.ipynb) is a **draft**. The code runs and the
  outputs are saved, but the models have not been tuned and several conclusions still need checking.
  Section 9 lists what is left to do before the final delivery on August 11.
- [`DRAFT_NOTEBOOK_AUG_09.md`](DRAFT_NOTEBOOK_AUG_09.md) describes what changed since the EDA.

## Draft results so far

I compared logistic regression and a random forest against two baselines with 5-fold cross-validation
repeated 10 times, using Average Precision (AP) instead of accuracy because the output is a ranked list
and only 23.3% of the businesses have a failure status. Logistic regression averaged an AP of 0.375 and
the random forest 0.385, against 0.233 for a ranking in random order. The two averages are close, and
this analysis does not show that one model is better than the other.

The main limitations: 219 rows and 51 positives after cleaning, an unconfirmed label definition, a
ranking analysis based on one out-of-fold split, and no tuning yet.

## Dataset

The data comes from the City of Vancouver Business Licences open dataset and covers food-related
businesses such as restaurants, food retailers, wholesalers, markets, and manufacturers. The filtered
CSV is in this repository; the larger raw city export is not. `make_foodbank_dataset.py` is the script
that produced the filtered file, kept here as a record of how it was made rather than as a step you
need to run.

## Files

```
notebooks/01_EDA.ipynb                 exploratory analysis and EDA progress report
notebooks/02_Modeling.ipynb            modelling draft
figures/                               figures saved by the notebooks
vancouver_food_businesses_sample.csv   the working dataset, 221 rows and 12 columns
make_foodbank_dataset.py               script used to filter the raw city export
DRAFT_NOTEBOOK_AUG_09.md               August 9 draft progress report
Phase1_ClientProposal.pdf              client proposal
Phase2_ClientProposal.pdf              client and data scientist agreement
```

## Running the notebooks

```bash
pip install -r requirements.txt
cd notebooks
jupyter lab
```

Both notebooks are written to be run from the `notebooks` folder. They read
`../vancouver_food_businesses_sample.csv` and save figures to `../figures/`. Open a notebook and use
Kernel > Restart Kernel and Run All Cells. The modelling notebook takes a couple of minutes because of
the repeated cross-validation, and its random seed is set to 461.

# Predicting Failed Food Businesses

IAT 461 final project, Summer 2026  
Student: Mahdi Taziki (301373483)  
Client: Jason Salonga, Greater Vancouver Food Bank

The goal of this project is to predict which Vancouver food businesses are more likely to fail. The
Greater Vancouver Food Bank could use the results to decide which businesses may need support. The
planned final output is a list of businesses ranked by predicted risk.

## Current progress

The exploratory data analysis is finished. The notebook contains the code, figures, and findings, and
the progress report is included both inside it and as a separate file:

- [EDA notebook](notebooks/01_EDA.ipynb), with the progress report as Section 12
- [Progress report](PROGRESS_REPORT.md)

The main findings so far are:

- The dataset has 221 rows and 12 original columns.
- The definition of a failed business has a large effect on the class balance. The original definition
  gives 20 failed businesses, while the broader definition gives 53.
- Missing values in `issueddate` and `expireddate` are closely connected to business status. These
  columns could leak the answer to a model, so I will not use them as predictors.
- Two licence numbers appear more than once. I plan to keep the latest record for each licence before
  modelling.
- Business type appears to be the most useful predictor in the current dataset. Neighbourhood and
  number of employees may also be useful, but none of the relationships are very strong by themselves.

## Dataset

The data comes from the City of Vancouver Business Licences open dataset. The working file contains
food-related businesses such as restaurants, food retailers, wholesalers, markets, and manufacturers.
The filtered CSV is included in this repository. The larger raw City of Vancouver export is not
included.

`make_foodbank_dataset.py` is the script that produced the filtered file. It reads the raw city export
and keeps only the food business types. Because the raw export is not in this repository, the script
is included as a record of how the working file was created rather than as a step you need to run.

## Files

```
notebooks/01_EDA.ipynb                 exploratory analysis and progress report
figures/                               figures saved by the notebook
vancouver_food_businesses_sample.csv   the working dataset, 221 rows and 12 columns
make_foodbank_dataset.py               script used to filter the raw city export
PROGRESS_REPORT.md                     progress report on its own
Phase1_ClientProposal.pdf              client proposal
Phase2_ClientProposal.pdf              client and data scientist agreement
```

## Running the notebook

```bash
pip install -r requirements.txt
jupyter lab notebooks/01_EDA.ipynb
```

Then use Kernel > Restart Kernel and Run All Cells. File paths are worked out from the repository
root, so the notebook runs whether it is started from the root folder or from `notebooks/`. The random
seed is fixed at 461.

## Next steps

I will confirm the label definition with the client, write the cleaning and deduplication steps, and
build a baseline classification model to compare against a random forest. Evaluation will use
precision near the top of the ranked list, recall, and PR-AUC rather than accuracy alone.

Three questions are still open with the client:

1. Should a `Pending` status count as a failed business? It may only mean the city has not finished
   processing the application. My current recommendation is to leave these records out of training
   until this is confirmed.
2. How was the 63% baseline in the Phase 2 agreement calculated? Predicting the majority class gives
   91% with the narrow label and 76% with the broader one.
3. How many businesses can the coordinator contact each week? This number decides where the cutoff on
   the ranked list should be.

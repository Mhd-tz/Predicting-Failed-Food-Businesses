# Predicting Failed Food Businesses

IAT 461 final project, Summer 2026
Data scientist: Mahdi Taziki (301373483)
Client: Jason Salonga (301400669), Greater Vancouver Food Bank

This project looks at whether information in Vancouver business licence records can help rank food
businesses for support. The final output is a trial contact list of businesses with an `Issued`
licence, ordered by how similar they are to records in the failure group.

## Submission links

- **Final notebook:** [`notebooks/03_Final_Model.ipynb`](notebooks/03_Final_Model.ipynb)
- **Ranked list:** [`outputs/ranked_contact_list.csv`](outputs/ranked_contact_list.csv)

The notebook and app code are complete. The app link still needs to be added after deployment.

## Project files

- [`notebooks/01_EDA.ipynb`](notebooks/01_EDA.ipynb) contains the exploratory analysis submitted for
  the first checkpoint.
- [`notebooks/02_Modeling.ipynb`](notebooks/02_Modeling.ipynb) contains the August 9 draft model
  comparison.
- [`notebooks/03_Final_Model.ipynb`](notebooks/03_Final_Model.ipynb) is the final notebook. It contains
  the problem restatement, EDA summary, method choice, assumptions log, model evaluation, contact list,
  limitations, executive summary, and submission links.
- [`CLIENT_SUMMARY.md`](CLIENT_SUMMARY.md) explains the result for the client in plain language.
- [`FINAL_REPORT_AUG_11.md`](FINAL_REPORT_AUG_11.md) records the work completed after the draft.
- [`streamlit_app.py`](streamlit_app.py) is the interactive version of the contact list.

## Decisions from the client check-in

The Phase 1 proposal defines failure as `Cancelled` or `Gone Out of Business`. In an August 9
follow-up, the client confirmed that `Pending` and `Inactive` should also count because he treats both
as cases where the business became unresponsive. I used this broader label in the final model and also
tested three stricter versions. Jason's answer sets the label for this project, but the licence data
does not prove that every record in this group was an actual business failure.

The client also said the coordinator should contact around 10 businesses per week. I used 10 for the
schedule and the precision@10 evaluation. The schedule can be changed by editing
`CONTACTS_PER_WEEK` in the final notebook and app if the coordinator's capacity changes.

## Results

After removing two duplicate licence records, the modelling data has 219 records. The broader label
marks 51 records, or 23.3%, with a failure status. I used Average Precision (AP) because the client
wants a ranking and the classes are uneven.

With 5-fold cross-validation repeated 10 times, the random forest reached an AP of 0.385 and logistic
regression reached 0.375. The random-order baseline is 0.233. Nested tuning did not improve either
model, so I kept the original settings.

In 25 repeated cross-validated rankings, the random forest's mean precision@10 was 0.292. This means
that the top 10 validation records contained an average of 2.9 records already marked with a failure
status, compared with 2.3 under random ordering. It does not mean that 2.9 of the currently issued
businesses will later fail. The dataset is a single snapshot and has no future outcomes for the
businesses in the delivered list.

The final model is the random forest requested in the Phase 2 agreement. It was fitted on all 219
records and used to score the 168 records whose current status is `Issued`. Because those 168 records
were also training examples, their scores are in-sample. The CSV is therefore a trial contact list,
not a validated forecast or a list of failure probabilities.

## Main limitations

The dataset is small, uses only business type, neighbourhood, and employee count, and represents one
point in time. The raw scores are not calibrated probabilities. Multi-year licence data with known
future outcomes would be needed to test whether the ranking identifies currently open businesses that
later close.

## Repository contents

```
notebooks/01_EDA.ipynb                 EDA checkpoint
notebooks/02_Modeling.ipynb            August 9 modelling draft
notebooks/03_Final_Model.ipynb         final analysis and ranked-list generation
outputs/ranked_contact_list.csv        trial contact list of 168 issued businesses
streamlit_app.py                       interactive app
figures/                               figures saved by the notebooks
vancouver_food_businesses_sample.csv   working dataset, 221 rows and 12 columns
make_foodbank_dataset.py               script used to make the filtered dataset
CLIENT_SUMMARY.md                      client-facing explanation
FINAL_REPORT_AUG_11.md                 final progress report
DRAFT_NOTEBOOK_AUG_09.md               August 9 progress report
Phase1_ClientProposal.pdf              client proposal
Phase2_ClientProposal.pdf              client and data scientist agreement
ASSIGNMENT_README.md                   course assignment brief
```

## Running the project

Install the packages from the repository root:

```bash
pip install -r requirements.txt
```

Run the notebooks from the `notebooks` folder:

```bash
cd notebooks
jupyter lab
```

The final notebook reads `../vancouver_food_businesses_sample.csv`, saves figures to `../figures/`,
and writes `../outputs/ranked_contact_list.csv`. It uses the fixed seed 461 and takes a few minutes
because of repeated cross-validation.

Run the app from the repository root:

```bash
streamlit run streamlit_app.py
```

The app fits the same random forest when it starts, so no separate model file is required.

# Final Progress Report

**Project:** Predicting Failed Food Businesses
**Student:** Mahdi Taziki (301373483)
**Client:** Jason Salonga, Greater Vancouver Food Bank
**Course:** IAT 461, Summer 2026
**Date:** August 11, 2026

## Work completed after the August 9 draft

The August 9 submission compared logistic regression with a random forest and left the final checks
unfinished. Since then, I tested different failure labels, ran nested hyperparameter tuning, repeated
the precision-at-k evaluation, checked calibration, completed the agreed 80/20 held-out check, and
created the ranked CSV and Streamlit app. The full analysis is in
[`notebooks/03_Final_Model.ipynb`](notebooks/03_Final_Model.ipynb).

I also corrected my reading of the 63% baseline mentioned in the Phase 2 agreement. That baseline is
in the section about the separate Aquila project, not this food-business project, so it is not used
here.

## Client decisions used in the final analysis

The Phase 1 proposal counts `Cancelled` and `Gone Out of Business` as failures. In an August 9
follow-up, the client confirmed that `Pending` and `Inactive` should also count because he considers
both to be cases where the business became unresponsive. I used this broader label in the final model.
This gives the project a clear label, but the licence data does not prove that every record in this
group was an actual business failure.

The client also confirmed that the coordinator should contact around 10 businesses per week. I used
10 to build the contact schedule and to report precision@10. I have not tested whether 10 is the best
cutoff for future outcomes because the dataset does not include them.

## Label sensitivity

I compared four definitions such as the broader label Jason confirmed, the same data with the 26 `Pending` records
removed, the original narrow label, and `Cancelled` alone. Their class rates differ, so I compared AP
as a multiple of each definition's random baseline.

The random forest reached 1.65 times the random baseline with the broad label, 1.76 times when
`Pending` records were removed, 2.03 times with the narrow label, and 2.08 times with `Cancelled`
alone. The stricter labels contain fewer positive examples and have more variation across folds. These
results suggest that the ranking signal is not entirely produced by the `Pending` records. They still
do not prove that every `Pending` record represents an actual business failure.

## Model tuning and selection

I ran grid searches inside nested cross-validation so that the outer folds evaluated data that had not
been used to choose settings. On the same outer folds, the untuned AP scores were 0.384 for logistic
regression and 0.385 for the random forest. The tuned nested scores were 0.362 and 0.368. These
differences are small compared with the variation across folds, so I found no evidence that tuning
helped. I kept the untuned settings.

The random forest is the final model because that is the model requested in the Phase 2 agreement. It
also had slightly higher mean scores than logistic regression, although the differences were too small
to show that it is reliably better. Logistic regression remains useful as an easier model to explain.

## Ranking evaluation

I rebuilt the out-of-fold ranking 25 times with different splits. At k = 10, logistic regression had a
mean precision of 0.280 and the random forest had 0.292. The random-order baseline was 0.233. In other
words, the top 10 validation records contained an average of about 2.8 to 2.9 records with a failure
status, compared with 2.3 under random ordering.

The result varied considerably. Precision@10 ranged from 0.10 to 0.40 for logistic regression and
from 0.10 to 0.50 for the forest. The models beat the base rate in 64% and 60% of the repeated splits.
At k = 30, both models beat the base rate in 96% of the splits.

This evaluation ranks all 219 historical records, including records that already have a failure
status. It does not test whether issued businesses in the contact list later fail. The precision@10
result therefore describes how well the model recognizes status patterns in this dataset, not how many
future closures the coordinator should expect from 10 calls.

## Calibration and held-out check

The model scores should not be read as probabilities. The forest's mean out-of-fold score was 0.402
while the observed failure-status rate was 0.233. Balanced class weights help the model rank the
minority class but make the raw scores too high for probability interpretation. The CSV includes a
rank and band so the coordinator does not have to interpret the score as a chance of closure.

The 80/20 held-out check used 44 records with 10 positives. Untuned AP was 0.562 for logistic
regression and 0.581 for the forest. These values are higher than the repeated cross-validation
results, but the test set is too small for that difference to be convincing. I use the repeated
cross-validation results as the main evaluation.

## Deliverable

The final random forest was fitted on all 219 records and used to score the 168 businesses whose
current licence status is `Issued`. The output is
[`outputs/ranked_contact_list.csv`](outputs/ranked_contact_list.csv). It includes the licence number,
business name, type, neighbourhood, employee count, score, rank, band, and a contact week.

The top 30 records form the high band because the repeated validation was more stable at k = 30 than
at k = 10. This is an organizational choice, not proof that the top 30 issued businesses will fail.
The issued records were part of the training data as negatives, so their final scores are in-sample.

The Streamlit app lets the user filter the nine delivered columns, download the filtered view, and
compare a hypothetical business with the current list. Its reliability page explains that the model is
cross-sectional and that its scores are not probabilities.

## Limitations and next step

The cleaned dataset contains only 219 records and 51 positives under the broader label. The model uses
only business type, neighbourhood, and number of employees. It cannot see revenue, rent, debt,
ownership changes, business age, or previous contact with the food bank. The rare-category cutoffs
were also chosen from the full dataset during EDA, which makes the validation slightly optimistic.

The largest limitation is time. This is a snapshot of current licence statuses, not a dataset showing
which businesses were open at one date and failed later. I would next get records from several years,
define a future outcome such as "open this year and closed next year," and test the model on a later
time period. Until then, the contact list should be treated as a trial list based on similarity, and
the results of real contacts should be recorded.

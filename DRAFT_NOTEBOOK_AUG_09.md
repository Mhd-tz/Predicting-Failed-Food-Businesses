# Progress Report

**Project:** Predicting Failed Food Businesses  
**Student:** Mahdi Taziki (301373483)  
**Client:** Jason Salonga, Greater Vancouver Food Bank  
**Course:** IAT 461, Summer 2026  
**Stage:** August 9 checkpoint, draft submission

## Where the project is (August 9)

The exploratory data analysis is finished and the modelling notebook is a draft. The full EDA write-up is Section 12 of [the EDA notebook](notebooks/01_EDA.ipynb),
and the modelling is in [the modelling notebook](notebooks/02_Modeling.ipynb).

## Short summary of the EDA

The dataset is a filtered sample of the City of Vancouver Business Licences open data, with 221 rows and
12 columns. Three findings shaped the modelling. Missing values in `issueddate` and `expireddate`
almost exactly identify `Pending` and `Cancelled` records, so those columns would leak the answer and I
dropped them. Two licence numbers appear twice with different statuses, so I keep only the most recent
record for each. And the label definition matters: the narrow definition (`Cancelled`,
`Gone Out of Business`) gives 20 failures, while the wide one, which also counts `Pending` and
`Inactive`, gives 53. The features I carried forward are business type, neighbourhood, and number of
employees.

## What I did since the EDA

I put the cleaning decisions into a single function, which leaves 219 rows with 51 failures under the
wide label. I used the wide label for the draft because it is the definition in the Phase 2 agreement
and because the narrow label leaves only about four failures per fold, which would make model
comparisons much less stable. This is a practical choice for the draft, not an answer to the label
question.

I then built two pipelines and compared them against two baselines. Logistic regression gets `log1p` on
the employee count followed by scaling, since that column is very skewed. The random forest gets the raw
count, because trees split on the order of values. One-hot encoding and the numeric transformation are
fitted inside each fold. The category grouping thresholds are not; they were chosen during the EDA and
are applied first as fixed cleaning rules, which is a limitation I note in the notebook.

Because the dataset is small, I did not rely on one train and test split. I used 5-fold stratified
cross-validation repeated 10 times, giving 50 fold scores per model, and I report Average Precision
(AP) rather than accuracy. A ranking in random order has an expected AP equal to the positive rate,
which is 0.233.

## Results

Logistic regression averaged an AP of 0.375 and the random forest 0.385. Both are above 0.233, so the
three predictors carry some signal. The averages are close and this analysis does not show that either
model is better. The standard deviations across folds are 0.066 and 0.084, which describe how much each
model moves from fold to fold. I have not run a test of whether the two models actually differ.

The majority-class baseline reaches 76.7% accuracy with 0 recall and 0 precision because it never
predicts a failure. This shows why accuracy alone is not useful for this project.

I also produced one out-of-fold ranking of all 219 businesses. In it, logistic regression has 4 of the
top 10 and 7 of the top 20, and the random forest has 2 of the top 10 and 11 of the top 30. Both sit
above the 23.3% base rate at most values of k, but the values move around a lot at small k and this is a
single split, so I am not choosing a cutoff from it yet.

For feature importance I used cross-validated permutation importance, fitting a fresh forest on each
training fold and permuting the validation fold. Business type has the largest positive mean drop in
AP, at about 0.06. Employee count is near zero, neighbourhood is slightly negative, and the
fold-to-fold variation is large relative to the mean values. I therefore cannot confidently rank the
three predictors from this result.

Sorting the ranking by status shows `Cancelled` businesses higher than the rest (median rank 52 of 219)
and `Pending` at 81, while `Gone Out of Business` and `Inactive` sit near or below the middle. This is
worth following up, but there are only 2 `Gone Out of Business` and 5 `Inactive` records after cleaning,
so the sample is much too small to conclude anything about those groups.

## Limitations

The dataset has 219 rows and 51 positives, so all of these numbers carry a lot of uncertainty. The label
definition is not settled, the ranking analysis rests on one out-of-fold split, two of the status groups
are tiny, and neither model has been tuned. The model is also cross-sectional: it learns which kinds of
businesses currently have failure statuses, not what happens to a business over time.

## Remaining work before August 11

- Label sensitivity: rerun with `Pending` excluded, with the narrow label, and with a `Cancelled`-only
  label
- Tune both models inside the cross-validation
- Repeat the ranking analysis over several splits before considering a cutoff
- One held-out evaluation as a final check
- Check calibration of the predicted probabilities
- Choose a final model and record the reason
- Build the contact list from one fitted model, excluding businesses that are already closed
- Short plain-language summary for the client

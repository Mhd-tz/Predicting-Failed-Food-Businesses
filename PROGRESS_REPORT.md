# Progress Report

**Project:** Predicting Failed Food Businesses  
**Student:** Mahdi Taziki (301373483)  
**Client:** Jason Salonga, Greater Vancouver Food Bank  
**Course:** IAT 461, Summer 2026

## Current stage

I have completed the initial exploratory data analysis for the project. The dataset is a filtered
sample of the City of Vancouver Business Licences open data. It contains 221 rows and 12 original
columns. The sample focuses on food-related businesses, including restaurants, food retailers,
wholesalers, markets, and manufacturers.

In the EDA notebook, I checked the structure of the dataset, missing values, duplicate records, the
distribution of the target variable, and the relationships between the possible predictors and
business failure. I also reviewed each column to decide whether it should be used in the modelling
stage.

## Main findings

The first important issue is the definition of a failed business. In the Phase 1 proposal, a business
was counted as failed if its status was `Cancelled` or `Gone Out of Business`. This gives 20 failed
businesses out of 221, or 9.0%. A broader definition discussed in Phase 2 also includes `Pending` and
`Inactive`. That definition gives 53 failed businesses, or 24.0%. I kept both versions in the notebook
because this decision changes the class balance and will affect the model results.

The second issue is possible data leakage. About 22% of the values in `issueddate` and `expireddate`
are missing. The missing values almost perfectly identify records with a `Pending` or `Cancelled`
status. This means a model could appear very accurate by learning the way the licence records are
completed rather than learning which businesses are likely to fail. For this reason, I plan to remove
both date columns from the predictors and not create missing-value flags for them. This is a change
from the Phase 2 agreement, where the plan was to keep `issueddate` and add a flag for the blank
values. That flag is the part that leaks, so I will explain the result to the client before the
modelling stage.

I also found two licence numbers that appear twice. In each case, the records have different statuses.
This could place two versions of the same licence in both the training and test data. Before modelling,
I plan to deduplicate the dataset by licence number and keep the latest record. This reduces the data
from 221 to 219 rows.

Business type has the clearest relationship with the broader failure label. For example, the observed
failure rate is 4.8% for `Wholesale Dealer - Food` and 43.5% for `Retail Dealer - Food`. These groups
are still small, so the percentages should be treated carefully. Very rare business types will be
combined into an `Other` category.

Neighbourhood may also be useful. Among neighbourhoods with at least eight records, Downtown has a
36.4% failure rate and Strathcona has an 8.7% failure rate. Smaller neighbourhood categories will be
combined to reduce the number of one-hot encoded columns.

The number of employees is strongly right-skewed. The median is 5 employees, but the maximum is 1,955.
Failed businesses have fewer employees on average, although the group medians are close. I will test a
log transformation for models that are affected by this skew.

## Feature decisions

At this stage, the planned predictors are `businesstype`, `localarea`, and `numberofemployees`.
`licencenumber` and `businessname` are identifiers and will only be used to connect predictions back to
businesses. `status` is the source of the target label, so it cannot be a predictor. I will exclude the
two date columns because of leakage, `feepaid` because 52.5% of its values are missing, `folderyear`
because it is almost constant, and `postalcode` because it overlaps with `localarea` and has many
nearly unique values.

The remaining predictors only have weak to moderate relationships with failure. This means I do not
expect a near-perfect model, especially with only 219 records after deduplication. The small number of
failed businesses will also make evaluation less stable.

## Questions still to resolve

The main question is whether `Pending` should count as a failed business. A pending licence may only
mean that the city has not finished processing it, so it may not represent an actual business failure.
My current recommendation is to exclude `Pending` records from model training until this is confirmed.

I also need to confirm where the 63% baseline in the Phase 2 agreement came from. Predicting the
majority class gives 91% accuracy with the narrow label and 76% with the broader label. These high
accuracy values are misleading because such a model would never identify a failed business.

## Next steps

Next, I will finalize the label definition, create the cleaning and deduplication steps, and build a
simple baseline classification model. I will then compare it with a random forest. Since the final
output is a ranked list, I plan to focus on precision near the top of the list, recall, and PR-AUC
instead of using accuracy alone.

The full analysis and figures are available in [the EDA notebook](notebooks/01_EDA.ipynb).

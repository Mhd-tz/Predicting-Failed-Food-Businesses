# Summary for the Greater Vancouver Food Bank

**Prepared by:** Mahdi Taziki, IAT 461, Summer 2026
**For:** Jason Salonga
**Date:** August 11, 2026

## Deliverable

I created a trial contact list of the 168 Vancouver food businesses whose current licence status is `Issued`.
The list is sorted by how closely each business resembles records with a failure status in the dataset.
It is available at [`outputs/ranked_contact_list.csv`](outputs/ranked_contact_list.csv).

Each row includes the rank, a contact week, a high, medium, or low band, the licence number, business
name, type, neighbourhood, employee count, and model score. The schedule uses 10 businesses per week,
which is the approximate capacity you confirmed. It can be changed later if the coordinator's capacity
changes.

The Streamlit app shows the same nine columns, provides filters, and allows the user to download the
filtered view. It also has a page for comparing a hypothetical business with the current list.

## How to use the list

Start at rank 1 and work down the list. The rank and band are more useful than the raw score. A score
of 0.70 does not mean a 70% chance that the business will close. It only places that business higher
than businesses with lower scores.

The high band contains the first 30 businesses. This gives the coordinator three weeks of contacts at
10 per week. During the trial, record what happens with each contact rather than assuming the
model has identified a future closure.

## Evaluation result

I tested the random forest by repeatedly hiding parts of the 219-record dataset and ranking the hidden
records. In those tests, the first 10 positions contained an average of 2.9 records already marked with
a failure status. A random ordering would contain about 2.3. The result varied from one split to
another, and only 60% of the repeated top-10 rankings beat the random baseline. The ranking was more
consistent by the first 30 positions.

This test did not follow currently issued businesses into the future. Because of that, I cannot say
that about 3 of every 10 contacted businesses will later fail. The result only shows that the model
finds some patterns in the statuses already in this dataset.

## What the model uses

The model uses business type, neighbourhood, and number of employees. Business type had the largest
mean importance in cross-validation, but the importance estimates changed across folds. Employee
count and neighbourhood were close to zero on average, so the data is not strong enough to give a
confident ranking of all three predictors.

The model does not know anything about rent, revenue, debt, ownership changes, business age, or support
already received from the food bank. Similar businesses in the same area can therefore receive nearly
the same score.

## Client decisions used

The Phase 1 proposal defines failure as `Cancelled` or `Gone Out of Business`. In the August 9
follow-up, you confirmed that `Pending` and `Inactive` should also count because you consider both to
be cases where the business became unresponsive. I used that broader definition for the final model and
tested stricter versions as a sensitivity check.

You also confirmed a capacity of around 10 contacts per week. The notebook and app use 10 for the
weekly batches. Those are the two client decisions I used in the final model. The lack of future
outcome data is still a limitation of the dataset.

## What I would do next

The model needs licence records from more than one year. With records from two or more dates, the
outcome could be defined as a business that is open in one period and closes in a later period. That
would allow a real forecast and a test using a later year. Until those data are available, this list is
best used as a small trial whose results are recorded and reviewed.

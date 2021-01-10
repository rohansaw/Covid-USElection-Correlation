# Covid-USElection-Correlation

## Running the Code and viewing the Results
- **Option1:** We have hosted the current Version of our vizualization demo on https://lasklu.github.io/ Over there you can view our vizualizations and read about the different plots
- **Option2:** Building the html files: 

## Tasks
### Task 1 - Dataset acquisition
In our plotting we use two datasets:
- Dataset1 contains data on polls before the us-presidential election for every us-state
We first searched for polls from different institutes and then discovered the webpage https://projects.fivethirtyeight.com/polls/president-general/wyoming/ . Over there we find data for every month beginnging from march 2020 and poll data that is merged from many different institutes. To acquire this data we discovered that there the page sends a request to the server which returns the data in Jsonformat for a specific state.
So we then acquired a list of all available states from the website by using JSoup to save all possible states from a dropdown-menu. Then for every state we request the data in form of a Json. 

    Now we have acquired the poll data begging in march 2020 for every us-state. But we now have data from different dates and want work with a value for every month. In order to do that we parsed the date and then grouped by month(date) and state. We also added a column that directly saved who is leading in every state and a column that saves the monthy increase in predicted votes, in order to later on be able to plot this better. Finally we merged the dataframes we acquired for every state into on big dataset which for every us-state contains the polling results per month. The dataset than contains information on the vote-trend for Joe-biden and Donald Trump in percent of total votes for every month since march 2020 and the increase of votes per month as a extra-column.

- Dataset2 contains data on the development of Covid-19 Infections for every-us state
We acquired this Dataset from https://www.kaggle.com/sudalairajkumar/covid19-in-usa. Overthere we found a dataset in a csv format containg daily data on the development of covid-19 since the beginning of 2020. It contains data on positve cases, totalTests, hospitalized cases, cases on Ventilator and deaths for different dates and states. In order to properly be able to work with this data, we preprocessed this, and grouped the data by month  and state so that we can work with the monthly increase of covid-numbers.
Furthermore we added a third dataset which contains the population for every us-state. We need this to be able to normalize infections per inhabitans per state, so that we have a better value to compare. This population dataset was then merged via panas into the covid dataset. We also remuved states that contained bad data or that weren't present in the polls dataset.

Finally we merged the Dataset1 (Polls) and Dataset2 (Covid) by using the pandas merge function with state and date as parameters.

### Task 2 - Vizualization
# Covid-USElection-Correlation
## Installation
You need python3 for using this dashboard. Please install the needed packages via: ``pip3 install -r requirements.txt``.

## Running the Code and viewing the Results
- **Option1:** We have hosted the current Version of our vizualization demo on https://lasklu.github.io/ Over there you can view our vizualizations and read about the different plots
- **Option2:** Building the html files: We have built several graphs with plotly. You can see the code of each graph in the mainfolder: They start with ``plot_``. The plotting methods are also called in the [main method](https://github.com/rohansaw/Covid-USElection-Correlation/blob/60cdbad170d608cdcac6738a4ba8e7855f54b07a/main.py#L10). You have now two choices: To build the html files you use the method ``fig.write_html`` which are commented out. You can also start each plot via ``fig.show()``.


We further built a dashboard (usage described above). If you want to start it locally, you will have to use [serve](https://www.npmjs.com/package/serve) from npm (which builds a local server). But we recommend using the already deployed website on https://lasklu.github.io/. You can find a description of each graph at the left side of the dashboard.

## Tasks
### Task 1 - Dataset acquisition
In our plotting we use two datasets:
- Dataset1 contains data on polls before the us-presidential election for every us-state
We first searched for polls from different institutes and then discovered the webpage https://projects.fivethirtyeight.com/polls/president-general/wyoming/ . Over there we find data for every month beginnging from march 2020 and poll data that is merged from many different institutes. To acquire this data we discovered that there the page sends a request to the server which returns the data in Jsonformat for a specific state.
So we then acquired a list of all available states from the website by using JSoup to save all possible states from a dropdown-menu. Then for every state we request the data in form of a Json. This Json is an Object that has different attributes such as the state name and the vote-trend for biden and trump.

    Now we have acquired the poll data begging in march 2020 for every us-state. But we now have data from different dates and want work with a value for every month. In order to do that we parsed the date and then grouped by month(date) and state. We also added a column that directly saved who is leading in every state and a column that saves the monthy increase in predicted votes, in order to later on be able to plot this better. Finally we merged the dataframes we acquired for every state into on big dataset which for every us-state contains the polling results per month. The dataset than contains information on the vote-trend for Joe-biden and Donald Trump in percent of total votes for every month since march 2020 and the increase of votes per month as a extra-column.

- Dataset2 contains data on the development of Covid-19 Infections for every-us state
We acquired this Dataset from https://www.kaggle.com/sudalairajkumar/covid19-in-usa. Overthere we found a dataset in a csv format containg daily data on the development of covid-19 since the beginning of 2020. It contains data on positve cases, totalTests, hospitalized cases, cases on Ventilator and deaths for different dates and states. The data is structured in rows that have these attributes and contain the according value. In order to properly be able to work with this data, we preprocessed this, and grouped the data by month  and state so that we can work with the monthly increase of covid-numbers.
Furthermore we added a third dataset which contains the population for every us-state. We need this to be able to normalize infections per inhabitans per state, so that we have a better value to compare. This population dataset was then merged via panas into the covid dataset. We also remuved states that contained bad data or that weren't present in the polls dataset.

Finally we merged the Dataset1 (Polls) and Dataset2 (Covid) by using the pandas merge function with state and date as parameters.

### Task 2 - Vizualization
1. Challenges building the graphs

2. Which relation can be found?
I will describe each graph and show why which question we wanted to answer.
1. **Deaths per state**: This graph shows the development of the amount of deaths related to covid for each state from march to december. It visualises the strong influence of the "second wave", but also shows that especially states around New York were hit very strongly in the beginning of the pandemic.
2. **Correlation between Trump's popularity and the covid cases** We want to analyze the influence of the pandemic on the popularity of Donald Trump. How do the citizens of the US evaluate Trumps handling of the crisis? For this we created two different lines. The red line shows the development of Trump's popularity, the green line the amount of positive cases in the US. You can see that especially the "first wave" influenced the popularity of Donald Trump. Many us-americans were not satisfied by Trump's covid-strategy. But you can see that his popularity started falling in the very beginning of the pandemic. Only after a few weeks his approval rating started rising again. But his popularity could not reach its level as it was before the pandemic.
3. **Devlopment of Trump's approval rating in each state in relation to the amount of cases** The development of the graph before was very interesting: His approval has fallen very strongly, but only after approximately two months, it started rising continously again. We want to go a little bit more in detail: How does this look like for each state? Our first thought was to develop a similar graph to the second one for each state. But this is not very intuitive and does not help the user to see any relations. Because of that we decided to use an animated map. This map shows for each state of the united states a circle. The larger a circle, the higher is the average increase of new daily covid cases per month compared to the month before for every state.

This had impact on his popularity. In the summer his popularity started rising again because the 
--> ansprechen, dass wohl einige Entwicklungen nicht nur auf covid zurückzuführen sind. Erwähnen, dass viele states mit hohen Todeszahlen Ballunsgebiete sind, die auch hauptsächlich demokratisch sind.

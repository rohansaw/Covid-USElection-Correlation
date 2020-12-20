from processElectionData import get_election_dataset
from processCovidData import get_covid_dataset, merge_population
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def main():
    covid_set = get_covid_dataset()
    #print(merge_population(covid_set))
    print("DGHAFDHJG")
    covid_set = covid_set.xs('FL', level=0)
    #covid_set['positive'].plot()
    # Need to save increase from month before normalized
    #plt.show()
    election_set = get_election_dataset("https://projects.fivethirtyeight.com/polls/president-general/")
    election_set = election_set.xs(('FL', 'Donald Trump'), level=[0, 2])
    election_set['increase'].plot()
    plt.show()


if __name__ == "__main__":
    main()

from processElectionData import get_election_dataset
from processCovidData import get_covid_dataset
from plot_map_usa_per_state import plot_map
from plot_state_line import plot_state_line
from plot_deaths_state import plot_map_deaths
from plot_scatter_tests import plot_scatter_tests
import pandas as pd


def main():
    df_covid = get_covid_dataset()
    df_polls = get_election_dataset("https://projects.fivethirtyeight.com/polls/president-general/")
    df_merged = merge(df_covid, df_polls)
    plot_scatter_tests(df_merged)
    plot_state_line(df_polls, df_covid, 'FL')
    plot_map(df_merged)
    plot_map_deaths(df_covid)


def merge(df_covid, df_polls):
    df = pd.merge(df_covid, df_polls, how='outer', left_on=['state','date'], right_on=['state', 'date'])
    df.fillna(0, inplace=True)
    return df

if __name__ == "__main__":
    main()

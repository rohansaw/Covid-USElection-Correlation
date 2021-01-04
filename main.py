from processElectionData import get_election_dataset
from processCovidData import get_covid_dataset
from plot_map_usa_per_state import plot_map
from plot_state_line import plot_state_line
from plot_deaths_state import plot_map_deaths
from plot_scatter_tests import plot_scatter_tests


def main():
    df_covid = get_covid_dataset()
    df_polls = get_election_dataset("https://projects.fivethirtyeight.com/polls/president-general/")
    df_merged = merge(df_covid, df_polls)
    plot_scatter_tests(df_merged)
    #plot_state_line(election_set, covid_set, 'FL')
    #plot_map(election_set, covid_set)
    plot_map_deaths(df_covid)


def merge(df_1, df_2):
    return

if __name__ == "__main__":
    main()

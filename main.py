from processElectionData import get_election_dataset
from processCovidData import get_covid_dataset
from plot_map_usa_per_state import plot_map
from plot_state_line import plot_state_line
from plot_deaths_state import plot_map_deaths


def main():
    df_covid = get_covid_dataset()
    #election_set = get_election_dataset("https://projects.fivethirtyeight.com/polls/president-general/")
    #plot_state_line(election_set, covid_set, 'FL')
    #plot_map(election_set, covid_set)
    plot_map_deaths(df_covid)


if __name__ == "__main__":
    main()

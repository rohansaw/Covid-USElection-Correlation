from processElectionData import get_election_dataset
from processCovidData import get_covid_dataset


def main():
    covid_set = get_covid_dataset()
    print(covid_set)
    election_set = get_election_dataset("https://projects.fivethirtyeight.com/polls/president-general/")    
    print(election_set)


if __name__ == "__main__":
    main()

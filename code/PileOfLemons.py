import logging
import os
import requests
from datetime import datetime,
from ParseStats import ParseStats
from ReportsPoke import ReportsPoke
from dateutil.relativedelta import relativedelta


'''Made by pileoflemons
With help from FelineAirline, Yak Attack,Intenzi, chatgpt'''

class PileOfLemons:
    def __init__(self, start_date, end_date, format_value, ranking):
        self.start_date = datetime.strptime(start_date, '%Y-%m')
        self.end_date = datetime.strptime(end_date, '%Y-%m')
        self.format_value = format_value
        self.ranking = ranking
        self.form_rank = f"{format_value}-{ranking}"
        self.folder_path = self.form_rank
        self.smogon_link = 'https://www.smogon.com/stats/'

    def get_files(self):
        current_date = self.start_date
        while current_date <= self.end_date:
            # Get the folder name for the current month
            folder_name = current_date.strftime('%Y-%m')

            # Print the name of the current month
            month_name = current_date.strftime('%B %Y')
            print(f"Processing files for: {month_name}")

            # Construct URLs for usage, moveset, and leads data
            usage_url = f"{self.smogon_link}{folder_name}/{self.form_rank}.txt"
            moveset_url = f"{self.smogon_link}{folder_name}/moveset/{self.form_rank}.txt"
            leads_url = f"{self.smogon_link}{folder_name}/leads/{self.form_rank}.txt"

            # Create directory if it doesn't exist
            folder_directory = os.path.join(self.folder_path, folder_name)
            os.makedirs(folder_directory, exist_ok=True)

            # Download and save usage.json
            usage_response = requests.get(usage_url)
            if usage_response.status_code == 200:
                with open(os.path.join(folder_directory, 'usage.json'), 'wb') as usage_file:
                    usage_file.write(usage_response.content)

            # Download and save moveset.json
            moveset_response = requests.get(moveset_url)
            if moveset_response.status_code == 200:
                with open(os.path.join(folder_directory, 'moveset.json'), 'wb') as moveset_file:
                    moveset_file.write(moveset_response.content)

            # Download and save leads.json
            leads_response = requests.get(leads_url)
            if leads_response.status_code == 200:
                with open(os.path.join(folder_directory, 'leads.json'), 'wb') as leads_file:
                    leads_file.write(leads_response.content)

            # Move to the next month using relativedelta to handle month transitions
            current_date += relativedelta(months=1)

        # After the loop, all required files should have been downloaded
        print("All files downloaded successfully.")


def main():
    print('Thanks for using PileOfLemons Pokemon program')
    print('Any problems, questions, or concerns you come up with. My discord name is PileOfLemons.')
    # Prompt the user for start_date1
    start_date1 = input("Enter start date (YYYY-MM): ")

    # Prompt the user for end_date1
    end_date1 = input("Enter end date (YYYY-MM): ")

    # Prompt the user for format_value1
    format_value1 = input("Enter format value (gen1ou, gen9uu,etc): ")

    # Prompt the user for ranking1
    ranking1 = input("Enter ranking(0,1500,1630,1760) for everything but highest gen ou which uses (0,1500,1695,1825): ")
    top_count = input("How many pokemon on the graph?: ")  # HOW MANY POKEMON DO YOU WANT ON THE GRAPH

    # Prompt the user to specify whether to download necessary files or not
    download_input = input("Need files? (y/n): ").strip().lower()
    download = download_input == 'y'
    # Prompt the user to specify whether to download necessary files or not
    pretty_input = input("Need to make the files pretty? You need to do this once per fileset(y/n): ").strip().lower()
    pretty = pretty_input == 'y'
    # Prompt the user to specify whether to save the graph
    save_graph_input = input("Save graph? (y/n) It will display either way: ").strip().lower()
    save_graph = save_graph_input == 'y'

    # Create PileOfLemons instance with user-provided input
    lemon = PileOfLemons(start_date1, end_date1, format_value1, ranking1)

    if download:
        lemon.get_files()


    # Create ParseStats instance with PileOfLemons attributes
    parser = ParseStats(start_date=lemon.start_date, end_date=lemon.end_date, new_folder=lemon.form_rank,
                        stats_location=lemon.form_rank,
                        format_value=lemon.format_value, ranking=lemon.ranking)
    try: parser.iterate_date_range()
    # Code that might raise an error
    except Exception as e:
        logging.error(f"An error occurred: {e}")

    # Create ReportsPoke instance with lemon.form_rank and top_count
    reporter = ReportsPoke(lemon.form_rank, top_count)

    # Convert datetime objects to strings for analyze_top_pokemon_ranks
    start_date_str = lemon.start_date.strftime('%Y-%m')
    end_date_str = lemon.end_date.strftime('%Y-%m')

    # Analyze top Pokémon rankings across the specified date range
    reporter.analyze_top_pokemon_ranks(start_date_str, end_date_str)
    graph_folder = f"{format_value1}-{ranking1}-graph"

    top_pokemon_dict = reporter.get_top_pokemon_dictionary()
    print("Dictionary of Top Pokémon:")
    for pokemon, count in top_pokemon_dict.items():
        print(f"{pokemon}: {count}")
    # Plot monthly rankings with multiple pages
    if save_graph:
        reporter.plot_monthly_rankings(save_folder=graph_folder)
    else:
        reporter.plot_monthly_rankings()  # Without save_folder parameter

    # Retrieve and print dictionary of top Pokémon


    input("Press enter to exit")

if __name__ == "__main__":
    main()
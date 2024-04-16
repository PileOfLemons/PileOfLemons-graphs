import os
import json
from datetime import datetime, timedelta  # Ensure correct import

class PrettyUsageStats:
    def __init__(self, base_folder):
        self.base_folder = base_folder

    def get_top_pokemon_data(self, target_date, top_n=10):
        target_month_folder = os.path.join(self.base_folder, target_date)
        target_json_path = os.path.join(target_month_folder, 'pretty', 'usage.json')

        if not os.path.exists(target_json_path):
            print(f"No usage.json file found for {target_date}.")
            return []

        try:
            with open(target_json_path, 'r') as json_file:
                data = json.load(json_file)
                pokemon_data = data.get('pokemon_data', {})

                if not pokemon_data:
                    print(f"No 'pokemon_data' found in {target_json_path}.")
                    return []

                # Sort pokemon_data by usage percentage (descending order) and extract top N
                sorted_pokemon = sorted(pokemon_data.items(), key=lambda x: x[1].get('usage_perc', 0), reverse=True)[:top_n]

                # Create a list of tuples with (pokemon_name, usage_percentage)
                top_pokemon_data = [(pokemon, usage_data.get('usage_perc', 0)) for pokemon, usage_data in sorted_pokemon]

                return top_pokemon_data

        except Exception as e:
            print(f"Error processing data for {target_date}: {e}")
            return []

    def generate_monthly_rankings(self, start_date='2014-11', end_date='2024-03', top_n=10):
        months = {}

        # Convert start_date and end_date to datetime objects for iteration
        start_datetime = datetime.strptime(start_date, '%Y-%m')
        end_datetime = datetime.strptime(end_date, '%Y-%m')

        current_date = start_datetime
        while current_date <= end_datetime:
            target_date = current_date.strftime('%Y-%m')  # Format datetime as string
            top_pokemon_data = self.get_top_pokemon_data(target_date, top_n)
            months[target_date] = top_pokemon_data

            # Move to the next month
            year = current_date.year
            month = current_date.month + 1
            if month > 12:
                year += 1
                month = 1
            current_date = datetime(year, month, 1)

        return months

# Example usage
if __name__ == "__main__":
    '''base_folder = 'gen9ru-1760'
    stats = PrettyUsageStats(base_folder)
    monthly_rankings = stats.generate_monthly_rankings(start_date='2023-02', end_date='2024-03', top_n=10)

    # Print the monthly rankings
    for month, top_pokemon_data in monthly_rankings.items():
        print(f"Top 10 Pokémon Rankings for {month}:")
        for pokemon, usage_percentage in top_pokemon_data:
            print(f"{pokemon}: {usage_percentage}")
        print()  # Print a blank line for separation'''

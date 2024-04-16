import matplotlib.pyplot as plt
import numpy as np
import json
import os
from datetime import datetime
import random
import string

class ReportsPoke:
    def __init__(self, folder_path, top_count=10):
        self.folder_path = folder_path
        self.top_count = int(top_count)
        self.monthly_rankings = {}
        self.pokemon_colors = {
            'Tauros': '#DEA44A',
            'Exeggutor': '#73AC31',
            'Chansey': '#FFACAC',
            'Starmie': '#8B73BD',
            'Snorlax': '#E6C5AC',
            'Alakazam': '#CDB410',
            'Golem': '#9C8B52',
            'Slowbro': '#FF9494',
            'Jynx': '#F6315A',
            'Rhydon': '#8B8B94',
            'Lapras': '#397BA4',
            'Jolteon': '#FFDE52',
            'Gengar': '#5A4A9C',
            'Zapdos': '#D5AC08',
            'Machamp': '#838B94',
            'Victreebel': '#8BC57B',
            'Cloyster': '#AC7BBD',
            'Dragonite': '#EE9C39',
            'Hypno': '#F6DE00'
            '''these colors have been chosen by pokemon palette'''
        }

    def load_data(self, target_date):
        month_label = target_date
        filename = os.path.join(self.folder_path, month_label, 'pretty', 'usage.json')

        try:
            with open(filename, 'r') as file:
                data = json.load(file)
                pokemon_data = data.get('pokemon_data', {})
                # Sort Pokémon by usage percentage (descending)
                sorted_pokemon = sorted(pokemon_data.items(), key=lambda x: x[1].get('usage_perc', 0), reverse=True)
                # Keep only the top N Pokémon
                top_pokemon = [(pokemon, stats.get('usage_perc', 0)) for pokemon, stats in sorted_pokemon[:self.top_count]]
                self.monthly_rankings[target_date] = top_pokemon

        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")

    def analyze_top_pokemon_ranks(self, start_date, end_date):
        current_date = datetime.strptime(start_date, '%Y-%m')
        end_date = datetime.strptime(end_date, '%Y-%m')

        while current_date <= end_date:
            target_date = current_date.strftime('%Y-%m')
            self.load_data(target_date)
            current_date = current_date.replace(day=1)  # Move to the first day of next month
            if current_date.month == 12:
                current_date = current_date.replace(year=current_date.year + 1, month=1)
            else:
                current_date = current_date.replace(month=current_date.month + 1)

    def plot_monthly_rankings(self, save_folder=None):
        if not self.monthly_rankings:
            print("No monthly rankings data available.")
            return

        months = list(self.monthly_rankings.keys())
        num_months = len(months)

        # Group months by year
        yearly_data = {}
        for month in months:
            year = month[:4]  # Extract the year part from the month (e.g., '2023' from '2023-01')
            if year not in yearly_data:
                yearly_data[year] = []
            yearly_data[year].append(month)

        # Sort years and corresponding months
        yearly_data_sorted = sorted(yearly_data.items())

        if save_folder:
            os.makedirs(save_folder, exist_ok=True)  # Create save folder if specified

        # Create a dictionary to collect new pokemon and colors
        new_pokemon_colors = {}

        for year, months_in_year in yearly_data_sorted:
            num_months_in_year = len(months_in_year)
            num_pages_for_year = (num_months_in_year + 11) // 12  # Calculate number of pages for the year

            for page in range(num_pages_for_year):
                fig, axes = plt.subplots(3, 4, figsize=(16, 12))
                axes = axes.ravel()  # Flatten the 2D array of axes

                for i in range(12):
                    ax = axes[i]
                    idx = page * 12 + i
                    if idx < num_months_in_year:
                        target_date = months_in_year[idx]
                        top_pokemon = self.monthly_rankings[target_date]
                        pokemon_names = [pokemon for pokemon, _ in top_pokemon]
                        usage_percents = [usage for _, usage in top_pokemon]

                        # Get colors based on pokemon_names, assign new random colors if not in self.pokemon_colors
                        colors = []
                        for pokemon in pokemon_names:
                            if pokemon in self.pokemon_colors:
                                colors.append(self.pokemon_colors[pokemon])
                            else:
                                if pokemon not in new_pokemon_colors:
                                    # Generate a random color
                                    new_color = '#' + ''.join(random.choices(string.hexdigits, k=6))
                                    new_pokemon_colors[pokemon] = new_color
                                colors.append(new_pokemon_colors[pokemon])

                        bars = ax.bar(pokemon_names, usage_percents, color=colors)
                        ax.set_title(f"Top 10 Pokémon Usage - {target_date}")
                        ax.set_xlabel('Pokémon')
                        ax.set_ylabel('Usage Percentage')

                        # Set ticks and labels
                        ax.set_xticks(np.arange(len(pokemon_names)))
                        ax.set_xticklabels(pokemon_names, rotation=45, ha='right')

                        # Annotate bars with usage percentages
                        for bar, usage_percent in zip(bars, usage_percents):
                            height = bar.get_height()
                            ax.text(bar.get_x() + bar.get_width() / 2, height, f'{usage_percent:.1f}%',
                                    ha='center', va='bottom', fontsize=8, color='black', fontweight='bold')

                        ax.set_facecolor('lightgrey')  # Set background color
                    else:
                        ax.axis('off')  # Hide empty subplots

                # Set title of the page to display the year
                fig.suptitle(f"Top 10 Pokémon Usage - Year {year}", fontsize=14, fontweight='bold')
                plt.tight_layout()

                # Save the figure as JPEG if save_folder is specified
                if save_folder:
                    save_filename = os.path.join(save_folder, f"Top10_Pokemon_Year{year}_Page{page + 1}.jpg")
                    plt.savefig(save_filename, format='jpeg')
                    plt.show()
                    plt.close()  # Close the figure to release memory
                else:
                    plt.show()

        # Update self.pokemon_colors with new_pokemon_colors
        self.pokemon_colors.update(new_pokemon_colors)

    def get_top_pokemon_dictionary(self):
        top_pokemon_dict = {}

        for top_pokemon_list in self.monthly_rankings.values():
            for pokemon, _ in top_pokemon_list:
                if pokemon not in top_pokemon_dict:
                    top_pokemon_dict[pokemon] = 0
                top_pokemon_dict[pokemon] += 1

        return top_pokemon_dict

def main():
    print('hi')

if __name__ == '__main__':
    main()

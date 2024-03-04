#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 14:29:24 2024

@author: sarahmehiyddine
"""

import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import os

# Liste des URL de base
base_urls = [
    'https://www.skysports.com/football/manchester-united-women-vs-reading-women/',
    'https://www.skysports.com/football/arsenal-women-vs-brighton-and-hove-albion-women/',
    'https://www.skysports.com/football/arsenal-women-vs-liverpool-women/'
]

# Liste des premiers et derniers numéros de match pour chaque saison
match_numbers = [
    (456246, 456376),
    (473902, 474027),
    (494310, 494397)
]

# User agent header
user_agent = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0'
}

# Function to get the HTML of the page
def get_page(urlpage):
    # Avoid getting banned
    # Get the HTML of the webpage
    print(f"Requesting {urlpage}")
    res = requests.get(urlpage, headers=user_agent)
    print(f"Response {res.status_code}")
    # Parse the HTML
    soup = BeautifulSoup(res.text, 'html.parser')
    return soup

# Function to scrape match details
def scrape_match_details(match_url):
    soup = get_page(match_url)

    # Extracting match details
    match_date = extract_match_date(soup)
    team_names = extract_team_names(soup)
    attendance = extract_attendance(soup)

    # Create a dictionary with all the information
    match_data = {
        'Match Date': match_date,
        'Teams': f"{team_names[0]} vs {team_names[1]}",
        'Attendance': attendance
    }

    return match_data

# Function to extract match date
def extract_match_date(soup):
    match_date_tag = soup.find('time', {'class': 'sdc-site-match-header__detail-time'})
    return match_date_tag.get('aria-label').split(',')[1].strip() if match_date_tag else None

# Function to extract team names
def extract_team_names(soup):
    team_names_tag = soup.find('p', {'class': 'sdc-site-match-header__detail-fixture'})
    return team_names_tag.text.split(' vs ') if team_names_tag else [None, None]

# Function to extract attendance
def extract_attendance(soup):
    attendance_tag = soup.find('span', {'class': 'sdc-site-match-header__detail-attendance'})
    return attendance_tag.contents[-1].strip() if attendance_tag else None

# Function to main
def main():
    match_data_list = []

    # Iterate through each season
    for base_url, (start_match, end_match) in zip(base_urls, match_numbers):
        # Scrape match details from each match for the current season
        for match_number in range(start_match, end_match + 1):
            match_url = base_url + f"{match_number}/"
            match_data = scrape_match_details(match_url)
            match_data_list.append(match_data)

    # Create DataFrame from the list of dictionaries
    df = pd.DataFrame(match_data_list)

    # Specify the new path with .xlsx extension
    directory_path = "/Users/sarahmehiyddine/Desktop/Cours/Magistère/M1/S2/Économétrie_appliquée /Time_series/Dossier"
    file_path = os.path.join(directory_path, "data.xlsx")
    
    # Check if the directory exists, if not, create it
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

    # Save DataFrame to Excel file
    df.to_excel(file_path, index=False)

    print(f"DataFrame created and saved to {file_path}")

if __name__ == "__main__":
    main()


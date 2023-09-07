#!/usr/bin/env python3

from flask import Flask, send_from_directory, render_template, request
from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import datetime

app = Flask(__name__)


@app.route('/')
def home():
    return "Welcome to the Voting Data Scraper! Visit /get_votes to scrape the votes and download the Excel file."


@app.route('/get_votes')
def get_votes():
    data_list = find_votes()
    df = pd.DataFrame(data_list)
    df = df.sort_values(by="Votes", ascending=False)

    if request.args.get('download') == 'true':
        filename = "votes_data_{}.xlsx".format(datetime.now().strftime('%Y%m%d_%H%M%S'))
        df.to_excel(f"downloads/{filename}", index=False)
        return send_from_directory(directory="downloads", path=filename, as_attachment=True)
    else:
        return render_template("votes_table.html", data=df.to_dict(orient="records"))


def find_votes():
    user_agent = {
        'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'}
    html_text = requests.get('https://www.comoncluj.ro/initiative', headers=user_agent).text
    soup = BeautifulSoup(html_text, 'lxml')

    toate_initiativele = soup.find_all('li', class_='initdatalisting page_1')
    data_list = []

    for initiative_individuale in toate_initiativele:
        initiative = initiative_individuale.find('div', class_='initdata')
        group_name = initiative.find('div', class_='group_name').text
        init_name = initiative.find('div', class_='init_name').text
        voturi_div = initiative_individuale.find('div', class_='voteswrap')
        voturi = int(voturi_div.find('span', class_='num').text.replace('voturi', ''))

        data = {
            "Group Name": group_name,
            "Initiative Name": init_name,
            "Votes": voturi
        }

        data_list.append(data)

    return data_list


if __name__ == '__main__':
    app.run(debug=True)

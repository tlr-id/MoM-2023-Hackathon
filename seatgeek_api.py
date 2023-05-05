import pandas as pd
import csv
import requests

api_key = 'MzIwOTAwOTd8MTY3NzQxMjc3NC41NDcxNzg1'
name_artist = 'Beyonce'

def query_venue_capa(venue_id):
  endpoint = 'https://api.seatgeek.com/2/venues'
  params = {
      'id': venue_id,
      'client_id': api_key
  }
  response = requests.get(endpoint, params=params)
  #print(response)

  if response.status_code == 200:
    venue_data = response.json()
    #print(venue_data['venues'][0]['capacity'])
    #print(json.dumps(venue_data,indent=4))
    return venue_data['venues'][0]['capacity']

def median_usd_value_country(df, country_name):
    if len(country_name) >= 3:
        filtered_df = df[df["country"] == country_name]
    else:
       filtered_df = df[df["cca2"] == country_name]
    median = int((filtered_df.iloc[0]["medianIncome"]/12))
    mean = int((filtered_df.iloc[0]["meanIncome"]/12))
    gdp = int((filtered_df.iloc[0]["gdpPerCapitaPPP"]/12))
    '''
    exchange_rate = 0.82
    medianeur_values = int(median / exchange_rate)
    meaneur_values = int(mean / exchange_rate)
    gdp_eur = int(gdp / exchange_rate)
    print(f"The median income for {country_name} is {median} USD or {medianeur_values} EUR per month")
    print(f"The mean income for {country_name} is {mean} USD or {meaneur_values} EUR per month")
    print(f"The GDP per capita for {country_name} is {gdp} USD or {gdp_eur} EUR per month")
    '''
    return median

def get_seatgeek_data(name_artist):
    df = pd.read_csv('income_country.csv')
   

    # 1st step : Get artist id 
    endpoint = 'https://api.seatgeek.com/2/performers'
    params = {
        'q': name_artist,
        'client_id': api_key
    }
    response = requests.get(endpoint, params=params)
   
    if response.status_code == 200:
        perf_data = response.json()
        print(f'Artist name : {perf_data["performers"][0]["name"]} ; id : {perf_data["performers"][0]["id"]}')
        performer_id = perf_data['performers'][0]['id']
    else:
       out_err = f'ERROR - Recovering ID issue - Response : {response}'
       return out_err
    
    # 2nd step : List of events

    endpoint = 'https://api.seatgeek.com/2/events'
    params = {
        'performers.id': performer_id,
        'client_id': api_key
    }

    response = requests.get(endpoint, params=params)
    
    if response.status_code == 200:
        data = []
        event_data = response.json()
        #print(event_data)
        if event_data['events'] == []:
            out_err = f'No concert planned on the database for this artist : {name_artist}'
            return out_err
    
        for event in event_data['events']:
            title = event['title']
            date = event['datetime_local']
            venue_name = event['venue']['name']
            country_name = event['venue']['country']
            venue_lat = event['venue']['location']['lat']
            venue_lon = event['venue']['location']['lon']
            med_price = event['stats']['median_price']
            med_gdp = median_usd_value_country(df,country_name)
            if med_price==None or med_gdp ==None:
               price_vs_gdp = 0
            else:
                price_vs_gdp = med_price/med_gdp*100
            listing_avail = event['stats']['listing_count']
            venue_id = event['venue']['id']
            capacity = query_venue_capa(venue_id)
            if capacity == 0:
               pourcentage_fill = 0
            else:
                pourcentage_fill = (capacity-listing_avail)/capacity*100
            row = {
                'Title': title,
                'Date': date,
                'Venue Name': venue_name,
                #'Country': country_name,
                #'Venue Latitude': venue_lat,
                #'Venue Longitude': venue_lon,
                'Median Price': med_price,
                'Median GDP': med_gdp,
                'Price vs GDP': price_vs_gdp,
                #'Listing Availability': listing_avail,
                #'Venue Capacity': capacity,
                'Percentage Fill': pourcentage_fill if pourcentage_fill !=0  else None
            }
            data.append(row)
    else:
       out_err = f'ERROR - Recovering Concerts issue - Response : {response}'
       return out_err
    
    
    df = pd.DataFrame(data)

    return df

#print(get_seatgeek_data('Adele'))

# a
# #first_line = ['artist name', 'Country', 'date', 'venue_name', 'venue_lat', 'venue_lon', 'median_price', 'median_gdp', 'price_vs_gdp', 'listing_avail', 'capacity', 'pourcentage_fill']
# # Check request successful
# if response.status_code == 200:
#     event_data = response.json()
#     with open('./extract_seatgeek.csv', 'w') as fp:
#         writer = csv.writer(fp)
#         writer.writerow(first_line)
#         #print(json.dumps(event_data,indent=4))   
#         for event in event_data['events']:
#             title = event['title']
#             date = event['datetime_local']
#             venue_name = event['venue']['name']
#             country_name = event['venue']['country']
#             venue_lat = event['venue']['location']['lat']
#             venue_lon = event['venue']['location']['lon']
#             med_price = event['stats']['median_price']
#             med_gdp = median_usd_value_country(df,country_name)
#             price_vs_gdp = med_price/med_gdp*100
#             listing_avail = event['stats']['listing_count']
#             venue_id = event['venue']['id']
#             #print(venue_id)
#             capacity = query_venue_capa(venue_id)
#             if capacity == 0:
#                pourcentage_fill = 0
#             else:
#                 pourcentage_fill = (capacity-listing_avail)/capacity*100
#             line_ = [title, country_name, date, venue_name, venue_lat, venue_lon, med_price, med_gdp, price_vs_gdp, listing_avail, capacity, pourcentage_fill ]
            
#             writer.writerow(line_)
#             '''
#             #print(event)
#             #print(event['title'])
#             print(event['datetime_local'])
#             print(event['venue']['name'])
            
#             print(f'Country name : {country_name}')
#             #median_usd_country = median_usd_value_country(df,country_name)
#             print(event['venue']['location']['lat'])
#             print(event['venue']['location']['lon'])
#             print(event['stats']['lowest_price'])
#             prices = [ event['stats']['lowest_price'], event['stats']['average_price'] , event['stats']['median_price'], event['stats']['highest_price'] ]
#             print(f'prices : {prices}')
#             print(f'Median GDP of the country : {med_gdp}')
#             print(f'Median price / Median GDP : {prices[2]/med_gdp*100}%')


#             venue_id = event['venue']['id']
#             print(venue_id)
#             capacity = query_venue_capa(venue_id)
#             listings = event['stats']['listing_count']
#             if capacity > 0:
#                 print(f'Capacity : {capacity} ; listings : {listings} => {(capacity-listings)/capacity*100}% full')
#                 print('---')
#             line_ = [title, country_name, date, venue_name, venue_lat, venue_lon, med_price, med_gdp, price_vs_gdp, listing_avail, capacity, pourcentage_fill ]
#             '''  

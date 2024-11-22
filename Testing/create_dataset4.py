import pandas as pd
import numpy as np
from datetime import datetime


def get_season(date):
    if date.month in [12]:
        return 'Christmas Season'
    elif date.month in [3, 4, 5]:
        return 'Spring'
    elif date.month in [6, 7, 8]:
        return 'Summer'
    elif date.month in [9, 10, 11]:
        return 'Fall'
    elif date.month in [1, 2]:
        return 'Winter'


def adjust_occupancy(occupancy_rate, season, date, room_type):
    if season == 'Christmas Season':
        return min(100, occupancy_rate + np.random.randint(15, 21))
    elif season == 'Summer':
        if room_type == 'Single':
        
            return max(0, occupancy_rate * (1 - np.random.uniform(0.08, 0.12)))
        elif room_type == 'Double' or room_type == 'Family':
          
            return min(100, occupancy_rate * (1 + np.random.uniform(0.12, 0.20)))
        elif room_type == 'Deluxe' or room_type == 'Suite':
         
            return min(100, occupancy_rate * (1 + np.random.uniform(0.05, 0.15)))
    elif season == 'Spring':
        return max(0, occupancy_rate - np.random.randint(0, 21))
    elif season == 'Fall':
        return max(0, occupancy_rate + np.random.randint(-10, 4))
    
    # Additional increase for April and May for Family, Deluxe, and Suite rooms
    if date.month in [4, 5] and room_type in ['Family', 'Deluxe', 'Suite']:
        return min(100, occupancy_rate * (1 + np.random.uniform(0.03, 0.09)))
    
    return occupancy_rate



def check_holiday(date):
    holidays = {
        datetime(date.year, 12, 20): 1.7,
        datetime(date.year, 12, 21): 1.7,
        datetime(date.year, 12, 22): 1.8,
        datetime(date.year, 12, 23): 1.8,
        datetime(date.year, 12, 24): 2.0,
        datetime(date.year, 12, 25): 2.0,
        datetime(date.year, 12, 26): 1.9,
        datetime(date.year, 12, 31): 2.0,
        datetime(date.year, 1, 1): 2.0,
        datetime(date.year, 1, 2): 1.9,
        datetime(date.year, 2, 10): 1.2,
        datetime(date.year, 2, 14): 1.5,
        datetime(date.year, 3, 28): 1.3,
        datetime(date.year, 3, 29): 1.3,
        datetime(date.year, 11, 1): 1.35,
        datetime(date.year, 11, 2): 1.35,
    }
    return holidays.get(date, 1.0)


def get_weather(season):
    weather_options = ['Sunny', 'Cloudy', 'Rainy', 'Stormy']
    if season == 'Christmas Season':
        return np.random.choice(weather_options, p=[0.1, 0.15, 0.45, 0.3])
    elif season == 'Spring':
        return np.random.choice(weather_options, p=[0.3, 0.3, 0.3, 0.1])
    elif season == 'Summer':
        return np.random.choice(weather_options, p=[0.5, 0.3, 0.1, 0.1])
    elif season == 'Fall':
        return np.random.choice(weather_options, p=[0.1, 0.25, 0.35, 0.3])
    else:
        return np.random.choice(weather_options, p=[0.35, 0.3, 0.25, 0.1])


def generate_event(season):
    events = {
        'Christmas Season': ['Christmas Bazaar', 'Concert'],
        'Spring': ['Convention', 'Music Festival', 'Conference'],
        'Summer': ['Summer Concert', 'Music Festival', 'Outdoor Festival', 'Convention'],
        'Fall': ['Halloween Festival', 'Convention'],
        'Winter': []
    }
    if events[season]:
        return np.random.choice(events[season])  
    return None

def generate_weather_data(start_date, end_date):
 
    date_range = pd.date_range(start=start_date, end=end_date)

    
    weather_data = {
        'Date': [],
        'Weather': [],
        'Season': []
      
    }

    for date in date_range:
        season = get_season(date)
        weather = get_weather(season)
        
        
        
        weather_data['Date'].append(date)
        weather_data['Weather'].append(weather)
        weather_data['Season'].append(season)
      

   
    weather_df = pd.DataFrame(weather_data)

 
    weather_df.to_csv('weather_data3.csv', index=False)
    print("Weather dataset generated and saved as 'weather_data2.csv'")


def generate_events_data(start_date, end_date):
 
    date_range = pd.date_range(start=start_date, end=end_date)

    events_data = {
        'Date': [],
        'Events': []
    }

    for date in date_range:
        season = get_season(date)
        event = generate_event(season)
        
        
        if not event:
            event = 'No Events'  
           
        
        events_data['Date'].append(date)
        events_data['Events'].append(event)

    
    events_df = pd.DataFrame(events_data)

   
    if events_df['Events'].isnull().any():
        print("Warning: There are empty values in the 'Events' column.")
    
 
    events_df.to_csv('events_data2.csv', index=False)
    print("Events dataset generated and saved as 'events_data2.csv'")



room_info = {
    'Single': {
        'occupancy_ranges': {
            'Winter': (40, 80),
            'Spring': (35, 85),
            'Summer': (30, 80),
            'Fall': (30, 75),
            'Christmas Season': (70, 100)
        }
    },
    'Double': {
        'occupancy_ranges': {
            'Winter': (35, 80),
            'Spring': (20, 70),
            'Summer': (25, 75),
            'Fall': (10, 70),
            'Christmas Season': (65, 100)
        }
    },
    'Suite': {
        'occupancy_ranges': {
            'Winter': (20, 60),
            'Spring': (15, 55),
            'Summer': (10, 60),
            'Fall': (20, 50),
            'Christmas Season': (50, 95)
        }
    },
    'Deluxe': {
        'occupancy_ranges': {
            'Winter': (25, 65),
            'Spring': (20, 60),
            'Summer': (15, 65),
            'Fall': (15, 55),
            'Christmas Season': (60, 95)
        }
    },
    'Family': {
        'occupancy_ranges': {
            'Winter': (30, 70),
            'Spring': (25, 75),
            'Summer': (20, 90),
            'Fall': (25, 70),
            'Christmas Season': (60, 95)
        }
    }
}


def generate_hotel_data(start_date, end_date):

    date_range = pd.date_range(start=start_date, end=end_date)

 
    data = {
        'Date': [],
        'Room Type': [],
        'Occupancy Rate (%)': [],
        'Season': [],
        'Holidays': [],
        'Weather': [],
        'Events': [],
        'Holiday Multiplier': [],
        'Event Multiplier': [],
        'Weather Multiplier': []
    }

    
    for date in date_range:
        season = get_season(date)
        weather = get_weather(season)
        event = generate_event(season)
        
        for room_type in room_info.keys():
           
            occupancy_range = room_info[room_type]['occupancy_ranges'][season]
            occupancy_rate = np.random.randint(*occupancy_range)
            adjusted_rate = adjust_occupancy(occupancy_rate, season, date, room_type)

            holiday_multiplier = check_holiday(date)
            final_rate = min(100, adjusted_rate * holiday_multiplier)

            
            weather_multiplier = 1.0
            if weather == 'Stormy':
                weather_multiplier = 1.05  
            elif weather == 'Rainy':
                weather_multiplier = 1.02  
            
            final_rate = min(100, final_rate * weather_multiplier)

            
            event_multiplier = 1.0
            if event:
                event_multiplier = 1.1  
                final_rate = min(100, final_rate * event_multiplier)

            holiday_name = '' if holiday_multiplier == 1.0 else 'Holiday'

            data['Date'].append(date)
            data['Room Type'].append(room_type)
            data['Occupancy Rate (%)'].append(final_rate)
            data['Season'].append(season)
            data['Holidays'].append(holiday_name)
            data['Weather'].append(weather)
            data['Events'].append(event if event else '')
            data['Holiday Multiplier'].append(holiday_multiplier)
            data['Event Multiplier'].append(event_multiplier)
            data['Weather Multiplier'].append(weather_multiplier)

  
    df = pd.DataFrame(data)


    df.to_csv('synthetic_data_transparent.csv', index=False)
    df[['Date', 'Room Type', 'Occupancy Rate (%)']].to_csv('synthetic_data_cleaned2.csv', index=False)

    print("Datasets generated and saved as 'synthetic_data_transparent.csv' and 'synthetic_data_cleaned.csv'")


start_date_input = '2000-01-01'  
end_date_input = '2024-10-31'    

#generate_weather_data(start_date_input, end_date_input)
#generate_events_data(start_date_input, end_date_input)
#generate_hotel_data(start_date_input, end_date_input)


import pandas as pd
import json
import os

class FitFamDataLoader:
    def __init__(self, data_dir=None):
        if data_dir is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            self.data_dir = os.path.join(base_dir, 'fitfam-json')
        else:
            self.data_dir = data_dir

    def _load_json(self, filename):
        filepath = os.path.join(self.data_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return pd.DataFrame(data)

    def _parse_json_field(self, df, column, key='en'):
        """Parses a column containing JSON strings and extracts a specific key."""
        def extract(x):
            try:
                if isinstance(x, str):
                    return json.loads(x).get(key, x)
                return x
            except (json.JSONDecodeError, TypeError):
                return x
        
        if column in df.columns:
            return df[column].apply(extract)
        return df[column] if column in df.columns else None

    def load_users(self):
        df = self._load_json('users.json')
        # Convert timestamps if they exist (checking common names)
        for col in ['created_at', 'updated_at']:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col])
        return df

    def load_locations(self):
        df = self._load_json('locations.json')
        df['name_en'] = self._parse_json_field(df, 'name', 'en')
        return df

    def load_events(self):
        df = self._load_json('events.json')
        df['name_en'] = self._parse_json_field(df, 'name', 'en')
        
        date_cols = ['start_time', 'end_time', 'registration_start', 'registration_end']
        for col in date_cols:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col])
        return df

    def load_event_user(self):
        df = self._load_json('event_user.json')
        return df

    def load_cities(self):
        return self._load_json('cities.json')

    def load_wechat_users(self):
        df = self._load_json('wechat_users.json')
        return df

    def load_categories(self):
        df = self._load_json('categories.json')
        df['name_en'] = self._parse_json_field(df, 'name', 'en')
        return df

    def load_category_event(self):
        return self._load_json('category_event.json')

    def get_unified_data(self):
        """
        Merges events, locations, and attendance data.
        Returns a merged DataFrame of individual attendances (one row per user-event).
        """
        users = self.load_users()
        wechat_users = self.load_wechat_users()
        
        # Merge users with wechat_users to get gender
        # users.id matches wechat_users.user_id
        users_full = users.merge(wechat_users[['user_id', 'gender', 'city', 'province', 'country']], left_on='id', right_on='user_id', how='left')
        
        events = self.load_events()
        locations = self.load_locations()
        event_user = self.load_event_user()
        cities = self.load_cities()
        
        # Load Categories
        categories = self.load_categories()
        category_event = self.load_category_event()
        
        # Merge Categories with Events
        # category_event has event_id, category_id
        # We merge category_event with categories to get names
        cat_merged = category_event.merge(categories[['id', 'name_en']], left_on='category_id', right_on='id', suffixes=('', '_cat'))
        cat_merged = cat_merged.rename(columns={'name_en': 'category_name'})
        
        
        cat_agg = cat_merged.groupby('event_id')['category_name'].apply(lambda x: ', '.join(x)).reset_index()
        
        # Merge Events with Locations
        events_loc = events.merge(locations[['id', 'name_en', 'city_id']], left_on='location_id', right_on='id', suffixes=('', '_loc'))
        events_loc = events_loc.rename(columns={'name_en': 'location_name', 'id_loc': 'location_id_redundant'})
        
        # Merge with Cities
        events_loc = events_loc.merge(cities[['id', 'name']], left_on='city_id', right_on='id', suffixes=('', '_city'))
        events_loc = events_loc.rename(columns={'name': 'city_name'})
        
        # Merge with Categories
        # events_loc has 'id' (event id), cat_agg has 'event_id'
        events_loc = events_loc.merge(cat_agg, left_on='id', right_on='event_id', how='left')

        # Merge Attendance with Events
        # event_user has event_id, user_id
        # events_loc has id (which is the event id)
        full_data = event_user.merge(events_loc, left_on='event_id', right_on='id', how='left', suffixes=('', '_organizer'))
        
        # Merge with User info
        # We use the merged users_full dataframe
        full_data = full_data.merge(users_full[['id', 'username', 'created_at', 'gender', 'city', 'province']], left_on='user_id', right_on='id', suffixes=('_attendance', '_user'))
        
        return full_data

if __name__ == "__main__":
    loader = FitFamDataLoader()
    print("Loading users...")
    users = loader.load_users()
    print(f"Users: {len(users)}")
    
    print("Loading events...")
    events = loader.load_events()
    print(f"Events: {len(events)}")
    
    print("Loading attendance...")
    attendance = loader.load_event_user()
    print(f"Attendance records: {len(attendance)}")
    
    print("Testing unified data...")
    unified = loader.get_unified_data()
    print(f"Unified records: {len(unified)}")
    print("Columns:", unified.columns.tolist())

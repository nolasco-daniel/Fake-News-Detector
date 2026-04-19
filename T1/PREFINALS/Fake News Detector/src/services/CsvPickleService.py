import pandas as pd
import pickle
from pathlib import Path

def process_csv_to_pickle(csv_path, pickle_path, label):
    print(f"Processing {csv_path}...")

    df = pd.read_csv(csv_path)
    
    processed_data = []
    
    for _, row in df.iterrows():

        title = str(row.get('title', row.get('headline', ''))).strip()
        body = str(row.get('text', '')).strip()

        combined = '. '.join(filter(None, [title, body]))
        
        if combined:
            processed_data.append({
                'text': combined,
                'label': label
            })
    
    # Save to pickle
    with open(pickle_path, 'wb') as f:
        pickle.dump(processed_data, f)
    
    print(f"Saved {len(processed_data)} records to {pickle_path}")

def main():
    # Get the data directory
    script_dir = Path(__file__).parent
    data_dir = script_dir.parent / "data"
    
    # Define file paths
    true_csv = data_dir / "True.csv"
    fake_csv = data_dir / "Fake.csv"
    true_pickle = data_dir / "True.pkl"
    fake_pickle = data_dir / "Fake.pkl"
    
    # Check if CSV files exist
    if not true_csv.exists():
        print(f"Error: {true_csv} not found")
        return
    
    if not fake_csv.exists():
        print(f"Error: {fake_csv} not found")
        return
    
    # Create data directory if it doesn't exist
    data_dir.mkdir(exist_ok=True)
    
    # Convert CSV files to pickle
    process_csv_to_pickle(true_csv, true_pickle, 'real')
    process_csv_to_pickle(fake_csv, fake_pickle, 'fake')
    
    print("\nConversion completed successfully!")
    print(f"Files created:")
    print(f"- {true_pickle}")
    print(f"- {fake_pickle}")

if __name__ == "__main__":
    main()

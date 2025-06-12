import os
import json
import pandas as pd
from typing import List, Dict, Any, Set


def collect_json_files(
    input_dir: str, 
    output_file: str, 
    output_format: str = "csv"
) -> None:
    # Find all JSON files
    json_files: List[str] = [
        os.path.join(input_dir, file) 
        for file in os.listdir(input_dir) 
        if file.endswith(".json")
    ]
    
    if not json_files:
        print(f"No JSON files found in '{input_dir}'.")
        return
    
    print(f"Found {len(json_files)} JSON files.")
    
    # Read and combine all JSON data
    all_profiles: List[Dict[str, Any]] = []
    
    for file_path in json_files:
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                
                if isinstance(data, list):
                    all_profiles.extend(data)
                else:
                    all_profiles.append(data)
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
    
    print(f"Total profiles collected: {len(all_profiles)}")
    
    unique_profiles: List[Dict[str, Any]] = []
    seen_names: Set[str] = set()
    
    for profile in all_profiles:
        try:
            full_name = profile.get('personal_data', {}).get('full_name', '')
            if full_name:
                if full_name in seen_names:
                    continue
                seen_names.add(full_name)
            unique_profiles.append(profile)
        except Exception:
            unique_profiles.append(profile)
    
    print(f"Removed {len(all_profiles) - len(unique_profiles)} duplicate profiles.")
    print(f"Final count: {len(unique_profiles)} unique profiles.")
    
    if output_format.lower() == 'csv':
        if not output_file.lower().endswith('.csv'):
            output_file = output_file + '.csv'
            
        df = pd.json_normalize(unique_profiles)
        df.to_csv(output_file, index=False)
    else:
        if not output_file.lower().endswith('.json'):
            output_file = output_file + '.json'
            
        with open(output_file, 'w') as f:
            json.dump(unique_profiles, f, indent=2)
    
    print(f"Successfully saved {len(unique_profiles)} profiles to {output_file}")


if __name__ == "__main__":
    input_directory: str = "./"
    output_filename: str = "client_profiles.csv"  
    
    collect_json_files(
        input_dir=input_directory,
        output_file=output_filename
    )

# ExoForge/preprocess_data.py

import pandas as pd
import numpy as np

def standardize_disposition(series):
    """Maps various disposition labels to a standard numerical format."""
    # Ensure the series is treated as a string type before applying string operations
    series = series.astype(str).str.upper().str.strip()
    
    # Define mappings: 2 for Confirmed, 1 for Candidate, 0 for False Positive
    disposition_map = {
        'CONFIRMED': 2,
        'CANDIDATE': 1,
        'FALSE POSITIVE': 0,
        'PC': 1,  # TESS Planet Candidate
        'CP': 2,  # TESS Confirmed Planet
        'FP': 0   # TESS False Positive
    }
    return series.map(disposition_map)

def process_file(filepath, column_map, mission_name):
    """
    Generic function to load, filter, and standardize data from a given mission file.
    """
    print(f"\n--- Processing {mission_name} data from '{filepath}' ---")
    
    try:
        df = pd.read_csv(filepath, comment='#')
    except FileNotFoundError:
        print(f"Warning: File not found at '{filepath}'. Skipping.")
        return None

    # Find which of the desired columns are actually in the file
    available_cols = {k: v for k, v in column_map.items() if k in df.columns}
    if not available_cols:
        print(f"Warning: None of the target columns found in '{filepath}'. Skipping.")
        return None
        
    print(f"Found {len(available_cols)} out of {len(column_map)} target columns.")

    # Keep only the columns we need and rename them to the standard format
    df_processed = df[list(available_cols.keys())].rename(columns=available_cols)
    
    # Standardize the disposition column
    if 'disposition' in df_processed.columns:
        df_processed['disposition'] = standardize_disposition(df_processed['disposition'])
    else:
        print(f"Warning: Disposition column not found for {mission_name}. Skipping this file.")
        return None
        
    return df_processed


if __name__ == '__main__':
    # --- Define Standard Column Names and Mappings for Each Mission ---

    # Our goal is to have these standard, mission-agnostic column names
    standard_columns = {
        'disposition': 'disposition',
        'period': 'period',
        'duration': 'duration',
        'depth': 'depth',
        'planet_radius': 'planet_radius',
        'equilibrium_temp': 'equilibrium_temp',
        'insolation_flux': 'insolation_flux',
        'model_snr': 'model_snr',
        'stellar_temp': 'stellar_temp',
        'stellar_logg': 'stellar_logg',
        'stellar_radius': 'stellar_radius'
    }

    # Kepler Mission Mapping ('cumulative.csv')
    kepler_map = {
        'koi_disposition': 'disposition',
        'koi_period': 'period',
        'koi_duration': 'duration',
        'koi_depth': 'depth',
        'koi_prad': 'planet_radius',
        'koi_teq': 'equilibrium_temp',
        'koi_insol': 'insolation_flux',
        'koi_model_snr': 'model_snr',
        'koi_steff': 'stellar_temp',
        'koi_slogg': 'stellar_logg',
        'koi_srad': 'stellar_radius'
    }

    # K2 Mission Mapping ('k2.csv') - **CORRECTION**: K2 data uses 'koi_' prefixes, not 'k2_'
    k2_map = {
        'koi_disposition': 'disposition',
        'koi_period': 'period',
        'koi_duration': 'duration',
        'koi_depth': 'depth',
        'koi_prad': 'planet_radius',
        'koi_teq': 'equilibrium_temp',
        'koi_insol': 'insolation_flux',
        'koi_model_snr': 'model_snr',
        'koi_steff': 'stellar_temp',
        'koi_slogg': 'stellar_logg',
        'koi_srad': 'stellar_radius'
    }
    
    # TESS Mission Mapping ('TOI.csv')
    tess_map = {
        'tfopwg_disp': 'disposition',
        'pl_orbper': 'period',
        'pl_trandurh': 'duration',
        'pl_trandep': 'depth',
        'pl_rade': 'planet_radius',
        'pl_eqt': 'equilibrium_temp',
        'pl_insol': 'insolation_flux',
        'pl_snr': 'model_snr',
        'st_teff': 'stellar_temp',
        'st_logg': 'stellar_logg',
        'st_rad': 'stellar_radius'
    }

    # --- Process and Combine ---
    
    df_kepler = process_file('data/cumulative.csv', kepler_map, "Kepler")
    df_k2 = process_file('data/k2.csv', k2_map, "K2")
    df_tess = process_file('data/TOI.csv', tess_map, "TESS")
    
    # Combine the datasets that were successfully processed
    data_frames = [df for df in [df_kepler, df_k2, df_tess] if df is not None]
    
    if not data_frames:
        print("\nError: No data could be processed. Please check your CSV files and paths.")
    else:
        print("\n--- Combining datasets ---")
        combined_df = pd.concat(data_frames, ignore_index=True, sort=False)
        print(f"Total combined rows before cleaning: {combined_df.shape[0]}")
        
        # --- Final Cleaning ---
        
        # Drop rows where disposition could not be mapped (e.g., 'UNK', 'SEE OTHER')
        combined_df.dropna(subset=['disposition'], inplace=True)
        combined_df['disposition'] = combined_df['disposition'].astype(int)
        
        # Ensure all feature columns exist, fill missing ones with NaN
        for col in standard_columns.values():
            if col not in combined_df.columns:
                combined_df[col] = np.nan

        # Fill any missing feature values with the median of their column
        for col in combined_df.columns:
            if col != 'disposition' and combined_df[col].isnull().any():
                median_val = combined_df[col].median()
                combined_df[col].fillna(median_val, inplace=True)
                print(f"Filled missing values in '{col}' using median: {median_val:.2f}")

        # Reorder columns to a standard format
        final_cols = [standard_columns['disposition']] + [v for k, v in standard_columns.items() if k != 'disposition']
        combined_df = combined_df[final_cols]

        print(f"Final cleaned dataset has {combined_df.shape[0]} rows and {combined_df.shape[1]} columns.")
        
        # Save the final combined and processed dataset
        OUTPUT_PATH = 'data/processed_combined.csv'
        combined_df.to_csv(OUTPUT_PATH, index=False)
        print(f"\nSuccessfully saved combined data to '{OUTPUT_PATH}'")
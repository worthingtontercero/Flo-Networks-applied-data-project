from __future__ import annotations

from pathlib import Path
from typing import Iterable, Optional

import pandas as pd
import requests


def load_county_cbsa_crosswalk(filepath: Path) -> pd.DataFrame:
    """
    Load the Census county->CBSA crosswalk .xls and return a clean dataframe:
    columns: cbsa_code, cbsa_name, fips_county
    """
    filepath = Path(filepath)
    if not filepath.exists():
        raise FileNotFoundError(f"Crosswalk not found: {filepath}")

    xwalk = pd.read_excel(filepath, dtype=str, header=3)
    xwalk.columns = xwalk.columns.astype(str).str.strip()

    required = {"CBSA Code", "CBSA Title", "FIPS"}
    missing = required -  set(xwalk.columns)
    if missing:
        raise ValueError(
            f"Crosswalk missing expected columns {missing}. "
            f"Found columns: {list(xwalk.columns)}. "
            f"Try changing header=3 if the file format differs."
        )

    xwalk = xwalk[["CBSA Code", "CBSA Title", "FIPS"]].rename(columns={
        "CBSA Code": "cbsa_code",
        "CBSA Title": "cbsa_name",
        "FIPS": "fips_county",
    })

    xwalk["cbsa_code"] = xwalk["cbsa_code"].astype(str).str.strip()
    xwalk["cbsa_name"] = xwalk["cbsa_name"].astype(str).str.strip()
    xwalk["fips_county"] = xwalk["fips_county"].astype(str).str.strip().str.zfill(5)

    return xwalk


def fetch_cbp_county_by_naics(
    year: int,
    naics_list: Iterable[str],
    api_key: Optional[str],
    cache_path: Optional[Path] = None,
    force_refresh: bool = False,
) -> pd.DataFrame:
    """
    Fetch Census CBP county-level EMP and ESTAB for selected NAICS codes.

    Returns a dataframe with columns:
    EMP, ESTAB, NAICS2017, STATE, COUNTY
    """
    if not api_key:
        raise ValueError(
            "CENSUS_API_KEY is not set. In your terminal run:\n"
            "  export CENSUS_API_KEY='YOUR_KEY'\n"
            "Then restart the notebook kernel."
        )

    if cache_path is not None:
        cache_path = Path(cache_path)
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        if cache_path.exists() and not force_refresh:
            return pd.read_csv(cache_path, dtype=str)

    base_url = f"https://api.census.gov/data/{year}/cbp"
    out_frames = []

    for naics in naics_list:
        params = {
            "get": "EMP,ESTAB,NAICS2017,STATE,COUNTY",
            "for": "county:*",
            "NAICS2017": naics,
            "key": api_key,
        }

        r = requests.get(base_url, params=params, timeout=60)
        r.raise_for_status()
        data = r.json()

        if not data or len(data) < 2:
            continue

        df = pd.DataFrame(data[1:], columns=data[0])

        # Keep NAICS code explicit (the API echoes it, but we enforce)
        df["NAICS2017"] = naics

        # Normalize numeric fields (CBP sometimes uses non-numeric placeholders)
        for col in ["EMP", "ESTAB"]:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)

        out_frames.append(df)

    if not out_frames:
        raise RuntimeError("No CBP data returned. Check your API key, year, and NAICS codes.")

    result = pd.concat(out_frames, ignore_index=True)

    if cache_path is not None:
        # save numeric columns as numbers, others as strings
        result.to_csv(cache_path, index=False)

    return result

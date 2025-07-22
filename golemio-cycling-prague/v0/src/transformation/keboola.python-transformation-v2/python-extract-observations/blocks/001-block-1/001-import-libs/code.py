#!/usr/bin/env python3
"""
Cyclist Observations Extractor
=============================

This script extracts cyclist observation data from the Golemio API by:
1. Reading direction IDs from the location_directions table
2. Making API calls to the detections endpoint for each direction
3. Collecting and outputting the results to cyclists_observations table

Input: location_directions table with direction_id column
Output: cyclists_observations table with cyclist detection data
"""

import os
import sys
import json
import csv
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

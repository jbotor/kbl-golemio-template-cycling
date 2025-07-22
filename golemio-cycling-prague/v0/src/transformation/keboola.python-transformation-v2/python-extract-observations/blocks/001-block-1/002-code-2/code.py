class CyclistObservationsExtractor:
    """
    Extracts cyclist observation data from Golemio API for multiple directions
    """
    
    def __init__(self, api_token: str, base_url: str = "https://api.golemio.cz/v2/"):
        """
        Initialize the extractor with API credentials
        
        Args:
            api_token: Golemio API token
            base_url: Base URL for Golemio API
        """
        self.api_token = api_token
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'accept': 'application/json; charset=utf-8',
            'x-access-token': api_token
        })
        
    def get_fixed_weekly_intervals(self, weeks_back: int = 3) -> List[tuple[str, str]]:
        """
        Calculate fixed weekly date intervals (Monday-Sunday) for API calls

        Args:
            weeks_back: Number of complete weeks to look back from current week

        Returns:
            List of (from_date, to_date) tuples in ISO format, one per complete week
        """
        INCLUDE_CURRENT_WEEK = {{include_current_week}}

        intervals = []
        today = datetime.now().date()

        # Find the Monday of current week (weekday() returns 0=Monday, 6=Sunday)
        current_monday = today - timedelta(days=today.weekday())

        # Determine the starting point for the range
        if INCLUDE_CURRENT_WEEK:
            # Include current week (week 0) and go back weeks_back-1 more weeks
            start_week = 0
            end_week = weeks_back
        else:
            # Original behavior: skip current week, start from week 1
            start_week = 1
            end_week = weeks_back + 1

        for i in range(start_week, end_week):
            # Calculate Monday and Sunday for week i weeks ago
            week_monday = current_monday - timedelta(weeks=i)
            week_sunday = week_monday + timedelta(days=6)  # 6 days after Monday

            # Create start and end timestamps for the week
            start_datetime = datetime.combine(week_monday, datetime.min.time())
            end_datetime = datetime.combine(week_sunday, datetime.max.time())

            # Format as ISO strings
            from_str = start_datetime.strftime("%Y-%m-%dT%H:%M:%S.000Z")
            to_str = end_datetime.strftime("%Y-%m-%dT%H:%M:%S.999Z")

            intervals.append((from_str, to_str))

            if i == 0:
                logger.info(f"Current week: {week_monday} (Monday) to {week_sunday} (Sunday)")
            else:
                logger.info(f"Week {i}: {week_monday} (Monday) to {week_sunday} (Sunday)")

        return intervals

    def read_direction_ids(self, input_file: str) -> List[str]:
        """
        Read direction IDs from input CSV file
        
        Args:
            input_file: Path to CSV file containing direction IDs
            
        Returns:
            List of direction IDs
        """
        try:
            direction_ids = []
            with open(input_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                # Check if required column exists
                if 'direction_id' not in reader.fieldnames:
                    raise ValueError("Input file must contain 'direction_id' column")
                
                for row in reader:
                    direction_id = row.get('direction_id', '').strip()
                    if direction_id:  # Skip empty values
                        direction_ids.append(direction_id)
            
            logger.info(f"Found {len(direction_ids)} direction IDs to process")
            return direction_ids
            
        except Exception as e:
            logger.error(f"Error reading direction IDs from {input_file}: {str(e)}")
            raise
    
    def call_detections_api(self, direction_id: str, from_date: str, to_date: str) -> List[Dict[str, Any]]:
        """
        Make API call to get cyclist detection data for a specific direction
        
        Args:
            direction_id: Direction ID to query
            from_date: Start date in ISO format
            to_date: End date in ISO format
            
        Returns:
            List of detection records
        """
        url = f"{self.base_url}bicyclecounters/detections"
        
        params = {
            'id': direction_id,
            'from': from_date,
            'to': to_date,
            'limit': 100,
            'offset': 0,
            'aggregate': 'true'
        }
        
        try:
            logger.info(f"Calling API for direction {direction_id}")
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            # API returns array of detection records
            if isinstance(data, list):
                logger.info(f"Retrieved {len(data)} records for direction {direction_id}")
                return data
            else:
                logger.warning(f"Unexpected response format for direction {direction_id}: {type(data)}")
                return []
                
        except requests.exceptions.RequestException as e:
            logger.error(f"API call failed for direction {direction_id}: {str(e)}")
            return []
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response for direction {direction_id}: {str(e)}")
            return []
    
    def transform_record(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transform API response record to match output schema
        
        Args:
            record: Raw API response record
            
        Returns:
            Transformed record matching cyclists_observations schema
        """
        return {
            'location_id': record.get('locations_id', ''),
            'observed_cyclists': record.get('value', ''),
            'location_direction_id': record.get('id', ''),
            'measured_from': record.get('measured_from', ''),
            'measured_to': record.get('measured_to', '')
        }
    
    def extract_all_observations(self, direction_ids: List[str], weeks_back: int = 3) -> List[Dict[str, Any]]:
        """
        Extract cyclist observations for all direction IDs across weekly intervals
        
        Args:
            direction_ids: List of direction IDs to process
            weeks_back: Number of weeks to look back
            
        Returns:
            List of all observation records
        """
        weekly_intervals = self.get_fixed_weekly_intervals(weeks_back)
        logger.info(f"Will process {len(weekly_intervals)} fixed weekly intervals for {len(direction_ids)} directions")
        logger.info(f"Date range: {weekly_intervals[-1][0]} to {weekly_intervals[0][1]}")
        
        all_observations = []
        total_calls = len(direction_ids) * len(weekly_intervals)
        call_count = 0
        
        for direction_id in direction_ids:
            logger.info(f"Processing direction: {direction_id}")
            
            # Process each weekly interval for this direction
            for from_date, to_date in weekly_intervals:
                call_count += 1
                logger.info(f"  API call {call_count}/{total_calls}: {from_date[:10]} to {to_date[:10]}")
                
                # Get data for this direction and weekly interval
                raw_records = self.call_detections_api(direction_id, from_date, to_date)
                
                # Transform records
                for record in raw_records:
                    transformed_record = self.transform_record(record)
                    all_observations.append(transformed_record)
                
                # Add small delay between requests
                if call_count < total_calls:  # Don't delay after the last request
                    import time
                    time.sleep(0.2)  # 100ms delay between requests
                    
            if call_count < total_calls:  # Don't delay after the last request
                    import time
                    time.sleep(0.4)  # 100ms delay between requests
        
        logger.info(f"Total observations extracted: {len(all_observations)}")
        return all_observations
    
    def write_output(self, observations: List[Dict[str, Any]], output_file: str):
        """
        Write observations to output CSV file
        
        Args:
            observations: List of observation records
            output_file: Path to output CSV file
        """
        try:
            # Ensure output directory exists
            output_dir = os.path.dirname(output_file)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            # Define column order
            column_order = [
                'location_id',
                'observed_cyclists', 
                'location_direction_id',
                'measured_from',
                'measured_to'
            ]
            
            # Write to CSV using standard library
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=column_order)
                writer.writeheader()
                
                for observation in observations:
                    # Ensure all required fields exist
                    row = {col: observation.get(col, '') for col in column_order}
                    writer.writerow(row)
            
            logger.info(f"Successfully wrote {len(observations)} observations to {output_file}")
            
        except Exception as e:
            logger.error(f"Error writing output to {output_file}: {str(e)}")
            raise

def main():
    """
    Main execution function
    """
    logger.info("Starting Cyclist Observations Extractor")
    
    # Debug: Print all environment variables
    logger.info("Available environment variables:")
    for key, value in os.environ.items():
        if 'TOKEN' in key.upper() or 'WEEK' in key.upper():
            logger.info(f"  {key}: {value[:50]}..." if len(value) > 50 else f"  {key}: {value}")
    
    # Get configuration from environment variables
    api_token = {{api_token}}
    weeks_back = 3
    
    # Remove quotes if present
    if api_token and api_token.startswith('"') and api_token.endswith('"'):
        api_token = api_token[1:-1]
    
    # Get input/output file paths
    input_file = 'in/tables/bicycle_counters_directions.csv'
    output_file = 'out/tables/bicycles_observations'
    
    # Debug: Check file system
    logger.info(f"Current working directory: {os.getcwd()}")
    logger.info(f"Contents of current directory: {os.listdir('.')}")
    if os.path.exists('in'):
        logger.info(f"Contents of 'in' directory: {os.listdir('in')}")
        if os.path.exists('in/tables'):
            logger.info(f"Contents of 'in/tables' directory: {os.listdir('in/tables')}")
    
    # Validate required parameters
    if not api_token:
        logger.error("API_TOKEN environment variable is required")
        sys.exit(1)
    
    if not os.path.exists(input_file):
        logger.error(f"Input file not found: {input_file}")
        sys.exit(1)
    
    try:
        # Initialize extractor
        extractor = CyclistObservationsExtractor(api_token)
        
        # Read direction IDs
        direction_ids = extractor.read_direction_ids(input_file)
        
        if not direction_ids:
            logger.warning("No direction IDs found in input file")
            # Create empty output file
            os.makedirs('out/tables', exist_ok=True)
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=[
                    'location_id', 'observed_cyclists', 'location_direction_id',
                    'measured_from', 'measured_to'
                ])
                writer.writeheader()
            return
        
        # Extract observations
        observations = extractor.extract_all_observations(direction_ids, weeks_back)
        
        # Write output
        extractor.write_output(observations, output_file)
        
        logger.info("Cyclist Observations Extractor completed successfully")
        
    except Exception as e:
        logger.error(f"Script execution failed: {str(e)}")
        sys.exit(1)

main()

The `Golemio Bicycle Counters - Complete Flow` is designed to extract and transform bicycle counter data. It consists of two sequential phases, each with specific tasks aimed at processing the data efficiently.

## Step 1
This phase focuses on data extraction. The task in this phase uses the `generic api extracotr` component to extract data from the Golemio API gateway to obtain amount of cyclists that passed certain "measurement locations" in Prague. The api is available at 'https://api.golemio.cz/docs/openapi/index.htm#/%F0%9F%A7%AE%20Bicycle%20Counters%20(v2)/get_v2_bicyclecounters'

## Step 2
This phase is dedicated to data transformation. It depends on the successful completion of Step 1. The task in this phase utilizes the python transformation `Cyclist observations extractor`. In this step, counts of cyclists per last 3 weeks are ingested

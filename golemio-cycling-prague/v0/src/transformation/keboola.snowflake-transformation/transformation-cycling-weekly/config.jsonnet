{
  parameters: {},
  storage: {
    input: {
      tables: [
        {
          source: "in.c-cycling_in_prague.bicycle_counters",
          destination: "bicycle_counters",
          where_column: "",
          where_values: [],
          where_operator: "eq",
          columns: [],
          keep_internal_timestamp_column: false,
        },
        {
          source: "in.c-cycling_in_prague.bicycle_counters_directions",
          destination: "bicycle_counters_directions",
          where_column: "",
          where_values: [],
          where_operator: "eq",
          columns: [],
          keep_internal_timestamp_column: false,
        },
        {
          source: "out.c-cyclists-in-prague.bicycles_observations",
          destination: "bicycles_observations",
          where_column: "",
          where_values: [],
          where_operator: "eq",
          columns: [],
          keep_internal_timestamp_column: false,
        },
      ],
    },
    output: {
      tables: [
        {
          destination: "out.c-Cycling-Analytics-Weekly-Summary.cyclists_weekly_summary",
          source: "cyclists_weekly_summary",
        },
      ],
    },
  },
}

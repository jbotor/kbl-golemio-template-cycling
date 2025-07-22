{
  storage: {
    input: {
      tables: [
        {
          source: "in.c-cycling_in_prague.bicycle_counters_directions",
          destination: "bicycle_counters_directions.csv",
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
          source: "bicycles_observations",
          destination: "out.c-cyclists-in-prague.bicycles_observations",
          primary_key: [],
        },
      ],
    },
  },
  parameters: {
    packages: [
      "requests>=2.28.0",
    ],
    variables: [
      {
        name: "api_token",
        type: "string",
        value: Input("ex-generic-v2-config-auth-token"),
      },
      {
        name: "include_current_week",
        type: "string",
        value: Input("transf-incl-current-week"),
      },
    ],
  },
}

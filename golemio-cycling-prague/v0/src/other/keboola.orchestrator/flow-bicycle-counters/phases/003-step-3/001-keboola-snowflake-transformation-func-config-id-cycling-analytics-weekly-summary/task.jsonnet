{
  name: "keboola.snowflake-transformation-" + ConfigId("cycling-analytics-weekly-summary"),
  enabled: true,
  task: {
    mode: "run",
    configPath: "transformation/keboola.snowflake-transformation/transformation-cycling-weekly",
  },
  continueOnFailure: false,
}

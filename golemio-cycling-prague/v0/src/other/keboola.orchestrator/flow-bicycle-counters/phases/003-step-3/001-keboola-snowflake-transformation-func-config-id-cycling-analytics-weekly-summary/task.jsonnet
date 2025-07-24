{
  name: "keboola.snowflake-transformation-" + ConfigId("cycling-analytics-weekly-summary"),
  enabled: true,
  task: {
    mode: "run",
    configPath: "transformation/keboola.snowflake-transformation/cycling-analytics-weekly-summary",
  },
  continueOnFailure: false,
}

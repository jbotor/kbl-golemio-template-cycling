{
  name: "keboola.python-transformation-v2-" + ConfigId("cyclist-observations-extractor"),
  enabled: true,
  task: {
    mode: "run",
    configPath: "transformation/keboola.python-transformation-v2/python-extract-observations",
  },
  continueOnFailure: false,
}

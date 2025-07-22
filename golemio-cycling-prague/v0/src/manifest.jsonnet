{
  configurations: [
    {
      componentId: "keboola.data-apps",
      id: ConfigId("prague-cycling-dashboard"),
      path: "app/keboola.data-apps/prague-cycling-dashboard",
      metadata: {
        "KBC.MCP.createdBy": "true",
        "KBC.MCP.updatedBy.version.3": "true",
      },
      rows: [],
    },
    {
      componentId: "ex-generic-v2",
      id: ConfigId("api-extractor-golemio"),
      path: "extractor/ex-generic-v2/api-extractor-golemio",
      rows: [],
    },
    {
      componentId: "keboola.orchestrator",
      id: ConfigId("flow-bicycle-counters"),
      path: "other/keboola.orchestrator/flow-bicycle-counters",
      metadata: {
        "KBC.MCP.createdBy": "true",
      },
      rows: [],
    },
    {
      componentId: "keboola.python-transformation-v2",
      id: ConfigId("python-extract-observations"),
      path: "transformation/keboola.python-transformation-v2/python-extract-observations",
      metadata: {
        "KBC.MCP.updatedBy.version.14": "true",
        "KBC.MCP.updatedBy.version.15": "true",
        "KBC.MCP.updatedBy.version.16": "true",
        "KBC.MCP.updatedBy.version.17": "true",
        "KBC.MCP.updatedBy.version.18": "true",
        "KBC.configuration.folderName": "Golemio-Cycling",
      },
      rows: [],
    },
    {
      componentId: "keboola.snowflake-transformation",
      id: ConfigId("transformation-cycling-weekly"),
      path: "transformation/keboola.snowflake-transformation/transformation-cycling-weekly",
      metadata: {
        "KBC.MCP.createdBy": "true",
        "KBC.MCP.updatedBy.version.2": "true",
        "KBC.configuration.folderName": "Golemio-Cycling",
      },
      rows: [],
    },
  ],
}

{
  parameters: {
    api: {
      baseUrl: "https://api.golemio.cz/v2/",
      http: {
        headers: {
          "x-access-token": {
            attr: "#__AUTH_TOKEN",
          },
        },
        retryHeader: "Retry-After",
        maxRetries: 10,
        codes: [
          408,
          420,
          429,
          500,
          502,
          503,
          504,
        ],
        connectTimeout: 30,
        requestTimeout: 300,
      },
    },
    config: {
      outputBucket: "cycling_in_prague",
      incrementalOutput: false,
      jobs: [
        {
          __NAME: "bicyclecounters",
          endpoint: "bicyclecounters",
          children: [],
          method: "GET",
          dataType: "bicycle_counters",
          dataField: {
            path: "features",
            separator: ".",
            delimiter: ".",
          },
          params: {
            latlng: "50.1003731,14.4459514",
            range: "3000",
            limit: "100",
            offset: "0",
          },
        },
      ],
      mappings: {
        bicycle_counters: {
          "properties.id": {
            type: "column",
            mapping: {
              destination: "id",
              primaryKey: true,
            },
          },
          "properties.name": {
            mapping: {
              destination: "name",
            },
          },
          "properties.route": {
            mapping: {
              destination: "route",
            },
          },
          "properties.updated_at": {
            mapping: {
              destination: "updated_at",
            },
          },
          "geometry.coordinates.1": {
            mapping: {
              destination: "lat",
            },
          },
          "geometry.coordinates.0": {
            mapping: {
              destination: "lon",
            },
          },
          "properties.directions": {
            type: "table",
            destination: "bicycle_counters_directions",
            parentKey: {
              primaryKey: true,
              destination: "counter_id",
            },
            tableMapping: {
              id: {
                mapping: {
                  destination: "direction_id",
                  primaryKey: true,
                },
              },
              name: {
                mapping: {
                  destination: "direction_name",
                },
              },
            },
          },
        },
      },
      debug: true,
      accept: "application/json; charset=utf-8",
      __AUTH_METHOD: "api-key",
      "#__AUTH_TOKEN": Input("ex-generic-v2-config-auth-token"),
      userData: {},
    },
  },
}

{
  stepsGroups: [
    {
      description: "Prague Cycling App Setup",
      required: "all",
      steps: [
        {
          icon: "common:settings",
          name: "Default Step",
          description: "Default Step",
          inputs: [
            {
              id: "ex-generic-v2-config-auth-token",
              name: "Config AUTH TOKEN",
              description: "Create authentication: https://api.golemio.cz/api-keys",
              type: "string",
              kind: "hidden"
            },
            {
              id: "transf-incl-current-week",
              name: "Include current week",
              description: "Should current week be included to report?",
              type: "bool",
              default: false,
              kind: "input"
            },
          ],
        },
      ],
    },
  ],
}

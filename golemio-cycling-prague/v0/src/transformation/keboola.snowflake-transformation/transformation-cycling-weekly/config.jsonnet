{
  parameters: {},
  storage: {
    input: {
      tables: [],
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

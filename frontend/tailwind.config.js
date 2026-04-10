export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        gambia: {
          red: "#CE1126",
          blue: "#0C1C8C",
          green: "#3A7728",
          gold: "#C9A227",
          white: "#FFFFFF"
        }
      },
      boxShadow: {
        soft: "0 20px 60px rgba(2, 6, 23, 0.08)"
      }
    }
  },
  plugins: []
};

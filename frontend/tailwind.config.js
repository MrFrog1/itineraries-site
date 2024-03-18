/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: "class", // Changed from array to string for correct syntax
  content: [
    './pages/**/*.{js,jsx,ts,tsx}', // Added ts, tsx for TypeScript support
    './components/**/*.{js,jsx,ts,tsx}',
    './app/**/*.{js,jsx,ts,tsx}',
    './src/**/*.{js,jsx,ts,tsx}',
  ],
  theme: {
    container: {
      center: true,
      padding: "2rem",
      screens: {
        "2xl": "1400px",
      },
    },
    extend: {
      keyframes: {
        "accordion-down": {
          from: { height: "0" },
          to: { height: "var(--radix-accordion-content-height)" },
        },
        "accordion-up": {
          from: { height: "var(--radix-accordion-content-height)" },
          to: { height: "0" },
        },
      },
      fontFamily: {
        roboto: ['Roboto', 'sans-serif'],
        montserrat: ['Montserrat', 'sans-serif'],
        optimaroman: ['OptimaRoman', 'serif'],

      },
      colors: {
        background: 'var(--background)',
        foreground: 'var(--foreground)',
        // ...
      },
      animation: {
        "accordion-down": "accordion-down 0.2s ease-out",
        "accordion-up": "accordion-up 0.2s ease-out",
      },
    },
  },
  plugins: [require('@tailwindcss/forms'), require('@tailwindcss/typography'), require("tailwindcss-animate")], // Added common plugins for forms and typography
};

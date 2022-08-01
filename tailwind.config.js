/** @type {import('tailwindcss').Config} */
module.exports = {
  mode: 'jit',
  content: ['./templates/*.html'],
  theme: {
    extend: {},
    screens: {
     'md': '1200px',
    }
  },
  plugins: [],
}

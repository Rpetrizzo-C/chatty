import { createApp } from 'vue'
import App from './App.vue'

// Vuetify
import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import * as labs from 'vuetify/labs/components'

const vuetify = createVuetify({
  components: {
    ...components,
    ...labs
  },
  directives,
  theme: {
    defaultTheme: 'light',
    themes: {
      light: {
        colors: {
          primary: '#6200EA', // Deep Purple
          secondary: '#9D46FF', // Lighter Purple
          accent: '#E0B0FF', // Light Purple
          background: '#F5F0FF', // Very Light Purple
          'message-other': '#E8E8E8', // Darker grey for better contrast
          'message-own': '#D1C4E9', // Light Purple for own messages
        }
      }
    }
  }
})

const app = createApp(App)
app.use(vuetify)
app.mount('#app') 
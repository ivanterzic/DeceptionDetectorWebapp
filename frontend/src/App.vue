<template>
  <div id="app">
    <!-- Input View -->
    <InputView 
      v-if="currentView === 'input'"
      :available-models="availableModels"
      :error="error"
      @analyze="analyzeText"
    />
    
    <!-- Loading Screen -->
    <LoadingScreen 
      v-else-if="currentView === 'loading'"
      @cancel="cancelAnalysis"
    />
    
    <!-- Analysis Results -->
    <AnalysisView 
      v-else-if="currentView === 'results'"
      :results="results"
      @back="goBack"
    />
  </div>
</template>

<script>
import axios from 'axios'
import config from './config.js'
import InputView from './views/InputView.vue'
import AnalysisView from './views/AnalysisView.vue'
import LoadingScreen from './components/LoadingScreen.vue'

export default {
  name: 'App',
  // Imported Components
  components: {
    InputView,
    AnalysisView,
    LoadingScreen
  },
  data() {
    // State management for the app
    return {
      currentView: 'input', // 'input', 'loading', 'results'
      availableModels: [],
      results: null,
      error: null,
      apiBaseUrl: config.apiBaseUrl,
      currentRequest: null
    }
  },
  // Lifecycle hook to load available models on mount
  mounted() {
    this.loadAvailableModels()
  },
  methods: {
    // method to load available models from the backend
    async loadAvailableModels() {
      try {
        const response = await axios.get(`${this.apiBaseUrl}/models`)
        this.availableModels = response.data
      } catch (error) {
        console.error('Failed to load models:', error)
        this.error = 'Failed to load available models. Please ensure the backend is running.'
      }
    },
    
    // method to handle text analysis, is called from InputView via event "analyze"
    async analyzeText(data) {
      this.currentView = 'loading'
      this.error = null
      this.results = null

      try {
        this.currentRequest = axios.post(`${this.apiBaseUrl}/predict`, {
          text: data.text,
          model: data.model
        })
        
        const response = await this.currentRequest
        this.results = response.data
        this.currentView = 'results'
        
      } catch (error) {
        if (error.name === 'CanceledError') {
          // Request was cancelled, go back to input
          this.currentView = 'input'
          return
        }
        
        console.error('Analysis failed:', error)
        this.error = error.response?.data?.error || 'Analysis failed. Please try again.'
        this.currentView = 'input'
      } finally {
        this.currentRequest = null
      }
    },
    
    // method to handle cancellation of analysis, is called from component LoadingScreen via event "cancel"
    cancelAnalysis() {
      if (this.currentRequest) {
        this.currentRequest.cancel?.()
        this.currentRequest = null
      }
      this.currentView = 'input'
    },
    
    // method to go back to input view from results view, is called from AnalysisView via event "back"
    goBack() {
      this.currentView = 'input'
      this.results = null
      this.error = null
    }
  }
}
</script>

<style>
#app {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

* {
  box-sizing: border-box;
}

body {
  margin: 0;
  padding: 0;
}

.card {
  border: none;
  border-radius: 10px;
}

.btn {
  border-radius: 6px;
  transition: all 0.2s ease;
}

.btn:hover {
  transform: translateY(-1px);
}
</style>

<template>
  <div id="app">
    <!-- Navigation Tabs -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
      <div class="container">
        <a class="navbar-brand d-flex align-items-center" href="#">
          <i class="fas fa-user-secret me-2 text-primary" style="font-size: 1.5rem;"></i>
          <span class="fw-bold">Deception Detector</span>
        </a>
        
        <!-- Tab Navigation -->
        <ul class="nav nav-tabs nav-tabs-transparent ms-auto">
          <li class="nav-item">
            <button 
              class="nav-link"
              :class="{ active: activeTab === 'analysis' }"
              @click="switchTab('analysis')"
            >
              <i class="fas fa-search me-1"></i>
              Analysis
            </button>
          </li>
          <li class="nav-item">
            <button 
              class="nav-link"
              :class="{ active: activeTab === 'training' }"
              @click="switchTab('training')"
            >
              <i class="fas fa-cogs me-1"></i>
              Fine-tuning
            </button>
          </li>
          <li class="nav-item">
            <button 
              class="nav-link"
              :class="{ active: activeTab === 'custom' }"
              @click="switchTab('custom')"
            >
              <i class="fas fa-code me-1"></i>
              Model Access
            </button>
          </li>
        </ul>
      </div>
    </nav>

    <!-- Tab Content -->
    <div class="tab-content">
      <!-- Analysis Tab -->
      <div v-if="activeTab === 'analysis'">
        <!-- Input View -->
        <InputView 
          v-if="analysisView === 'input'"
          :available-models="availableModels"
          :error="analysisError"
          @analyze="analyzeText"
        />
        
        <!-- Loading Screen -->
        <LoadingScreen 
          v-else-if="analysisView === 'loading'"
          @cancel="cancelAnalysis"
        />
        
        <!-- Analysis Results -->
        <AnalysisView 
          v-else-if="analysisView === 'results'"
          :results="analysisResults"
          @back="goBackAnalysis"
          @explanation-complete="onExplanationComplete"
        />
      </div>

      <!-- Training Tab -->
      <div v-if="activeTab === 'training'">
        <TrainingView 
          @training-started="onTrainingStarted"
        />
      </div>

      <!-- Custom Model Access Tab -->
      <div v-if="activeTab === 'custom'">
        <CustomModelView 
          :pending-model-code="pendingModelCode"
          @explanation-complete="onExplanationComplete"
          @clear-pending-code="pendingModelCode = null"
        />
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import config from './config.js'
import InputView from './views/InputView.vue'
import AnalysisView from './views/AnalysisView.vue'
import TrainingView from './views/TrainingView.vue'
import CustomModelView from './views/CustomModelView.vue'
import LoadingScreen from './components/LoadingScreen.vue'

export default {
  name: 'App',
  // Imported Components
  components: {
    InputView,
    AnalysisView,
    TrainingView,
    CustomModelView,
    LoadingScreen
  },
  data() {
    // State management for the app
    return {
      activeTab: 'analysis', // 'analysis', 'training', 'custom'
      analysisView: 'input', // 'input', 'loading', 'results'
      availableModels: [],
      analysisResults: null,
      analysisError: null,
      apiBaseUrl: config.apiBaseUrl,
      currentRequest: null,
      pendingModelCode: null // Store model code to pass to custom view
    }
  },
  // Lifecycle hook to load available models on mount
  mounted() {
    this.loadAvailableModels()
  },
  methods: {
    // Tab management
    switchTab(tab) {
      this.activeTab = tab
      if (tab === 'analysis') {
        // Reset analysis view when switching back
        this.analysisView = 'input'
        this.analysisResults = null
        this.analysisError = null
      }
    },

    // method to load available models from the backend
    async loadAvailableModels() {
      try {
        const response = await axios.get(`${this.apiBaseUrl}/models`)
        this.availableModels = response.data
      } catch (error) {
        console.error('Failed to load models:', error)
        this.analysisError = 'Failed to load available models. Please ensure the backend is running.'
      }
    },
    
    // method to handle text analysis, is called from InputView via event "analyze"
    async analyzeText(data) {
      this.analysisView = 'loading'
      this.analysisError = null
      this.analysisResults = null

      try {
        this.currentRequest = axios.post(`${this.apiBaseUrl}/predict`, {
          text: data.text,
          model: data.model
        })
        
        const response = await this.currentRequest
        this.analysisResults = response.data
        this.analysisView = 'results'
        
      } catch (error) {
        if (error.name === 'CanceledError') {
          // Request was cancelled, go back to input
          this.analysisView = 'input'
          return
        }
        
        console.error('Analysis failed:', error)
        this.analysisError = error.response?.data?.error || 'Analysis failed. Please try again.'
        this.analysisView = 'input'
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
      this.analysisView = 'input'
    },
    
    // method to go back to input view from results view, is called from AnalysisView via event "back"
    goBackAnalysis() {
      this.analysisView = 'input'
      this.analysisResults = null
      this.analysisError = null
    },

    // Event handlers
    onExplanationComplete() {
      // Explanation completed
    },

    onTrainingStarted() {
      // Model training started
    },

    // Method to set model code in custom model view
    setCustomModelCode(modelCode) {
      // Store the model code to be used by CustomModelView
      this.pendingModelCode = modelCode
    }
  }
}
</script>

<style>
#app {
  font-family: 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background-color: #f8f9fa;
  min-height: 100vh;
}

* {
  box-sizing: border-box;
}

body {
  margin: 0;
  padding: 0;
  background-color: #f8f9fa;
}

/* Typography */
h1, h2, h3, h4, h5, h6 {
  font-weight: 600;
  color: #2c3e50;
}

/* Card Improvements */
.card {
  border: none;
  border-radius: 15px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
}

.card:hover {
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.12);
}

.card-header {
  border-radius: 15px 15px 0 0 !important;
  border-bottom: none;
  padding: 1.5rem 1.5rem 1rem;
}

.card-body {
  padding: 1.5rem;
}

/* Button Improvements */
.btn {
  border-radius: 10px;
  font-weight: 500;
  padding: 0.5rem 1.5rem;
  transition: all 0.2s ease;
  border: none;
}

.btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.btn-outline-primary {
  border: 2px solid #667eea;
  color: #667eea;
}

.btn-outline-primary:hover {
  background: #667eea;
  border-color: #667eea;
}

.btn-lg {
  padding: 0.75rem 2rem;
  font-size: 1.1rem;
}

/* Form Elements */
.form-control, .form-select {
  border-radius: 10px;
  border: 1px solid #e1e5e9;
  padding: 0.75rem 1rem;
  transition: all 0.2s ease;
}

.form-control:focus, .form-select:focus {
  border-color: #667eea;
  box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25);
}

/* Navigation Styles */
.navbar {
  padding: 1rem 0;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.navbar-brand {
  font-size: 1.5rem;
  font-weight: 700;
}

.nav-tabs-transparent {
  border-bottom: none;
}

.nav-tabs-transparent .nav-link {
  border: none;
  color: rgba(255, 255, 255, 0.8);
  background: transparent;
  transition: all 0.3s ease;
  border-radius: 10px;
  margin: 0 0.25rem;
  font-weight: 500;
}

.nav-tabs-transparent .nav-link:hover {
  color: white;
  background: rgba(255, 255, 255, 0.15);
  transform: translateY(-1px);
}

.nav-tabs-transparent .nav-link.active {
  color: white;
  background: rgba(255, 255, 255, 0.25);
  border-bottom: none;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

/* Tab Content */
.tab-content {
  min-height: calc(100vh - 100px);
  padding: 2rem 0;
}

/* Container spacing */
.container {
  padding-left: 1.5rem;
  padding-right: 1.5rem;
}

/* Responsive Design */
@media (max-width: 768px) {
  .navbar-brand {
    font-size: 1.25rem;
  }
  
  .nav-tabs-transparent .nav-link {
    font-size: 0.9rem;
    padding: 0.5rem 0.75rem;
  }
  
  .container {
    padding-left: 1rem;
    padding-right: 1rem;
  }
  
  .tab-content {
    padding: 1rem 0;
  }
}

/* Loading Animation */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.card, .alert {
  animation: fadeIn 0.5s ease-out;
}

/* Scrollbar Styling */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
}

::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}
</style>

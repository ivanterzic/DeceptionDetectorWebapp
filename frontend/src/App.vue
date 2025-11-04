<template>
  <div id="app" :class="{ 'dark-mode': isDarkMode }">
    <!-- Navigation Tabs -->
    <nav class="navbar navbar-expand-lg navbar-light">
      <div class="container">
        <a class="navbar-brand d-flex align-items-center" href="#">
          <img :src="isDarkMode ? '/logo-dark.svg' : '/logo-light.svg'" alt="Deception Detector" class="logo-img me-2">
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
          
          <!-- Dark Mode Toggle -->
          <li class="nav-item ms-3">
            <button 
              class="nav-link theme-toggle"
              @click="toggleDarkMode"
              title="Toggle dark mode"
            >
              <i :class="isDarkMode ? 'fas fa-sun' : 'fas fa-moon'"></i>
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
      pendingModelCode: null, // Store model code to pass to custom view
      isDarkMode: false // Dark mode state
    }
  },
  // Lifecycle hook to load available models on mount
  mounted() {
    this.loadAvailableModels()
    this.loadDarkModePreference()
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
    },

    // Dark mode methods
    toggleDarkMode() {
      this.isDarkMode = !this.isDarkMode
      // Persist preference
      try {
        localStorage.setItem('darkMode', this.isDarkMode.toString())
      } catch (e) {
        // ignore localStorage errors (e.g., private mode)
      }

      // Apply to both body and #app root to ensure styles apply
      document.body.classList.toggle('dark-mode', this.isDarkMode)
      const appEl = document.getElementById('app')
      if (appEl) appEl.classList.toggle('dark-mode', this.isDarkMode)
      
      // Update favicon
      this.updateFavicon()
    },

    loadDarkModePreference() {
      // Load saved preference or fallback to OS preference
      let savedPreference = null
      try {
        savedPreference = localStorage.getItem('darkMode')
      } catch (e) {
        savedPreference = null
      }

      if (savedPreference !== null) {
        this.isDarkMode = savedPreference === 'true'
      } else if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
        this.isDarkMode = true
      } else {
        this.isDarkMode = false
      }

      // Ensure classes reflect the preference on both body and #app root
      document.body.classList.toggle('dark-mode', this.isDarkMode)
      const appEl = document.getElementById('app')
      if (appEl) appEl.classList.toggle('dark-mode', this.isDarkMode)
      
      // Update favicon
      this.updateFavicon()
    },
    
    updateFavicon() {
      // Update favicon based on dark mode
      const favicon = document.querySelector("link[rel*='icon']") || document.createElement('link')
      favicon.type = 'image/png'
      favicon.rel = 'icon'
      favicon.href = this.isDarkMode ? '/favicon-light.png' : '/favicon-dark.png'
      document.getElementsByTagName('head')[0].appendChild(favicon)
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
  color: #213544;
}

a {
  color: #FE483E;
  text-decoration: none;
  transition: color 0.2s ease;
}

a:hover {
  color: #e63d33;
  text-decoration: none;
}

.text-primary {
  color: #FE483E !important;
}

.bg-primary {
  background-color: #FE483E !important;
}

.border-primary {
  border-color: #FE483E !important;
}

/* Card Improvements */
.card {
  border: none;
  border-radius: 15px;
  box-shadow: 0 2px 10px rgba(33, 53, 68, 0.08);
  transition: all 0.3s ease;
}

.card:hover {
  box-shadow: 0 4px 20px rgba(33, 53, 68, 0.12);
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
  box-shadow: 0 4px 12px rgba(254, 72, 62, 0.25);
}

.btn-primary {
  background: linear-gradient(135deg, #FE483E 0%, #FF6B63 100%);
}

.btn-outline-primary {
  border: 2px solid #FE483E;
  color: #FE483E;
}

.btn-outline-primary:hover {
  background: #FE483E;
  border-color: #FE483E;
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
  border-color: #FE483E;
  box-shadow: 0 0 0 0.2rem rgba(254, 72, 62, 0.25);
}

/* Navigation Styles */
.navbar {
  padding: 1rem 0;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%) !important;
}

.navbar.navbar-dark {
  background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%) !important;
}

.navbar-brand {
  font-size: 1.5rem;
  font-weight: 700;
}

.logo-img {
  height: 40px;
  width: auto;
  transition: transform 0.3s ease;
}

.navbar-brand:hover .logo-img {
  transform: scale(1.05);
}

.nav-tabs-transparent {
  border-bottom: none;
}

.nav-tabs-transparent .nav-link {
  border: none;
  color: #213544;
  background: transparent;
  transition: all 0.3s ease;
  border-radius: 10px;
  margin: 0 0.25rem;
  font-weight: 500;
}

.nav-tabs-transparent .nav-link:hover {
  color: #FE483E;
  background: rgba(254, 72, 62, 0.1);
  transform: translateY(-1px);
}

.nav-tabs-transparent .nav-link.active {
  color: white;
  background: linear-gradient(135deg, #FE483E 0%, #FF6B63 100%);
  border-bottom: none;
  box-shadow: 0 2px 8px rgba(254, 72, 62, 0.3);
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

/* ========================================
   DARK MODE STYLES
   ======================================== */

/* Dark Mode Root */
#app.dark-mode {
  background-color: #1a1a1a;
  color: #e0e0e0;
  min-height: 100vh;
}

body.dark-mode {
  background-color: #1a1a1a !important;
  color: #e0e0e0;
}

.dark-mode * {
  scrollbar-color: #5d5d5d #2d2d2d;
}

/* Dark Mode Typography */
.dark-mode h1,
.dark-mode h2,
.dark-mode h3,
.dark-mode h4,
.dark-mode h5,
.dark-mode h6 {
  color: #ffffff;
}

.dark-mode p,
.dark-mode span,
.dark-mode label {
  color: #e0e0e0;
}

/* Dark Mode Navbar */
.dark-mode .navbar {
  background: linear-gradient(135deg, #2d2d2d 0%, #1a1a1a 100%) !important;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.5);
}

.dark-mode .nav-tabs-transparent .nav-link {
  color: #e0e0e0;
}

.dark-mode .nav-tabs-transparent .nav-link:hover {
  color: #FE483E;
  background: rgba(254, 72, 62, 0.15);
}

.dark-mode .nav-tabs-transparent .nav-link.active {
  color: white;
  background: linear-gradient(135deg, #FE483E 0%, #FF6B63 100%);
}

/* Theme Toggle Button */
.theme-toggle {
  background: transparent !important;
  border: 2px solid transparent;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  padding: 0 !important;
}

.theme-toggle:hover {
  border-color: #FE483E;
  background: rgba(254, 72, 62, 0.1) !important;
  transform: rotate(15deg);
}

.dark-mode .theme-toggle {
  color: #ffd700;
}

.theme-toggle i {
  font-size: 1.2rem;
}

/* Dark Mode Cards */
.dark-mode .card {
  background-color: #2d2d2d;
  border: 1px solid #3d3d3d;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
  border-radius: 15px;
}

.dark-mode .card:hover {
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
}

.dark-mode .card-header {
  background-color: #252525;
  border-bottom: 1px solid #3d3d3d;
  color: #ffffff;
  border-radius: 15px 15px 0 0 !important;
}

.dark-mode .card-body {
  background-color: #2d2d2d;
  border-radius: 0 0 15px 15px;
}

/* Dark Mode Forms */
.dark-mode .form-control,
.dark-mode .form-select {
  background-color: #3d3d3d;
  border-color: #4d4d4d;
  color: #ffffff !important;
  border-radius: 10px;
}

.dark-mode .form-control:focus,
.dark-mode .form-select:focus {
  background-color: #3d3d3d;
  border-color: #FE483E;
  color: #ffffff !important;
  box-shadow: 0 0 0 0.2rem rgba(254, 72, 62, 0.25);
  border-radius: 10px;
}

.dark-mode .form-control::placeholder {
  color: #888;
}

.dark-mode .form-control:disabled {
  background-color: #2a2a2a;
  color: #666;
}

/* Dark Mode Buttons */
.dark-mode .btn-outline-secondary {
  border-color: #4d4d4d;
  color: #e0e0e0;
}

.dark-mode .btn-outline-secondary:hover {
  background-color: #4d4d4d;
  border-color: #5d5d5d;
  color: #ffffff;
}

.dark-mode .btn-secondary {
  background-color: #4d4d4d;
  border-color: #4d4d4d;
}

.dark-mode .btn-secondary:hover {
  background-color: #5d5d5d;
  border-color: #6d6d6d;
}

/* Dark Mode Alerts */
.dark-mode .alert {
  background-color: #2d2d2d;
  border-color: #3d3d3d;
  color: #e0e0e0;
}

.dark-mode .alert-danger {
  background-color: #3d2222;
  border-color: #5d3333;
  color: #ff8080;
}

.dark-mode .alert-success {
  background-color: #223d22;
  border-color: #335d33;
  color: #80ff80;
}

.dark-mode .alert-info {
  background-color: #22333d;
  border-color: #33505d;
  color: #80c0ff;
}

.dark-mode .alert-warning {
  background-color: #3d3522;
  border-color: #5d5033;
  color: #ffd080;
}

/* Dark Mode Badges */
.dark-mode .badge {
  background-color: #3d3d3d;
  color: #e0e0e0;
}

.dark-mode .badge-success {
  background-color: #2d5d2d;
}

.dark-mode .badge-danger {
  background-color: #5d2d2d;
}

/* Dark Mode Tables */
.dark-mode table {
  color: #e0e0e0;
}

.dark-mode .table {
  border-color: #3d3d3d;
}

.dark-mode .table thead th {
  background-color: #252525;
  border-color: #3d3d3d;
  color: #ffffff;
}

.dark-mode .table tbody td {
  border-color: #3d3d3d;
}

.dark-mode .table-striped tbody tr:nth-of-type(odd) {
  background-color: #2a2a2a;
}

/* Dark Mode Modal */
.dark-mode .modal-content {
  background-color: #2d2d2d;
  border: 1px solid #3d3d3d;
}

.dark-mode .modal-header {
  background-color: #252525;
  border-bottom: 1px solid #3d3d3d;
}

.dark-mode .modal-footer {
  background-color: #252525;
  border-top: 1px solid #3d3d3d;
}

.dark-mode .modal-title {
  color: #ffffff;
}

.dark-mode .btn-close {
  filter: invert(1);
}

/* Dark Mode Progress Bars */
.dark-mode .progress {
  background-color: #3d3d3d;
}

/* Dark Mode Scrollbar */
.dark-mode ::-webkit-scrollbar-track {
  background: #2d2d2d;
}

.dark-mode ::-webkit-scrollbar-thumb {
  background: #5d5d5d;
}

.dark-mode ::-webkit-scrollbar-thumb:hover {
  background: #6d6d6d;
}

/* Dark Mode Links */
.dark-mode a {
  color: #FF6B63;
}

.dark-mode a:hover {
  color: #FE483E;
}

/* Dark Mode Text Colors */
.dark-mode .text-muted {
  color: #999 !important;
}

.dark-mode .text-secondary {
  color: #aaa !important;
}

/* Dark Mode Borders */
.dark-mode .border {
  border-color: #3d3d3d !important;
}

.dark-mode hr {
  border-color: #3d3d3d;
  opacity: 1;
}

/* Dark Mode List Groups */
.dark-mode .list-group-item {
  background-color: #2d2d2d;
  border-color: #3d3d3d;
  color: #e0e0e0;
}

.dark-mode .list-group-item:hover {
  background-color: #3d3d3d;
}

/* Dark Mode Dropdowns */
.dark-mode .dropdown-menu {
  background-color: #2d2d2d;
  border-color: #3d3d3d;
}

.dark-mode .dropdown-item {
  color: #e0e0e0;
}

.dark-mode .dropdown-item:hover {
  background-color: #3d3d3d;
  color: #ffffff;
}

/* Dark Mode Utility Classes */
.dark-mode .bg-light {
  background-color: #2d2d2d !important;
}

.dark-mode .bg-white {
  background-color: #252525 !important;
}

.dark-mode .bg-light-success {
  background-color: rgba(40, 167, 69, 0.15) !important;
}

.dark-mode .bg-light-danger {
  background-color: rgba(220, 53, 69, 0.15) !important;
}

.dark-mode .requirements-panel {
  background-color: #2d2d2d !important;
  color: #e0e0e0 !important;
  border-radius: inherit;
}

.dark-mode .configuration-section {
  background-color: #2d2d2d !important;
  color: #e0e0e0 !important;
  border-radius: inherit;
}

.dark-mode .info-card {
  background-color: #2d2d2d !important;
  border-color: #3d3d3d !important;
  color: #e0e0e0 !important;
  border-radius: inherit;
}

.dark-mode .upload-area {
  background-color: #252525 !important;
  color: #e0e0e0 !important;
  border-radius: 12px !important;
}

.dark-mode .upload-area.border-success.bg-light-success {
  background-color: rgba(40, 167, 69, 0.1) !important;
}

.dark-mode .upload-area.border-danger.bg-light-danger {
  background-color: rgba(220, 53, 69, 0.1) !important;
}

.dark-mode .tab-content {
  background-color: transparent !important;
}

.dark-mode .container {
  background-color: transparent !important;
}

/* Preserve rounded corners in dark mode */
.dark-mode .rounded {
  border-radius: 0.375rem !important;
}

.dark-mode .rounded-3 {
  border-radius: 0.5rem !important;
}

.dark-mode .alert {
  border-radius: 10px;
}

.dark-mode .text-display {
  border-radius: 10px;
}

/* Smooth Transitions for Mode Switch */
#app,
.navbar,
.card,
.form-control,
.form-select,
.btn,
.modal-content,
.table {
  transition: background-color 0.3s ease, color 0.3s ease, border-color 0.3s ease;
}
</style>

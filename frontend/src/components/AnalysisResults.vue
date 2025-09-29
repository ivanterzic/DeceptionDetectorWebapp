<template>
  <div class="analysis-results">
    <div class="container">
      <!-- Header with back button -->
      <div class="row mb-4">
        <div class="col">
          <button @click="$emit('back')" class="btn btn-outline-primary mb-3">
            <i class="fas fa-arrow-left me-2"></i>
            Analyze Another Text
          </button>
          <h2 class="mb-0">Analysis Results</h2>
        </div>
      </div>

      <!-- Prediction Results -->
      <div class="row mb-4">
        <div class="col-md-6">
          <div class="card border-0 shadow-sm result-card">
            <div class="card-body text-center">
              <div class="result-icon mb-3">
                <i 
                  :class="results.prediction === 'deceptive' ? 'fas fa-times-circle text-danger' : 'fas fa-check-circle text-success'"
                  style="font-size: 3rem;"
                ></i>
              </div>
              <h6 class="card-title text-muted">Prediction</h6>
              <h3 :class="results.prediction === 'deceptive' ? 'text-danger' : 'text-success'">
                {{ formatPrediction(results.prediction) }}
              </h3>
              <p class="text-muted small mb-0">
                The text appears to be {{ results.prediction === 'deceptive' ? 'deceptive' : 'truthful' }}
              </p>
            </div>
          </div>
        </div>
        <div class="col-md-6">
          <div class="card border-0 shadow-sm result-card">
            <div class="card-body text-center">
              <div class="confidence-circle mb-3">
                <svg width="80" height="80" class="confidence-svg">
                  <circle
                    cx="40"
                    cy="40"
                    r="35"
                    stroke="#e9ecef"
                    stroke-width="6"
                    fill="none"
                  />
                  <circle
                    cx="40"
                    cy="40"
                    r="35"
                    :stroke="results.prediction === 'deceptive' ? '#dc3545' : '#28a745'"
                    stroke-width="8"
                    fill="none"
                    stroke-linecap="round"
                    :stroke-dasharray="circumference"
                    :stroke-dashoffset="circumference - (results.confidence * circumference)"
                    class="confidence-progress"
                  />
                </svg>
                <div class="confidence-text">
                  {{ (results.confidence * 100).toFixed(1) }}%
                </div>
              </div>
              <h6 class="card-title text-muted">Confidence</h6>
              <p class="text-muted small mb-0">
                Model confidence in this prediction
              </p>
            </div>
          </div>
        </div>
      </div>

      <!-- Text Analysis -->
      <div class="row mb-4">
        <div class="col">
          <div class="card border-0 shadow-sm">
            <div class="card-body">
              <h6 class="mb-3">
                <i class="fas fa-text-width me-2"></i>
                Original Text
              </h6>
              <div class="text-display p-3 border rounded bg-light">
                {{ results.original_text }}
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Explainable AI Tabs -->
      <div class="row">
        <div class="col">
          <div class="card border-0 shadow-sm">
            <div class="card-header bg-white">
              <h5 class="mb-0">
                <i class="fas fa-brain me-2"></i>
                Explainable AI Analysis
              </h5>
            </div>
            <div class="card-body">
              <ul class="nav nav-tabs" role="tablist">
                <li class="nav-item" role="presentation">
                  <button
                    class="nav-link active"
                    data-bs-toggle="tab"
                    data-bs-target="#lime-tab"
                    type="button"
                    role="tab"
                    @click="onTabChange('lime')"
                  >
                    <i class="fas fa-lightbulb me-2"></i>
                    LIME Explanation
                  </button>
                </li>
                <li class="nav-item" role="presentation">
                  <button
                    class="nav-link"
                    data-bs-toggle="tab"
                    data-bs-target="#shap-tab"
                    type="button"
                    role="tab"
                    @click="onTabChange('shap')"
                  >
                    <i class="fas fa-chart-bar me-2"></i>
                    SHAP Explanation
                  </button>
                </li>
              </ul>

              <div class="tab-content mt-3">
                <!-- LIME Tab -->
                <div class="tab-pane fade show active" id="lime-tab" role="tabpanel">
                  <LimeExplanation 
                    :lime-explanation="limeExplanation"
                    :loading="limeLoading"
                    :error="limeError"
                    @load-explanation="loadLimeExplanation"
                  />
                </div>

                <!-- SHAP Tab -->
                <div class="tab-pane fade" id="shap-tab" role="tabpanel">
                  <ShapExplanation 
                    :shap-explanation="shapExplanation"
                    :loading="shapLoading"
                    :error="shapError"
                    @load-explanation="loadShapExplanation"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Model Information -->
      <div class="row mt-4">
        <div class="col">
          <div class="card border-0 bg-light">
            <div class="card-body">
              <small class="text-muted">
                <i class="fas fa-info-circle me-2"></i>
                <!-- TODO: decide wether to use formatted name or not-->
                Analysis performed using {{ results.model_used }} model
              </small>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import config from '../config.js'
import LimeExplanation from './LimeExplanation.vue'
import ShapExplanation from './ShapExplanation.vue'

export default {
  name: 'AnalysisResults',
  components: {
    LimeExplanation,
    ShapExplanation
  },
  props: {
    results: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      limeExplanation: null,
      shapExplanation: null,
      limeLoading: false,
      shapLoading: false,
      limeError: null,
      shapError: null,
      apiBaseUrl: config.apiBaseUrl
    }
  },
  computed: {
    circumference() {
      return 2 * Math.PI * 35 // radius is 35
    }
  },
  methods: {
    formatPrediction(prediction) {
      if (prediction === 'deceptive') return 'Deceptive'
      if (prediction === 'truthful') return 'Truthful'
      return prediction.charAt(0).toUpperCase() + prediction.slice(1)
    },
    
    async loadLimeExplanation() {
      if (this.limeLoading || this.limeExplanation) return
      
      this.limeLoading = true
      this.limeError = null
      
      try {
        const response = await axios.post(`${this.apiBaseUrl}/explain/lime`, {
          text: this.results.original_text,
          model: this.results.model_used
        })
        this.limeExplanation = response.data.lime_explanation
      } catch (error) {
        console.error('Failed to load LIME explanation:', error)
        this.limeError = error.response?.data?.error || 'Failed to load LIME explanation'
      } finally {
        this.limeLoading = false
      }
    },
    
    async loadShapExplanation() {
      if (this.shapLoading || this.shapExplanation) return
      
      this.shapLoading = true
      this.shapError = null
      
      try {
        const response = await axios.post(`${this.apiBaseUrl}/explain/shap`, {
          text: this.results.original_text,
          model: this.results.model_used
        })
        this.shapExplanation = response.data.shap_explanation
      } catch (error) {
        console.error('Failed to load SHAP explanation:', error)
        this.shapError = error.response?.data?.error || 'Failed to load SHAP explanation'
      } finally {
        this.shapLoading = false
      }
    },
    
    onTabChange(tab) {
      // Explanations are already loading from mounted(), but this ensures they're loaded if user manually retries
      if (tab === 'shap' && !this.shapExplanation && !this.shapLoading) {
        this.loadShapExplanation()
      }
      if (tab === 'lime' && !this.limeExplanation && !this.limeLoading) {
        this.loadLimeExplanation()
      }
    }
  },
  
  mounted() {
    // Auto-load both LIME and SHAP explanations immediately when results are displayed
    this.loadLimeExplanation()
    this.loadShapExplanation()
  }
}
</script>

<style scoped>
.analysis-results {
  min-height: 100vh;
  background: #f8f9fa;
  padding: 2rem 0;
}

.result-card {
  height: 100%;
  border-radius: 10px;
}

.result-icon {
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.05);
  }
  100% {
    transform: scale(1);
  }
}

.confidence-circle {
  position: relative;
  display: inline-block;
}

.confidence-svg {
  transform: rotate(-90deg);
}

.confidence-progress {
  transition: stroke-dashoffset 1s ease-in-out;
}

.confidence-text {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-weight: bold;
  font-size: 1.1rem;
}

.card {
  border-radius: 10px;
}

.nav-tabs .nav-link {
  border-radius: 6px 6px 0 0;
}
</style>

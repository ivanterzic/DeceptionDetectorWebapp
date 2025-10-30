<template>
  <div class="custom-model-view">
    <div class="container mt-4">
    <!-- Header -->
    <div class="row">
      <div class="col-12">
        <div class="card shadow border-0">
          <div class="card-header bg-primary text-white">
            <h3 class="card-title mb-0">
              <i class="fas fa-code me-2"></i>
              Custom Model Access
            </h3>
            <p class="mb-0 mt-2 small opacity-90">
              Enter your 6-digit model code to access your trained model
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- Model Code Input -->
    <div class="row mt-4" v-if="currentView === 'input'">
      <div class="col-lg-6 mx-auto">
        <div class="card shadow border-0">
          <div class="card-body p-5">
            <div class="text-center mb-4">
              <div class="model-code-icon mb-3">
                <i class="fas fa-key text-primary" style="font-size: 3rem;"></i>
              </div>
              <h5 class="card-title">Enter Model Code</h5>
              <p class="text-muted">Access your fine-tuned deception detection model</p>
            </div>
            
            <div class="mb-4">
              <label for="modelCode" class="form-label fw-semibold">6-Digit Model Code</label>
              <input 
                type="text" 
                class="form-control form-control-lg text-center model-code-input" 
                id="modelCode"
                v-model="modelCode"
                placeholder="ABC123"
                maxlength="6"
                @input="formatModelCode"
                @keyup.enter="loadModel"
              >
              <div class="form-text text-center mt-2">
                <small><i class="fas fa-info-circle me-1"></i>Enter the code you received when training started</small>
              </div>
            </div>

            <div class="d-grid">
              <button 
                class="btn btn-primary btn-lg py-3"
                @click="loadModel"
                :disabled="!isValidCode || isLoading"
              >
                <i class="fas fa-search me-2"></i>
                {{ isLoading ? 'Loading Model...' : 'Access Model' }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Model Status (Training) -->
    <div class="row mt-4" v-if="currentView === 'training'">
      <div class="col-lg-8 mx-auto">
        <div class="card shadow border-0">
          <div class="card-body text-center p-5">
            <div class="mb-4">
              <div class="training-animation mb-4">
                <i v-if="modelInfo.status === 'failed'" class="fas fa-times-circle fa-3x text-danger"></i>
                <i v-else class="fas fa-cog fa-3x text-warning fa-spin"></i>
              </div>
              <h4 :class="modelInfo.status === 'failed' ? 'text-danger' : 'text-warning'" class="mb-3">
                {{ modelInfo.status === 'failed' ? 'Model Training Failed' : 'Model Training in Progress' }}
              </h4>
              <p class="text-muted mb-0">
                Model <span class="badge bg-primary">{{ modelCode }}</span> 
                {{ modelInfo.status === 'failed' ? 'failed to train.' : 'is still being trained.' }}
              </p>
              <p v-if="modelInfo.status === 'failed' && modelInfo.error" class="text-danger small mt-2">
                <i class="fas fa-exclamation-triangle me-1"></i>
                Error: {{ modelInfo.error }}
              </p>
            </div>

            <div v-if="modelInfo" class="model-info-grid mb-4">
              <div class="row g-3">
                <div class="col-md-4">
                  <div class="info-card p-3 bg-white border rounded">
                    <h6 class="text-secondary mb-1">Model Name</h6>
                    <p class="fw-bold text-dark mb-0">{{ modelInfo.name }}</p>
                  </div>
                </div>
                <div class="col-md-4">
                  <div class="info-card p-3 bg-white border rounded">
                    <h6 class="text-secondary mb-1">Base Model</h6>
                    <p class="fw-bold text-dark mb-0">{{ modelInfo.base_model }}</p>
                  </div>
                </div>
                <div class="col-md-4">
                  <div class="info-card p-3 bg-white border rounded">
                    <h6 class="text-secondary mb-1">Status</h6>
                    <p class="fw-bold text-dark mb-0 text-capitalize">
                      <i v-if="modelInfo.status === 'failed'" class="fas fa-times-circle text-danger me-1"></i>
                      <i v-else-if="modelInfo.status === 'training'" class="fas fa-cog fa-spin text-warning me-1"></i>
                      <i v-else-if="modelInfo.status === 'completed'" class="fas fa-check-circle text-success me-1"></i>
                      {{ modelInfo.status }}
                    </p>
                  </div>
                </div>
              </div>
              
              <!-- Dataset Information Row -->
              <div class="row g-3 mt-2" v-if="modelInfo.train_size">
                <div class="col-md-3">
                  <div class="info-card p-3 bg-light border rounded">
                    <h6 class="text-secondary mb-1">Training Data</h6>
                    <p class="fw-bold text-primary mb-0">{{ modelInfo.train_size }} samples</p>
                  </div>
                </div>
                <div class="col-md-3">
                  <div class="info-card p-3 bg-light border rounded">
                    <h6 class="text-secondary mb-1">Validation Data</h6>
                    <p class="fw-bold text-primary mb-0">{{ modelInfo.val_size }} samples</p>
                  </div>
                </div>
                <div class="col-md-3">
                  <div class="info-card p-3 bg-light border rounded">
                    <h6 class="text-secondary mb-1">Learning Rate</h6>
                    <p class="fw-bold text-info mb-0">{{ modelInfo.learning_rate }}</p>
                  </div>
                </div>
                <div class="col-md-3">
                  <div class="info-card p-3 bg-light border rounded">
                    <h6 class="text-secondary mb-1">Epochs</h6>
                    <p class="fw-bold text-info mb-0">{{ modelInfo.epochs }}</p>
                  </div>
                </div>
              </div>
            </div>

            <div v-if="modelInfo.status === 'training'" class="alert alert-warning border-0 rounded">
              <i class="fas fa-clock me-2"></i>
              <strong>Please wait:</strong> Your model is currently being trained. This process takes time to complete depending on your dataset size and configuration.
              You can bookmark this page and check back later.
            </div>
            
            <div v-else-if="modelInfo.status === 'failed'" class="alert alert-danger border-0 rounded">
              <i class="fas fa-exclamation-triangle me-2"></i>
              <strong>Training Failed:</strong> The model training process encountered an error. 
              Please try training again with different parameters or contact support if the issue persists.
            </div>

            <div class="action-buttons">
              <button class="btn btn-outline-secondary me-3" @click="goBack">
                <i class="fas fa-arrow-left me-2"></i>
                Back to Input
              </button>
              <button class="btn btn-outline-primary" @click="refreshStatus">
                <i class="fas fa-sync me-2"></i>
                Refresh Status
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Model Analysis Interface -->
    <div class="row mt-4" v-if="currentView === 'analysis'">
      <div class="col-12">
        <!-- Model Info Header -->
        <div class="card shadow border-0 mb-4">
          <div class="card-body p-4">
            <div class="row align-items-center">
              <div class="col-md-8">
                <h4 class="mb-2">
                  <i class="fas fa-robot me-2 text-success"></i>
                  {{ modelInfo.name }}
                </h4>
                <p class="text-muted mb-3">{{ modelInfo.notes || 'No description provided' }}</p>
                <div class="d-flex flex-wrap gap-2">
                  <span class="badge bg-secondary fs-6 px-3 py-2">
                    <i class="fas fa-microchip me-1"></i>{{ modelInfo.base_model }}
                  </span>
                  <span class="badge bg-info fs-6 px-3 py-2">
                    <i class="fas fa-repeat me-1"></i>{{ modelInfo.epochs }} epochs
                  </span>
                  <span v-if="modelInfo.accuracy !== null" class="badge bg-success fs-6 px-3 py-2">
                    <i class="fas fa-chart-line me-1"></i>{{ (modelInfo.accuracy * 100).toFixed(1) }}% validation accuracy
                  </span>
                  <span class="badge bg-warning text-dark fs-6 px-3 py-2">
                    <i class="fas fa-clock me-1"></i>{{ modelInfo.remaining_time }} remaining
                  </span>
                </div>
              </div>
              <div class="col-md-4 text-end">
                <div class="btn-group">
                  <button class="btn btn-outline-success" @click="downloadModel">
                    <i class="fas fa-download me-2"></i>
                    Download Model
                  </button>
                  <button class="btn btn-outline-secondary" @click="goBack">
                    <i class="fas fa-arrow-left me-2"></i>
                    Back
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Text Analysis -->
        <div class="row">
          <div class="col-12">
            <!-- Show Text Input Form when no results -->
            <div v-if="!analysisResults">
              
              <!-- Text Input Form -->
              <TextAnalysisForm
                v-if="!isAnalyzing && !analysisResults"
                :show-model-selection="false"
                :show-model-info="false"
                :button-text="'Analyze Text'"
                :is-loading="false"
                :initial-text="analysisText"
                @analyze="handleAnalyze"
                @text-changed="analysisText = $event"
              />
              
              <!-- Loading Screen during analysis -->
              <LoadingScreen 
                v-else-if="isAnalyzing"
                title="Analyzing Text..."
                message="Processing your text with the custom model"
                :showCancelButton="true"
                @cancel="cancelAnalysis"
              />
            </div>
            
            <!-- Show Analysis Results when available -->
            <AnalysisResults 
              v-if="analysisResults"
              :results="analysisResults"
              :lime-endpoint="`${apiBaseUrl}/custom/explain/lime/${modelCode}`"
              :shap-endpoint="`${apiBaseUrl}/custom/explain/shap/${modelCode}`"
              @back="clearResults"
            />
          </div>
        </div>

        <!-- Error Display -->
        <div class="row mt-4" v-if="error">
          <div class="col-lg-8 mx-auto">
            <div class="alert alert-danger">
              <i class="fas fa-exclamation-triangle me-2"></i>
              <strong>Error:</strong> {{ error }}
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Download Progress Modal -->
    <div v-if="showDownloadProgress" class="modal fade show d-block" tabindex="-1" style="background-color: rgba(0,0,0,0.5);">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header bg-primary text-white">
            <h5 class="modal-title" style="color: white;">
              <i class="fas fa-download me-2"></i>
              Downloading Model {{ modelCode }}
            </h5>
          </div>
          <div class="modal-body text-center bg-primary">
            <div class="mb-4">
              <div class="progress-circle mb-3">
                <div class="progress-circle-inner">
                  <span class="progress-percentage">{{ downloadProgress?.progress || 0 }}%</span>
                </div>
                <svg class="progress-circle-svg" width="120" height="120">
                  <circle 
                    cx="60" cy="60" r="50" 
                    stroke="#e9ecef" 
                    stroke-width="8" 
                    fill="none"
                  />
                  <circle 
                    cx="60" cy="60" r="50" 
                    stroke="#667eea" 
                    stroke-width="8" 
                    fill="none"
                    stroke-linecap="round"
                    :stroke-dasharray="`${(downloadProgress?.progress || 0) * 3.14} 314`"
                    transform="rotate(-90 60 60)"
                  />
                </svg>
              </div>
              
              <h6 class="mb-2" style="color: white;">{{ downloadProgress?.phase || 'Initializing...' }}</h6>
              
              <div v-if="downloadProgress?.elapsed_time" class="text-sm">
                <small style="color: white;">Elapsed: {{ Math.round(downloadProgress.elapsed_time) }}s</small>
              </div>
              
              <div v-if="downloadProgress?.archive_size_mb" class="text-sm mt-1">
                <small style="color: white;">Archive size: {{ downloadProgress.archive_size_mb.toFixed(1) }} MB</small>
              </div>
            </div>
            
            <div v-if="downloadProgress?.status === 'failed'" class="alert alert-danger">
              <i class="fas fa-exclamation-triangle me-2"></i>
              {{ downloadProgress.error || 'Download failed' }}
            </div>
            
            <div v-if="downloadProgress?.status === 'completed'" class="alert alert-success">
              <i class="fas fa-check-circle me-2"></i>
              File compressing completed! Your browser should start downloading the file.
            </div>
          </div>
          <div class="modal-footer">
            <button 
              type="button" 
              class="btn btn-secondary" 
              @click="cancelDownload"
              :disabled="downloadProgress?.status === 'completed'"
            >
              <i class="fas fa-times me-1"></i>
              {{ downloadProgress?.status === 'completed' ? 'Close' : 'Cancel' }}
            </button>
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
import AnalysisResults from '../components/AnalysisResults.vue'
import TextAnalysisForm from '../components/TextAnalysisForm.vue'
import LoadingScreen from '../components/LoadingScreen.vue'

export default {
  name: 'CustomModelView',
  components: {
    AnalysisResults,
    TextAnalysisForm,
    LoadingScreen
  },
  props: {
    pendingModelCode: {
      type: String,
      default: null
    }
  },
  data() {
    return {
      currentView: 'input', // 'input', 'training', 'analysis'
      modelCode: '',
      modelInfo: null,
      analysisText: '',
      analysisResults: null,
      isLoading: false,
      isAnalyzing: false,
      error: null,
      apiBaseUrl: config.apiBaseUrl,
      refreshInterval: null, // For periodic updates
      downloadProgress: null, // Progress tracking for downloads
      downloadProgressInterval: null, // Interval for polling progress
      showDownloadProgress: false // Show progress modal
    }
  },
  computed: {
    isValidCode() {
      return /^[a-z0-9]{6}$/.test(this.modelCode.toLowerCase())
    }
  },
  watch: {
    pendingModelCode(newCode) {
      if (newCode) {
        this.modelCode = newCode
        this.loadModel()
        this.$emit('clear-pending-code')
      }
    }
  },
  mounted() {
    // If there's a pending model code when mounted, use it
    if (this.pendingModelCode) {
      this.modelCode = this.pendingModelCode
      this.loadModel()
      this.$emit('clear-pending-code')
    }
  },
  unmounted() {
    // Clear any running intervals when component is destroyed
    if (this.refreshInterval) {
      clearInterval(this.refreshInterval)
    }
    if (this.downloadProgressInterval) {
      clearInterval(this.downloadProgressInterval)
    }
  },
  methods: {
    formatModelCode() {
      // Keep only alphanumeric characters and convert to lowercase
      this.modelCode = this.modelCode.toLowerCase().replace(/[^a-z0-9]/g, '').slice(0, 6)
    },

    async loadModel() {
      if (!this.isValidCode) return

      this.isLoading = true
      this.error = null

      try {
        const response = await axios.get(`${this.apiBaseUrl}/training/status/${this.modelCode}`)
        this.modelInfo = response.data

        if (this.modelInfo.completed) {
          this.currentView = 'analysis'
          // Clear any existing refresh interval since model is complete
          if (this.refreshInterval) {
            clearInterval(this.refreshInterval)
            this.refreshInterval = null
          }
        } else {
          this.currentView = 'training'
          // Set up periodic updates for training models (every 10 seconds)
          if (!this.refreshInterval) {
            this.refreshInterval = setInterval(() => {
              this.refreshStatus()
            }, 10000) // 10 seconds
          }
        }

      } catch (error) {
        console.error('Model load error:', error)
        if (error.response?.status === 404) {
          this.error = 'Model not found. Please check your code.'
        } else if (error.response?.status === 410) {
          this.error = 'Model has expired (7+ days old).'
        } else {
          this.error = error.response?.data?.error || 'Failed to load model'
        }
      } finally {
        this.isLoading = false
      }
    },

    async refreshStatus() {
      await this.loadModel()
    },

    handleAnalyze(data) {
      // Update the analysisText with the text from the form
      this.analysisText = data.text
      // Call the existing analyzeText method
      this.analyzeText()
    },

    async analyzeText() {
      if (!this.analysisText.trim()) return

      this.isAnalyzing = true
      this.error = null
      this.analysisResults = null

      try {
        const response = await axios.post(`${this.apiBaseUrl}/custom/predict/${this.modelCode}`, {
          text: this.analysisText
        })

        // Ensure the results structure is compatible with AnalysisResults component
        this.analysisResults = {
          ...response.data,
          original_text: this.analysisText,
          model_used: this.modelInfo.name || `Custom Model ${this.modelCode}`
        }

      } catch (error) {
        console.error('Analysis error:', error)
        this.error = error.response?.data?.error || 'Analysis failed'
      } finally {
        this.isAnalyzing = false
      }
    },

    cancelAnalysis() {
      this.isAnalyzing = false
      this.analysisResults = null
    },

    async downloadModel() {
      try {
        this.showDownloadProgress = true
        this.downloadProgress = { progress: 0, phase: 'Initializing download...', status: 'initializing' }
        
        console.log('Step 1: Initializing download for model:', this.modelCode)
        
        // Step 1: Initialize the download and get a download ID
        const initResponse = await axios.post(`${this.apiBaseUrl}/custom/download/init/${this.modelCode}`)
        const downloadId = initResponse.data.download_id
        
        console.log('Step 2: Download ID received:', downloadId)
        console.log('Step 3: Starting progress polling...')
        
        // Step 2: Start polling for progress updates
        this.startProgressPolling(downloadId)
        
        // Step 3: Start the actual file download in the background
        console.log('Step 4: Initiating file download...')
        setTimeout(async () => {
          try {
            const downloadResponse = await axios.get(
              `${this.apiBaseUrl}/custom/download/${this.modelCode}?download_id=${downloadId}`,
              { responseType: 'blob' }
            )
            
            console.log('Step 5: File download complete, creating download link...')
            // When the file arrives, trigger the browser download
            this.createDownloadLink(downloadResponse.data)
          } catch (downloadError) {
            console.error('File download error:', downloadError)
            this.downloadProgress.status = 'failed'
            this.downloadProgress.error = 'Failed to download file'
          }
        }, 100) // Small delay to ensure polling starts first
        
      } catch (error) {
        console.error('Download initialization error:', error)
        
        this.downloadProgress = { 
          progress: 0, 
          phase: 'Download failed', 
          status: 'failed',
          error: error.response?.data?.error || 'Failed to initialize download'
        }
      }
    },

    startProgressPolling(downloadId) {
      // Clear any existing polling
      if (this.downloadProgressInterval) {
        clearInterval(this.downloadProgressInterval)
      }
      
      console.log('Starting progress polling for download ID:', downloadId)
      
      // Poll every 250ms for progress updates
      this.downloadProgressInterval = setInterval(async () => {
        try {
          const response = await axios.get(`${this.apiBaseUrl}/custom/download-progress/${downloadId}`)
          const progressData = response.data
          
          // Update progress with backend data
          this.downloadProgress = {
            progress: progressData.progress || 0,
            phase: progressData.phase || 'Processing...',
            status: progressData.status || 'processing',
            error: progressData.error,
            elapsed_time: progressData.elapsed_time,
            archive_size_mb: progressData.archive_size_mb
          }
          
          console.log('Progress update:', {
            progress: this.downloadProgress.progress,
            phase: this.downloadProgress.phase,
            status: this.downloadProgress.status
          })
          
          // Check if download is complete or failed
          if (progressData.status === 'completed') {
            console.log('Download completed! Stopping polling.')
            clearInterval(this.downloadProgressInterval)
            this.downloadProgressInterval = null
            
            // Auto-close modal after 3 seconds
            setTimeout(() => {
              this.showDownloadProgress = false
            }, 3000)
            
          } else if (progressData.status === 'failed') {
            console.log('Download failed! Stopping polling.')
            clearInterval(this.downloadProgressInterval)
            this.downloadProgressInterval = null
          }
          
        } catch (error) {
          console.error('Progress polling error:', error)
          // Continue polling on error (might be temporary)
        }
      }, 250) // Poll every 250ms for more responsive updates
    },

    createDownloadLink(blobData) {
      console.log('Creating download link for blob:', blobData.size, 'bytes')
      // Create download link
      const url = window.URL.createObjectURL(new Blob([blobData]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', `custom_model_${this.modelCode}.zip`)
      document.body.appendChild(link)
      link.click()
      link.remove()
      window.URL.revokeObjectURL(url)
      console.log('Download link triggered')
    },

    cancelDownload() {
      // Stop polling
      if (this.downloadProgressInterval) {
        clearInterval(this.downloadProgressInterval)
        this.downloadProgressInterval = null
      }
      
      // Close modal
      this.showDownloadProgress = false
      
      // Reset progress
      this.downloadProgress = null
    },

    clearResults() {
      this.analysisResults = null
      this.analysisText = ''
    },

    goBack() {
      // Clear any running refresh interval
      if (this.refreshInterval) {
        clearInterval(this.refreshInterval)
        this.refreshInterval = null
      }
      
      this.currentView = 'input'
      this.modelCode = ''
      this.modelInfo = null
      this.analysisText = ''
      this.analysisResults = null
      this.error = null
    }
  }
}
</script>

<style scoped>
/* Model Code Input Styling */
.model-code-icon {
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.05); }
  100% { transform: scale(1); }
}

.model-code-input {
  font-size: 1.5rem;
  font-weight: bold;
  letter-spacing: 3px;
  text-transform: uppercase;
  background: linear-gradient(145deg, #ffffff, #f8f9fa);
  border: 2px solid #dee2e6;
  transition: all 0.3s ease;
}

.model-code-input:focus {
  border-color: #667eea;
  box-shadow: 0 0 0 0.25rem rgba(102, 126, 234, 0.25);
  transform: translateY(-1px);
}

/* Training Animation */
.training-animation {
  animation: bounce 2s infinite;
}

@keyframes bounce {
  0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
  40% { transform: translateY(-10px); }
  60% { transform: translateY(-5px); }
}

/* Info Cards */
.info-card {
  transition: all 0.3s ease;
  border: 1px solid #e9ecef !important;
}

.info-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

/* Model Info Grid */
.model-info-grid .col-md-4 {
  margin-bottom: 1rem;
}

/* Action Buttons */
.action-buttons .btn {
  font-weight: 500;
  padding: 0.75rem 1.5rem;
  border-radius: 10px;
  transition: all 0.2s ease;
}

.action-buttons .btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

/* Form Controls */
.form-control-lg {
  border-radius: 10px;
  border: 2px solid #e1e5e9;
  transition: all 0.2s ease;
  font-size: 1rem;
}

.form-control-lg:focus {
  border-color: #667eea;
  box-shadow: 0 0 0 0.25rem rgba(102, 126, 234, 0.25);
}

/* Cards */
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
  border-bottom: 1px solid #f0f0f0;
  padding: 1.25rem 1.5rem;
}

.card-body {
  padding: 1.5rem;
}

/* Buttons */
.btn {
  border-radius: 10px;
  font-weight: 500;
  padding: 0.6rem 1.25rem;
  transition: all 0.2s ease;
  border: none;
}

.btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.btn-lg {
  padding: 0.875rem 2rem;
  font-size: 1.1rem;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.btn-outline-info {
  border: 2px solid #17a2b8;
  color: #17a2b8;
}

.btn-outline-info:hover {
  background: #17a2b8;
  border-color: #17a2b8;
}

.btn-outline-warning {
  border: 2px solid #ffc107;
  color: #856404;
}

.btn-outline-warning:hover {
  background: #ffc107;
  border-color: #ffc107;
  color: #212529;
}

/* Badges */
.badge {
  border-radius: 8px;
  font-weight: 500;
}

.badge.fs-6 {
  font-size: 0.875rem !important;
  padding: 0.5rem 0.75rem;
}

/* Responsive Design */
@media (max-width: 768px) {
  .model-code-input {
    font-size: 1.25rem;
    letter-spacing: 2px;
  }
  
  .btn-group {
    flex-direction: column;
    width: 100%;
  }
  
  .btn-group .btn {
    margin-bottom: 0.5rem;
  }
  
  .action-buttons .btn {
    margin-bottom: 0.5rem;
    width: 100%;
  }
  
  .info-card {
    margin-bottom: 1rem;
  }
}

/* Loading Animation */
.fa-spin {
  animation: spin 2s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Form Text */
.form-text {
  color: #6c757d;
  font-size: 0.875rem;
}

/* Alert Styling */
.alert {
  border-radius: 12px;
  border: none;
  font-weight: 500;
  box-shadow: 0 2px 8px rgba(0,0,0,0.15);
}

.modal-body .alert {
  background-color: rgba(255, 255, 255, 0.95);
  color: #333;
}

.modal-body .alert-danger {
  background-color: rgba(220, 53, 69, 0.95);
  color: white;
}

.modal-body .alert-success {
  background-color: rgba(40, 167, 69, 0.95);
  color: white;
}

/* Progress Circle */
.progress-circle {
  position: relative;
  display: inline-block;
}

.progress-circle-inner {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100px;
  height: 100px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.progress-percentage {
  font-size: 24px;
  font-weight: bold;
  color: white;
}

.progress-circle-svg {
  transform: rotate(-90deg);
}

/* Modal Styles */
.modal {
  z-index: 1060;
}

.modal-content {
  border-radius: 15px;
  border: none;
  box-shadow: 0 10px 30px rgba(0,0,0,0.3);
}

.modal-header {
  border-radius: 15px 15px 0 0;
  border-bottom: none;
  padding: 1.5rem;
}

.modal-body {
  padding: 2rem;
  color: white;
}

.modal-footer {
  border-top: none;
  padding: 1rem 1.5rem;
  background-color: #f8f9fa;
  border-radius: 0 0 15px 15px;
}

/* Component Background */
.custom-model-view {
  background-color: #f8f9fa;
  min-height: calc(100vh - 100px);
}
</style>
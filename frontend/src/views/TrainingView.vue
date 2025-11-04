<template>
  <div class="training-view">
    <div class="container mt-4">
    <!-- Header -->
    <div class="row">
      <div class="col-12">
        <div class="card shadow border-0">
          <div class="card-header bg-primary text-white">
            <h3 class="card-title mb-0">
              <i class="fas fa-cogs me-2"></i>
              Model Fine-tuning
            </h3>
            <p class="mb-0 mt-2 small opacity-90">
              Upload your CSV data and train a custom deception detection model
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- Training Form -->
    <div class="row mt-4" v-if="currentStep === 'upload'">
      <div class="col-12">
        <div class="card shadow border-0">
          <div class="card-body p-4">
            <h5 class="card-title mb-4">
              <i class="fas fa-upload me-2 text-primary"></i>
              Upload Training Data
            </h5>
            
            <div class="row">
              <!-- Upload Area -->
              <div class="col-md-6">
                <div 
                  class="upload-area border-2 border-dashed d-flex flex-column align-items-center justify-content-center text-center p-4"
                  :class="{ 
                    'border-success bg-light-success': validationResults && validationResults.valid,
                    'border-danger bg-light-danger': validationResults && !validationResults.valid,
                    'border-primary': !validationResults,
                    'upload-hover': isDragOver
                  }"
                  @dragover.prevent="isDragOver = true"
                  @dragleave.prevent="isDragOver = false"
                  @drop.prevent="handleDrop"
                  @click="triggerFileInput"
                  style="min-height: 200px; cursor: pointer; border-radius: 12px;"
                >
                  <i 
                    class="fas fa-cloud-upload-alt mb-3"
                    :class="{
                      'text-success': validationResults && validationResults.valid,
                      'text-danger': validationResults && !validationResults.valid,
                      'text-primary': !validationResults
                    }"
                    style="font-size: 3rem;"
                  ></i>
                  
                  <h6 class="mb-2">
                    {{ selectedFile ? selectedFile.name : 'Drop your CSV file here' }}
                  </h6>
                  
                  <p class="text-muted small mb-0">
                    or click to browse
                  </p>
                  
                  <!-- Hidden file input -->
                  <input 
                    type="file" 
                    ref="csvFile"
                    accept=".csv"
                    @change="onFileSelected"
                    style="display: none;"
                  >
                </div>
              </div>
              
              <!-- File Requirements -->
              <div class="col-md-6">
                <div class="requirements-panel h-100 p-3 bg-light rounded">
                  <h6 class="mb-3">
                    <i class="fas fa-info-circle me-2 text-info"></i>
                    File Requirements
                  </h6>
                  
                  <ul class="list-unstyled mb-0">
                    <li class="mb-2">
                      <i class="fas fa-circle me-2 text-primary" style="font-size: 0.5rem;"></i>
                      <strong>Format:</strong> CSV file only
                    </li>
                    <li class="mb-2">
                      <i class="fas fa-circle me-2 text-primary" style="font-size: 0.5rem;"></i>
                      <strong>Size:</strong> Maximum 16MB
                    </li>
                    <li class="mb-2">
                      <i class="fas fa-circle me-2 text-primary" style="font-size: 0.5rem;"></i>
                      <strong>Columns:</strong> 'text' and 'label'
                    </li>
                    <li class="mb-2">
                      <i class="fas fa-circle me-2 text-primary" style="font-size: 0.5rem;"></i>
                      <strong>Labels:</strong> 0/1 or deceptive/truthful
                    </li>
                    <li class="mb-2">
                      <i class="fas fa-circle me-2 text-primary" style="font-size: 0.5rem;"></i>
                      <strong>Rows:</strong> Minimum 10 entries
                    </li>
                    <li class="mb-0">
                      <i class="fas fa-circle me-2 text-primary" style="font-size: 0.5rem;"></i>
                      <strong>Encoding:</strong> UTF-8 recommended
                    </li>
                  </ul>
                </div>
              </div>
            </div>

            <!-- File Validation Results -->
            <div v-if="validationResults || validationError" class="mt-4">
              <div class="row">
                <div class="col-12">
                  <div class="validation-results">
                    <!-- Success -->
                    <div v-if="validationResults && validationResults.valid" class="alert alert-success border-0 shadow-s w-100">
                      <div class="align-items-center">
                        <i class="fas fa-check-circle me-3" style="font-size: 1.5rem;"></i>
                        <div>
                          <h6 class="alert-heading mb-1">File Validated Successfully!</h6>
                          <div class="row mt-2">
                            <div class="col-md-3">
                              <small class="text-muted">Rows:</small><br>
                              <strong>{{ validationResults.rows }}</strong>
                            </div>
                            <div class="col-md-4">
                              <small class="text-muted">Columns:</small><br>
                              <strong>{{ validationResults.columns.join(', ') }}</strong>
                            </div>
                            <div class="col-md-5">
                              <small class="text-muted">Label Distribution:</small><br>
                              <span v-for="(count, label) in validationResults.label_distribution" :key="label" class="badge bg-primary me-1">
                                {{ label }}: {{ count }}
                              </span>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                    
                    <!-- Error -->
                    <div v-else-if="validationError" class="alert alert-danger border-0 shadow-sm">
                      <div class="d-flex align-items-center">
                        <i class="fas fa-exclamation-triangle me-3" style="font-size: 1.5rem;"></i>
                        <div>
                          <h6 class="alert-heading mb-1">Validation Failed</h6>
                          <p class="mb-0">{{ validationError }}</p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Model Configuration -->
            <div v-if="validationResults && validationResults.valid" class="mt-4">
              <div class="configuration-section p-4 bg-light rounded">
                <h6 class="mb-4">
                  <i class="fas fa-cog me-2 text-primary"></i>
                  Model Configuration
                </h6>
                
                <div class="row">
                  <div class="col-md-6 mb-3">
                    <label for="modelName" class="form-label fw-semibold">Model Name *</label>
                    <input 
                      type="text" 
                      class="form-control form-control-lg" 
                      :class="{ 'is-valid': config.name.trim().length >= 3, 'is-invalid': config.name.length > 0 && config.name.trim().length < 3 }"
                      id="modelName"
                      v-model="config.name"
                      placeholder="e.g., Marketing Text Classifier"
                      maxlength="100"
                    >
                    <div class="form-text">
                      <small>Give your model a descriptive name (minimum 3 characters)</small>
                    </div>
                    <div class="invalid-feedback" v-if="config.name.length > 0 && config.name.trim().length < 3">
                      Model name must be at least 3 characters long
                    </div>
                    <div class="valid-feedback" v-if="config.name.trim().length >= 3">
                      Great! Model name looks good
                    </div>
                  </div>
                  
                  <div class="col-md-6 mb-3">
                    <label for="baseModel" class="form-label fw-semibold">Base Model *</label>
                    <select 
                      class="form-select form-select-lg" 
                      :class="{ 'is-valid': config.base_model, 'is-invalid': config.base_model === '' && validationResults }"
                      id="baseModel" 
                      v-model="config.base_model"
                    >
                      <option value="">Choose a foundation model...</option>
                      <option 
                        v-for="model in availableBaseModels" 
                        :key="model.key"
                        :value="model.key"
                      >
                        {{ model.name }}
                      </option>
                    </select>
                    <div class="form-text">
                      <small>Pre-trained model to fine-tune</small>
                    </div>
                    <div class="invalid-feedback" v-if="config.base_model === '' && validationResults">
                      Please select a base model to continue
                    </div>
                    <div class="valid-feedback" v-if="config.base_model">
                      Perfect! {{ availableBaseModels.find(m => m.key === config.base_model)?.name }} selected
                    </div>
                  </div>
                </div>

                <div class="row">
                  <div class="col-md-6 mb-3">
                    <label for="epochs" class="form-label fw-semibold">Training Epochs</label>
                    <input 
                      type="number" 
                      class="form-control" 
                      :class="{ 'is-valid': config.epochs >= 1 && config.epochs <= 10, 'is-invalid': config.epochs < 1 || config.epochs > 10 }"
                      id="epochs"
                      v-model.number="config.epochs"
                      min="1"
                      max="10"
                    >
                    <div class="form-text">
                      <small><i class="fas fa-info-circle me-1"></i>More epochs = longer training but potentially better results (Max: 10)</small>
                    </div>
                    <div class="invalid-feedback" v-if="config.epochs < 1 || config.epochs > 10">
                      Epochs must be between 1 and 10
                    </div>
                    <div class="valid-feedback" v-if="config.epochs >= 1 && config.epochs <= 10">
                      Good choice! {{ config.epochs }} epoch{{ config.epochs > 1 ? 's' : '' }}
                    </div>
                  </div>
                  
                  <div class="col-md-6 mb-3">
                    <label for="learningRate" class="form-label fw-semibold">Learning Rate</label>
                    
                    <!-- Preset Selection -->
                    <div class="mb-2">
                      <select class="form-select" v-model="selectedLearningRatePreset" @change="onPresetChange">
                        <option value="">Quick Select (Recommended)</option>
                        <option value="1e-5">1e-5 (Conservative)</option>
                        <option value="2e-5">2e-5 (Recommended)</option>
                        <option value="5e-5">5e-5 (Aggressive)</option>
                        <option value="custom">Custom Value</option>
                      </select>
                    </div>
                    
                    <!-- Manual Input -->
                    <div v-if="showCustomLearningRate" class="mb-2">
                      <input 
                        type="number" 
                        class="form-control" 
                        :class="{ 'is-valid': isValidLearningRate, 'is-invalid': !isValidLearningRate && config.learning_rate }"
                        v-model="config.learning_rate"
                        placeholder="Enter learning rate (e.g., 0.00002)"
                        step="0.00001"
                        min="0.000001"
                        max="0.01"
                      >
                      <div class="invalid-feedback" v-if="!isValidLearningRate && config.learning_rate">
                        Learning rate must be between 0.000001 and 0.01
                      </div>
                      <div class="valid-feedback" v-if="isValidLearningRate">
                        Valid learning rate: {{ config.learning_rate }}
                      </div>
                    </div>
                    
                    <!-- Slider for Custom -->
                    <div v-if="showCustomLearningRate" class="mb-2">
                      <input 
                        type="range" 
                        class="w-100" 
                        v-model="learningRateSlider"
                        @input="onSliderChange"
                        min="1"
                        max="100"
                        step="1"
                      >
                      <div class="d-flex justify-content-between text-muted small">
                        <span>0.000001</span>
                        <span>0.01</span>
                      </div>
                    </div>
                    
                    <div class="form-text">
                      <small><i class="fas fa-info-circle me-1"></i>How fast the model learns. Lower = safer, Higher = faster but risky</small>
                    </div>
                  </div>
                </div>

                <div class="row">
                  <div class="col-md-6 mb-3">
                    <label for="validation" class="form-label fw-semibold">Model Validation</label>
                    <select 
                      class="form-select" 
                      id="validation"
                      v-model="config.validation_split"
                    >
                      <option value="0">No Validation (Use all data for training)</option>
                      <option value="0.1">10% for validation, 90% for training</option>
                      <option value="0.15">15% for validation, 85% for training</option>
                      <option value="0.2">20% for validation, 80% for training (Recommended)</option>
                      <option value="0.25">25% for validation, 75% for training</option>
                      <option value="0.3">30% for validation, 70% for training</option>
                    </select>
                    <div class="form-text">
                      <small><i class="fas fa-info-circle me-1"></i>Reserve data for validation to monitor training progress and prevent overfitting</small>
                    </div>
                  </div>
                  
                  <div class="col-md-6 mb-3">
                    <!-- Empty column for spacing, can be used for future options -->
                  </div>
                </div>

                <div class="mb-4">
                  <label for="notes" class="form-label fw-semibold">Notes <span class="text-muted">(Optional)</span></label>
                  <textarea 
                    class="form-control" 
                    id="notes"
                    v-model="config.notes"
                    rows="3"
                    maxlength="500"
                    placeholder="Describe your dataset, training purpose, or any special considerations..."
                  ></textarea>
                  <div class="form-text">
                    <small>{{ config.notes.length }}/500 characters</small>
                  </div>
                </div>

                <!-- Start Training Button -->
                <div class="d-grid">
                  <button 
                    class="btn btn-lg py-3"
                    :class="canStartTraining ? 'btn-primary' : 'btn-outline-secondary'"
                    @click="startTraining"
                    :disabled="!canStartTraining || isTraining"
                  >
                    <i class="fas me-2" :class="canStartTraining ? 'fa-rocket' : 'fa-lock'"></i>
                    <span v-if="isTraining">
                      <i class="fas fa-spinner fa-spin me-2"></i>
                      Initializing Training...
                    </span>
                    <span v-else-if="!canStartTraining">
                      Complete Required Fields to Start
                    </span>
                    <span v-else>
                      Start Fine-tuning
                    </span>
                  </button>
                  
                  <!-- Validation Summary -->
                  <div class="validation-summary mt-3" v-if="!canStartTraining && (config.name || config.base_model || validationResults)">
                    <small class="text-muted">
                      <i class="fas fa-info-circle me-1"></i>
                      Still needed:
                      <span v-if="!validationResults" class="text-warning"> Valid CSV file,</span>
                      <span v-if="!config.name.trim() || config.name.trim().length < 3" class="text-warning"> Model name,</span>
                      <span v-if="!config.base_model" class="text-warning"> Base model selection</span>
                    </small>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Training Progress -->
    <div class="row mt-4" v-if="currentStep === 'training'">
      <div class="col-lg-8 mx-auto">
        <div class="card shadow">
          <div class="card-body text-center">
            <div class="mb-4">
              <i class="fas fa-cogs fa-3x text-primary mb-3 fa-spin"></i>
              <h4>Training in Progress</h4>
              <p class="text-muted">
                Model Code: <strong class="text-primary">{{ trainingModelCode }}</strong>
              </p>
            </div>

            <div class="alert alert-info">
              <i class="fas fa-info-circle me-2"></i>
              Training is running in the background. This will take several minutes depending on your dataset size and configuration.
              You can close this page and return later using your model code.
            </div>

            <div class="row text-center">
              <div class="col-4">
                <button class="btn btn-outline-secondary" @click="resetForm">
                  <i class="fas fa-plus me-1"></i>
                  Train Another
                </button>
              </div>
              <div class="col-4">
                <button class="btn btn-outline-primary" @click="switchToCustomTab">
                  <i class="fas fa-code me-1"></i>
                  Access Model
                </button>
              </div>
              <div class="col-4">
                <button class="btn btn-outline-info" @click="copyModelCode">
                  <i class="fas fa-copy me-1"></i>
                  Copy Code
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Error Display -->
    <div class="row mt-4" v-if="error">
      <div class="col-lg-8 mx-auto">
        <div class="alert alert-danger border-0 shadow-sm">
          <div class="d-flex align-items-center">
            <i class="fas fa-exclamation-triangle me-3" style="font-size: 1.5rem;"></i>
            <div>
              <h6 class="alert-heading mb-1">Operation Failed</h6>
              <p class="mb-0">{{ error }}</p>
            </div>
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

export default {
  name: 'TrainingView',
  data() {
    return {
      currentStep: 'upload', // 'upload', 'training'
      selectedFile: null,
      validationResults: null,
      validationError: null,
      availableBaseModels: [],
      config: {
        name: '',
        base_model: '',
        epochs: 3,
        learning_rate: '2e-5',
        validation_split: '0.2', // Default to 20% validation
        notes: ''
      },
      selectedLearningRatePreset: '2e-5', // Default to recommended
      learningRateSlider: 50, // Slider position (1-100)
      isTraining: false,
      trainingModelCode: null,
      error: null,
      apiBaseUrl: config.apiBaseUrl,
      isDragOver: false
    }
  },
  computed: {
    canStartTraining() {
      return this.config.name.trim().length >= 3 && 
             this.config.base_model && 
             this.validationResults && 
             this.validationResults.valid &&
             this.config.epochs >= 1 && 
             this.config.epochs <= 10 &&
             this.isValidLearningRate
    },
    showCustomLearningRate() {
      return this.selectedLearningRatePreset === 'custom'
    },
    isValidLearningRate() {
      const lr = parseFloat(this.config.learning_rate)
      return !isNaN(lr) && lr >= 0.000001 && lr <= 0.01
    }
  },
  mounted() {
    this.loadBaseModels()
  },
  methods: {
    async loadBaseModels() {
      try {
        const response = await axios.get(`${this.apiBaseUrl}/training/models`)
        this.availableBaseModels = response.data.models
      } catch (error) {
        console.error('Failed to load base models:', error)
        this.error = 'Failed to load available base models'
      }
    },

    onFileSelected(event) {
      const file = event.target.files[0]
      this.processFile(file)
    },

    handleDrop(event) {
      this.isDragOver = false
      const files = event.dataTransfer.files
      if (files.length > 0) {
        this.processFile(files[0])
      }
    },

    triggerFileInput() {
      this.$refs.csvFile.click()
    },

    processFile(file) {
      this.selectedFile = null
      this.validationResults = null
      this.validationError = null
      this.error = null
      
      if (!file) return

      // Basic file validation
      if (!file.name.toLowerCase().endsWith('.csv')) {
        this.validationError = 'Please select a CSV file'
        return
      }

      if (file.size > 16 * 1024 * 1024) { // 16MB
        this.validationError = 'File size must be less than 16MB'
        return
      }

      this.selectedFile = file
      this.validateFile()
    },

    async validateFile() {
      if (!this.selectedFile) return

      const formData = new FormData()
      formData.append('file', this.selectedFile)

      try {
        this.error = null
        const response = await axios.post(`${this.apiBaseUrl}/training/upload-csv`, formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })

        if (response.data.valid) {
          this.validationResults = response.data
        } else {
          this.validationError = response.data.error
        }

      } catch (error) {
        console.error('Validation error:', error)
        this.validationError = error.response?.data?.error || 'File validation failed'
        this.validationResults = null
      }
    },

    async startTraining() {
      if (!this.canStartTraining) return

      this.isTraining = true
      this.error = null

      const formData = new FormData()
      formData.append('file', this.selectedFile)
      formData.append('config', JSON.stringify(this.config))

      try {
        const response = await axios.post(`${this.apiBaseUrl}/training/start`, formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })

        this.trainingModelCode = response.data.model_code
        this.currentStep = 'training'
        
        // Emit event to parent
        this.$emit('training-started', this.trainingModelCode)

      } catch (error) {
        console.error('Training start error:', error)
        this.error = error.response?.data?.error || 'Failed to start training'
      } finally {
        this.isTraining = false
      }
    },

    resetForm() {
      this.currentStep = 'upload'
      this.selectedFile = null
      this.validationResults = null
      this.validationError = null
      this.trainingModelCode = null
      this.error = null
      this.isDragOver = false
      this.selectedLearningRatePreset = '2e-5'
      this.learningRateSlider = 50
      this.config = {
        name: '',
        base_model: '',
        epochs: 3,
        learning_rate: '2e-5',
        validation_split: '0.2',
        notes: ''
      }
      if (this.$refs.csvFile) {
        this.$refs.csvFile.value = ''
      }
    },

    switchToCustomTab() {
      // Copy model code to clipboard automatically
      if (this.trainingModelCode) {
        navigator.clipboard.writeText(this.trainingModelCode).then(() => {
          // Model code copied successfully
        }).catch(() => {
          // Failed to copy, but continue anyway
        })
        
        // Set the model code in the custom tab and switch
        this.$parent.setCustomModelCode(this.trainingModelCode)
      }
      
      // Switch to custom model tab
      this.$parent.switchTab('custom')
    },

    copyModelCode() {
      if (this.trainingModelCode) {
        navigator.clipboard.writeText(this.trainingModelCode).then(() => {
          // Model code copied to clipboard
        }).catch(() => {
          // Failed to copy model code
        })
      }
    },

    onPresetChange() {
      if (this.selectedLearningRatePreset && this.selectedLearningRatePreset !== 'custom') {
        this.config.learning_rate = this.selectedLearningRatePreset
      } else if (this.selectedLearningRatePreset === 'custom') {
        // Set a reasonable default for custom
        this.config.learning_rate = '2e-5'
        this.updateSliderFromLearningRate()
      }
    },

    onSliderChange() {
      // Convert slider position (1-100) to learning rate (1e-6 to 1e-2)
      // Using logarithmic scale for better distribution
      const minLog = Math.log10(0.000001) // 1e-6
      const maxLog = Math.log10(0.01)     // 1e-2
      const scale = (maxLog - minLog) / 99 // 99 steps (1-100)
      const logValue = minLog + (this.learningRateSlider - 1) * scale
      const learningRate = Math.pow(10, logValue)
      
      // Format to scientific notation if very small, otherwise regular
      if (learningRate < 0.0001) {
        this.config.learning_rate = learningRate.toExponential(0)
      } else {
        this.config.learning_rate = learningRate.toFixed(6).replace(/\.?0+$/, '')
      }
    },

    updateSliderFromLearningRate() {
      // Convert learning rate back to slider position
      const lr = parseFloat(this.config.learning_rate)
      if (!isNaN(lr) && lr >= 0.000001 && lr <= 0.01) {
        const minLog = Math.log10(0.000001)
        const maxLog = Math.log10(0.01)
        const scale = (maxLog - minLog) / 99
        const logValue = Math.log10(lr)
        this.learningRateSlider = Math.round(((logValue - minLog) / scale) + 1)
      }
    }
  }
}
</script>

<style scoped>
.fa-spin {
  animation: spin 2s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.card {
  border: none;
  border-radius: 15px;
}

.btn {
  border-radius: 8px;
  font-weight: 500;
}

.form-control, .form-select {
  border-radius: 8px;
  border: 1px solid #dee2e6;
  transition: all 0.2s ease;
}

.form-control:focus, .form-select:focus {
  border-color: #0d6efd;
  box-shadow: 0 0 0 0.2rem rgba(13, 110, 253, 0.25);
}

.form-control-lg {
  padding: 0.75rem 1rem;
  font-size: 1.1rem;
}

.form-select-lg {
  padding: 0.75rem 1rem;
  font-size: 1.1rem;
}

/* Upload Area Styles */
.upload-area {
  transition: all 0.3s ease;
  background: #fafafa;
}

.upload-area:hover, .upload-hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
}

.bg-light-success {
  background-color: rgba(25, 135, 84, 0.1) !important;
}

.bg-light-danger {
  background-color: rgba(220, 53, 69, 0.1) !important;
}

/* Requirements Panel */
.requirements-panel {
  border: 1px solid #e9ecef;
}

.requirements-panel ul li {
  padding: 0.25rem 0;
}

/* Configuration Section */
.configuration-section {
  border: 1px solid #e9ecef;
}

/* Validation Results */
.validation-results .alert {
  border-radius: 10px;
}

/* Form Labels */
.form-label.fw-semibold {
  color: #495057;
  margin-bottom: 0.5rem;
}

/* Badge styling */
.badge {
  font-size: 0.75rem;
  padding: 0.35em 0.65em;
}

/* Better spacing */
.form-text {
  margin-top: 0.25rem;
  color: #6c757d;
}

/* Responsive improvements */
@media (max-width: 768px) {
  .upload-area {
    min-height: 150px !important;
  }
  
  .requirements-panel {
    margin-top: 1rem;
  }
  
  .configuration-section {
    margin-top: 1rem;
  }
}

/* Component Background */
.training-view {
  background-color: #f8f9fa;
  min-height: calc(100vh - 100px);
}

.dark-mode .training-view {
  background-color: transparent;
}

/* Dark mode overrides */
.dark-mode .requirements-panel {
  border-color: #3d3d3d;
}

.dark-mode .configuration-section {
  border-color: #3d3d3d;
}

.dark-mode .form-label.fw-semibold {
  color: #e0e0e0;
}

.dark-mode .requirements-panel h6 {
  color: #ffffff;
}
</style>
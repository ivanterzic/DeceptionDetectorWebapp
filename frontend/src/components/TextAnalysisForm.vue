<template>
  <div class="text-analysis-form">
    <div class="card shadow border-0">
      <div class="card-body p-4">
        <form @submit.prevent="analyzeText">
          <div class="mb-4">
            <textarea
              id="textInput"
              v-model="inputText"
              class="form-control form-control-lg"
              :class="{ 'is-invalid': isTextTooLong }"
              rows="8"
              placeholder="Enter the text you want to analyze..."
              required
              maxlength="1300"
              style="resize: vertical; min-height: 200px;"
            ></textarea>
            <div class="form-text">
              <small><span class="text-muted">({{ inputText.length }}/1300 characters)</span></small>
            </div>
            <div v-if="isTextTooLong" class="invalid-feedback">
              Text is too long. Please limit to 1300 characters to avoid model token limits.
            </div>
          </div>
          
          <!-- Model Selection (only show if multiple models available) -->
          <div v-if="showModelSelection" class="mb-4">
            <label for="modelSelect" class="form-label fw-semibold">Select Model</label>
            <select
              id="modelSelect"
              v-model="selectedModel"
              class="form-select form-select-lg"
              required
            >
              <option value="">Choose a model...</option>
              <option v-for="model in availableModels" :key="model" :value="model">
                {{ formatModelName(model) }}
              </option>
            </select>
            <div class="form-text">
              <small>Select the appropriate model for your text domain.</small>
            </div>
          </div>
          
          <div class="d-grid">
            <button
              type="submit"
              class="btn btn-primary btn-lg py-3"
              :disabled="!canAnalyze || isLoading"
            >
              <i class="fas fa-search me-2"></i>
              <span v-if="isLoading">Analyzing...</span>
              <span v-else>{{ buttonText || 'Analyze Text' }}</span>
            </button>
          </div>
        </form>
      </div>
    </div>
    
    <!-- Model Information -->
    <div v-if="selectedModel && showModelInfo" class="card mt-3">
      <div class="card-body">
        <h6 class="card-title">Model Information</h6>
        <p class="card-text text-muted mb-0">
          {{ getModelDescription(selectedModel) }}
        </p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TextAnalysisForm',
  props: {
    // Available models for selection
    availableModels: {
      type: Array,
      default: () => []
    },
    // Whether to show model selection dropdown
    showModelSelection: {
      type: Boolean,
      default: true
    },
    // Whether to show model information card
    showModelInfo: {
      type: Boolean,
      default: true
    },
    // Custom button text
    buttonText: {
      type: String,
      default: null
    },
    // Loading state
    isLoading: {
      type: Boolean,
      default: false
    },
    // Initial text value
    initialText: {
      type: String,
      default: ''
    },
    // Pre-selected model
    preselectedModel: {
      type: String,
      default: ''
    }
  },
  data() {
    return {
      inputText: this.initialText,
      selectedModel: this.preselectedModel
    }
  },
  computed: {
    isTextTooLong() {
      return this.inputText.length > 1300
    },
    canAnalyze() {
      if (this.showModelSelection) {
        return this.inputText.trim() && this.selectedModel && !this.isTextTooLong
      } else {
        return this.inputText.trim() && !this.isTextTooLong
      }
    }
  },
  watch: {
    initialText(newValue) {
      this.inputText = newValue
    },
    preselectedModel(newValue) {
      this.selectedModel = newValue
    },
    inputText(newValue) {
      this.$emit('text-changed', newValue)
    },
    selectedModel(newValue) {
      this.$emit('model-changed', newValue)
    }
  },
  methods: {
    analyzeText() {
      if (!this.canAnalyze) return
      
      this.$emit('analyze', {
        text: this.inputText,
        model: this.selectedModel
      })
    },
    formatModelName(modelName) {
      // Convert model names to user-friendly format
      const modelFormats = {
        'bert-covid-1': 'BERT COVID-19',
        'bert-climate-change-1': 'BERT Climate Change',
        'bert-combined-1': 'BERT Combined Dataset',
        'deberta-covid-1': 'DeBERTa COVID-19',
        'deberta-climate-change-1': 'DeBERTa Climate Change',
        'deberta-combined-1': 'DeBERTa Combined Dataset'
      }
      
      return modelFormats[modelName] || modelName.replace(/-/g, ' ').replace(/\b\w/g, l => l.toUpperCase())
    },
    getModelDescription(modelName) {
      // Model descriptions
      const descriptions = {
        'bert-covid-1': 'BERT model fine-tuned for COVID-19 related misinformation detection',
        'bert-climate-change-1': 'BERT model fine-tuned for climate change related misinformation detection',
        'bert-combined-1': 'BERT model fine-tuned for general-purpose deception detection across multiple domains, trained on both COVID-19 and climate change datasets',
        'deberta-covid-1': 'DEBERTa model fine-tuned for COVID-19 related misinformation detection with enhanced attention mechanisms',
        'deberta-climate-change-1': 'DEBERTa model fine-tuned for climate change related misinformation detection with improved context understanding',
        'deberta-combined-1': 'DEBERTa model fine-tuned for general-purpose deception detection across multiple domains, trained on both COVID-19 and climate change datasets with advanced architecture'
      }
      
      return descriptions[modelName] || 'Custom trained model for deception detection'
    },
    clearText() {
      this.inputText = ''
      this.$emit('text-changed', '')
    },
    setText(text) {
      this.inputText = text
      this.$emit('text-changed', text)
    }
  }
}
</script>

<style scoped>
/* Responsive adjustments */
@media (max-width: 768px) {
  .text-analysis-form .form-control-lg {
    font-size: 1rem;
  }
  
  .text-analysis-form .btn-lg {
    font-size: 1.1rem;
  }
}

/* Dark Mode Styles */
.dark-mode .card {
  background-color: #2d2d2d;
  border-radius: 15px;
}

.dark-mode .card-body {
  color: #ffffff;
}

.dark-mode .form-label {
  color: #ffffff !important;
}

.dark-mode .form-text small {
  color: #b0b0b0 !important;
}

.dark-mode .card-title {
  color: #ffffff;
}

.dark-mode .card-text {
  color: #b0b0b0 !important;
}

</style>
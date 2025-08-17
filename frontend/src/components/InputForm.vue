<template>
  <div class="input-form">
    <div class="card shadow">
      <div class="card-header bg-primary text-white">
        <h4 class="mb-0">
          <i class="fas fa-microscope me-2"></i>
          Analyze Text for Deception
        </h4>
      </div>
      <div class="card-body">
        <form @submit.prevent="analyzeText">
          <div class="mb-3">
            <label for="textInput" class="form-label">Text to Analyze</label>
            <textarea
              id="textInput"
              v-model="inputText"
              class="form-control"
              :class="{ 'is-invalid': isTextTooLong }"
              rows="6"
              placeholder="Enter the text you want to analyze for deception..."
              required
              maxlength="2000"
            ></textarea>
            <div class="form-text">
              Enter the text you want to check for truthfulness or deception.
              <span class="text-muted">({{ inputText.length }}/2000 characters)</span>
            </div>
            <div v-if="isTextTooLong" class="invalid-feedback">
              Text is too long. Please limit to 2000 characters to avoid model token limits.
            </div>
          </div>
          
          <div class="mb-3">
            <label for="modelSelect" class="form-label">Select Model</label>
            <select
              id="modelSelect"
              v-model="selectedModel"
              class="form-select"
              required
            >
              <option value="">Choose a model...</option>
              <!-- TODO: do we want model names full or formatted? -->
              <option v-for="model in availableModels" :key="model" :value="model">
                {{ formatModelName(model) }}
              </option>
            </select>
            <div class="form-text">
              Select the appropriate model for your text domain.
            </div>
          </div>
          
          <div class="d-grid">
            <button
              type="submit"
              class="btn btn-primary btn-lg"
              :disabled="!inputText || !selectedModel || isTextTooLong"
            >
              <i class="fas fa-search me-2"></i>
              Analyze Text
            </button>
          </div>
        </form>
      </div>
    </div>
    
    <!-- Model Information -->
    <div v-if="selectedModel" class="card mt-3">
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
  name: 'InputForm',
  props: {
    availableModels: {
      type: Array,
      required: true
    }
  },
  data() {
    return {
      inputText: '',
      selectedModel: '',
      maxTextLength: 2000 // Conservative limit to avoid BERT's 512 token limit
    }
  },
  computed: {
    isTextTooLong() {
      return this.inputText.length > this.maxTextLength
    }
  },
  methods: {
    // if the form data is OK, emit the analyze event with the input text and selected model, this will be processed in the component and emitted further to App.vue
    analyzeText() {
      if (!this.inputText || !this.selectedModel || this.isTextTooLong) {
        return
      }
      
      this.$emit('analyze', {
        text: this.inputText,
        model: this.selectedModel
      })
    },
    // TODO: Hardcoded for the six examples now in this phase of the work
    formatModelName(model) {
      const names = {
        'covid': 'COVID-19 Model',
        'climate': 'Climate Change Model', 
        'combined': 'Combined Model'
      }
      if (names[model]) {
        return names[model]
      }
      return model.split(/[-_]/).map(word => 
        word.charAt(0).toUpperCase() + word.slice(1)
      ).join(' ') + ' Model'
    },
    // TODO: potential model description if they will be predetermined in the future
    getModelDescription(model) {
      return `Model for deception detection optimized for ${model}-related content.`
    }
  }
}
</script>

<style scoped>
.input-form {
  max-width: 800px;
  margin: 0 auto;
}

.card {
  border: none;
  border-radius: 10px;
}

.btn {
  border-radius: 6px;
}

.form-control:focus,
.form-select:focus {
  border-color: #0d6efd;
  box-shadow: 0 0 0 0.2rem rgba(13, 110, 253, 0.25);
}
</style>

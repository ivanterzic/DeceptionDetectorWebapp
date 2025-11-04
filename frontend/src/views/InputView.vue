<template>
  <div class="input-view">
    <div class="container mt-4">
      <!-- Header -->
      <div class="row">
        <div class="">
          <div class="card shadow border-0">
            <div class="card-header bg-primary text-white">
              <h3 class="card-title mb-0">
                <i class="fas fa-search me-2"></i>
                Text Analysis
              </h3>
              <p class="mb-0 mt-2 small opacity-90">
                Analyze text for deception using advanced AI models
              </p>
            </div>
          </div>
        </div>
      </div>

      <div class="row mt-4">
        <div class="">
          <InputForm 
            :available-models="availableModels"
            @analyze="handleAnalyze"
          />
          
          <!-- Error Message -->
          <div v-if="error" class="alert alert-danger border-0 shadow-sm mt-4">
            <div class="d-flex align-items-center">
              <i class="fas fa-exclamation-triangle me-3" style="font-size: 1.5rem;"></i>
              <div>
                <h6 class="alert-heading mb-1">Analysis Failed</h6>
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
import InputForm from '../components/InputForm.vue'

export default {
  name: 'InputView',
  components: {
    InputForm
  },
  props: {
    // Available models passed from parent component
    availableModels: {
      type: Array,
      required: true
    },
    error: {
      type: String,
      default: null
    }
  },
  // handleAnalyze method to emit analyze event with input data recieved from InputForm, the InputForm component will pass the text and selected model to the parent component (App.vue)
  // this is just for sending it to app.vue 
  methods: {
    handleAnalyze(data) {
      this.$emit('analyze', data)
    }
  }
}
</script>

<style scoped>
.input-view {
  background-color: #f8f9fa;
  min-height: calc(100vh - 100px);
}

.dark-mode .input-view {
  background-color: transparent;
}
</style>

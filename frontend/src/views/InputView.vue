<template>
  <div class="input-view">
    <div class="container">
      <div class="row">
        <div class="col-lg-8 mx-auto">
          <div class="text-center mb-5">
            <h1 class="display-4 mb-3">
              <i class="fas fa-user-secret me-3"></i>
              Deception Detector
            </h1>
            <p class="lead text-muted">
              Advanced AI-powered analysis to detect deception and misinformation in text
            </p>
          </div>
          
          <InputForm 
            :available-models="availableModels"
            @analyze="handleAnalyze"
          />
          
          <!-- Error Message -->
          <div v-if="error" class="alert alert-danger mt-4">
            <i class="fas fa-exclamation-circle me-2"></i>
            {{ error }}
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
  min-height: 100vh;
  background: linear-gradient(135deg, #000000 0%, #3628af 100%);
  color: white;
  padding: 2rem 0;
  display: flex;
  align-items: center;
}

.display-4 {
  font-weight: 300;
}

.lead {
  color: rgba(255, 255, 255, 0.8) !important;
}
</style>

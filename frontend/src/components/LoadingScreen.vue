<template>
  <div class="loading-screen">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-md-6">
          <div class="card shadow">
            <div class="card-body text-center py-5">
              <div class="spinner-border text-primary mb-3" style="width: 3rem; height: 3rem;" role="status">
                <span class="visually-hidden">Loading...</span>
              </div>
              <h4 class="mb-3">{{ title }}</h4>
              <p class="text-muted mb-4">
                {{ message }}
              </p>
              
              <div v-if="showCancelButton" class="mt-4">
                <button 
                  @click="$emit('cancel')" 
                  class="btn btn-outline-secondary"
                >
                  Cancel Analysis
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LoadingScreen',
  props: {
    title: {
      type: String,
      default: 'Analyzing Text...'
    },
    message: {
      type: String,
      default: 'Our AI model is processing your text for deception detection. This may take a few moments. Please do not reset the page.'
    },
    showCancelButton: {
      type: Boolean,
      default: true
    }
  }
}
</script>

<style scoped>
.loading-screen {
  min-height: 100vh;
  display: flex;
  align-items: center;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
}

.dark-mode .loading-screen {
  background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
}

.card {
  border: none;
  border-radius: 15px;
}

.dark-mode .card {
  background-color: #2d2d2d;
  border-radius: 15px;
}

.dark-mode .card-body h4 {
  color: #ffffff;
}

.dark-mode .card-body p {
  color: #b0b0b0 !important;
}
</style>

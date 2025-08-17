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
              <h4 class="mb-3">Analyzing Text...</h4>
              <p class="text-muted mb-4">
                Our AI model is processing your text for deception detection.
                This may take a few moments. 
                <br>
                Please do not reset the page.
              </p>
              
              <div class="mt-4">
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
  name: 'LoadingScreen'
}
</script>

<style scoped>
.loading-screen {
  min-height: 100vh;
  display: flex;
  align-items: center;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
}

.card {
  border: none;
  border-radius: 15px;
}
</style>

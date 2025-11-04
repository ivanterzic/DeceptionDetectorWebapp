<template>
  <div class="lime-explanation" v-if="isActive">
    <div class="explanation-header mb-3">
      <h6>
        <i class="fas fa-lightbulb me-2"></i>
        LIME Feature Importance
      </h6>
      <p class="text-muted small">
        Local Interpretable Model-agnostic Explanations showing which words contribute most to the prediction.
        Positive values support truthfulness, negative values support deception.
      </p>
    </div>

    <!-- Feature Importance List -->
    <div class="feature-list">
      <h6 class="mb-2">Top Contributing Words</h6>
      
      <!-- Loading State -->
      <div v-if="loading" class="text-center py-2">
        <div class="spinner-border spinner-border-sm text-primary" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
        <p class="mt-1 text-muted small">Generating LIME explanation...</p>
      </div>
      
      <!-- Error State -->
      <div v-else-if="error" class="alert alert-warning py-2 mb-2">
        <i class="fas fa-exclamation-triangle me-2"></i>
        {{ error }}
        <button @click="$emit('load-explanation')" class="btn btn-sm btn-outline-primary ms-2">
          Try Again
        </button>
      </div>
      
      <!-- No Explanation State -->
      <div v-else-if="!limeExplanation && isActive" class="text-center py-2">
        <i class="fas fa-lightbulb mb-1" style="font-size: 1.5rem; color: #ddd;"></i>
        <p class="text-muted mb-2 small">LIME explanation not loaded yet</p>
        <button @click="$emit('load-explanation')" class="btn btn-sm btn-primary">
          <i class="fas fa-play me-1"></i>
          Load LIME Explanation
        </button>
      </div>
      
      <!-- Explanation Results -->
      <div v-else-if="limeExplanation && limeExplanation.length > 0">
        <div
          v-for="(item, index) in limeExplanation.slice(0, 10)"
          :key="index"
          class="explanation-item d-flex justify-content-between align-items-center py-1 border-bottom"
        >
          <span class="fw-bold word-label">{{ item[0] }}</span>
          <div class="d-flex align-items-center">
            <span
              class="badge explanation-value me-2"
              :class="item[1] > 0 ? 'bg-success' : 'bg-danger'"
            >
              {{ item[1].toFixed(3) }}
            </span>
          </div>
        </div>
      </div>
      
      <!-- Empty Results -->
      <div v-else-if="isActive" class="text-muted text-center py-2">
        <i class="fas fa-info-circle me-2"></i>
        No LIME explanation available for this text.
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LimeExplanation',
  props: {
    limeExplanation: {
      type: Array,
      default: null
    },
    loading: {
      type: Boolean,
      default: false
    },
    error: {
      type: String,
      default: null
    },
    isActive: {
      type: Boolean,
      default: true
    }
  },
  emits: ['load-explanation']
}
</script>

<style scoped>
.word-label {
  font-family: 'Courier New', monospace;
}

.explanation-bar {
  border-radius: 6px;
}

.explanation-value {
  min-width: 60px;
  font-family: 'Courier New', monospace;
}

.progress {
  border-radius: 6px;
}

/* Dark Mode Styles */
.dark-mode .explanation-header h6 {
  color: #ffffff;
}

.dark-mode .explanation-header p {
  color: #b0b0b0 !important;
}

.dark-mode .feature-list h6 {
  color: #ffffff;
}

.dark-mode .explanation-item {
  border-bottom-color: #555555 !important;
}

.dark-mode .word-label {
  color: #ffffff;
}

.dark-mode .text-muted {
  color: #b0b0b0 !important;
}
</style>

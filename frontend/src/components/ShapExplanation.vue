<template>
  <div class="shap-explanation">
    <div class="explanation-header mb-3">
      <h6>
        <i class="fas fa-chart-bar me-2"></i>
        SHAP Feature Importance
      </h6>
      <p class="text-muted small">
        SHapley Additive exPlanations showing the contribution of each word to the model's decision.
        Higher absolute values indicate more important words.
      </p>
    </div>

    <!-- Feature Importance List -->
    <div class="feature-list">
      <h6 class="mb-3">Top Contributing Words</h6>
      
      <!-- Loading State -->
      <div v-if="loading" class="text-center py-4">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
        <p class="mt-2 text-muted">Generating SHAP explanation...</p>
      </div>
      
      <!-- Error State -->
      <div v-else-if="error" class="alert alert-warning">
        <i class="fas fa-exclamation-triangle me-2"></i>
        {{ error }}
        <button @click="$emit('load-explanation')" class="btn btn-sm btn-outline-primary ms-2">
          Try Again
        </button>
      </div>
      
      <!-- No Explanation State -->
      <div v-else-if="!shapExplanation" class="text-center py-4">
        <i class="fas fa-chart-bar mb-2" style="font-size: 2rem; color: #ddd;"></i>
        <p class="text-muted mb-3">SHAP explanation not loaded yet</p>
        <button @click="$emit('load-explanation')" class="btn btn-primary">
          <i class="fas fa-play me-2"></i>
          Load SHAP Explanation
        </button>
      </div>
      
      <!-- Explanation Results -->
      <div v-else-if="shapExplanation && shapExplanation.length > 0">
        <div
          v-for="(item, index) in shapExplanation.slice(0, 10)"
          :key="index"
          class="explanation-item d-flex justify-content-between align-items-center py-2 border-bottom"
        >
          <span class="fw-bold word-label">{{ item[0] }}</span>
          <div class="d-flex align-items-center">
            <div
              class="progress explanation-bar me-2"
              style="width: 120px; height: 12px;"
            >
              <div
                class="progress-bar"
                :class="item[1] > 0 ? 'bg-success' : 'bg-danger'"
                :style="{ width: Math.min(Math.abs(item[1] * 100), 100) + '%' }"
              ></div>
            </div>
            <span
              class="badge explanation-value"
              :class="item[1] > 0 ? 'bg-success' : 'bg-danger'"
            >
              {{ item[1].toFixed(3) }}
            </span>
          </div>
        </div>
      </div>
      
      <!-- Empty Results -->
      <div v-else class="text-muted text-center py-4">
        <i class="fas fa-info-circle me-2"></i>
        No SHAP explanation available for this text.
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ShapExplanation',
  props: {
    shapExplanation: {
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
</style>

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
      <div v-if="shapExplanation && shapExplanation.length > 0">
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
      <div v-else class="text-muted">
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
      default: () => []
    }
  }
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

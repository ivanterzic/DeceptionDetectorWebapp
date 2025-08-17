<template>
  <div class="lime-explanation">
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
      <h6 class="mb-3">Top Contributing Words</h6>
      <div v-if="limeExplanation && limeExplanation.length > 0">
        <div
          v-for="(item, index) in limeExplanation.slice(0, 10)"
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
      default: () => []
    }
  },
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

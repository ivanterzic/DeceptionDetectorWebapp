<template>
  <div class="analysis-view container">
    <AnalysisResults 
      :results="results"
      @back="$emit('back')"
    />
  </div>
</template>

<script>
import AnalysisResults from '../components/AnalysisResults.vue'

export default {
  name: 'AnalysisView',
  components: {
    AnalysisResults
  },
  props: {
    results: {
      type: Object,
      required: true
    }
  }
}
</script>

<style scoped>
.analysis-view {
  background-color: #f8f9fa;
  min-height: 100vh;
  padding: 2rem 0;
}

.dark-mode .analysis-view {
  background-color: #1a1a1a;
}
</style>

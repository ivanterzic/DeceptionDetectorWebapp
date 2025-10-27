<template>
  <div class="input-form">
    <TextAnalysisForm
      :available-models="availableModels"
      :show-model-selection="true"
      :show-model-info="true"
      @analyze="handleAnalyze"
    />
  </div>
</template>

<script>
import TextAnalysisForm from './TextAnalysisForm.vue'

export default {
  name: 'InputForm',
  components: {
    TextAnalysisForm
  },
  props: {
    availableModels: {
      type: Array,
      required: true
    }
  },
  methods: {
    handleAnalyze(data) {
      this.$emit('analyze', data)
    }
  }
}
</script>

<style scoped>
.input-form {
  margin: 0 auto;
}
</style>

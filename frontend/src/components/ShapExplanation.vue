<template>
  <div class="shap-explanation" v-if="isActive">
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

    <!-- Colored Text Display -->
    <div v-if="shapExplanation && shapExplanation.length > 0 && originalText && !loading && !error" class="colored-text-display mb-4">
      <h6 class="mb-2">Explanation Visualisation</h6>
      <div class="text-display-box">
        <span 
          v-for="(word, index) in coloredWords" 
          :key="index"
          class="colored-word"
          :class="{ 'has-weight': word.weight !== 0 }"
          :style="{ 
            color: word.color, 
            fontWeight: word.weight !== 0 ? 'bold' : 'normal',
            backgroundColor: word.weight !== 0 ? getBackgroundColor(word.weight) : 'transparent'
          }"
          :title="word.weight !== 0 ? `${word.text}: ${word.weight.toFixed(4)} (${word.weight > 0 ? 'Truthful' : 'Deceptive'})` : ''"
        >
          {{ word.text }}{{ word.separator }}
        </span>
      </div>
    </div>

    <!-- Feature Importance List -->
    <div class="feature-list">
      <div class="d-flex justify-content-between align-items-center mb-2">
        <h6 class="mb-0">Top Contributing Words</h6>
        
        <!-- Word Count Selector -->
        <div v-if="shapExplanation && shapExplanation.length > 0 && !loading && !error" class="btn-group btn-group-sm" role="group">
          <button 
            v-for="option in wordCountOptions" 
            :key="option"
            type="button" 
            class="btn"
            :class="selectedWordCount === option ? 'btn-primary' : 'btn-outline-primary'"
            @click="selectedWordCount = option"
          >
            {{ option }}
          </button>
        </div>
      </div>
      
      <!-- Loading State -->
      <div v-if="loading" class="text-center py-2">
        <div class="spinner-border spinner-border-sm text-primary" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
        <p class="mt-1 text-muted small">Generating SHAP explanation...</p>
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
      <div v-else-if="!shapExplanation && isActive" class="text-center py-2">
        <i class="fas fa-chart-bar mb-1" style="font-size: 1.5rem; color: #ddd;"></i>
        <p class="text-muted mb-2 small">SHAP explanation not loaded yet</p>
        <button @click="$emit('load-explanation')" class="btn btn-sm btn-primary">
          <i class="fas fa-play me-1"></i>
          Load SHAP Explanation
        </button>
      </div>
      
      <!-- Explanation Results -->
      <div v-else-if="shapExplanation && shapExplanation.length > 0">
        <div
          v-for="(item, index) in displayedWords"
          :key="index"
          class="explanation-item d-flex justify-content-between align-items-center py-1 border-bottom"
        >
          <span class="fw-bold word-label">
            {{ item[0] }}
          </span>
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
    originalText: {
      type: String,
      default: ''
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
  emits: ['load-explanation'],
  data() {
    return {
      selectedWordCount: 10,
      wordCountOptions: [1, 3, 5, 10, 20, 'all']
    }
  },
  computed: {
    displayedWords() {
      if (!this.shapExplanation || this.shapExplanation.length === 0) {
        return [];
      }
      // Sort by absolute value (highest impact first)
      const sorted = [...this.shapExplanation].sort((a, b) => Math.abs(b[1]) - Math.abs(a[1]));
      
      if (this.selectedWordCount === 'all') {
        return sorted;
      }
      return sorted.slice(0, this.selectedWordCount);
    },
    maxWeight() {
      if (!this.shapExplanation || this.shapExplanation.length === 0) {
        return 1;
      }
      return Math.max(...this.shapExplanation.map(item => Math.abs(item[1])));
    },
    coloredWords() {
      if (!this.originalText || !this.shapExplanation) {
        return [];
      }
      
      // Create a map of words to their weights
      const wordWeights = new Map();
      this.shapExplanation.forEach(item => {
        const word = item[0].toLowerCase();
        wordWeights.set(word, item[1]);
      });
      
      // Split text into words while preserving separators
      const words = this.originalText.split(/(\s+|[.,!?;:])/);
      
      return words.map(word => {
        const cleanWord = word.toLowerCase().replace(/[.,!?;:]/g, '');
        const weight = wordWeights.get(cleanWord) || 0;
        const color = weight !== 0 ? this.getWordColor(weight) : 'inherit';
        
        // Check if this part is a separator or actual word
        const isSeparator = /^[\s.,!?;:]+$/.test(word);
        
        return {
          text: isSeparator ? '' : word,
          separator: isSeparator ? word : '',
          color: color,
          weight: weight
        };
      });
    }
  },
  methods: {
    getWordColor(weight) {
      // Green for positive (truthful), Red for negative (deceptive)
      // Using solid colors with better visibility for low values
      const intensity = Math.abs(weight) / this.maxWeight;
      // Scale intensity to range 0.4-1.0 so minimum is 40% intensity (more visible)
      const scaledIntensity = 0.4 + (intensity * 0.6);
      
      if (weight > 0) {
        // Green color with minimum visibility
        const green = Math.floor(34 + (197 - 34) * scaledIntensity);
        const red = Math.floor(200 - (200 - 34) * scaledIntensity);
        const blue = Math.floor(150 - (150 - 94) * scaledIntensity);
        return `rgb(${red}, ${green}, ${blue})`;
      } else {
        // Red color with minimum visibility
        const red = Math.floor(150 + (239 - 150) * scaledIntensity);
        const green = Math.floor(100 - (100 - 68) * scaledIntensity);
        const blue = Math.floor(100 - (100 - 68) * scaledIntensity);
        return `rgb(${red}, ${green}, ${blue})`;
      }
    },
    
    getBackgroundColor(weight) {
      // Light background color on hover for better visibility
      const intensity = Math.abs(weight) / this.maxWeight;
      const scaledIntensity = 0.15 + (intensity * 0.2); // Light background
      
      if (weight > 0) {
        return `rgba(34, 197, 94, ${scaledIntensity})`;
      } else {
        return `rgba(239, 68, 68, ${scaledIntensity})`;
      }
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

/* Colored Text Display */
.colored-text-display {
  background-color: #f8f9fa;
  padding: 1rem;
  border-radius: 10px;
  border: 1px solid #e1e5e9;
}

.text-display-box {
  background-color: white;
  padding: 1rem;
  border-radius: 8px;
  line-height: 1.8;
  font-size: 1rem;
  border: 1px solid #dee2e6;
}

.colored-word {
  transition: all 0.2s ease;
  padding: 2px 4px;
  border-radius: 3px;
  cursor: default;
}

.colored-word.has-weight {
  cursor: help;
}

.colored-word.has-weight:hover {
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  padding: 3px 5px;
}

.legend {
  display: flex;
  align-items: center;
  margin-top: 0.5rem;
}

.legend-item {
  display: flex;
  align-items: center;
}

.legend-box {
  display: inline-block;
  width: 16px;
  height: 16px;
  border-radius: 3px;
  margin-right: 0.5rem;
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

.dark-mode .colored-text-display {
  background-color: #252525;
  border-color: #3d3d3d;
}

.dark-mode .colored-text-display h6 {
  color: #ffffff;
}

.dark-mode .text-display-box {
  background-color: #2d2d2d;
  border-color: #3d3d3d;
  color: #e0e0e0;
}
</style>

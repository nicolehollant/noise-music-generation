<template>
  <div class="container">
    <div id="sketch" />
    <div id="filter" />
    <div class="album--wrapper">
      <div class="album-view">
        <div class="text">
          <h1 class="title">noise</h1>
          <p class="blurb">
            Noise is unwanted sound judged to be unpleasant, loud or disruptive
            to hearing. From a physics standpoint, noise is indistinguishable
            from sound, as both are vibrations through a medium, such as air or
            water. The difference arises when the brain receives and perceives a
            sound.
          </p>
        </div>
        <Album :tracklist="tracklist" />
      </div>
    </div>
  </div>
</template>

<script>
import noise from '~/components/noise.js'
import Album from '~/components/Album.vue'

export default {
  components: {
    Album
  },
  data() {
    return {
      tracklist: [
        { src: '/Permutation.mp3', name: 'Permutation' },
        { src: '/Calculation.mp3', name: 'Calculation' },
        { src: '/Interpolation.mp3', name: 'Interpolation' }
      ],
      sketch: null
    }
  },
  mounted() {
    if (process.browser) {
      const p5 = require('p5')
      this.sketch = new p5(noise, document.getElementById('sketch'), window)
    }
  }
}
</script>

<style scoped lang="postcss">
.container {
  z-index: 2;
  @apply text-center mx-auto;
}

.title {
  font-family: 'Quicksand', 'Source Sans Pro', -apple-system, BlinkMacSystemFont,
    'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  letter-spacing: 1px;
  @apply text-6xl font-hairline text-gray-400;
}
.text {
  @apply pb-4 text-gray-500;
}

.album--wrapper {
  z-index: 2;
  margin-top: 15vh;
  margin-bottom: 15vh;
  @apply relative max-w-xl mx-auto;
}

.album-view {
  background-color: #000000d0;
  backdrop-filter: blur(8px);
  @apply p-8 rounded;
}

#sketch {
  z-index: 0;
  filter: blur(10px);
  background-color: #00000030;
  @apply w-screen h-screen fixed top-0 left-0;
}

#filter {
  z-index: 1;
  background: radial-gradient(#00000000 50%, #000000c0);
  @apply w-screen h-screen fixed top-0 left-0;
}
</style>

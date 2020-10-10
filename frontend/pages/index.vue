<template>
  <div class="container">
    <div id="sketch" />
    <div id="filter" />
    <div class="album--wrapper">
      <div class="album-view">
        <div class="text">
          <h1 class="title">noise</h1>
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
  /* @apply text-3xl font-thin text-gray-400 leading-none mb-4; */
  @apply text-3xl font-normal text-gray-400 leading-none mb-4;
}
.text {
  @apply pb-4 text-gray-500;
}
.blurb {
  @apply text-sm leading-tight;
}

.album--wrapper {
  z-index: 2;
  width: 36rem;
  max-width: calc(100% - 2rem);
  @apply relative mx-auto h-screen flex justify-center items-center overflow-scroll;
}

.album-view {
  /* background-color: #00000060; */
  background: radial-gradient(#000000f0 0%, #00000000 70%);
  /* backdrop-filter: blur(4px); */
  @apply w-full px-4 pb-4 pt-4 rounded-lg;
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

@media (min-width: 640px) {
  .title {
    /* @apply text-6xl font-hairline; */
    @apply text-5xl font-thin;
  }
  .album-view {
    @apply px-8 pb-8 pt-4;
  }
  .blurb {
    @apply text-base leading-tight;
  }
}
</style>

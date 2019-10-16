<template>
  <div class="album">
    <audio id="song" ref="song" :key="`src-${tracklist[trackIndex].src}`">
      <source :src="tracklist[trackIndex].src" type="audio/mpeg" />
      Your browser does not support the audio element.
    </audio>

    <div class="album--tracklist">
      <ul>
        <li
          v-for="(track, index) in tracklist"
          :key="`track-${index}`"
          class="album--tracklist__track"
        >
          <button
            class="album--tracklist__track-button"
            @click="() => changeSong(index, true)"
          >
            {{ track.name }}
          </button>
        </li>
      </ul>
    </div>

    <div class="album--controls">
      <div class="album--controls__progress-shell">
        <div
          class="album--controls__progress"
          :style="`width: ${progressVal / 10}%`"
        />
        <input
          id="progress"
          v-model="progressVal"
          type="range"
          name="progress"
          class="album--controls__slider"
          min="1"
          max="1000"
          @change="changeTime"
        />
      </div>

      <div class="album-controls--row">
        <div class="row-item">
          <div class="album-controls--row__info">
            <p>{{ tracklist[trackIndex].name }}</p>
          </div>
        </div>
        <div class="row-item">
          <div class="album-controls--row__buttons">
            <div id="backward" class="button" @click="back">
              <img src="~/assets/svg/backwards.svg" alt="back" />
            </div>
            <div v-if="playing" class="button button-main" @click="pause">
              <img src="~/assets/svg/pause.svg" alt="pause" />
            </div>
            <div v-else class="button button-main" @click="play">
              <img src="~/assets/svg/play.svg" alt="play" />
            </div>
            <div id="forward" class="button" @click="forward">
              <img src="~/assets/svg/forwards.svg" alt="forward" />
            </div>
          </div>
        </div>
        <div class="row-item">
          <div class="album-controls--row__duration">
            <p>{{ currentTime }} / {{ duration }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    tracklist: {
      type: Array,
      default: () => [{ src: 'oops', name: 'oops' }]
    }
  },
  data() {
    return {
      trackIndex: 0,
      duration: -1,
      playing: false,
      progressVal: 0,
      currentTime: '0:00',
      tracking: null
    }
  },
  mounted() {
    this.changeSong(0, false)
  },
  methods: {
    changeSong(track, play) {
      this.trackIndex = track
      setTimeout(() => {
        this.duration = this.minSecStr(this.$refs.song.duration)
        if (play) {
          this.play()
        }
      }, 1000)
    },
    play() {
      this.playing = true
      this.$refs.song.play()
      this.tracking = setInterval(() => {
        this.progressVal =
          (1000 * this.$refs.song.currentTime) / this.$refs.song.duration
        this.setCurrentTime()
      }, 1000)
    },
    pause() {
      this.playing = false
      this.$refs.song.pause()
      clearInterval(this.tracking)
    },
    forward() {
      let ind = this.trackIndex
      if (++ind > this.tracklist.length - 1) {
        ind = 0
      }
      this.changeSong(ind, true)
    },
    back() {
      let ind = this.trackIndex
      if (--ind < 0) {
        ind = this.tracklist.length - 1
      }
      this.changeSong(ind, true)
    },
    minSecStr(timeSeconds) {
      const minutes = Math.floor(timeSeconds / 60)
      const seconds = Math.floor(timeSeconds % 60)
        .toString()
        .padStart(2, '0')
      return `${minutes}:${seconds}`
    },
    changeTime() {
      this.$refs.song.currentTime =
        (this.progressVal / 1000) * this.$refs.song.duration
    },
    setCurrentTime() {
      this.currentTime = this.minSecStr(this.$refs.song.currentTime)
    }
  }
}
</script>

<style lang="postcss">
.album {
  width: min-content;
  @apply mx-auto;
}
.album--tracklist {
  background-color: #4a556880;
  @apply py-4;
}
.album--tracklist__track {
  transition: all 0.2s ease-out;
  @apply px-4 py-2 text-gray-100;
}
.album--tracklist__track:hover {
  @apply bg-gray-500;
}
.album--tracklist__track-button {
  @apply w-full h-full;
}
.album--tracklist__track-button:focus {
  @apply outline-none;
}
.album--now-playing {
  @apply text-xl;
}
.album--controls {
  width: 500px;
  background-color: #2d3748a0;
  @apply m-auto text-gray-100;
}
.album--controls__progress-shell {
  height: 1rem;
  @apply w-full bg-blue-800 relative;
}
.album--controls__progress {
  @apply absolute top-0 left-0 h-full w-1/2 bg-blue-500;
}
.album--controls__slider {
  -webkit-appearance: none;
  outline: none;
  background: #274d6d80;
  @apply absolute top-0 left-0 h-full w-full;
}
.album--controls__slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 1.5rem;
  height: 1.5rem;
  border-radius: 50%;
  background: #4792cf;
  cursor: pointer;
}
.album-controls--row {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  @apply py-4;
}
.row-item {
  @apply flex items-center justify-center;
}
.album-controls--row__buttons {
  @apply flex items-center justify-center;
}
.button {
  fill: aquamarine;
  width: 2.5rem;
  height: 2.5rem;
  @apply p-3 cursor-pointer bg-blue-800 text-blue-200 font-bold rounded-full flex items-center justify-center text-sm;
}
.button-main {
  width: 3rem;
  height: 3rem;
  @apply p-4 mx-2 bg-blue-600 text-lg;
}
</style>

export default function(p, window) {
  let width, height, ps
  let which = 0
  let running = false
  let timer = 0
  const timeout = 2
  let zoff = 0
  const grid = []
  const gridSize = 100
  let song
  let image

  p.setup = function() {
    width = document.getElementById('sketch').clientWidth
    height = document.getElementById('sketch').clientHeight
    p.createCanvas(width, height)
    p.frameRate(24)
    p.noStroke()
    for (let i = 0; i < gridSize; i++) {
      grid[i] = []
    }
    ps = new ParticleSystem(100)
    const tracks = document.getElementsByClassName(
      'album--tracklist__track-button'
    )
    for (let i = 0; i < tracks.length; i++) {
      tracks[i].addEventListener('click', () => {
        which = i
        if (which > 2) which = 0
        p.background(ps.backgroundColor)
        p.fill(ps.fillColor)
        addPlayListeners()
      })
    }
    addPlayListeners()
  }

  const addPlayListeners = () => {
    song = document.getElementById('song')
    song.addEventListener('playing', () => {
      running = true
    })
    song.addEventListener('play', () => {
      running = true
    })
    song.addEventListener('pause', () => {
      running = false
    })
    song.addEventListener('ended', () => {
      running = false
      p.clear()
    })
  }

  p.draw = function() {
    if (running) {
      if (which === 0) smoke()
      else if (which === 1) terrain()
      else if (which === 2) ps.step()
      if (timer++ > timeout) {
        zoff += 0.001
        timer = 0
      }
    }
  }

  function smoke() {
    let yoff = 0
    const step = 20
    const inc = 0.2
    for (let y = 0; y < height; y += step) {
      let xoff = 0
      for (let x = 0; x < width; x += step) {
        const r = octave(xoff, yoff, zoff * 20, 2, 8)
        p.fill(r * 255)
        p.rect(x, y, step, step)
        xoff += inc
      }
      yoff += inc
    }
  }

  function terrain() {
    let yoff = 0
    const step = 20
    const inc = 0.05
    for (let y = 0; y < height; y += step) {
      let xoff = 0
      for (let x = 0; x < width; x += step) {
        const r = octave(xoff, yoff, zoff, 2, 4)
        let c = p.color(255, 255, 255)
        if (r < 0.35) {
          // deep blue
          c = p.color(28, 28, 71)
        } else if (r < 0.45) {
          // blue
          c = p.color(12, 44, 90)
        } else if (r < 0.475) {
          // light blue
          c = p.color(52, 94, 140)
        } else if (r < 0.5) {
          // beach
          c = p.color(239, 247, 178)
        } else if (r < 0.6) {
          // dark grass
          c = p.color(10, 114, 9)
        } else if (r < 0.7) {
          // grass
          c = p.color(41, 173, 39)
        } else if (r < 1) {
          // light grass
          c = p.color(60, 209, 58)
        }
        p.fill(c)
        p.rect(x, y, step, step)
        xoff += inc
      }
      yoff += inc
    }
  }

  function octave(x, y, z, octaves, persistence) {
    let total = 0
    let frequency = 1
    let amplitude = 1
    let maxValue = 0
    for (let i = 0; i < octaves; i++) {
      total += p.noise(x * frequency, y * frequency, z * frequency) * amplitude
      maxValue += amplitude
      amplitude *= persistence
      frequency *= 2
    }
    return total / maxValue
  }

  class ParticleSystem {
    constructor(num) {
      this.timeout = 600
      this.time = 0
      this.mode = 0
      this.num = num
      this.particles = []
      this.switching = false
      this.switchtimeout = 60
      this.backgroundColor = 40
      this.fillColor = 255
      p.fill(255)
      p.background(40)
      for (let i = 0; i < this.num; i++) {
        this.particles.push(new Particle())
      }
    }

    step() {
      this.time++
      if (this.time > this.timeout) {
        this.switching = true
        if (this.mode === 0) {
          this.backgroundColor += 140 / this.switchtimeout
          this.fillColor -= 255 / this.switchtimeout
        } else {
          this.backgroundColor -= 140 / this.switchtimeout
          this.fillColor += 255 / this.switchtimeout
        }
        p.fill(this.backgroundColor, 300 / this.switchtimeout)
        p.rect(0, 0, width, height)
        p.fill(this.fillColor)
        if (this.time > this.timeout + this.switchtimeout) {
          this.time = 0
          this.mode++
          if (this.mode > 1) {
            this.mode = 0
          }
          if (this.mode === 0) {
            p.fill(255)
            p.background(40)
          } else {
            p.fill(0)
            p.background(180)
          }
        }
      }

      for (const particle of this.particles) {
        particle.update()
        particle.display()
      }
    }
  }

  class Particle {
    constructor() {
      this.c = p.color(p.random(255), p.random(255), p.random(255))
      this.x = p.random(width)
      this.y = p.random(height)
      this.vel = p.random(10)
      this.rad = this.vel
      this.dir = p.map(
        p.noise(
          this.x / (width * this.vel),
          this.y / (height * this.vel),
          zoff
        ),
        0,
        1,
        0,
        360
      )
    }

    reset() {
      this.x = p.random(width)
      this.y = p.random(height)
      this.vel = p.random(3, 6)
      this.rad = this.vel
      this.dir = p.map(
        p.noise(
          this.x / (width * this.vel),
          this.y / (height * this.vel),
          zoff
        ),
        0,
        1,
        0,
        360
      )
    }

    update() {
      this.x += Math.cos(this.dir) * this.vel
      this.y += Math.sin(this.dir) * this.vel
      if (this.x < 0 || this.x > width || this.y < 0 || this.y > height) {
        this.reset()
      }
      this.dir = p.map(
        octave(
          this.x / (width * this.vel),
          this.y / (height * this.vel),
          zoff,
          4,
          6
        ),
        0,
        1,
        0,
        360
      )
    }

    display() {
      p.fill(this.c)
      p.ellipse(this.x, this.y, this.rad, this.rad)
    }
  }
}

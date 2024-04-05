<template>
  <h1>Carbone Climate Control</h1>
  <div class="container">
    <vue-gauge
      :key="`temperature_${temperature}`"
      refid="temperature"
      class="metricsGauge"
      style="translate: 25%"
      :options="{
        needleValue: temperatureNeedle,
        centralLabel: temperature + '°C',
        needleColor: '#410082',
        arcDelimiters: [40, 50, 75, 85],
        arcColors: ['#B81D13', '#EFB700', '#008450', '#EFB700', '#B81D13'],
        arcOverEffect: false,
        chartWidth: 500,
        needleUpdateSpeed: 0,
        hasNeedle: true,
      }"
    />
    <p class="temp-label">Temperatuur</p>

    <vue-gauge
      :key="`humidity_${humidity}`"
      refid="humidity"
      class="metricsGauge"
      style="translate: -25%"
      :options="humOptions"
    />

    <p class="hum-label">Luchtvochtigheid</p>
  </div>
</template>

<script>
import VueGauge from "vue-gauge";

export default {
  components: { VueGauge },
  data() {
    return {
      temperature: 10,
      humidity: 50,
    };
  },
  computed: {
    temperatureNeedle () {
        return (this.temperature + 5) * 2;
    },
    humOptions () {
      return {
        needleValue: this.humidity,
        centralLabel: this.humidity + '%',
        needleColor: '#410082',
        arcDelimiters: [30, 40, 60, 80],
        arcColors: ['#B81D13', '#EFB700', '#008450', '#EFB700', '#B81D13'],
        arcOverEffect: false,
        needleUpdateSpeed: 0,
        chartWidth: 500,
        hasNeedle: true
      };
    }
  },
  mounted () {
    setInterval(() => {
      this.temperature = Math.floor(Math.random() * 30);
      this.humidity = Math.floor(Math.random() * 100);
    }, 2000);
  }
};
</script>

<style>
body, html {
    width: 100%;
    height: 100%;
    position: absolute;
    margin: 0;
}

#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  width: 100%;
  height: 100%;
  margin: 0;
}
.container {
  display: flex;
  justify-content: center;
}

.metricsGauge {
  scale: 0.5;
  margin-top: -15%;
}

.temp-label {
    position: absolute;
    bottom: 50px;
    left: 65px;
}

.hum-label {
    position: absolute;
    bottom: 50px;
    right: 55px;
}
</style>

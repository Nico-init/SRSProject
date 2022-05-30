import { ApexOptions } from 'apexcharts'

export const defaultOptions: ApexOptions = {
  chart: {
    type: 'line',
    zoom: {
      enabled: false
    }
  },
  yaxis: {
    title: {
      text: 'Score'
    }
  },
  grid: {
    borderColor: '#e7e7e7',
    row: {
      colors: ['#f3f3f3', 'transparent'], // takes an array which will be repeated on columns
      opacity: 0.5
    },
  },
  markers: {
    size: 1
  },
  dataLabels: {
    enabled: true
  }
};
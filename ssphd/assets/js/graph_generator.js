// get the CSS colors


function legendFormatter(data) {

  if (data.x == null) {
     // This happens when there's no selection and {legend: 'always'} is set.
     return '<div class="dygraph-legend-data-container">' + '<div class="x-data-line">' + this.getLabels()[0] + ':&nbsp—</div>' + data.series.map(function(series) {
       return '<div class="y-data-line">' + series.dashHTML + series.labelHTML + '</div>'
     }).join("") + '</div>';
  }

  var html = '<div class="x-data-line highlighted">' + this.getLabels()[0] + ': ' + '<span class="legend-data">' + data.xHTML + '</span></div>';
  data.series.forEach(function(series) {
  	var labeledData = series.labelHTML + ':&nbsp<span class="legend-data">' + series.yHTML + '</span>';
    if (!series.isVisible) {
    	labeledData = series.labelHTML + ':&nbsp<span class="legend-data">—</span>';
    }
    if (series.isHighlighted) {
      html += '<div class="y-data-line highlighted">' + series.dashHTML +  labeledData + '</div>';
    }
    if (!series.isHighlighted) {
      html += '<div class="y-data-line">' + series.dashHTML + labeledData + '</div>';
    }
  });
  html = '<div class="dygraph-legend-data-container">' + html + '</div>'
  return html;
}

function kmb (x) {
  if (x >= 1e9) {
    // For billions
    return (x / 1e9).toFixed(2).replace(/\.00$/, '') + 'G';
  } else if (x >= 1e6) {
    // For millions
    return (x / 1e6).toFixed(2).replace(/\.00$/, '') + 'M';
  } else if (x >= 1e3) {
    // For thousands
    return (x / 1e3).toFixed(2).replace(/\.00$/, '') + 'K';
  } else if (x < 1 && x >= 1e-3) {
    // For milli (m)
    return (x * 1e3).toFixed(2).replace(/\.00$/, '') + 'm';
  } else if (x < 1e-3 && x >= 1e-6) {
    // For micro (µ)
    return (x * 1e6).toFixed(2).replace(/\.00$/, '') + 'µ';
  } else if (x < 1e-6 && x >= 1e-9) {
    // For nano (n)
    return (x * 1e9).toFixed(2).replace(/\.00$/, '') + 'n';
  }
  return x; // Return the number without formatting if it's near 1
}

function generateGraph(id, data, xlabel, ylabel, legendPosition='graph', kmblabels=true) {

    // getting the colors
    var style = getComputedStyle(document.documentElement)

    if (legendPosition == 'caption') {
      var legendId = 'legend_'+id;
    } else if (legendPosition == '') {

    }
    else {
      legendId = '';
    };
    let default_options = {
      colors: [
        style.getPropertyValue('--color-qualitative-blue'),
        style.getPropertyValue('--color-qualitative-red'),
        style.getPropertyValue('--color-qualitative-yellow'),
        style.getPropertyValue('--color-qualitative-green'),
        style.getPropertyValue('--color-qualitative-purple'),
        style.getPropertyValue('--color-qualitative-orange'),
      ],
      /* legend: 'always', */
      animatedZooms: true,
      labelsSeparateLines: true,
      legendFormatter: legendFormatter,
      strokeWidth: 1.5,
      // highlightSeriesOpts: {
      //   strokeWidth: 2,
      //   strokeBorderColor: style.getPropertyValue("--color-background"),
      //   strokeBorderWidth: 1.5,
      //   highlightCircleSize: 3
      // },
      highlightSeriesBackgroundAlpha: 1,
      highlightCircleSize: 2,
      xRangePad: 15,
      yRangePad: 15,
      //highlightCircleBorderWidth: 1,
      legend: 'always',
      // labelsKMB: true,
      axes: {
        x: {
          drawAxis: true,
          axisLineColor: style.getPropertyValue('--color-darkergray'),
          axisLineWidth: 0.5,
        },  
        y: {
          drawAxis: true,
          axisLineColor: style.getPropertyValue('--color-darkergray'),
          axisLineWidth: 0.5,
        }
      },
      gridLineColor: style.getPropertyValue('--color-darkgray'),
      gridLinePattern: [5, 5],
      gridLineWidth: 0.5,
      labelsDiv: legendId,
    };
    if (kmblabels) {
      default_options.axes.x.axisLabelFormatter = kmb
      default_options.axes.y.axisLabelFormatter = kmb
    }
    let graph = new Dygraph(
        document.getElementById(id),
        data,
        Object.assign({
            // labels: [xdata].concat(ydata.split(', ')),
            xlabel: [xlabel],
            ylabel: [ylabel],
            /* labelsDiv: document.getElementById('legend-graph-2'), */
          },
          default_options,
        )
    );
    return graph;
}

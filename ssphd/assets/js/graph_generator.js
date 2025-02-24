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

function generateGraph(id, data, xdata='', ydata='', xlabel, ylabel, legendPosition='graph') {

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
          style.getPropertyValue('--color-qualitiative-blue'),
          style.getPropertyValue('--color-qualitiative-red'),
          style.getPropertyValue('--color-qualitiative-yellow'),
          style.getPropertyValue('--color-qualitiative-green'),
          style.getPropertyValue('--color-qualitiative-purple'),
          style.getPropertyValue('--color-qualitiative-orange'),
        ],
        /* legend: 'always', */
        animatedZooms: true,
        labelsSeparateLines: true,
        legendFormatter: legendFormatter,
        // highlightSeriesOpts: {
        //   strokeWidth: 2,
        //   strokeBorderColor: style.getPropertyValue("--color-background"),
        //   strokeBorderWidth: 1.5,
        //   highlightCircleSize: 3
        // },
        highlightSeriesBackgroundAlpha: 1,
        highlightCircleSize: 2,
        //highlightCircleBorderWidth: 1,
        labelsKMB: true,
        legend: 'always',
        axes: {
          x: {
            drawAxis: true,
            axisLineColor: style.getPropertyValue('--color-text'),
            axisLineWidth: 0.5,
          },
          y: {
            drawAxis: true,
            axisLineColor: style.getPropertyValue('--color-text'),
            axisLineWidth: 0.5
          }
        },
        gridLineColor: style.getPropertyValue('--color-darkgray'),
        gridLinePattern: [5, 5],
        gridLineWidth: 0.5,
        labelsDiv: legendId,
      };
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

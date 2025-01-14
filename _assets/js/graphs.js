graphCaptions = [];
graphIds = []
document.querySelectorAll('.graph-container').forEach((gDiv) => {
  graphCaptions.push(gDiv.parentNode.getElementsByTagName('figcaption')[0]);
  graphIds.push(gDiv.id);
});

console.log(graphIds);

graphCaptions.forEach(
	(graphCap, i) => {
    legendDiv = document.createElement("div");
    legendDiv.classList.add('graph-legend');
    legendDiv.id = 'legend_'+graphIds[i];
    graphCap.appendChild(legendDiv) ;
  }
)
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

                    var dygraph_0 = generateGraph(id="dygraph_0", data="./_assets/graphs/xo_2024.csv", xdata="A", ydata="B, C", xlabel="A", ylabel="C", legendPosition="graph");
                

                    var dygraph_1 = generateGraph(id="dygraph_1", data="_assets/graphs/data1.csv", xdata="T (°C)", ydata="Data1 (unit1), Data2 (unit2), Data3 (unit3), Data4 (unit4), Data5 (unit5)", xlabel="Légende X", ylabel="Légende Y", legendPosition="graph");
                

                    var dygraph_2 = generateGraph(id="dygraph_2", data="_assets/graphs/data1.csv", xdata="T (°C)", ydata="Data1 (unit1), Data2 (unit2), Data3 (unit3), Data4 (unit4), Data5 (unit5)", xlabel="Légende X", ylabel="Légende Y", legendPosition="caption");
                

                    var dygraph_0 = generateGraph(id="dygraph_0", data="./_assets/graphs/xo_2024.csv", xdata="A", ydata="B, C", xlabel="A", ylabel="C", legendPosition="graph");
                

                    var dygraph_1 = generateGraph(id="dygraph_1", data="_assets/graphs/data1.csv", xdata="T (°C)", ydata="Data1 (unit1), Data2 (unit2), Data3 (unit3), Data4 (unit4), Data5 (unit5)", xlabel="Légende X", ylabel="Légende Y", legendPosition="graph");
                

                    var dygraph_2 = generateGraph(id="dygraph_2", data="_assets/graphs/data1.csv", xdata="T (°C)", ydata="Data1 (unit1), Data2 (unit2), Data3 (unit3), Data4 (unit4), Data5 (unit5)", xlabel="Légende X", ylabel="Légende Y", legendPosition="caption");
                

                    var dygraph_0 = generateGraph(id="dygraph_0", data="./_assets/graphs/xo_2024.csv", xdata="A", ydata="B, C", xlabel="A", ylabel="C", legendPosition="graph");
                

                    var dygraph_1 = generateGraph(id="dygraph_1", data="_assets/graphs/data1.csv", xdata="T (°C)", ydata="Data1 (unit1), Data2 (unit2), Data3 (unit3), Data4 (unit4), Data5 (unit5)", xlabel="Légende X", ylabel="Légende Y", legendPosition="graph");
                

                    var dygraph_2 = generateGraph(id="dygraph_2", data="_assets/graphs/data1.csv", xdata="T (°C)", ydata="Data1 (unit1), Data2 (unit2), Data3 (unit3), Data4 (unit4), Data5 (unit5)", xlabel="Légende X", ylabel="Légende Y", legendPosition="caption");
                
(function () {
    var svg = d3.select("#network-diagram")
        .append("svg")
        .attr("id", "networkGraph")
        .attr("width", "100%")
        .attr("height", "100%");

    class Network {
        constructor(x) {
            this.x = x
        }

        getCenter() {
            return [this.x, 0]
        }

        build() {
            svg.append("rect")
                .attr("width", "10")
                .attr("height", "100%")
                .attr("x", this.x)
                .attr("rx", 5);

            let vH = d3.select("#networkGraph").node().getBoundingClientRect().height
            svg.append("text")
                .text("Testing")
                .attr("x", vH * 0.85)
                .attr("y", -(this.x + 20))
                .attr("transform", function () {
                    return "rotate(90)";
                });
        }
    };

    class VM {
        constructor(x, y) {
            this.x = x
            this.y = y
        }

        build() {
            let img1 = svg.append("svg:image")
                .attr("xlink:href", "assets/chip.png")
                .attr("x", this.x)
                .attr("y", this.y)
                .attr("width", 50)
                .attr("height", 50);

            img1.on("click", function () { alert("VM") })

        }
    }

    class Router {
        constructor(x, y) {
            this.x = x
            this.y = y
        }

        getCenter() {
            return [this.x + 25, this.y + 20]
        }

        build() {
            let img = svg.append("svg:image")
                .attr("xlink:href", "assets/router2.png")
                .attr("x", this.x)
                .attr("y", this.y)
                .attr("width", 50)
                .attr("height", 50);

            img.on("click", function () { alert("Router") })

        }
    }

    class Connection {
        constructor(x, y) {
            this.x = x
            this.y = y
        }

        connect() {
            let c1 = this.x.getCenter()
            let c2 = this.y.getCenter()

            svg.append("line")
                .attr("x1", c1[0])
                .attr("y1", c2[1])
                .attr("x2", c2[0])
                .attr("y2", c2[1])
                .attr("stroke-width", 2)
                .attr("stroke", "black");

        }
    }
}())
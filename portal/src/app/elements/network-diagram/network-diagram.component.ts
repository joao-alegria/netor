import { Component, OnInit } from '@angular/core';
import { HttpClient, HttpParams, HttpHeaders } from "@angular/common/http";
import * as d3 from 'd3';
import * as $ from "jquery";
import { ModalserviceService } from '../../services/modalService/modalservice.service';
import { NONE_TYPE } from '@angular/compiler/src/output/output_ast';

@Component({
  selector: 'app-network-diagram',
  templateUrl: './network-diagram.component.html',
  styleUrls: ['./network-diagram.component.css']
})
export class NetworkDiagramComponent implements OnInit {

  constructor(private http: HttpClient, private service: ModalserviceService) { }

  async ngOnInit() {


    var svg = d3.select("#network-diagram")
      .append("svg")
      .attr("id", "networkGraph")
      .attr("width", "100%")
      .attr("height", "100%");



    let n = new Network(svg, 10)
    n.build()

    let r = new Router(svg, 30, 50)
    let c = new Connection(svg, n, r)
    c.build()
    r.build()



    let n1 = new Network(svg, 80)
    n1.build()

    let vm = new VM(svg, 100, 100)
    let c2 = new Connection(svg, n1, vm)
    c2.build()
    vm.build()


    let n2 = new Network(svg, 150)
    n2.build()

    // svg.append("rect")
    //   .attr("x", 0)
    //   .attr("y", 40)
    //   .attr("width", 250)
    //   .attr("height", 50)
    //   .attr("fill", "none")
    //   .attr("stroke", "black");


    let teste = new NetworkDiagram("teste", { "t1": "banana", "t2": "pera" })
  }
}












interface DiagramComponent {
  build(): void;
}

class Network implements DiagramComponent {
  x;; svg;
  constructor(svg, x) {
    this.x = x
    this.svg = svg
  }

  getCenter() {
    return [this.x, 0]
  }

  build() {
    this.svg.append("rect")
      .attr("width", 5)
      .attr("height", "100%")
      .attr("x", this.x)
      .attr("rx", 5);

    let vH = d3.select("#networkGraph").node().getBoundingClientRect().height
    this.svg.append("text")
      .text("Testing")
      .attr("x", vH * 0.85)
      .attr("y", -(this.x + 10))
      .attr("transform", function () {
        return "rotate(90)";
      });
  }
}

class VM implements DiagramComponent {
  x; y; svg;
  constructor(svg, x, y) {
    this.x = x
    this.y = y
    this.svg = svg;
  }

  getCenter() {
    return [this.x, this.y + 15]
  }

  build() {
    let img1 = this.svg.append("svg:image")
      .attr("xlink:href", "assets/chip.png")
      .attr("x", this.x)
      .attr("y", this.y)
      .attr("width", 30)
      .attr("height", 30)
      .attr("border", "1px solid black");

    img1.on("click", function () { alert("VM") })

  }
}

class Router implements DiagramComponent {
  x; y; svg;
  constructor(svg, x, y) {
    this.x = x
    this.y = y
    this.svg = svg
  }

  getCenter() {
    return [this.x, this.y + 15]
  }

  build() {
    let img = this.svg.append("svg:image")
      .attr("xlink:href", "assets/router2.png")
      .attr("x", this.x)
      .attr("y", this.y)
      .attr("width", 30)
      .attr("height", 30);

    img.on("click", function () { alert("Router") })

  }
}

class Connection implements DiagramComponent {
  x; y; svg;
  constructor(svg, x, y) {
    this.x = x
    this.y = y
    this.svg = svg
  }

  build() {
    let c1 = this.x.getCenter()
    let c2 = this.y.getCenter()

    this.svg.append("line")
      .attr("x1", c1[0])
      .attr("y1", c2[1])
      .attr("x2", c2[0])
      .attr("y2", c2[1])
      .attr("stroke-width", 2)
      .attr("stroke", "black");

  }
}

class NetworkDiagram {
  svg; network;
  constructor(diagramId, network) {
    this.svg = d3.select(diagramId)
      .append("svg")
      .attr("id", "networkGraph")
      .attr("width", "100%")
      .attr("height", "100%");

    this.network = network
    this.constructAndBuild()
  }

  constructAndBuild() {
    // for (let key in this.network) {
    //   console.log(this.network[key])
    // }
  }
}
class BubbleChart
  constructor: (data) ->
    @data = data
    @width = 900
    @height = 500

    @tooltip = CustomTooltip("gates_tooltip", 240)

    # locations the nodes will move towards
    # depending on which view is currently being
    # used
    @center = {x: @width / 2, y: @height / 2}
    @year_centers = {
      "2013": {x: @width / 3, y: @height / 2},
      "2014": {x: @width / 2, y: @height / 2},
      "2015": {x: 2 * @width / 3, y: @height / 2}
    }

    @muni_centers = {
      "hura": {x: 500, y: 200},
      "gush_etzion": {x: 200, y: 200},
      "ashdod": {x: 700, y: 200},
      "beer_sheva": {x: 100, y: 500},
      "qiryat_bialik": {x: 500 , y: 500},
      "kfar_shmaryahu": {x: 500, y: 500},
      "rishon_letzion": {x: 700, y: 700}
    }


    # used when setting up force and
    # moving around nodes
    @layout_gravity = -0.01
    @damper = 0.1

    # these will be set in create_nodes and create_vis
    @vis = null
    @nodes = []
    @force = null
    @circles = null

    # nice looking colors - no reason to buck the trend
    @fill_color = d3.scale.ordinal()
      #TODO muni names are hardcoded here, one day we could get them from the server at api/v1/get_munis
      .domain(["hura", "gush_etzion", "ashdod", "beer_sheva", "qiryat_bialik", "kfar_shmaryahu", "rishon_letzion"])
      .range(["#d84b2a", "#FF83AE", "#53AF0D","#3397BF","#11D3EA","#FCFA3F","#E741CF"])

    # use the max total_amount in the data as the max in the scale's domain
    max_amount = d3.max(@data, (d) -> parseInt(d.amount))
    @radius_scale = d3.scale.pow().exponent(0.5).domain([0, max_amount]).range([2, 85])

    this.create_nodes()
    this.create_vis()

  # create node objects from original data
  # that will serve as the data behind each
  # bubble in the vis, then add each node
  # to @nodes to be used later
  Debug_numberOfDisplayedNodes = 0 #TODO REMOVE DEBUG
  create_nodes: () =>
    @data.forEach (d) =>
      node = {
        id: d._id
        radius: @radius_scale(r = parseInt(d.amount);
        if r > 0 #TODO REMOVE DEBUG
          Debug_numberOfDisplayedNodes++
        )
        value: d.amount
        name: d.name
        org: "org"
        group: d.muni
        year: d.year
        x: Math.random() * @width
        y: Math.random() * @height
      }
      @nodes.push node

    @nodes.sort (a,b) -> b.value - a.value
    console.log("DEBUG: Number of nodes " + Debug_numberOfDisplayedNodes) #TODO REMOVE DEBUG
  # create svg at #vis and then
  # create circle representation for each node
  create_vis: () =>
    @vis = d3.select("#vis").append("svg")
      .attr("width", @width)
      .attr("height", @height)
      .attr("id", "svg_vis")

    @circles = @vis.selectAll("circle")
      .data(@nodes, (d) -> d.id)

    # used because we need 'this' in the
    # mouse callbacks
    that = this

    # radius will be set to 0 initially.
    # see transition below
    @circles.enter().append("circle")
      .attr("r", 0)
      .attr("fill", (d) => @fill_color(d.group))
      .attr("stroke-width", 2)
      .attr("stroke", (d) => d3.rgb(@fill_color(d.group)).darker())
      .attr("id", (d) -> "bubble_#{d.id}")
      .on("mouseover", (d,i) -> that.show_details(d,i,this))
      .on("mouseout", (d,i) -> that.hide_details(d,i,this))

    # Fancy transition to make bubbles appear, ending with the
    # correct radius
    @circles.transition().duration(2000).attr("r", (d) -> d.radius)


  # Charge function that is called for each node.
  # Charge is proportional to the diameter of the
  # circle (which is stored in the radius attribute
  # of the circle's associated data.
  # This is done to allow for accurate collision
  # detection with nodes of different sizes.
  # Charge is negative because we want nodes to
  # repel.
  # Dividing by 8 scales down the charge to be
  # appropriate for the visualization dimensions.
  charge: (d) ->
    -Math.pow(d.radius, 2.0) / 8

  # Starts up the force layout with
  # the default values
  start: () =>
    @force = d3.layout.force()
      .nodes(@nodes)
      .size([@width, @height])

  # Sets up force layout to display
  # all nodes in one circle.
  display_group_all: () =>
    @force.gravity(@layout_gravity)
      .charge(this.charge)
      .friction(0.9)
      .on "tick", (e) =>
        @circles.each(this.move_towards_center(e.alpha))
          .attr("cx", (d) -> d.x)
          .attr("cy", (d) -> d.y)
    @force.start()

    this.hide_years()

  # Moves all circles towards the @center
  # of the visualization
  move_towards_center: (alpha) =>
    (d) =>
      d.x = d.x + (@center.x - d.x) * (@damper + 0.02) * alpha
      d.y = d.y + (@center.y - d.y) * (@damper + 0.02) * alpha

  # sets the display of bubbles to be separated
  # into each year. Does this by calling move_towards_year
  display_by_year: () =>
    @force.gravity(@layout_gravity)
      .charge(this.charge)
      .friction(0.9)
      .on "tick", (e) =>
        @circles.each(this.move_towards_year(e.alpha))
          .attr("cx", (d) -> d.x)
          .attr("cy", (d) -> d.y)
    @force.start()

    this.display_years()

  # move all circles to their associated @year_centers
  move_towards_year: (alpha) =>
    (d) =>
      target = @year_centers[d.year]
      d.x = d.x + (target.x - d.x) * (@damper + 0.02) * alpha * 1.1
      d.y = d.y + (target.y - d.y) * (@damper + 0.02) * alpha * 1.1

  # sets the display of bubbles to be separated
  # into each muni. Does this by calling move_towards_muni
  display_by_muni: () =>
    @force.gravity(@layout_gravity)
      .charge(this.charge)
      .friction(0.9)
      .on "tick", (e) =>
        @circles.each(this.move_towards_muni(e.alpha))
          .attr("cx", (d) -> d.x)
          .attr("cy", (d) -> d.y)
    @force.start()

  # move all circles to their associated @muni_centers
  move_towards_muni: (alpha) =>
    (d) =>
      target = @muni_centers[d.group]
      d.x = d.x + (target.x - d.x) * (@damper + 0.02) * alpha * 1.1
      d.y = d.y + (target.y - d.y) * (@damper + 0.02) * alpha * 1.1


  # Method to display year titles
  display_years: () =>
    years_x = {"2013": 160, "2014": @width / 2, "2015": @width - 160}
    years_data = d3.keys(years_x)
    years = @vis.selectAll(".years")
      .data(years_data)

    years.enter().append("text")
      .attr("class", "years")
      .attr("x", (d) => years_x[d] )
      .attr("y", 40)
      .attr("text-anchor", "middle")
      .text((d) -> d)

  # Method to hide year titiles
  hide_years: () =>
    years = @vis.selectAll(".years").remove()

  show_details: (data, i, element) =>
    d3.select(element).attr("stroke", "black")
    content = "<span class=\"name\">Title:</span><span class=\"value\"> #{data.name}</span><br/>"
    content +="<span class=\"name\">Amount:</span><span class=\"value\"> $#{addCommas(data.value)}</span><br/>"
    content +="<span class=\"name\">Year:</span><span class=\"value\"> #{data.year}</span><br/>"
    content +="<span class=\"name\">Muni:</span><span class=\"value\"> #{data.group}</span>"
    @tooltip.showTooltip(content,d3.event)


  hide_details: (data, i, element) =>
    d3.select(element).attr("stroke", (d) => d3.rgb(@fill_color(d.group)).darker())
    @tooltip.hideTooltip()


root = exports ? this

$ ->
  chart = null

  render_vis = (csv) ->
    chart = new BubbleChart csv
    chart.start()
    root.display_all()
  root.display_all = () =>
    chart.display_group_all()
  root.display_year = () =>
    chart.display_by_year()
  root.display_muni = () =>
    chart.display_by_muni()
  root.toggle_view = (view_type) =>
    if view_type == 'year'
      root.display_year()
    else if view_type == 'muni'
      root.display_muni()
    else
      root.display_all()
# <<<<<<< Updated upstream
  d3.json "/api/v1/get_budget?layer=1&muni=ashdod&year=2015&year=2010", render_vis
# =======
  # d3.json "/api/v1/get_budget?layer=1&year=2011&muni=beer_sheva", render_vis

  #d3.json "http://localhost:3000/data/TEST__EXAMPLE_budget.json", render_vis
  #d3.json "data/convertcsv.json", render_vis
  #d3.csv "data/gates_money.csv", render_vis

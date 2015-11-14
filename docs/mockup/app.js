App = {
    setupMinimap: function(map, minimap) {
        var rectLayer = L.rectangle(map.getBounds(),
                                    {stroke: true,
                                     weight: 2,
                                     color: "#ff0000",
                                     fill: true});
        minimap.addLayer(rectLayer);
        map.on("drag moveend resize zoomend", function(e) {
            rectLayer.setBounds(map.getBounds());
        });
        minimap.on("click", function(e) {
            map.setView(e.latlng);
            console.log(rectLayer);
        });
    },

    init: function() {
        var source = "http://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png",
            bounds = [[42.4190212708995, -71.07150077819824],
                      [42.372305415983895, -71.13570213317871]];

        var map = L.map("map"),
            proposals = L.featureGroup();

        window.map = map;

<<<<<<< HEAD
        map.addLayer(L.tileLayer("http://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png"));
        map.fitBounds([[42.42009843116784, -71.05768203735352],
                       [42.370720143531976, -71.14445686340332]]);
=======
        map.addLayer(L.tileLayer(source));
        map.addLayer(proposals);
        map.fitBounds(bounds);

        var minimap = L.map("minimap",
                            {attributionControl: false,
                             dragging: false,
                             touchZoom: false,
                             scrollWheelZoom: false,
                             boxZoom: false,
                             zoomControl: false});
        minimap.setView(map.getCenter());
        minimap.setZoom(11);
        minimap.addLayer(L.tileLayer(source));
        App.setupMinimap(map, minimap);

>>>>>>> origin/master
        $.getJSON("https://raw.githubusercontent.com/cityofsomerville/geodata/master/somerville.geojson")
            .done(function(features) {
                map.addLayer(
                    L.geoJson(features,
                              {style: {
<<<<<<< HEAD
                                  stroke: 0.5,
                                  color: "orange",
=======
                                  stroke: true,
                                  weight: 2,
                                  color: "#EB4E12",
>>>>>>> origin/master
                                  fill: false
                              }}));
                minimap.addLayer(
                    L.geoJson(features,
                              {style: {
                                  stroke: true,
                                  weight: 2,
                                  fill: false
                              }}));

            });
<<<<<<< HEAD
=======

        $.getJSON("http://localhost:3000/proposal/list")
            .done(function(response) {
                $(response.proposals).each(function(i, feature) {
                    if (feature.location) {
                        var marker = L.marker(feature.location).addTo(proposals);

                        marker.proposal = feature;
                    }
                });
            });

        map.locate();

        function updateMarkers() {
            if (map.getZoom() >= 17) {
                var bounds = map.getBounds();
                proposals.eachLayer(function(marker) {
                    var images = marker.proposal.images;
                    if (!images || !images.length ||
                        !bounds.contains(marker.getLatLng()))
                        return;

                    marker._unzoomedIcon =
                        marker.icon || new L.Icon.Default();
                    marker.setIcon(L.divIcon({
                        className: "zoomed-proposal-marker",
                        iconSize: L.point(100, 75),
                        html: "<img src='http://localhost:3000" +
                            images[0].thumb + "'/>"
                    }));
                });
            } else {
                proposals.eachLayer(function(marker) {
                    if (marker._unzoomedIcon) {
                        marker.setIcon(marker._unzoomedIcon);
                        delete marker._unzoomedIcon;
                    }
                });
            }
        }

        map.on("zoomend", updateMarkers)
            .on("moveend", updateMarkers);

        $("#main_activated").on("change", function(e) {
            if (this.checked) {
                $(document.body).addClass("main");
            } else {
                $(document.body).removeClass("main");
            }
        });

        if ($(document.body).hasClass("main")) {
            $("#main_activated").prop("checked", true);
        }
>>>>>>> origin/master
    }
}
/* Drawing/Layer Controls */
let drawnItems = new L.FeatureGroup().addTo(mapObj);   // FeatureGroup is to store editable layers
let shpLayer = new L.FeatureGroup().addTo(mapObj);

let drawControl = new L.Control.Draw({
    edit: {
        featureGroup: drawnItems,
        edit: true,
    },
    draw: {
        polyline: false,
        circlemarker: false,
        circle: false,
        polygon: false,
        rectangle: true,
        trash: true,
    },
});

/* Add the controls to the map */
mapObj.addControl(drawControl);

/* Controls for when drawing on the maps */
mapObj.on(L.Draw.Event.CREATED, function (event) {
    drawnItems.addLayer(event.layer);
});

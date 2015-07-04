/**
 * View responsible for exposing the permit filters to the user.
 */
define(["backbone", "ref-location", "utils", "arcgis"], function(B, refLocation, $u, arcgis) {
    return B.View.extend({
        el: function() {
            return document.getElementById("permit-filters");
        },

        events: {
            "change #desc-filter": "refreshDescriptionFilter",
            "keyup #desc-filter": "descFilterChanged",
            "change #pb-filter": "refreshSPGAFilter",
            "change #zba-filter": "refreshSPGAFilter",

            "submit #ref-address-form": "submitAddress",
            "focus #ref-address-form": "removeGuessClass",
            "click #geolocate": "geolocate"
        },

        refreshDescriptionFilter: function() {
            var s = ($("#desc-filter").val() || "").trim();
            this.collection.filterByDescriptionString(s);
        },


        descFilterChanged: function(e) {
            var self = this;
            clearTimeout(this._descTimeout);
            this._descTimeout = setTimeout(function() {
                self.refreshDescriptionFilter();
            }, 200);
        },

        refreshSPGAFilter: function() {
            var spga = [];
            if ($("#pb-filter").prop("checked"))
                spga.push("PB");
            if ($("#zba-filter").prop("checked"))
                spga.push("ZBA");
            this.collection.filterByAuthority(spga);
        },

        submitAddress: function(e) {
            var addr = e.target.elements["address"].value;

            refLocation.setFromAddress(addr).fail(function(err) {
                // Indicate to the user why geocoding failed.
            });

            return false;
        },

        /**
         * Given a [lat, long] array, attempt to retrieve an address and
         * set the value of the address input. If reverse geocoding is
         * successful, the address input will have a 'guess' class
         * added.
         */
        reverseGeocodeAddress: function(loc) {
            return arcgis.reverseGeocode(loc[0], loc[1]).done(function(json) {
                $("#ref-address-form input")
                    .val(json.address.Address)
                    .addClass("guess");
            });
        },

        removeGuessClass: function(e) {
            $(e.target).removeClass("guess");
        },

        /**
         * When the geolocate button is clicked, set the reference
         * location to the user's current location and update the
         * address input with the reverse-geocoded address for that
         * location.
         */
        geolocate: function(e) {
            return refLocation.setFromBrowser().then(this.reverseGeocodeAddress);
        }
    });
});
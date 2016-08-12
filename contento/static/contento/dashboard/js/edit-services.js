(function(){
"use strict";

angular.module("edit-app")
.factory('DataServiceRestangular', DataServiceRestangular);

function DataServiceRestangular(Restangular){
    return Restangular.withConfig(function(RestangularConfigurer) {
        RestangularConfigurer.setBaseUrl(djangoUrls.dashboardBase+"/api/");

        // Example configuration of httpFields
        RestangularConfigurer.setDefaultHttpFields({
            'withCredentials': false
        });

        /* Custom response extractor for Restangular  */
        /* This one plays well with djangorestframework */
        RestangularConfigurer.setResponseExtractor(function(response, operation, what, url) {
        var newResponse;
        if (operation === "getList") {
            newResponse = response.results != undefined ? response.results : response;
            newResponse.metadata = {
                count : response.count,
                next : response.next,
                previous : response.previous,
                number : response.number,
            }
        } else {
            newResponse = response;
        }
            return newResponse;
        });

        /* Restangular requestSuffix, appended to all urls -- plays well with django */

        RestangularConfigurer.setRequestSuffix('/?');

    });
}

angular.module("edit-app")
.factory('DataService', DataService);

function DataService(DataServiceRestangular){
    var svc = {};

    svc.renderersMeta = DataServiceRestangular.oneUrl("renderers-meta");

    return svc;
}


})();

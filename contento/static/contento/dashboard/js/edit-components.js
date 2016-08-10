(function(){
  const pageEditor = {
    templateUrl : djangoUrls.angularTemplatesBase + 'page-editor.html',
    bindings : {
      pageContext : '<'
    },
    controller: function () {

    }
  };

  const fragmentEditor = {
    templateUrl : djangoUrls.angularTemplatesBase + 'fragment-editor.html',
    bindings : {
      content : '=',
      region : '<',
      pageContext : '<'
    },
    controller: function () {
      this.getPreviewUrl = function(){
        return "/dashboard/preview/"
      }
    }
  };

  angular.module("edit-app")
  .component('pageEditor', pageEditor)
  .component('fragmentEditor', fragmentEditor);


})();;;;

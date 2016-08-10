(function(){

  function guid(prefix) {
    return prefix||'' + s4() + s4() + '-' + s4() + '-' + s4();
  }

  function s4() {
    return Math.floor((1 + Math.random()) * 0x10000)
      .toString(16)
      .substring(1);
  }

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
      path : '<',
      pageContext : '<'
    },
    controller: function () {
      this.randId = guid();
      this.formName  = "form" + this.randId;
      this.frameName  = "frame" + this.randId;
      this.token = djangoUrls.token;
      this.getPreviewUrl = function(){
        return "/dashboard/preview/" + this.pageContext.label + "?fragment_path="+this.region + "." + this.path;
      }

      this.jsonData = JSON.stringify(this.content.data);
      console.log("f", this.pageContext)
    }
  };


  const fragmentJsonEditor = {
    templateUrl : djangoUrls.angularTemplatesBase + 'fragment-json-editor.html',
    bindings : {
      content : '=',
      region : '<',
      path : '<',
      pageContext : '<'
    },
    controller: function () {
      console.log(this.content)
      this.contentJson = JSON.stringify(
        {type:this.content.type, data:this.content.data}, null, '\t')
    }
  };




  angular.module("edit-app")
  .component('pageEditor', pageEditor)
  .component('fragmentEditor', fragmentEditor)
  .component('fragmentJsonEditor', fragmentJsonEditor);


})();;;;

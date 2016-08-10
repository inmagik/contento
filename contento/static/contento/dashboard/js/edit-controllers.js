(function(){
"use strict";

angular.module("edit-app")
.controller('AppController', AppController);

function AppController($scope){
  console.log(window.pageContext);
  this.pageContext = pageContext;

};

})();;;;

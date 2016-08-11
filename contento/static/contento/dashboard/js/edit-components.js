(function(){

  function guid(prefix) {
    return prefix||'p' + s4() + s4() +  s4() +  s4();
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
      var that = this;

      this.jsonData = JSON.stringify(this.content.data);
      console.log("f", this.pageContext)

      this.onContentChange = function(content){
        console.log("cc", content);
        that.content = content;
      }
    }
  };


  const fragmentJsonEditor = {
    templateUrl : djangoUrls.angularTemplatesBase + 'fragment-json-editor.html',
    bindings : {
      content : '<',
      region : '<',
      path : '<',
      pageContext : '<',
      onContentChange : '&'
    },
    controller: function ($attrs) {
      var that = this;
      let fmt = ($attrs.format || "").toLowerCase();
      this.format = ["json", "yaml"].indexOf(fmt) !== -1 ? fmt : "json";

      var formatContent = function(content, format){
        if(format === 'yaml'){
          return YAML.stringify(content, 10, 2)
        }
        return JSON.stringify(content, null, '\t')
      }

      var parseContent = function(formattedContent, format){
        if(format === 'yaml'){
          return YAML.parse(formattedContent)
        }
        return JSON.parse(formattedContent)
      }

      this.contentFormatted = formatContent(this.content.data, this.format)
      this.$onChanges = function (changesObj) {
        console.log("222", changesObj, that.editor)
        if(!changesObj.content || !that.editor){
          return
        }
        //if we are focused we should return
        if(that.editor.textInput.isFocused()){
            return
        }

        that.contentFormatted = formatContent(changesObj.content.currentValue.data, that.format)
      };

      this.aceLoaded = function(editor){
        that.editor = editor;
      }



      this.aceChanged = function(value){
        try {
          that.content.data = parseContent(that.contentFormatted, that.format);
        } catch(err){
          console.log("pp")
          return
        }
        //that.content = angular.copy(that.content);
        that.onContentChange({content:angular.copy(that.content)});
      }
    }
  };


  const fragmentPreview = {
    templateUrl : djangoUrls.angularTemplatesBase + 'fragment-preview.html',
    bindings : {
      content : '<',
      region : '<',
      path : '<',
      pageContext : '<'
    },
    controller: function ($element, $timeout) {
      this.randId = guid();
      this.formName  = "formx";
      this.frameName  = "frame" + this.randId;
      frameName = this.frameName;
      var formId = "#"+this.formName;
      var that = this;
      var form;


      this.getPreviewUrl = function(){
        return "/dashboard/preview/" + this.pageContext.label + "?fragment_path="+this.region + "." + this.path;
      }

      this.$postLink = function(){
        var el = $($element);
        var iframe = $("<iframe noborder class='preview-iframe'/>");
        iframe.attr("name", this.frameName);
        iframe.attr("src", this.getPreviewUrl());
        el.append(iframe)
        form = $("form", el);

      }

      this.$onChanges = function (changesObj) {
        that.contentDataAsJson = JSON.stringify(that.content.data)
        $timeout(()=>{
            this.submit();
        })
      };


      this.submit = function () {
          if(form){
            form[0].submit()
          }
      };




    },


  };




  angular.module("edit-app")
  .component('pageEditor', pageEditor)
  .component('fragmentPreview', fragmentPreview)
  .component('fragmentEditor', fragmentEditor)
  .component('fragmentJsonEditor', fragmentJsonEditor);


})();;;;

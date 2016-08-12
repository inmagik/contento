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

      this.onContentChange = function(data){
        console.log("onContentChange", data )
        that.content.data = data;
      }
    }
  };


  const fragmentJsonEditor = {
    templateUrl : djangoUrls.angularTemplatesBase + 'fragment-json-editor.html',
    bindings : {
      contentType : '<',
      contentData : '<',
      region : '<',
      path : '<',
      pageContext : '<',
      onContentChange : '&'
    },
    controller: function ($attrs) {
      var that = this;
      this.randId = guid();
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

      this.contentFormatted = formatContent(this.contentData, this.format);
      this.$onChanges = function (changesObj) {
        console.info("changesObj")

        if(!changesObj.contentData || !that.editor) {
          return
        }
        if(that.editor.textInput.isFocused()){
          return
        }
        //let d = angular.copy(changesObj.contentData.currentValue);
        //delete d.editKey;
        that.contentFormatted = formatContent(changesObj.contentData.currentValue, that.format)
      };

      this.aceLoaded = function(editor){
        that.editor = editor;
        editor.$blockScrolling = Infinity;
      }

      this.aceChanged = function(value){
        if (!that.editor.textInput.isFocused()){
          return
        }

        try {
          that.contentData = parseContent(that.contentFormatted, that.format);
          //that.contentData.editKey = that.randId;
          that.onContentChange({content:that.contentData});
        } catch(err){
          console.error(err);
        }

        //that.content = angular.copy(that.content);

      }
    }
  };


  const fragmentJsonSchemaEditor = {
    templateUrl : djangoUrls.angularTemplatesBase + 'fragment-jsonschema-editor.html',
    bindings : {
      contentType : '<',
      contentData : '<',
      region : '<',
      path : '<',
      pageContext : '<',
      onContentChange : '&'
    },
    controller: function ($element, $attrs, DataService, $timeout) {
      var that = this;
      this.randId = guid();

      this.$onChanges = function (changesObj) {
        if(!changesObj.contentData || !that.editor){
          return
        }
        if( angular.equals(changesObj.contentData.currentValue, that.editor.getValue() )){
          return
        }

        that.editor.setValue(changesObj.contentData.currentValue)

      };

      var getFullType = function(t){
        const p = t.split(".")
        if(p.length < 2){
          t = "contento.renderers." + t;
        }
        return t
      }


      //that.onContentChange({content:angular.copy(that.content)});

      this.$postLink = function(){
        var el = $($element);
        var cont = $(".json-form-container", el)[0]

        //#TODO: should load from  a service ...
        DataService.renderersMeta.get()
        .then(resp => {
          that.renderersMeta = resp.plain();
          var typeName = getFullType(that.contentType)
          var m = that.renderersMeta[typeName];
          console.log(1, m)
          if(m){
            that.editor = new JSONEditor(
              cont,
              {
                schema:m,
                theme:'bootstrap3',
                startval:that.contentData,
                disable_collapse:true,
                disable_properties : true

               }
            );
            that.editor.on('change',function() {
              that.contentData = that.editor.getValue();
              $timeout(()=>{
                  that.onContentChange({content:that.contentData})
              })

            });
          }
        });


      }


    }
  };


  const fragmentPreview = {
    templateUrl : djangoUrls.angularTemplatesBase + 'fragment-preview.html',
    bindings : {
      contentType : '<',
      contentData : '<',
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
        console.log(1, "changing")
        let d = angular.copy(changesObj.contentData.currentValue);
        that.contentDataAsJson = JSON.stringify(d)
        $timeout(()=>{
            this.submit();
        })
      };


      this.submit = function () {
        console.log(100, "submitting form..", this.randId, this.contentType, this.region, this.path)
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
  .component('fragmentJsonEditor', fragmentJsonEditor)
  .component('fragmentJsonSchemaEditor', fragmentJsonSchemaEditor);


})();;;;

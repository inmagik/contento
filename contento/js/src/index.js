import jshook from 'jshook'

jshook.register('pages', require('./hooks/pages').default)

jshook.boot()

// import React from 'react'
// import ReactDOM from 'react-dom'
// import JsHook from './jshook'
// import ContentEditor from './components/ContentEditor'
// import Form from "react-jsonschema-form"
// import uuid from 'node-uuid'
// JsHook.register('pages-sortable', require('./hooks/sortablePages').default)
// export default (element) => {
//
// }
//
// JsHook.register('content-editor', require('./hooks/ContentEditor'))

// JsHook.register('content-editor', (element) => {
//   const originalRegions = JSON.parse(element.value || '{}');
//   const regions = Object.keys(originalRegions).reduce((r, name) => ({
//     ...r,
//     [name]: originalRegions[name].map(frag => ({ ...frag, uuid: uuid.v4() }))
//   }), {})
//   console.log(regions)
//
//   const allEmptyRegions = JSON.parse(element.getAttribute('data-contenteditor-regions') || '[]')
//     .reduce((all, name) => ({ ...all, [name]: [] }), {})
//
//   const fragmentsSchemas = JSON.parse(element.getAttribute('data-contenteditor-fragments-schemas') || '{}')
//
//   const reactContainer = document.createElement('div')
//   element.parentNode.insertBefore(reactContainer, element)
//   // element.style.visibility = 'hidden'
//
//   ReactDOM.render(
//     <ContentEditor
//       fragmentsSchemas={fragmentsSchemas}
//       regions={{ ...allEmptyRegions, ...regions }}
//       saveRegions={(regions) => element.value = JSON.stringify(regions)}
//     />,
//     reactContainer
//   )
// })
//
// JsHook.register('textarea-jsonschema', (element) => {
//   const value = JSON.parse(element.value || '{}');
//   const schema = JSON.parse(element.getAttribute('data-textarea-jsonschema') || '{}')
//
//
//   const reactContainer = document.createElement('div')
//   element.parentNode.insertBefore(reactContainer, element)
//   // element.style.visibility = 'hidden'
//
//   const handleChange = ({formData}) => {
//     element.value = JSON.stringify(formData);
//   }
//
//   ReactDOM.render(
//     <Form schema={schema} formData={value} onChange={handleChange}>
//       <div/>
//     </Form>,
//
//     reactContainer
//   )
// })

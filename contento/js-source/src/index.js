import React from 'react'
import ReactDOM from 'react-dom'
import JsHook from './jshook'
import ContentEditor from './components/ContentEditor'
import uuid from 'node-uuid'

JsHook.register('content-editor', (element) => {
  const originalRegions = JSON.parse(element.value || '{}');
  const regions = Object.keys(originalRegions).reduce((r, name) => ({
    ...r,
    [name]: originalRegions[name].map(frag => ({ ...frag, uuid: uuid.v4() }))
  }), {})
  console.log(regions)

  const allEmptyRegions = JSON.parse(element.getAttribute('data-contenteditor-regions') || '[]')
    .reduce((all, name) => ({ ...all, [name]: [] }), {})

  const fragmentsSchemas = JSON.parse(element.getAttribute('data-contenteditor-fragments-schemas') || '{}')

  const reactContainer = document.createElement('div')
  element.parentNode.insertBefore(reactContainer, element)
  // element.style.visibility = 'hidden'

  ReactDOM.render(
    <ContentEditor
      fragmentsSchemas={fragmentsSchemas}
      regions={{ ...allEmptyRegions, ...regions }}
      saveRegions={(regions) => element.value = JSON.stringify(regions)}
    />,
    reactContainer
  )
})

module.exports = JsHook

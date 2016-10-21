import React from 'react'
import ReactDOM from 'react-dom'
import JsHook from './jshook'
import ContentEditor from './components/ContentEditor'

JsHook.register('content-editor', (element) => {
  const regions = JSON.parse(element.value || '{}')
  element.style.visibility = 'hidden'

  const reactContainer = document.createElement('div')
  element.parentNode.insertBefore(reactContainer, element)

  ReactDOM.render(
    <ContentEditor
      regions={regions}
      saveRegions={(regions) => element.value = JSON.stringify(regions)}
    />,
    reactContainer
  )
})

module.exports = JsHook

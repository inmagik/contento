import React from 'react'
import { render } from 'react-dom'
import uuid from 'node-uuid'
import ContentEditor from './components/ContentEditor'

export default (element) => {
  const originalRegions = JSON.parse(element.value || '{}');
  const regions = Object.keys(originalRegions).reduce((r, name) => ({
    ...r,
    [name]: originalRegions[name].map(frag => ({ ...frag, uuid: uuid.v4() }))
  }), {})
  // console.log(regions)

  const allEmptyRegions = JSON.parse(element.getAttribute('data-contenteditor-regions') || '[]')
    .reduce((all, name) => ({ ...all, [name]: [] }), {})

  const fragmentsSchemas = JSON.parse(element.getAttribute('data-contenteditor-fragments-schemas') || '{}')

  const container = document.createElement('div')
  element.parentNode.insertBefore(container, element)
  if (process.env.NODE_ENV === 'production') {
    element.style.width = 0;
    element.style.visibility = 'hidden'
  }

  render(
    <ContentEditor
      fragmentsSchemas={fragmentsSchemas}
      regions={{ ...allEmptyRegions, ...regions }}
      saveRegions={(regions) => element.value = JSON.stringify(regions)}
    />,
    container
  )
}
